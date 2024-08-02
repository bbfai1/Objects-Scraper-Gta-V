from selenium import webdriver

path = r'C:\Users\BBFaiL\PycharmProjects\Objects-Scraper-Gta-V\uBlock-Origin-Chrome.crx'

options = webdriver.ChromeOptions()
options.add_extension(path)
options.add_argument("--mute-audio")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)