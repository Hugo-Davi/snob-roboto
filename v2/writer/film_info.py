from v2.scrapping.film_page import get_film_info

import csv

def generate_array_field(array):
    field = ''
    for x in array:
        if field == '': field = x
        else: field = f'{field},{x}'
    return field

def populate_info_dict():
    with open('fquo.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            filmHref = row[0]
            get_film_info(filmHref)
    with open('filmsF.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Year', 'Rating', 'Href', 'Actors', 'Directors', 'Original Writers', 'Countries', 'Genres'])
        # for key, values in filmInfo.items():
        #     print(f'csv {key}')
        #     fieldActors = generate_array_field(values['actors'])
        #     fieldDirec = generate_array_field(values['directors'])
        #     fieldOgW = generate_array_field(values['originalWriters'])
        #     fieldCount = generate_array_field(values['countries'])
        #     fieldGenr = generate_array_field(values['genres'])
        #     writer.writerow([values['name'],values['year'],'0', key, fieldActors, fieldDirec, fieldOgW, fieldCount, fieldGenr])

