import bs4

import requests
import re
import csv

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

def isTag(prioriTag, key):
    if not isinstance(prioriTag, bs4.element.Tag):
        print(f'{key} erro não é tag')
        return False
    return True

def addByRole(film, href, name, role):
    if not href in peopleDict:
        peopleDict[href] = {'name': name}
    if not film in filmInfo:
        filmInfo[film] = {'actors': [href]}
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
            getFilmInfo(row[0])
    with open('filmInfo.csv', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for key, values in filmInfo.items():
            print(f'csv {key}')
            fieldActors = generateArrayField(values['actors'])
            fieldDirec = generateArrayField(values['directors'])
            fieldOgW = generateArrayField(values['originalWriters'])
            fieldCount = generateArrayField(values['countries'])
            fieldGenr = generateArrayField(values['genres'])
            writer.writerow([key, values['year'], fieldActors, fieldDirec, fieldOgW, fieldCount, fieldGenr])

