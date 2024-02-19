import bs4

import requests
import re

from listsCatalog import listcatalog
def isTag(prioriTag, key, index):
    if not isinstance(prioriTag, bs4.element.Tag):
        print(f'{key} do indice {index} do catalogo não possui uma lista válida')
        return False
    return True

def getFilmsInLists():
###### Output Dict
    filmsInLists = {
#        'the-godfather': {                         this dict looks like this
#            'lists': [['Letterboxd 250', 3]]       but with muuuch mooore films
#        }
    }
###### Output Dict
    for index, (key, value) in enumerate(listcatalog.items()):
        pageLinkFragment = f''
        nextPage = True
        p = 1 ## Page 1
        filmIndex = 1
        listLinkFragment = value['link']
        ## Reading list page
        while nextPage == True:
            print
            listLink = f'https://letterboxd.com/{listLinkFragment}/detail/{pageLinkFragment}'
            print(listLink)
            htmlLi = requests.get(listLink).content
            soupLi = bs4.BeautifulSoup(htmlLi, 'html.parser')
            if not isTag(soupLi, key, index): break
            listEn = soupLi.find('ul', {'class': 'js-list-entries poster-list -p70 film-list clear film-details-list'})
            if not isTag(listEn, key, index): break
            if soupLi.find('a', {'class': 'next'}):
                nextPage = True
                p = p + 1
            else:
                nextPage = False
            entries = listEn.find_all('a', {'href': re.compile(r'/film/(.*)/'), 'class': ''})
            ## Loop inside List entries
            for entry in entries:
                entryParent = entry.parent
                if not str(entryParent)[1:3] == 'h2': continue
                year = entryParent.find('a', {'href': re.compile(r'/films/year/([0-9]{4})/')})['href'][12:-1]
                href = f'{entry['href'][6:-1]}-{year}'
                if href not in filmsInLists:
                    filmListArray = {
                        'lists': [[key, filmIndex]]
                    }
                    filmsInLists[href] = filmListArray
                else:
                    filmsInLists[href]['lists'].append([key, filmIndex])
                filmIndex = filmIndex + 1
            pageLinkFragment = f'page/{p}'
    return filmsInLists