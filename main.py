import time
import pandas as pd

from image_manipulation import visionbot, description_image
from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_check_site = int(input('Укажите сайт, через который вы хотите работать, 1 - plebmasters; 2 - gta-objects (рекомендуется): '))


object_list = []

while True:
    user_input = input("Введите строку (или нажмите кнопку ENTER для завершения): ")
    if user_input.lower() == '':
        break
    object_list.append(user_input)

print(object_list)


wait = WebDriverWait(driver, 10)


def plebmasters(input_object):
    try:
        driver.get(f'https://forge.plebmasters.de/objects/{input_object}')
        print(f'Сейчас обрабатывается: {input_object}')
        time.sleep(2)

        img_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".normal > img:nth-child(2)")))
        img_url = img_element.get_attribute("src")
        print(f"URL изображения: {img_url}")
        return img_url

    except Exception as e:
        print(f"Ошибка при обработке {input_object} на plebmasters: {e}")
        return None


def gta_objects_xyz(input_object):
    try:
        img_url = f'https://gta-objects.xyz/gallery/objects/{input_object}.jpg'
        print(f'Сейчас обрабатывается: {input_object}')
        print(f"URL изображения: {img_url}")
        return img_url

    except Exception as e:
        print(f"Ошибка при обработке {input_object} на gta_objects_xyz: Файл не найден. {e}")
        return None


def main(object_list):
    results = []

    for input_object in object_list:
        try:
            if user_check_site == 1:
                img_url = plebmasters(input_object)
            else:
                img_url = gta_objects_xyz(input_object)

            description = visionbot(img_url)

            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")

            short_description = description_image(description)

            results.append({
                'hash': input_object,
                'Description': short_description
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
