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

# Currently crawling the chewy website for hip/joint supplements
driver.get("https://www.chewy.com/b/hip-joint-1568")
driver.implicitly_wait(1)

columns = [
    "name",
    "description",
    "lifestage",
    "ailment",
    "health_condition",
    "breed_size",
]

dropdown = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "select.kib-input-select__control"))
)

select = Select(dropdown)
select.select_by_value("byPopularity")

while True:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "kib-product-title"))
    )
    elements = driver.find_elements(By.CLASS_NAME, "kib-product-title")
    links = [element.get_attribute("href") for element in elements]
    count = 0

    for link in links:
        driver.get(link)
        try:
            dropDown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='See More']")
                )
            )
            dropDown.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//section[@class="styles_infoGroupSection__ArCb9"]//table',
                    )
                )
            )
            name_element = driver.find_element(
                By.CLASS_NAME, "styles_productName__vSdxx"
            )
            name = name_element.text
            print(name)

            try:
                description_element = driver.find_element(
                    By.XPATH, '//section[@class="styles_infoGroupSection__ArCb9"]/p'
                )
                description = description_element.text
                print(description)
            except Exception as e:
                print("Description missed...")

            product_info = {
                "name": name,
                "health_condition": "Osteoarthritis, Hip Dysplasia, Joint Inflammation, Joint Pain, Joint Stiffness, Joint Support, Mobility",
                "description": description,
            }

            table_rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        '//div[contains(@class, "infoGroupSectionTitle") and contains(., "Specifications")]//following-sibling::div[contains(@class, "markdownTable")]//table/tbody/tr',
                    )
                )
            )

            for row in table_rows:
                try:
                    label = (
                        row.find_element(By.TAG_NAME, "th")
                        .text.lower()
                        .replace(" ", "_")
                        .replace("-", "_")
                        .replace("*", "")
                        .replace("(", "")
                        .replace(")", "")
                    )
                    value = row.find_element(By.TAG_NAME, "td").text
                    product_info[label] = value
                    print(label + " " + value)
                    if label not in columns:
                        print(label + " Not found in database************")
                except StaleElementReferenceException:
                    print("Encountered a stale element reference, retrying...")

            print("Stepped out")
            api_url = "http://localhost:8000/api/supplement"
            print("api_url step")
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(api_url, json=product_info, headers=headers)
            print("response step")

            if response.status_code == 201:
                print("Data posted successfully")
                count += 1
                print(str(count) + " rows added from page.")
            else:
                print(f"Failed to post data, status code: {response.status_code}")

        except Exception as e:
            print(f"Error processing {link}: {e}")

    try:
        next_page_button = driver.find_element(
            By.XPATH, "//button[@aria-label='Next page']"
        )
        next_page_button.click()
        time.sleep(10)
    except NoSuchElementException:
        print("No more pages to process.")
        break

driver.quit()
