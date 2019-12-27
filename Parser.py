import csv, re, time
from bs4 import BeautifulSoup
from color import color
from selenium import webdriver
from colorama import init
init()  # init color code for logs

class Insta_followers_parser(object):
    def __init__(self, profile_url, username, password, fl_headless_mode=True):
        self.profile_url = profile_url
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com/accounts/login/?hl=uk&source=auth_switcher"
        self.followers_list = []
        self.code_error = 0
        print(color.green('--> connecting to browser...'))
        if fl_headless_mode:
            options = webdriver.ChromeOptions()  # option Chrome
            options.add_argument('headless')  # to open the browser in Headless mode
            self.browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        else:
            self.browser = webdriver.Chrome(executable_path='chromedriver.exe')

    def run(self):
        self.login()
        self.parser()
        self.exit_from_profile()
        self.close_browser()

    def login(self):
        print(color.green('--> opening browser...'))
        try: self.browser.get(self.base_url)
        except:
            print(color.red("--> error open url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
            return
        time.sleep(2)
        input_username = self.browser.find_element_by_class_name('gr27e ').find_element_by_name('username')
        input_password = self.browser.find_element_by_class_name('gr27e ').find_element_by_name('password')
        input_username.send_keys(self.username)
        input_password.send_keys(self.password)
        print(color.green('--> login...'))
        self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        time.sleep(3)

    def parser(self):
        if self.code_error == 1: return
        print(color.green('--> opening profile...'))
        try: self.browser.get(self.profile_url)
        except:
            print(color.red("--> error open profile url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
            return
        try:
            number_followers = int(
                re.split(' ', self.browser.find_elements_by_class_name('-nal3 ')[1].get_attribute('text'))[0])
        except:
            print(color.red("--> error open profile url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
            return
        print(color.green('--> finding followers...'))
        self.browser.find_elements_by_class_name('Y8-fY ')[1].click()
        time.sleep(2)
        followers_panel = self.browser.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        print(color.green('--> parsing...'))
        if number_followers != 0:
            while len(self.followers_list) <= number_followers:
                print('gfgf')
                for i in range(100):
                    self.browser.execute_script(
                        "arguments[0].scrollTop += 500", followers_panel)
                    time.sleep(0.1)
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                followers = soup.find_all('a', attrs={'class': 'FPmhX notranslate _0imsa'})
                for follower in followers:
                    if not self.followers_list.__contains__([follower.text]):
                        self.followers_list.append([follower.text])

    def save_csv(self, path="followers.csv"):
        if self.code_error == 1: return
        with open(path, 'w+', encoding='cp1251', newline='') as file:
            print(color.green('--> creating csv file...'))
            writer = csv.writer(file, delimiter=';')
            print(color.green('--> saving result...'))
            for follower in self.followers_list:
                try:
                    writer.writerow(follower)
                except:
                    print(color.yellow('--> follower not save:('))

    def exit_from_profile(self):
        if self.code_error == 1: return
        print(color.green('--> back to your profile...'))
        self.browser.get('https://www.instagram.com/' + str(self.username) + '/')
        time.sleep(3)
        print(color.green('--> click menu bar'))
        self.browser.find_element_by_class_name('AFWDX').click()
        print(color.green('--> click button exit'))
        print(color.green('--> exiting from your profile...'))
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()

    def close_browser(self):
        print(color.green('--> closing browser...'))
        self.browser.quit()
