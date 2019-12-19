from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pyautogui

def read_file(filename):  # read data from file
    with open(filename, 'r') as file:
        return file.read()

browser = webdriver.Chrome(executable_path='chromedriver.exe')

base_url = "https://www.instagram.com/accounts/login/?hl=uk&source=auth_switcher"
login = read_file('login.txt')
password = read_file('password.txt')
profile_url = read_file('profile_url.txt')

browser.get(base_url)
time.sleep(2)
username_form = browser.find_element_by_class_name('gr27e ').find_element_by_name('username')
password_form = browser.find_element_by_class_name('gr27e ').find_element_by_name('password')

username_form.send_keys(login)
password_form.send_keys(password)

pyautogui.keyDown('enter')
pyautogui.keyUp('enter')
time.sleep(2)

browser.get(profile_url)
browser.find_elements_by_class_name('Y8-fY ')[1].click()

