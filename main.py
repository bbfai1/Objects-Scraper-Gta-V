import time
import pandas as pd
import os
import webbrowser

from image_manipulation import image_control
from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
wait = WebDriverWait(driver, 10)


def is_file_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.read()) == 0
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return False


file_path = 'input.txt'


if is_file_empty(file_path):
    print("Файл пустой. Пожалуйста, введите данные.")
    object_list = []
    while True:
        user_input = input("Введите hash (или просто нажмите Enter для завершения): ")
        if user_input == "":
            break
        object_list.append(user_input.strip())
else:
    with open(file_path, 'r') as file:
        object_list = [line.strip() for line in file]

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


def create_html_from_df(df):
    html_content = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Таблица с изображениями и описаниями</title>
        <style>
            .copy-btn {
                cursor: pointer;
                padding: 5px 10px;
                margin-left: 10px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            img {
                height: 350px; /* Высота изображения */
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f4f4f4;
            }
        </style>
    </head>
    <body>
        <h1>Таблицы с изображениями и описаниями</h1>
        <table>
            <thead>
                <tr>
                    <th>Изображение</th>
                    <th>Хэш</th>
                    <th>Описание</th>
                </tr>
            </thead>
            <tbody>
    '''
    for _, row in df.iterrows():
        html_content += f'''
            <tr>
                <td><img src="{row['img_url']}" alt="{row[' Description']}"></td>
                <td>
                    <span id="hash-{row[' hash']}">{row[' hash']}</span>
                    <button class="copy-btn" onclick="copyToClipboard('hash-{row[' hash']}')">Копировать</button>
                </td>
                <td>
                    <span id="desc-{row[' Description']}">{row[' Description']}</span>
                    <button class="copy-btn" onclick="copyToClipboard('desc-{row[' Description']}')">Копировать</button>
                </td>
            </tr>
        '''
    html_content += '''
            </tbody>
        </table>
        <script>
            function copyToClipboard(elementId) {
                var text = document.getElementById(elementId).innerText;
                var textArea = document.createElement("textarea");
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
            }
        </script>
    </body>
    </html>
    '''
    return html_content


# Главная функция программы
def main():
    # Создание простого списка для вывода данных
    results = []

    # Итерация по каждому объекту в списке object_list
    for input_object in object_list:
        img_url = gta_objects_xyz(input_object)

        # Проверка является ли переменная img_url = None
        if img_url is None:
            print(f"Пропущен объект {input_object}: получен None для URL изображения.")

            # Запись ошибки в файл
            with open('errors.txt', 'a') as file:
                file.write(f'{input_object} \n')

            # Продолжение программы со следующим элементом списка, пропуская ошибочный.
            continue

        short_description = image_control(img_url)

        # Запись hash'а и его сокращенного описания в список
        results.append({
            'img_url': img_url,
            ' hash': f' {input_object}',
            ' Description': f' {short_description}'
        })

    # Создание DataFrame с использованием списка
    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)

    # Чтение ошибок и повторная попытка обработки
    with open('errors.txt', 'r') as file:
        error_objects = [line.strip() for line in file]
        print(error_objects)

    for obj in error_objects:
        img_url = plebmasters(obj)

        short_description = image_control(img_url)

        # Запись hash'а и его сокращенного описания в список
        results.append({
            'img_url': img_url,
            ' hash': f' {obj}',
            ' Description': f' {short_description}'
        })

        # Создание DataFrame с новыми данными. Сохранение обновленного DataFrame в CSV формат без записи индексов строк
        df_retry = pd.DataFrame(results)
        df_retry.to_csv('results.csv', index=False)

    # Открываем файл errors.txt в режиме записи и очищаем его
    with open('errors.txt', 'w') as error_file:
        pass

    html_content = create_html_from_df(pd.DataFrame(results))
    with open('results.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    webbrowser.open(f'file://{os.path.realpath("results.html")}')

    # Закрывает окно браузера, завершаем сеанс WebDriver, освобождая ресурсы
    driver.close()
    driver.quit()


# Проверка, запущен ли скрипт напрямую и запуск главной функции программы
if __name__ == '__main__':
    main()
