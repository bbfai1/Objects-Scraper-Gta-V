import time
import getpass
import pyperclip
from names import search_tab, first_response, search_tab_gta_object_xyz, first_response_gta_object_xyz

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_check_site = int(input('Укажите сайт, через который вы хотите работать, 1 - plebmasters; 2 - gta-objects (рекомендуется): '))
input_object = str(input('Укажите название объекта: '))


options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_argument("--headless=new")


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 120)


def plebmasters(input_object):
    driver.maximize_window()
    driver.get('https://forge.plebmasters.de/')
    wait.until(EC.presence_of_element_located((By. XPATH, search_tab)))

    search = driver.find_element(By. XPATH, search_tab)
    search.clear()
    search.send_keys(f'{input_object}')
    search.send_keys(Keys.ENTER)
    print('Поиск завершен')
    wait.until(EC.visibility_of_element_located((By. XPATH, first_response)))

    first_layout = driver.find_element(By.XPATH, first_response)
    first_layout.click()
    print('Открыт объект')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".normal > img:nth-child(2)")))

    img_element = driver.find_element(By.CSS_SELECTOR, ".normal > img:nth-child(2)")
    img_url = img_element.get_attribute("src")
    print(f"URL изображения: {img_url}")
    return img_url


def gta_objects_xyz(input_object):
    driver.maximize_window()
    driver.get('https://gta-objects.xyz/objects')
    wait.until(EC.presence_of_element_located((By. XPATH, search_tab_gta_object_xyz)))

    search = driver.find_element(By. XPATH, search_tab_gta_object_xyz)
    search.clear()
    search.send_keys(f'{input_object}')
    search.send_keys(Keys.ENTER)
    print('Поиск завершен')
    wait.until(EC.presence_of_element_located((By.XPATH, first_response_gta_object_xyz)))

    first_layout = driver.find_element(By.XPATH, first_response_gta_object_xyz)
    first_layout.click()
    print('Открыт объект')
    wait.until(EC.presence_of_element_located((By.ID, "objectImage")))

    img_element = driver.find_element(By.ID, "objectImage")
    img_url = img_element.get_attribute("src")
    print(f"URL изображения: {img_url}")
    return img_url


def visionbot(img_url):
    driver.get('https://visionbot.ru/')
    time.sleep(0.1)

    paste_url = driver.find_element(By.XPATH, '//*[@id="userlink"]')
    paste_url.send_keys(img_url)
    paste_url.send_keys(Keys.ENTER)

    print('Вставлено')
    wait.until(EC.presence_of_element_located((By. ID, 'success1')))

    success_element = driver.find_element(By.ID, 'success1')
    text = success_element.text
    pyperclip.copy(text)

    print(text)


def main(input_object):
    if user_check_site == 1:
        img_url = plebmasters(input_object)
    else:
        img_url = gta_objects_xyz(input_object)
    visionbot(img_url)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main(input_object)