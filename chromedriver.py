from selenium import webdriver

# Путь до расширения, блокирующего рекламу, которое написано под браузеры использующие Chromium
path = r'C:\Users\BBFaiL\PycharmProjects\Objects-Scraper-Gta-V\uBlock-Origin-Chrome.crx'

# Добавление расширения, отключения звука и скрытие окна браузера
options = webdriver.ChromeOptions()
options.add_extension(path)
options.add_argument("--mute-audio")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)