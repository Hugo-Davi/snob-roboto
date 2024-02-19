from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import getFilmInLists
import calculateFilms

browser = webdriver.Firefox()
browser.get('https://letterboxd.com/sign-in/')

wait = WebDriverWait(browser, 60)
wait.until(EC.url_to_be('https://letterboxd.com/'))
time.sleep(1)

filmDict = getFilmInLists.getFilmsInLists()
filmsF = calculateFilms.calculateQuo(filmDict)

browser.get('https://letterboxd.com/cururu_dog/list/lista-teste/edit/')
time.sleep(1)
addFilm = browser.find_element(By.ID, 'frm-list-film-name')
i = 1
print(filmsF)
for key, values in filmsF.items():
    print(key, values['quo'])
    addFilm.send_keys(key)
    time.sleep(2)
    addFilm.send_keys(Keys.RETURN)
    time.sleep(0.5)
    editBtn = browser.find_element(By.XPATH, f'//*[@id="list-items"]/li[{i+1}]/div[3]/div[2]/span/a')
    editBtn.click()
    time.sleep(1)
    textAreaDetail = browser.find_element(By.ID, 'frm-review')
    textAreaDetail.send_keys(f'<blockquote><b>Quo:</b> {values['quo']}\n</blockquote><blockquote>{values['detail']}</blockquote>')
    inputSaveBtn = browser.find_element(By.ID, 'list-entry-save-button')
    inputSaveBtn.click()
    time.sleep(1)
    i = i + 1

time.sleep(5)

browser.quit()