from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()  # option Chrome
options.add_argument('headless')  # to open the browser in Headless mode
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)

base_url = "https://www.instagram.com/accounts/login/?hl=uk&source=auth_switcher"
login = ""
password = ""
username = ""
