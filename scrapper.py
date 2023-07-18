import string
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twocaptcha import TwoCaptcha

url = 'https://consulat.gouv.fr/ambassade-de-france-a-douala/rendez-vous?name=Visa'
#url = 'https://consulat.gouv.fr/ambassade-de-france-a-bogota/rendez-vous'
driver_path = 'D:\\Dev\\chromedriver\\chromedriver_win32\\chromedriver.exe'  

def bypass_captcha(driver)-> str:
    
    print("Tentative de résolution du captcha ...")
    solver = TwoCaptcha(apiKey='YOUR API KEY')
    # Perform captcha validation
    image_captcha = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, 'captcha-image'))
    )
    try:
        image_captcha.screenshot("foo.png")
    except:
        print("Problen when dowloading the captcha images")
    result = solver.normal('foo.png')
    print(f"Résolution du captcha ok : {result}")

    return result['code']

def get_available_days():
    #this function go to the website https://consulat.gouv.fr/ambassade-de-france-a-douala/rendez-vous?name=Visa
    #and verify if there is any timeslots available

    driver = webdriver.Chrome()
    driver.get(url)
    print("Passing First page")
    #pass the captcha
    input_captcha = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'gouv-step-captcha-input'))
    )
    input_captcha.send_keys( bypass_captcha(driver) )
    access_btn = driver.find_element( By.CLASS_NAME,"fr-icon-check-line")
    access_btn.click()

    print("Passing the Second page")
    time.sleep(1)
    choice = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, 'service-0'))
    )
    choice.click()
    confirm_btn = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'fr-icon-check-line'))
    )
    confirm_btn.click()

    print("Passing the Third Page")
    time.sleep(1)
    validate_chkbx = WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'custom-control-label'))
    )
    validate_chkbx.click()
    rdv_btn = driver.find_element(By.CLASS_NAME,"fr-icon-check-line")
    rdv_btn.click()

    print("Passing Fourth Page")
    time.sleep(3)
    WebDriverWait(driver, 10000).until(
        EC.presence_of_element_located((By.ID, 'main-content'))
    )

    print("GRAP THE ELEMENTS")
    html_containt = driver.page_source
    soup = BeautifulSoup(html_containt, "html.parser")
    available_days = soup.find_all('div', class_ = 'd-slot-container' ) 

    results = []
    if available_days :
        results = [ day.text
                    .replace("û", "u")
                    .replace("\n", "")
                    .replace("  ", "")
                    for day in available_days 
                ]
        print(f"\n\nHORAIRES DISPONIBLES \nNotification de l'utilisateur")
    else :
        print(f"\n\nAUCUNE HORAIRES DISPONIBLES ... Mise en veille")

    # Close the browser
    driver.quit()

    return results
