import time
import pandas as pd

from image_manipulation import visionbot, description_image
from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
wait = WebDriverWait(driver, 10)


# Запрашиваем у пользователя выбор сайта для работы и преобразуем введенное значение в целое число
user_check_site = int(input('Укажите сайт, через который вы хотите работать, 1 - plebmasters; 2 - gta-objects: '))


# Создание списка для хранения N-ного количества hash'ей.
object_list = []

while True:
    user_input = input("Введите hash предмета (или нажмите кнопку ENTER для завершения): ")
    if user_input.lower() == '':
        break
    object_list.append(user_input)

print(object_list)


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


# Главная функция программы
def main(object_list):
    # Создание простого списка для вывода данных
    results = []

    # Итерация по каждому объекту в списке object_list
    for input_object in object_list:
        # Проверка выбора сайта пользователем и вызов соответствующей функции с записей результата в переменную
        if user_check_site == 1:
            img_url = plebmasters(input_object)
        else:
            img_url = gta_objects_xyz(input_object)

        # Проверка является ли переменная img_url = None
        if img_url is None:
            print(f"Пропущен объект {input_object}: получен None для URL изображения.")

            # Запись hash'а с сообщением об ошибке выполнения
            results.append({
                'hash': input_object,
                'Description': "Файл не найден."
            })

            # Продолжение программы со следующим элементом списка, пропуская ошибочный.
            continue

        # Запись описание изображения в переменную "description"
        description = visionbot(img_url)

        # Очищение файлов куки, сессии и локальных файлов сайта, для обеспечения лучшей работы программы
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")

        # Запись сокращенного описания в переменную "short_description"
        short_description = description_image(description)

        # Запись hash'а и его сокращенного описания в список
        results.append({
            'hash': input_object,
            'Description': short_description
        })

    # Создание DataFrame с использованием списка и сохранением его в CSV формат без записи индексов строк
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)

    # Закрывает окно браузера, завершаем сеанс WebDriver, освобождая ресурсы
    driver.close()
    driver.quit()


# Проверка, запущен ли скрипт напрямую и запуск главной функции программы
if __name__ == '__main__':
    main(object_list)
