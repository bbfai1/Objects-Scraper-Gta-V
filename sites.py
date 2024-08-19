import time

from chromedriver import driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

wait = WebDriverWait(driver, 10)


# Function of plebmasters site that searches for an object on the site by substituting the hash of the object in the address bar.
def plebmasters(input_object):
    try:
        driver.get(f'https://forge.plebmasters.de/objects/{input_object}')
        print(f'Now processing: {input_object}')
        # Let the banner with the image load
        time.sleep(2)

        # Find the object image via CSS selector
        img_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".normal > img:nth-child(2)")))
        img_url = img_element.get_attribute("src")
        print(f"Image URL: {img_url}")

        # Return a variable for another function to use later on
        return img_url

    # Handle possible errors
    except Exception as e:
        print(f"Error while processing {input_object} on plebmasters: object not found. {e}")
        return None


# Function of gta-objects site that searches for an image of an object on the site by substituting the hash of the object in the address bar.
def gta_objects_xyz(input_object):
    img_url = f'https://gta-objects.xyz/gallery/objects/{input_object}.jpg'
    print(f'Now processing: {input_object}')
    print(f'Potential image URL: {img_url}')

    # Check if object hash is available on the site
    try:
        # Open the URL specified in img_url. Wait for the 'title' to become visible on the page.
        driver.get(img_url)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'title')))

        # Find the element with the error header
        error_element = driver.find_element(By.XPATH, '//h1[@class="title pt-4 pb-4"]')

        # Check if the element text contains a 404 error message.
        # If an error is found, print the error message and return None
        if "ERROR 404 :: Page not found" in error_element.text:
            return None
        else:
            # If 404 error not found, return image URL
            return img_url

    # Exception handling, if item not found or timeout expired, return img_url
    except (NoSuchElementException, TimeoutException):
        return img_url
