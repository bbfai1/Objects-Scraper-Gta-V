import time
import pandas as pd
from names import search_tab, first_response, search_tab_gta_object_xyz, first_response_gta_object_xyz

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_check_site = int(input('Укажите сайт, через который вы хотите работать, 1 - plebmasters; 2 - gta-objects (рекомендуется): '))


object_list = []

while True:
    user_input = input("Введите строку (или 'стоп' для завершения): ")
    if user_input.lower() == 'стоп':
        break
    object_list.append(user_input)

print(object_list)


options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_argument("--headless=new")


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)


def plebmasters(input_object):
    try:
        driver.maximize_window()
        driver.get('https://forge.plebmasters.de/')

        search = wait.until(EC.presence_of_element_located((By. XPATH, search_tab)))
        search.clear()
        search.send_keys(f'{input_object}')
        search.send_keys(Keys.ENTER)
        print('Поиск завершен')

        first_layout = wait.until(EC.visibility_of_element_located((By. XPATH, first_response)))
        first_layout.click()
        print('Открыт объект')

        img_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".normal > img:nth-child(2)")))
        img_url = img_element.get_attribute("src")
        print(f"URL изображения: {img_url}")
        return img_url

    except Exception as e:
        print(f"Ошибка при обработке {input_object} на gta-objects: {e}")
        return None


def gta_objects_xyz(input_object):
    try:
        driver.maximize_window()
        driver.get('https://gta-objects.xyz/objects')

        search = wait.until(EC.presence_of_element_located((By. XPATH, search_tab_gta_object_xyz)))
        search.clear()
        search.send_keys(f'{input_object}')
        search.send_keys(Keys.ENTER)
        print('Поиск завершен')

        first_layout = wait.until(EC.presence_of_element_located((By.XPATH, first_response_gta_object_xyz)))
        first_layout.click()
        print('Открыт объект')

        img_element = wait.until(EC.presence_of_element_located((By.ID, "objectImage")))
        img_url = img_element.get_attribute("src")
        print(f"URL изображения: {img_url}")
        return img_url

    except Exception as e:
        print(f"Ошибка при обработке {input_object} на plebmasters: {e}")
        return None


def visionbot(img_url):
    try:
        driver.get('https://visionbot.ru/')
        time.sleep(0.1)

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


def main(object_list):
    results = []

    for input_object in object_list:
        try:
            if user_check_site == 1:
                img_url = plebmasters(input_object)
            else:
                img_url = gta_objects_xyz(input_object)
            description = visionbot(img_url)

            results.append({
                'hash': input_object,
                'Description': description
            })

        except Exception as e:
            print(f"Ошибка при обработке объекта {input_object}: {e}")
            results.append({
                'hash': input_object,
                'Description': "Ошибка выполнения"
            })


    df = pd.DataFrame(results)
    df.to_csv('results.csv', index=False)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main(object_list)