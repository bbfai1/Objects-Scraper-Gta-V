from selenium import webdriver

# Add extension, mute and hide browser window
options = webdriver.ChromeOptions()
options.add_extension('uBlock-Origin-Chrome.crx')
options.add_argument("--mute-audio")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)