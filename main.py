import time
from names import search_button, object_preview, model_3d, idk_button, User

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageGrab


options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


def plebmasters():
    input_object = input('Укажите название объекта: ')

    driver.maximize_window()
    driver.get('https://forge.plebmasters.de/')
    wait.until(EC.presence_of_element_located((By. XPATH, '//*[@id="input-8"]')))

    search = driver.find_element(By. XPATH, '//*[@id="input-8"]')
    search.clear()
    search.send_keys(input_object)
    search.send_keys(Keys.ENTER)
    wait.until(EC.presence_of_element_located((By. XPATH, search_button)))

    photo_pre_view = driver.find_element(By. XPATH, object_preview)
    photo_pre_view.click()
    wait.until(EC.presence_of_element_located((By. XPATH, model_3d)))

    photo_view = driver.find_element(By. XPATH, idk_button)
    photo_view.click()
    time.sleep(4)

    return input_object


def screenshot(input_object):
    screenshot = ImageGrab.grab(bbox=(790, 400, 1528, 800))
    try:
        screenshot.save(rf"C:\Users\{User}\Desktop\{input_object}.png")
        screenshot.close()
    except:
        pass


def main():
    input_object = plebmasters()
    screenshot(input_object)


if __name__ == '__main__':
    main()