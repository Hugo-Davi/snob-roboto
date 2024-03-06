import bs4

import requests
import re
import csv
from utils import isTag

peopleDict = {
    # 'marlon-brando': {
    #     'name': 'Marlon Brando'
    # }
}
filmInfo = {
    # 'the-godfather': {
    #     'actors': ['marlon-brando']
    # }
}

def add_by_role(film, href, name, role):
    if not href in peopleDict:
        peopleDict[href] = {'name': name}
    if not film in filmInfo:
        filmInfo[film] = {role: [href]}
    else:
        if role in filmInfo[film]: filmInfo[film][role].append(href)
        else: filmInfo[film][role] = [href]
    return

def add_by_role2(film, section, role, **kwargs):
    pattern = r'([^\/]*)\/$'
    link = kwargs.get('link', False)
    print(f'---------start--------\nadd by role at {role}\n------------------')
    print(f'link = {link}')
    if link: elements = section.findAll('a', {'href': re.compile(link)})
    else: elements = section.findAll('a', {'href': re.compile(pattern)})

    if elements == []: filmInfo[film][role] = ['']
    for element in elements:
        href = re.search(pattern, element['href']).group()[:-1]
        print(href)
        if not role in filmInfo[film]: filmInfo[film][role] = [href]
        else: filmInfo[film][role].append(href)
    return

def get_film_info(film):
    print(film)
    filmLink = f'https://letterboxd.com/film/{film}/'
    filmHtml = requests.get(filmLink).content
    filmSoup = bs4.BeautifulSoup(filmHtml, 'html.parser')

    filmInfo[film] = {}

    castTab = filmSoup.find('div', {'id': 'tab-cast'})
    if isTag(castTab, film):
        add_by_role2(film, castTab, 'actors', link=r'/actor/(.*)/')
    else: filmInfo[film]['actors'] = ['']

    crewTab = filmSoup.find('div', {'id': 'tab-crew'})
    if isTag(crewTab, film):
        add_by_role2(film, crewTab, 'directors', link=r'/director/(.*)/')
        add_by_role2(film, crewTab, 'originalWriters', link=r'/original-writer/(.*)/')
        add_by_role2(film, crewTab, 'composers', link=r'/composer/(.*)/')
    else:
        filmInfo[film]['directors'] = ['']
        filmInfo[film]['originalWriters'] = ['']

    detailsTab = filmSoup.find('div', {'id': 'tab-details'})
    if isTag(detailsTab, film):
        add_by_role2(film, detailsTab, 'countries', link=r'films/country/(.*)/')
    else: filmInfo[film]['countries'] = ['']

    genresTab = filmSoup.find('div', {'id': 'tab-genres'})
    if isTag(genresTab, film):
        add_by_role2(film, genresTab, 'genres', link=r'/films/genre/(.*)/')
    else: filmInfo[film]['genres'] = ['']

    year = filmSoup.find('a', {'href': re.compile(r'/films/year/([0-9]{4})/')})['href'][12:-1]
    filmInfo[film]['year'] = year
    name = filmSoup.find('section', {'id': 'featured-film-header'}).find('h1').text
    filmInfo[film]['name'] = name
    return filmInfo[film]

