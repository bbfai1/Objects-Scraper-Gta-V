import requests
import win32clipboard
from PIL import Image
from io import BytesIO
import time

from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 60)


def visionbot(img_url):
    try:
        driver.get('https://visionbot.ru/')

        paste_url = driver.find_element(By.XPATH, '//*[@id="userlink"]')
        paste_url.send_keys(img_url)
        paste_url.send_keys(Keys.ENTER)

        print('Вставлено')
        success_element = wait.until(EC.presence_of_element_located((By. ID, 'success1')))
        description = success_element.text

        print(description)
        return description

    except Exception as e:
        print(f"Ошибка при обработке изображения на visionbot: {e}")
        return "Ошибка обработки"


def save_to_clipboard_photo(img_url):
    response = requests.get(url=img_url)
    image = Image.open(BytesIO(response.content))
    tempIO = BytesIO()
    image.save(tempIO, 'BMP')

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, tempIO.getvalue()[14:])
    win32clipboard.CloseClipboard()


def clear_image():
    driver.get('https://removal.ai/upload')

    body = driver.find_element(By. ID, 'upload-page-link')
    body.send_keys(Keys.CONTROL + 'v')

    finish = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rm-bg-result img')))
    time.sleep(7)
    finish_url = finish.get_attribute("src")
    print(f"URL изображения: {finish_url}")

    return finish_url