from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import requests
import time

PATH = r"C:\Users\khemo\Desktop\geckodriver.exe"
service = Service(executable_path=PATH)
driver = webdriver.Firefox(service=service)
driver.get("https://www.chewy.com/b/premium-food-132598")
driver.implicitly_wait(1)

columns = ["name" ,
    "ingredients" ,
    "crude_protein" ,
    "crude_fat" ,
    "crude_fiber" ,
    "moisture" ,
    "dietary_starch" ,
    "sugars",
    "epa",
    "eicosapentaenoic_acid_epa",
    "epa_eicosapentaenoic_acid" ,
    "dha",
    "docosahexaenoic_acid",
    "docosahexaenoic_acid_dha",
    "dha_docosahexaenoic_acid",
    "calcium" ,
    "ash",
    "l_carnitine",
    "bacillus_coagulants",
    "bacillus_coagulans",
    "taurine",
    "beta_carontene",
    "phosphorus" ,
    "phosphorous",
    "niacin",
    "chondroitin_sulfate",
    "pyridoxine_vitamin_b6",
    "vitamin_a",
    "vitamin_e" ,
    "ascorbic_acid",
    "ascorbic_acid_vitamin_c",
    "omega_6",
    "omega_6_fatty_acids" ,
    "omega_3",
    "omega_3_fatty_acids" ,
    "glucosamine" ,
    "glucoasmine",
    "zinc",
    "selenium",
    "microorganisms",
    "total_lactic_acid_microorganisms",
    "total_microorganisms"]

while True:

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "kib-product-title")))
    elements = driver.find_elements(By.CLASS_NAME, "kib-product-title")
    links = [element.get_attribute('href') for element in elements]
    count = 0

    for link in links:
        driver.get(link)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "styles_productName__vSdxx")))
            name_element = driver.find_element(By.CLASS_NAME, "styles_productName__vSdxx")
            name = name_element.text
            print(name)

            dropDown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Nutritional Information']")))
            dropDown.click()

            try :
                ingred_element = driver.find_element(By.XPATH, '//section[@id="INGREDIENTS-section"]/p')
                ingred = ingred_element.text
                print(ingred)
            except Exception as e:
                print("No ingredients found")

            product_info = {"type": "dry", "name": name, "ingredients": ingred}

            table_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//section[@id="GUARANTEED_ANALYSIS-section"]//table/tbody/tr')))

            for row in table_rows:

                try:
                    label = row.find_element(By.TAG_NAME, 'th').text.lower().replace(" ", "_").replace("-", "_").replace("*", "").replace("(", "").replace(")", "")
                    value = row.find_element(By.TAG_NAME, 'td').text
                    product_info[label] = value
                    if (label not in columns):
                        print(label + " Not found in database************")
                except StaleElementReferenceException:
                    print("Encountered a stale element reference, retrying...")


            print("Stepped out")
            api_url = "http://localhost:8000/api/food"
            print("api_url step")
            headers = {"Content-Type": "application/json",}
            response = requests.post(api_url, json=product_info, headers=headers)
            print("response step")

            if response.status_code == 201:
                print("Data posted successfully")
                count+=1
                print(str(count) + " rows added from page.")
            else:
                print(f"Failed to post data, status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error processing {link}: {e}")

    try:
        next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Next page']")
        next_page_button.click()
        time.sleep(10)
    except NoSuchElementException:
        print("No more pages to process.")
        break

driver.quit()
