from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

from selenium.common.exceptions import NoSuchElementException
def checkExistByXpath(xpath):
    try:
        browser.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

browser = webdriver.Firefox()
browser.get('https://letterboxd.com/sign-in/')

wait = WebDriverWait(browser, 60)
wait.until(EC.url_to_be('https://letterboxd.com/'))
time.sleep(1)

# filmDict = getFilmInLists.getFilmsInLists()
# filmsF = calculateFilms.calculateQuo(filmDict)

browser.get('https://letterboxd.com/cururu_dog/list/lista-teste-teste-2/edit/')
time.sleep(1)
addFilm = browser.find_element(By.ID, 'frm-list-film-name')
addFilm.send_keys('teste')
time.sleep(1)
addFilm.send_keys(Keys.RETURN)
time.sleep(1)
browser.find_element(By.CSS_SELECTOR, 'a.list-item-remove.replace').click()
addFilm.clear()
time.sleep(2)
acResults = browser.find_element(By.CLASS_NAME,"ac_results" )
addNoteBox = browser.find_element(By.ID, "colorbox")
i = 1
with open('films.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        filmUrl = row[0]
        filmYear = row[1]
        filmQuo = row[2]
        filmDetails = row[3]
        addFilm.send_keys(f'{filmUrl}-{filmYear}')
        wait.until(EC.invisibility_of_element(acResults))
        find = False
        while not find:
            if acResults.find_element(By.CSS_SELECTOR, '.ac_even'): find = True
            print(f'{find} ac results')
        time.sleep(0.75)
        addFilm.send_keys(Keys.RETURN)
        time.sleep(0.5)
        find = False
        while not find:
            find = checkExistByXpath(f'//*[@id="list-items"]/li[{i+1}]/div[3]/div[2]/span/a')
            if find: editBtn = browser.find_element(By.XPATH, f'//*[@id="list-items"]/li[{i+1}]/div[3]/div[2]/span/a')
            print(f'{find} edit Btn')
            addFilm.send_keys(Keys.RETURN)
            # if browser.find_element(By.XPATH, f'//*[@id="list-items"]/li[{i+1}]/div[3]/div[2]/span/a'):
            #     editBtn = browser.find_element(By.XPATH, f'//*[@id="list-items"]/li[{i+1}]/div[3]/div[2]/span/a')
            #     find = True
        editBtn.click()
        time.sleep(0.5)
        wait.until(EC.invisibility_of_element, addNoteBox)
        textAreaDetail = addNoteBox.find_element(By.ID, 'frm-review')
        textAreaDetail.send_keys(f'<blockquote><b>Quo:</b> {filmQuo}\n</blockquote><blockquote>{filmDetails}</blockquote>')
        inputSaveBtn = browser.find_element(By.ID, 'list-entry-save-button')
        inputSaveBtn.click()
        i = i + 1
# /html/body/div[1]/div/form[1]/div[1]/article/section/ul/li[3]/div[3]/div[2]/span/a
time.sleep(5)

browser.quit()