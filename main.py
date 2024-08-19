import pandas as pd
import os
import webbrowser

from image_manipulation import create_text_description
from chromedriver import driver
from sites import plebmasters, gta_objects_xyz


file_path = 'input.txt'
def is_file_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.read()) == 0
    except FileNotFoundError:
        print(f"The {file_path} file was not found and was created.")
        open(file_path, 'a').close()
        return True


if is_file_empty(file_path):
    print("The file is empty. Please enter data.")
    object_list = []
    while True:
        user_input = input("Enter hash (or press Enter to finalize the entry): ")
        if user_input == "":
            break
        object_list.append(user_input.strip())
else:
    with open(file_path, 'r') as file:
        object_list = [line.strip() for line in file]

print(f'Your object list: {object_list}')


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


# Main program function
def main():
    # Create a simple list to output data
    pd.DataFrame(columns=['img_url', 'hash', 'Description']).to_csv('results.csv', index=False)
    results = []

    # Clean up the errors.txt file, if it is not in the directory - create it
    if os.path.exists('errors.txt'):
        open('errors.txt', 'w').close()
    else:
        open('errors.txt', 'a').close()

    # Iterate over each object in object_list
    for input_object in object_list:
        img_url = gta_objects_xyz(input_object)

        # Check if img_url = None, write error to file and skip erroneous object.
        if img_url is None:
            with open('errors.txt', 'a') as file:
                file.write(f'{input_object} \n')
            continue

        short_description = create_text_description(img_url)

        # Write hash and its abbreviated description to the list
        result = {
            'img_url': img_url,
            'hash': input_object,
            'Description': short_description
        }
        results.append(result)

        # Create a DataFrame using a list
        df = pd.DataFrame(results)
        df.to_csv('results.csv', mode='a', header=not os.path.exists('results.csv'), index=False)

    # Read errors and retry processing
    with open('errors.txt', 'r') as file:
        error_objects = [line.strip() for line in file]
        print(f'Список файлов на обработку: {error_objects}')

    for obj in error_objects:
        img_url = plebmasters(obj)
        short_description = create_text_description(img_url)

        # Write hash and its abbreviated description to the list
        result = {
            'img_url': img_url,
            'hash': obj,
            'Description': short_description
        }
        results.append(result)

        # Create DataFrame with new data. Saving the updated DataFrame to CSV format without writing row indexes
        df = pd.DataFrame([result])
        df.to_csv('results.csv', mode='a', header=False, index=False)

    html_content = create_html_from_df(pd.DataFrame(results))
    with open('results.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    webbrowser.open(f'file://{os.path.realpath("results.html")}')

    # Closes browser window, terminates WebDriver session, freeing resources
    driver.close()
    driver.quit()


# Check if the script is running directly and run the main function of the program
if __name__ == '__main__':
    main()
