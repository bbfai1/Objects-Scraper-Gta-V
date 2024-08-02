from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)