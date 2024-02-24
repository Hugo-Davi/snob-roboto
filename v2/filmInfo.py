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

def addByRole(film, href, name, role):
    if not href in peopleDict:
        peopleDict[href] = {'name': name}
    if not film in filmInfo:
        filmInfo[film] = {role: [href]}
    else:
        if role in filmInfo[film]: filmInfo[film][role].append(href)
        else: filmInfo[film][role] = [href]
    return

def getFilmInfo(film):
    print(film)
    filmLink = f'https://letterboxd.com/film/{film}/'
    filmHtml = requests.get(filmLink).content
    filmSoup = bs4.BeautifulSoup(filmHtml, 'html.parser')

    castTab = filmSoup.find('div', {'id': 'tab-cast'})
    if isTag(castTab, film):
        actors = castTab.findAll('a', {'href': re.compile(r'/actor/(.*)/')})
        for actor in actors:
            actorHref = actor['href'][7:-1]
            actorName = actor.text
            addByRole(film, actorHref, actorName, 'actors')

    crewTab = filmSoup.find('div', {'id': 'tab-crew'})
    if isTag(crewTab, film):
        directors = crewTab.findAll('a', {'href': re.compile(r'/director/(.*)/')})
        for director in directors:
            directorHref = director['href'][10:-1]
            directorName = director.text
            addByRole(film, directorHref, directorName, 'directors')

        originalWriters = crewTab.findAll('a', {'href': re.compile(r'/original-writer/(.*)/')})
        if originalWriters == []: filmInfo[film]['originalWriters'] = ['']
        for ogWriter in originalWriters:
            ogWriterHref = ogWriter['href'][10:-1]
            ogWriterName = ogWriter.text
            addByRole(film, ogWriterHref, ogWriterName, 'originalWriters')

    detailsTab = filmSoup.find('div', {'id': 'tab-details'})
    if isTag(detailsTab, film):
        countries = detailsTab.findAll('a', {'href': re.compile(r'/films/country/(.*)/')})
        for country in countries:
            countryName = country.text
            if not 'countries' in filmInfo[film]: filmInfo[film]['countries'] = [countryName]
            else: filmInfo[film]['countries'].append(countryName)
    genresTab = filmSoup.find('div', {'id': 'tab-genres'})
    if isTag(genresTab, film):
        genres = genresTab.findAll('a', {'href': re.compile(r'/films/genre/(.*)/')})
        for genre in genres:
            genreName = genre.text
            if not 'genres' in filmInfo[film]: filmInfo[film]['genres'] = [genreName]
            else: filmInfo[film]['countries'].append(genreName)

    year = filmSoup.find('a', {'href': re.compile(r'/films/year/([0-9]{4})/')})['href'][12:-1]
    filmInfo[film]['year'] = year
    name = filmSoup.find('section', {'id': 'featured-film-header'}).find('h1').text
    filmInfo[film]['name'] = name
    return filmInfo[film]

def generateArrayField(array):
    field = ''
    for x in array:
        if field == '': field = x
        else: field = f'{field};{x}'
    return field

def populateInfoDict():
    with open('films.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            filmHref = row[0]
            getFilmInfo(filmHref)
    with open('filmsF.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Title', 'Year', 'Rating', 'Href', 'Actors', 'Directors', 'Original Writers', 'Countries', 'Genres'])
        for key, values in filmInfo.items():
            print(f'csv {key}')
            fieldActors = generateArrayField(values['actors'])
            fieldDirec = generateArrayField(values['directors'])
            fieldOgW = generateArrayField(values['originalWriters'])
            fieldCount = generateArrayField(values['countries'])
            fieldGenr = generateArrayField(values['genres'])
            writer.writerow([values['name'],values['year'],'0', key, fieldActors, fieldDirec, fieldOgW, fieldCount, fieldGenr])

