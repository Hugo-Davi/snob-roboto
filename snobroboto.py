from bs4 import BeautifulSoup

import requests
import re
import pyperclip

## SNOB ROBOTO
## V1.0 - 02 02 2024
## cururu_dog all rights reserved
## ------------------------------------------------------------------------ ##
## Arbitrary algorithm to generate a "quociente" of how much I should watch the film,
## with a smarty ass way to use letterboxd data (I was too lazy to get the API key kkkkk)
## --------------------------------------------------------------------------
## Um algorítmo arbitrário para gerar um quociente de quanto eu devo assitir o filme,
## com uma forma espertinha de usar as informações do letterboxd (Eu estava com preguiça de usar a API kkkkkkk)
## ------------------------------------------------------------------------ ##

## Film input
film = pyperclip.paste()
## String formatting to letterboxd URL
film = re.sub( r' ', '-', re.sub(r'\'|’', '', re.sub(r':', '', film.lower())))
## Quociente 0 for now (It can be till the end btw)
quociente = 0
quocientemodifiers = ''
page = 1
## Just add a list that should count in this Dictionary
listcatalog = {
    # criterium 0 = 2.5 + countrymod
    # criterium 1 = oldest more quociente points and mod of country
    # criterium 2 = 0.5 + countrymod
    "Letterboxd 250": {"link": "/dave/list/official-top-250-narrative-feature-films/", "criterium": 0},
    "IMDB 250": {"link": "/dave/list/imdb-top-250/", "criterium": 1},
    "Sight and Sound": {"link": "/bfi/list/sight-and-sounds-greatest-films-of-all-time/", "criterium": 0},
    "1001 Before Die": {"link": "/peterstanley/list/1001-movies-you-must-see-before-you-die/", "criterium": 2},
    "RYM 250": {"link": "/bman400/list/ryms-top-250-narrative-feature-films/", "criterium": 0},
    "Letterboxd 250 Most Fans": {"link": "/jack/list/official-top-250-films-with-the-most-fans/", "criterium": 1},
    "Metacritic Must See": {"link": "/richatthepics/list/metacritic-must-see-movies-of-all-time-metascore/", "criterium": 1},
    "Letterboxd 4.0+": {"link": "/mattheuswc/list/every-narrative-feature-film-on-letterboxd-1/", "criterium": 2},
    "TSPDT 1000": {"link": "/thisisdrew/list/they-shoot-pictures-dont-they-1000-greatest-1/", "criterium": 2},
    "New York Times 1000": {"link": "/mercurygothic/list/the-new-york-times-book-of-movies-the-essential/", "criterium": 2},
    "Palm D'or": {"link": "/list/palm-dor-winners-1939-2023/", "criterium": 0},
    "Oscar Best Picture": {"link": "/thaais/list/oscar/", "criterium": 0},
    "BFI 360 Classics": {"link": "/citizen_k/list/british-film-institute-sight-sound-360-film/", "criterium": 2}
}
## Array to check if the list has already found (0 = not found yet, 1 = found)
checklistocurr = []
for x in listcatalog:
    checklistocurr.append(0)
## Get film html
linkfilm = f'https://letterboxd.com/film/{film}'
htmlfilm = requests.get(linkfilm).content
soupfilm = BeautifulSoup(htmlfilm, 'html.parser')

## begin of Scrape year integer
year = int(soupfilm.find('a', {'href': re.compile(r'/films/year/([0-9]{4})/')}).string)
## end of Scrape year integer

## begin of Scrape countries array
allcountries = soupfilm.find_all('a', {'href': re.compile(r'/films/country/(.*)/')})
countries = []
usa = False
countrymod = 0
countryg0 = ['Japan', 'France', 'Germany', 'USSR', 'Italy', 'UK', 'South Korea']
for country in allcountries:
    if country.string == 'USA':
        usa = True
        countrymod = 0
    if country.string in countryg0 and not usa:
        countrymod = 0.5
    countries.append(country.string)
if countrymod == 0 and not usa:
    countrymod = 1
print(countries, countrymod)
## end of Scrape countries array

## ------------------------------------------------------------------------------------------ ##
## -- CODE LOGIC ---------------------------------------------------------------------------- ##
## ------------------------------------------------------------------------------------------ ##
def getlistsliked(p):
    if p == 1:
        linklists = f'https://letterboxd.com/cururu_dog/film/{film}/likes/lists/by/date/'
    elif p >= 2:
        linklists = f'https://letterboxd.com/cururu_dog/film/{film}/likes/lists/by/date/page/{p}/'
    else:
        print(f'Error at getlistliked p = {p}')
        return (None, False)
    htmllists = requests.get(linklists).content
    souplists = BeautifulSoup(htmllists, 'html.parser')
    return souplists.find('section', {"class": "list-set"}), True if souplists.find('a', {"class": "next"}) else False

def readlistspage(quocientemodifiers, quociente):
    for index, (key, value) in enumerate(listcatalog.items()):
        ## check if it was already found
        if checklistocurr[index] == 0:
            x = value['criterium']
            if listset.find('a', {'href': value['link']}):
                checklistocurr[index] = 1
                merit = 0
                match x:
                    case 0:
                        merit = 2.5 + countrymod
                    case 1:
                    # check the release date
                        if year > 1989 and year < 2005:
                            merit = 1
                        elif year > 1964 and year < 1990:
                            merit = 2
                        elif year < 1965:
                            merit = 3
                        else:
                            merit = 1
                        merit += countrymod
                    #
                    case 2:
                        merit = 0.5 + countrymod
                    case _:
                        merit = 1
                quocientemodifiers += f'{key}: {merit}\n'
                quociente += merit
    return (quocientemodifiers, quociente)
## ------------------------------------------------------------------------------------------ ##
## -- CODE LOGIC ---------------------------------------------------------------------------- ##
## ------------------------------------------------------------------------------------------ ##

## Get film "lists you liked" html
(listset, nextpage) = getlistsliked(page)

while nextpage or page == 1:
    if page != 1:
        (listset, nextpage) = getlistsliked(page)
        if listset == None:
            break
    (quocientemodifiers, quociente) = readlistspage(quocientemodifiers, quociente)
    print(nextpage, page, checklistocurr)
    page += 1
    if not 0 in checklistocurr:
        nextpage = False
        break

print(film, year)
output = f'<blockquote><b>Quociente: {quociente}</b></blockquote>\n<blockquote>{quocientemodifiers}</blockquote>'
print(output)
pyperclip.copy(output)