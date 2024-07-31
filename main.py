import time

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
    wait.until(EC.presence_of_element_located((By. XPATH,
    '/html/body/div[1]/div/div/div/main/div/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[3]')))

    photo_pre_view = driver.find_element(By. XPATH,
    '/html/body/div[1]/div/div/div/main/div/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div[3]')
    photo_pre_view.click()
    wait.until(EC.presence_of_element_located((By. XPATH,
    '/html/body/div[3]/div[6]/div[2]/div/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div/button[2]/span[3]')))

    photo_view = driver.find_element(By. XPATH,
    '/html/body/div[3]/div[6]/div[2]/div/div/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div/button[2]/span[3]')
    photo_view.click()
    time.sleep(4)

    return input_object


def screenshot(input_object):
    screenshot = ImageGrab.grab(bbox=(790, 400, 1528, 800))
    try:
        screenshot.save(rf"C:\Users\BBFaiL\Desktop\{input_object}.png")
        screenshot.close()
    except:
        pass


# todo: image to text


def main():
    input_object = plebmasters()
    screenshot(input_object)


if __name__ == '__main__':
    main()