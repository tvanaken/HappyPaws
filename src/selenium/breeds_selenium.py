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


while page < 25:

    url = f"https://www.akc.org/dog-breeds/page/{page}/"
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "attachment-rectangle_thumbnail size-rectangle_thumbnail wp-post-image lozad ")))
    elements = driver.find_elements(By.CLASS_NAME, "link-with-arrow mbauto")
    links = [element.get_attribute('href') for element in elements]

    print(links)

    for link in links:
        driver.get(link)
        try:
            breed_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "page-header__title"))
            ).text
            print(breed_name)

            breed_info = {"name": breed_name}

        except Exception as e:
            print(f"Error processing {link}: {e}")

    page += 1