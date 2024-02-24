import quo as quo
import filmInLists as filmInLists
from filmInfo import getFilmInfo, populateInfoDict

import csv

# a = getFilmInLists.getFilmsInLists()
# b = calculateFilms.calculateQuo(a)

# with open('films.csv', 'w', newline = '') as file:
#     writer = csv.writer(file)
#     fields = ['film', 'year', 'quo', 'detail']
#     writer.writerow(fields)
#     for key, values in b.items():
#         year = values['year']
#         quo = values['quo']
#         detail = values['detail']
#         writer.writerow([key, year, quo, detail])

populateInfoDict()