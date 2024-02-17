import bs4

import requests
import re

from listsCatalog import listcatalog
def isTag(prioriTag, key, index):
    if not isinstance(prioriTag, bs4.element.Tag):
        print(f'{key} do indice {index} do catalogo não possui uma lista válida')
        return False
    return True

def fillListDict():
    listPopulated = listcatalog
    for key in listPopulated:
        listPopulated[key]['films'] = []
    for index, (key, value) in enumerate(listcatalog.items()):
        pageLinkFragment = f'/'
        nextPage = True
        p = 1 ## Page 1
        filmIndex = 1
        while nextPage == True:
            listLink = f'https://letterboxd.com/{value['link']}/detail{pageLinkFragment}'
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
            for entry in entries:
                href = entry['href'][6:-1]
                # print(filmIndex, entry['href'][6:-1])
                listPopulated[key]['films'].append({'index': filmIndex, 'href': href})
                filmIndex = filmIndex + 1
            pageLinkFragment = f'/page/{p}'
    return listPopulated