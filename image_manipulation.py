import time

from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 60)


# Функция сайта visionbot, производящая описание изображения по его URL, подставленного из переменной "img_url"
def visionbot(img_url):
    try:
        driver.get('https://visionbot.ru/')

        # Поиск на сайте поля для ввода URL изображения и его ввод, с последующей обработкой от сайта
        paste_url = driver.find_element(By.XPATH, '//*[@id="userlink"]')
        paste_url.send_keys(img_url)
        paste_url.send_keys(Keys.ENTER)

        # Дожидаемся окончания описи изображения и записываем результат (описание) в отдельную переменную
        success_element = wait.until(EC.presence_of_element_located((By. ID, 'success1')))
        description = success_element.text

        # Возвращаем переменную, для последующей работы другой функцию
        return description

    # Обрабатываем возможные ошибки
    except Exception as e:
        print(f"Ошибка при обработке изображения на visionbot: {e}")
        return "Ошибка обработки"


# Функция сайта deepai, проводящая сокращение текста с использованием ИИ, подставленного из переменной "description"
def description_image(description):
    try:
        driver.get('https://deepai.org/chat')

        # Ожидание появления текстового поля и ввод promt'а с описанием подставленного из переменной "description"
        input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'chatbox')))
        input_box.clear()
        input_box.send_keys(f'Сократи описание объекта до 3 слов, не указывай логотипы и ватермарки, укажи самые нужные вещи. Пример: коричневое мягкое кресло. {description}')

        # Ожидание появления кнопки на экране, ждем маленькое количество времени, чтобы получить ответ и записываем
        # его в отдельную переменную
        body = wait.until(EC.visibility_of_element_located((By. CLASS_NAME, 'copytextButton')))
        time.sleep(3)
        ai_text = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[1]')))
        short_description = ai_text.text

        # Простое информирование пользователя в терминале с возвращением переменной, для работы другой функцию
        print(short_description)
        return short_description

    # Обрабатываем возможные ошибки
    except Exception as e:
        print(f'Ошибка: {e}')


def image_control(img_url):
    # Запись описание изображения в переменную "description"
    description = visionbot(img_url)

    # Очищение файлов куки, сессии и локальных файлов сайта, для обеспечения лучшей работы программы
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")

    # Запись сокращенного описания в переменную "short_description"
    short_description = description_image(description)

    return short_description