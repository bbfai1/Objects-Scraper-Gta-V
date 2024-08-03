import pandas as pd
import os
import webbrowser

from image_manipulation import image_control
from chromedriver import driver
from sites import plebmasters, gta_objects_xyz

from selenium.webdriver.support.ui import WebDriverWait


wait = WebDriverWait(driver, 10)
file_path = 'input.txt'


def is_file_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.read()) == 0
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return False

if is_file_empty(file_path):
    print("Файл пустой. Пожалуйста, введите данные.")
    object_list = []
    while True:
        user_input = input("Введите hash (или нажмите Enter для завершения): ")
        if user_input == "":
            break
        object_list.append(user_input.strip())
else:
    with open(file_path, 'r') as file:
        object_list = [line.strip() for line in file]

print(f'Ваш список объектов: {object_list}')


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
                <td><img src="{row['img_url']}" alt="{row['Description']}"></td>
                <td>
                    <span id="hash-{row['hash']}">{row['hash']}</span>
                    <button class="copy-btn" onclick="copyToClipboard('hash-{row['hash']}')">Копировать</button>
                </td>
                <td>
                    <span id="desc-{row['Description']}">{row['Description']}</span>
                    <button class="copy-btn" onclick="copyToClipboard('desc-{row['Description']}')">Копировать</button>
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
    pd.DataFrame(columns=['img_url', 'hash', 'Description']).to_csv('results.csv', index=False)

    # Создание простого списка для вывода данных
    results = []

    # Итерация по каждому объекту в списке object_list
    for input_object in object_list:
        img_url = gta_objects_xyz(input_object)

        # Проверка является ли переменная img_url = None, запись ошибки в файл и пропуск ошибочного объекта.
        if img_url is None:
            print(f"Для объекта {input_object} не найдено изображения.")
            with open('errors.txt', 'a') as file:
                file.write(f'{input_object} \n')
            continue

        short_description = image_control(img_url)

        # Запись hash'а и его сокращенного описания в список
        result = {
            'img_url': img_url,
            'hash': input_object,
            'Description': short_description
        }
        results.append(result)

        # Создание DataFrame с использованием списка
        df = pd.DataFrame(results)
        df.to_csv('results.csv', mode='a', header=not os.path.exists('results.csv'), index=False)

    # Чтение ошибок и повторная попытка обработки
    with open('errors.txt', 'r') as file:
        error_objects = [line.strip() for line in file]
        print(f'Список файлов на обработку: {error_objects}')

    for obj in error_objects:
        img_url = plebmasters(obj)
        short_description = image_control(img_url)

        # Запись hash'а и его сокращенного описания в список
        result = {
            'img_url': img_url,
            'hash': obj,
            'Description': short_description
        }
        results.append(result)

        # Создание DataFrame с новыми данными. Сохранение обновленного DataFrame в CSV формат без записи индексов строк
        df = pd.DataFrame([result])
        df.to_csv('results.csv', mode='a', header=False, index=False)

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
