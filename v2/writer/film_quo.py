import csv
from listsCatalog import listcatalog

def write_film_csv_w_quo(dict):
    with open('fquo.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        header = ['href', 'quo']
        for listKey in listcatalog: header.append(listKey)
        writer.writerow(header)
        for key, values in dict.items():
            row = [key]
            for x in header:
                if x == 'href': continue
                if x in values: row.append(values[x])
                else: row.append(0)
            writer.writerow(row)