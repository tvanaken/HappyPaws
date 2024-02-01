from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
# from app.models import Base, User, Breed, Food, Pet, Reminder
# from db_manager import DBManager
import selenium.webdriver.support.ui
import time

PATH = r"C:\Users\khemo\Desktop\geckodriver.exe"
service = Service(executable_path=PATH)
driver = webdriver.Firefox(service=service)

driver.get("https://www.chewy.com/b/premium-food-132598")
print(driver.title)

driver.implicitly_wait(3)

elements = driver.find_elements(By.CLASS_NAME, "kib-product-title")

driver.implicitly_wait(3)

links = [element.get_attribute('href') for element in elements]

driver.implicitly_wait(3)



for link in links:

    driver.get(link)
    driver.implicitly_wait(2)

    print(driver.title)

    # Extract data
    element = driver.find_element(By.CLASS_NAME, "styles_productName__vSdxx")
    name = element.text
    print(name)

    # new_food = Food(type='dry', name=name, ingredients='')