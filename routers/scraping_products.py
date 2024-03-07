from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pprint
import requests
import zipfile
import os


router = APIRouter()

def scraping_favorites_products():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


    driver.get("https://us.shein.com/")
    driver.add_cookie({"name":"sessionID_shein","value":"s%3A4DRG6JPOE9wVLCpG-ZX1zegpcH_fE2JB.eyyrWSFDWRC8OWRgzhmWOXMUUl6EHHW%2FjcH%2BwG1GeX8"})

    try:
        wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-close"))).click()
        wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "svgicon-arrow-left"))).click()
        pass
    except:
        pass

    wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "header-wishlist"))).click()
    products = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "j-product-list-info")))
    products = products.get_attribute('innerHTML')
    soup = BeautifulSoup(products, 'html.parser')
        
    cards = soup.find_all('section', class_='wish-list__item')

    list_products = []
    

    for element in cards:
        name = element.find('a', class_='S-product-item__link').text
        value = element.find('span', class_='normal-price-ctn__sale-price').text
        image = element.find('div', class_='crop-image-container')['data-before-crop-src']

        card_info = {'name': name, 'value': value, 'image': f"https:{image}"}
        list_products.append(card_info)


    zip_file_path = "products.zip"
    with zipfile.ZipFile(zip_file_path, "w") as zip_file:
        for product in list_products:
            image_url = product["image"]
            image_data = requests.get(image_url).content
            image_filename = os.path.basename(image_url)
            zip_file.writestr(image_filename, image_data)

        
    driver.close()

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(list_products) 
    return {"products": list_products, "zip_file_path": zip_file_path}

@router.get("/")
async def get_favorites_products():
    return scraping_favorites_products()

@router.get("/download/{filename}")
def download_zip(filename: str):
    # Ruta para descargar el archivo zip
    return FileResponse(filename, media_type="application/zip", filename=filename)
