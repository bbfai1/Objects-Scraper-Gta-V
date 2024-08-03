import time

from chromedriver import driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

wait = WebDriverWait(driver, 10)


# Функция сайта plebmasters, производящая поиск объекта на сайте, подставляя hash объекта в адресную строку
def plebmasters(input_object):
    try:
        driver.get(f'https://forge.plebmasters.de/objects/{input_object}')
        print(f'Сейчас обрабатывается: {input_object}')
        # Даем возможность прогрузится банеру с картинкой
        time.sleep(2)

        # Находим изображение объекта через CSS селектор
        img_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".normal > img:nth-child(2)")))
        img_url = img_element.get_attribute("src")
        print(f"URL изображения: {img_url}")

        # Возвращаем переменную, для последующей работы другой функцию
        return img_url

    # Обрабатываем возможные ошибки
    except Exception as e:
        print(f"Ошибка при обработке {input_object} на plebmasters: объект не найден. {e}")
        return None


# Функция сайта gta-objects, производящая поиск изображения объекта на сайте, подставляя hash объекта в адресную строку
def gta_objects_xyz(input_object):
    img_url = f'https://gta-objects.xyz/gallery/objects/{input_object}.jpg'
    print(f'Сейчас обрабатывается: {input_object}')
    print(f"Потенциальное URL изображения: {img_url}")

    # Проверка доступности hash'а объекта на сайте
    try:
        # Открываем URL, указанный в img_url. Ожидаем, пока 'title' станет видимым на странице.
        driver.get(img_url)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'title')))

        # Находим элемент с заголовком ошибки
        error_element = driver.find_element(By.XPATH, '//h1[@class="title pt-4 pb-4"]')

        # Проверяем, содержит ли текст элемента сообщение об ошибке 404.
        # Если ошибка найдена, выводим сообщение об ошибке и возвращаем None
        if "ERROR 404 :: Page not found" in error_element.text:
            print(f"Объект {input_object} не найден: ERROR 404")
            return None
        else:
            # Если ошибка 404 не найдена, возвращаем URL изображения
            return img_url

    # Обработка исключений, если элемент не найден или истекло время ожидания то возвращаем img_url
    except (NoSuchElementException, TimeoutException):
        return img_url
