import time
import pyautogui
import getpass
from names import search_tab, first_response, view_3D, copy_button

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageGrab, Image
from io import BytesIO
import win32clipboard


input_object = str(input('Укажите название объекта: '))
User = getpass.getuser()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 60)


def plebmasters(input_object):
    driver.maximize_window()
    driver.get('https://forge.plebmasters.de/')
    wait.until(EC.presence_of_element_located((By. XPATH, search_tab)))

    search = driver.find_element(By. XPATH, search_tab)
    search.click()
    search.clear()
    search.send_keys(f'{input_object}')
    search.send_keys(Keys.ENTER)
    wait.until(EC.visibility_of_element_located((By. XPATH, first_response)))

    first_layout = driver.find_element(By.XPATH, first_response)
    first_layout.click()
    # wait.until(EC.visibility_of_element_located((By.XPATH, view_3D)))

    # view = driver.find_element(By. XPATH, view_3D)
    # view.click()
    time.sleep(4.5)


def screenshot(input_object):
    screenshot = ImageGrab.grab(bbox=(790, 400, 1528, 800))
    try:
        screenshot.save(rf"C:\Users\{User}\Desktop\{input_object}.png")
        screenshot.close()
    except:
        pass


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def image_to_clipboard():
    filepath = rf"C:\Users\{User}\Desktop\{input_object}.png"
    image = Image.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)


def visionbot():
    driver.get('https://visionbot.ru/')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'v')
    wait.until(EC.presence_of_element_located((By. ID, 'success1')))

    copy_text = driver.find_element(By. XPATH, copy_button)
    copy_text.click()


def main(input_object):
    plebmasters(input_object)
    screenshot(input_object)
    image_to_clipboard()
    visionbot()
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main(input_object)