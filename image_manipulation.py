import time

from chromedriver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 180)


# Visionbot site function that describes an image by its URL substituted from the “img_url” variable.
def visionbot(img_url):
    try:
        driver.get('https://visionbot.ru/')

        # Search the site for an image URL field and enter it, followed by processing from the site
        paste_url = driver.find_element(By.XPATH, '//*[@id="userlink"]')
        paste_url.send_keys(img_url)
        paste_url.send_keys(Keys.ENTER)

        # Wait until the image inventory is complete and write the result (description) to a separate variable
        success_element = wait.until(EC.presence_of_element_located((By. ID, 'success1')))
        description = success_element.text

        # Return a variable for another function to use later on
        return description

    # Handle possible errors
    except Exception as e:
        print(f"Error during image processing on visionbot: {e}")
        return "Processing error"


# A deepai function that shortens text using AI substituted from the “description” variable
def description_image(description):
    try:
        driver.get('https://deepai.org/chat')

        # Waiting for the text field to appear and entering promt with the description substituted from the “description” variable
        input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'chatbox')))
        input_box.clear()
        input_box.send_keys(f'Сократи описание объекта до 3 слов, не указывай логотипы и ватермарки, укажи самые нужные вещи. Пример: коричневое мягкое кресло. {description}')

        # Wait for the button to appear on the screen, wait a small amount of time to get a response and write it down
        # it into a separate variable
        wait.until(EC.visibility_of_element_located((By. CLASS_NAME, 'copytextButton')))
        time.sleep(3)
        ai_text = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[1]')))
        short_description = ai_text.text

        # Simple informing the user in the terminal with a variable return, to run another function
        print(short_description)
        return short_description

    # Handle possible errors
    except Exception as e:
        print(f'Error: {e}')


def create_text_description(img_url):
    # Write the description of the image to the variable “description”
    description = visionbot(img_url)

    # Clearing cookies, session and local site files to ensure better program performance
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")

    # Write the short description to the variable “short_description”
    short_description = description_image(description)

    return short_description
