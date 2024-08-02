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

        success_element = wait.until(EC.presence_of_element_located((By. ID, 'success1')))
        description = success_element.text

        return description

    except Exception as e:
        print(f"Ошибка при обработке изображения на visionbot: {e}")
        return "Ошибка обработки"


def description_image(description):
    try:
        driver.get('https://deepai.org/chat')

        # Ожидание появления текстового поля
        input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'chatbox')))
        input_box.clear()
        input_box.send_keys(f'Сократи описание объекта до 3 слов, не указывай логотипы и ватермарки, укажи самые нужные вещи. Пример: коричневое мягкое кресло. {description}')

        # Ожидание появления ответа
        body = wait.until(EC.visibility_of_element_located((By. CLASS_NAME, 'copytextButton')))  # Время ожидания ответа от сервиса DeepAI может быть разным
        time.sleep(3)
        ai_text = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[1]')))
        short_description = ai_text.text

        print(short_description)
        return short_description
    except Exception as e:
        print(f'Ошибка: {e}')

