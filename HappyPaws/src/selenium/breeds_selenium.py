import time

import requests

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

PATH = r"C:\Users\khemo\Desktop\geckodriver.exe"
service = Service(executable_path=PATH)
driver = webdriver.Firefox(service=service)
driver.implicitly_wait(2)

columns = []
page = 1
count = 0

driver.get("https://www.akc.org/dog-breeds/")

letters = "ABCDEFGHIJKLMNOPRSTVWXY"
letters = "STVWXY"

for letter in letters:
    url = f"https://www.akc.org/dog-breeds/?letter={letter}"
    driver.get(url)
    time.sleep(2)

    keep_checking = True
    while keep_checking:
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "load-more-btn"))
            )
        except:
            button = None
            keep_checking = False
            print(f"No more button found")
            break
        button.click()
        time.sleep(2)

    elements = driver.find_elements(By.CSS_SELECTOR, ".breed-type-card__content a")
    links = [element.get_attribute("href") for element in elements]

    for link in links:
        driver.get(link)

        # Breed name
        breed_name = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located((By.CLASS_NAME, "page-header__title"))
            )
            .text
        )
        print(breed_name)

        # Weight
        weight_header = driver.find_element(
            By.XPATH, "//h3[contains(text(), 'Weight')]"
        )
        weight_paragraphs = weight_header.find_elements(
            By.XPATH, "./following-sibling::p"
        )
        weight_texts = [p.text for p in weight_paragraphs]
        weight_string = ", ".join(weight_texts)

        # Breed Description
        breed_description = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "breed-page__about__read-more__text")
                )
            )
            .text
        )

        # Health, Grooming, and Nutrition Description
        healthElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[contains(text(), 'Health')]")
            )
        )
        groomElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[contains(text(), 'Grooming')]")
            )
        )
        nutritionElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[contains(text(), 'Nutrition')]")
            )
        )
        healthElement.click()
        groomElement.click()
        nutritionElement.click()
        time.sleep(2)
        descriptions = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "breed-table__accordion-padding__p")
            )
        )
        health_description = descriptions[1].text
        groom_description = descriptions[2].text
        nutrition_description = descriptions[5].text

        api_url = "http://localhost:8000/api/breeds"
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(
            api_url,
            json={
                "name": breed_name,
                "weights": weight_string,
                "breed_description": breed_description,
                "health_description": health_description,
                "groom_description": groom_description,
                "nutrition_description": nutrition_description,
            },
            headers=headers,
        )

        if response.status_code == 201:
            print("Data posted successfully")
            count += 1
            print(str(count) + " rows added from page.")
        else:
            print(f"Failed to post data, status code: {response.status_code}")
