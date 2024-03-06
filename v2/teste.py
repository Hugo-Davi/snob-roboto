import catalog.quo as quo
# import v2.catalog.filmInLists as filmInLists
from v2.scrapping.film_page  import get_film_info, populateInfoDict
from scrapping.list_page import get_films_in_lists
from catalog.quo import calculate_quo
from writer.film_quo import write_film_csv_w_quo

x = get_films_in_lists()
y = calculate_quo(x)
write_film_csv_w_quo(y)


# print(y)

# import csv



# populateInfoDict()