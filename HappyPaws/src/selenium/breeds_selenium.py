from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import requests
import time

PATH = r"C:\Users\khemo\Desktop\geckodriver.exe"
service = Service(executable_path=PATH)
driver = webdriver.Firefox(service=service)
driver.implicitly_wait(2)

columns = []
page = 1

driver.get("https://www.akc.org/dog-breeds/")

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for letter in letters:

    url = f"https://www.akc.org/dog-breeds/?letter={letter}"
    driver.get(url)

    keep_checking = True
    while keep_checking:
        try:
            button = driver.find_element(By.ID, "load-more-btn")
        except:
            button = None
            keep_checking = False
            print(f"No more button found")
            break
        button.click()
        time.sleep(2)

    elements = driver.find_elements(By.CSS_SELECTOR, ".breed-type-card__content a")
    links = [element.get_attribute('href') for element in elements]
    print (links)


    for link in links:
        driver.get(link)

        #Breed name
        breed_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-header__title"))).text
        print(breed_name)

        #Breed Description
        breed_description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "breed-page__about__read-more__text"))).text
        print(breed_description)

        #Health Description
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Health')]")))
        element.click()
        health_description = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "breed-table__accordion-padding__p")))
        print(health_description[1].text)

        