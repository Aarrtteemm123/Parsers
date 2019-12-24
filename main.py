from selenium import webdriver
from bs4 import BeautifulSoup
import time,re,pyautogui

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
input_username = browser.find_element_by_class_name('gr27e ').find_element_by_name('username')
input_password = browser.find_element_by_class_name('gr27e ').find_element_by_name('password')
input_username.send_keys(login)
input_password.send_keys(password)

pyautogui.keyDown('enter')
pyautogui.keyUp('enter')
time.sleep(2)

browser.get(profile_url)
number_followers = int(re.split(' ',browser.find_elements_by_class_name('-nal3 ')[1].get_attribute('text'))[0])
browser.find_elements_by_class_name('Y8-fY ')[1].click()
time.sleep(2)
followers_panel = browser.find_element_by_xpath('/html/body/div[4]/div/div[2]')
followers_list = []
while len(followers_list) < number_followers:
    for i in range(100):
        browser.execute_script(
            "arguments[0].scrollTop += 500",followers_panel)
        time.sleep(0.1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    followers = soup.find_all('a',attrs={'class':'FPmhX notranslate _0imsa'})
    for follower in followers:
        if not followers_list.__contains__(follower.text):
            followers_list.append(follower.text)

print(len(followers_list))
print(followers_list)
browser.quit()



