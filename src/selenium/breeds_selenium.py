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

#Currently crawling the chewy website for hip/joint supplements
driver.get("https://www.akc.org/dog-breeds/")
driver.implicitly_wait(2)

columns = []

dropdown = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "selectize-control custom-select__select single"))
)

try:
    dropdown.click()
except Exception as e:
    print("Exception print: " + str(e))

options = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'option') and @data-selectable='']"))
)

links = [option.get_attribute("data-value") for option in options]

while True:

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