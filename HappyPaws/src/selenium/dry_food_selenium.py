"""
This script is used to scrape data from the Chewy website for premium pet food products. It uses Selenium to automate the web scraping process.
The script performs the following steps:
1. Imports necessary libraries and modules.
2. Sets the path for the geckodriver executable.
3. Initializes the Selenium Firefox webdriver.
4. Navigates to the Chewy website.
5. Defines a list of columns for the scraped data.
6. Iterates through the pages of the website.
7. Scrapes data for each product on the page.
8. Extracts information such as name, image URL, site URL, rating, review count, ingredients, and various nutritional values.
9. Posts the scraped data to a local API endpoint.
10. Prints status messages and error messages during the scraping process.
Note: The script assumes that the geckodriver executable is located at the specified path and that the local API endpoint is running at http://localhost:8000/api/food.
Usage:
- Make sure geckodriver is installed and the path is correctly set.
- Run the script to start the web scraping process.
"""
import time
import requests
import boto3
import re
from botocore.exceptions import ClientError
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Desktop
PATH = r"G:\Local_VsCode\CapstoneAssetts\geckodriver.exe"
# Laptop
#PATH = r"C:\Users\khemo\Desktop\geckodriver.exe"

service = Service(executable_path=PATH)
driver = webdriver.Firefox(service=service)
# 12 total pages
driver.get("https://www.chewy.com/b/premium-food_c132598_p8")

columns = [
    "name",
    "image_url",
    "site_url",
    "rating",
    "review_count",
    "ingredients",
    "crude_protein",
    "crude_fat",
    "fat_content",
    "crude_fiber",
    "moisture",
    "dietary_starch",
    "sugars",
    "potassium",
    "epa",
    "eicosapentaenoic_acid_epa",
    "epa_eicosapentaenoic_acid",
    "dha",
    "docosahexaenoic_acid",
    "docosahexaenoic_acid_dha",
    "dha_docosahexaenoic_acid",
    "calcium",
    "ash",
    "crude_ash",
    "l_carnitine",
    "bacillus_coagulants",
    "bacillus_coagulans",
    "taurine",
    "beta_carontene",
    "phosphorus",
    "phosphorous",
    "niacin",
    "chondroitin_sulfate",
    "chondroitin_sulphate",
    "pyridoxine_vitamin_b6",
    "vitamin_a",
    "vitamin_e",
    "ascorbic_acid",
    "ascorbic_acid_vitamin_c",
    "omega_6",
    "omega-6",
    "omega_6_fatty_acids",
    "linoleic_acid_omega_6_fatty_acid",
    "omega_3",
    "omega-3",
    "omega_3_fatty_acids",
    "alpha_linolenic_acid_omega_3_fatty_acid",
    "glucosamine",
    "glucoasmine",
    "zinc",
    "selenium",
    "microorganisms",
    "total_lactic_acid_microorganisms",
    "total_microorganisms",
]

for page_number in range(2, 13):
    
    url = f"https://www.chewy.com/b/premium-food_c132598_p{page_number}"
    driver.get(url)
    print(f"Processing {url}")

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

                rating_element = driver.find_element(By.CLASS_NAME, "kib-product-rating__label")
                review_count_element = driver.find_element(By.CLASS_NAME, "styles_reviews___c7yt")
                rating_text = rating_element.text
                review_count_text = review_count_element.text
                match = re.search(r"Rated (\d+(\.\d+)?) out of 5 stars", rating_text)
                rMatch = re.search(r"(\d+)", review_count_text)
                if match and rMatch:
                    rating_number = match.group(1)
                    print(f"Rating: {rating_number}")
                    review_count = int(rMatch.group(1))
                    print(f"Review count: {review_count}")
                else:
                    print("Rating not found.")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "styles_productName__vSdxx")
                    )
                )
                name_element = driver.find_element(
                    By.CLASS_NAME, "styles_productName__vSdxx"
                )
                name = name_element.text
                print(name)

                dropDown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Nutritional Information']")
                    )
                )
                dropDown.click()

                try:
                    ingred_element = driver.find_element(
                        By.XPATH, '//section[@id="INGREDIENTS-section"]/p'
                    )
                    ingred = ingred_element.text
                    print(ingred)
                except Exception as e:
                    print("No ingredients found")

                product_info = {"type": "dry", "name": name, "ingredients": ingred, "rating": rating_number, "review_count": review_count, "site_url": link}

                table_rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            '//section[@id="GUARANTEED_ANALYSIS-section"]//table/tbody/tr',
                        )
                    )
                )

                try :
                    images = driver.find_elements(By.CLASS_NAME, "styles_mainCarouselImage__wj_bU")
                    if len(images) > 1:
                        image_url = images[0].get_attribute('src')
                        print(image_url)
                        product_info['image_url'] = image_url
                except Exception as e:
                    print(f"Error fetching or uploading image: {e}")

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
                        if label not in columns:
                            print(label + " Not found in database************")
                    except StaleElementReferenceException:
                        print("Encountered a stale element reference, retrying...")

                print("Stepped out")
                api_url = "http://localhost:8000/api/food"
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
