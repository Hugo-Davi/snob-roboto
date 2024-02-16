import bs4

import requests
import re

from listsCatalog import listcatalog

for index, (key, value) in enumerate(listcatalog.items()):
    listLink = f'https://letterboxd.com/{value['link']}/detail'
    htmlLi = requests.get(listLink).content
    soupLi = bs4.BeautifulSoup(htmlLi, 'html.parser')
    if not isinstance(soupLi, bs4.element.Tag):
        print(f'{key} não possui uma lista válida')
        break
    listEn = soupLi.find('ul', {'class': 'js-list-entries poster-list -p70 film-list clear film-details-list'})
    if not isinstance(listEn, bs4.element.Tag):
        print(f'{key} não possui uma lista válida')
        break
    entries = listEn.find_all('a', {'href': re.compile(r'/film/(.*)/')})
    for entry in entries:
        print(entry)
#    for entry in entries:
# class="js-list-entries poster-list -p70 film-list clear film-details-list"