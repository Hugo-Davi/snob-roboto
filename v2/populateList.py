from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get('https://letterboxd.com/sign-in/')
# addFilm = browser.find_element(By.ID, 'frm-list-film-name')

wait = WebDriverWait(browser, 10)
element = wait.until(EC.url_to_be('https://letterboxd.com/'))
time.sleep(1)
# browser.find_element(By.ID, 'field-username').send_keys('$$$$$$$$$$$$')
# browser.find_element(By.ID, 'field-password').send_keys('$$$$$$$$$$$$')
# browser.find_element(By.XPATH, '//form').submit()

browser.get('https://letterboxd.com/cururu_dog/list/melhores-finais-que-ja-vi/edit/')
time.sleep(1)
addFilm = browser.find_element(By.ID, 'frm-list-film-name')
addFilm.send_keys('the-wolf-of-wall-street')
time.sleep(1)
addFilm.send_keys(Keys.RETURN)

time.sleep(5)

browser.quit()