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
        self.code_error = 0 # 1 if error
        print(color.green('--> connecting to browser...'))
        if fl_headless_mode:
            options = webdriver.ChromeOptions()  # option Chrome
            options.add_argument('headless')  # to open the browser in Headless mode
            # create "browser" object
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
            self.code_error = 1 # set code error
            return
        time.sleep(2) # pause for loading page data
        # finding form for input data
        input_username = self.browser.find_element_by_class_name('gr27e ').find_element_by_name('username')
        input_password = self.browser.find_element_by_class_name('gr27e ').find_element_by_name('password')
        # writing username and password into form
        input_username.send_keys(self.username)
        input_password.send_keys(self.password)
        print(color.green('--> login...'))
        # click by button input
        self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        time.sleep(3)

    def parser(self):
        if self.code_error == 1: return # check error
        print(color.green('--> opening profile...')) # console log
        try: self.browser.get(self.profile_url)
        except:
            print(color.red("--> error open profile url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
            return
        try:
            # set number followers for this string "X followers" from profile page
            number_followers = int(
                re.split(' ', self.browser.find_elements_by_class_name('-nal3 ')[1].get_attribute('text'))[0])
        except:
            print(color.red("--> error open profile url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
            return
        print(color.green('--> finding followers...'))
        # click by followers button
        self.browser.find_elements_by_class_name('Y8-fY ')[1].click()
        time.sleep(2)
        # get followers panel
        followers_panel = self.browser.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        print(color.green('--> parsing followers...'))
        if number_followers != 0:
            while len(self.followers_list) <= number_followers:
                for i in range(100): # down scrolling followers panel
                    self.browser.execute_script(
                        "arguments[0].scrollTop += 500", followers_panel)
                    time.sleep(0.1) # pause for loading page data
                soup = BeautifulSoup(self.browser.page_source, 'lxml') # get html code
                # finding followers block in html code by class name
                followers = soup.find_all('a', attrs={'class': 'FPmhX notranslate _0imsa'})
                for follower in followers:
                    if not self.followers_list.__contains__([follower.text]):
                        self.followers_list.append([follower.text]) # save result in list

    def save_csv(self, path="followers.csv"):
        if self.code_error == 1: return
        with open(path, 'w+', encoding='cp1251', newline='') as file:
            print(color.green('--> creating csv file...'))
            # create csv file
            writer = csv.writer(file, delimiter=';')
            print(color.green('--> saving result...'))
            for follower in self.followers_list:
                try:
                    # save in csv file
                    writer.writerow(follower)
                except:
                    print(color.yellow('--> follower not save:('))

    def exit_from_profile(self):
        if self.code_error == 1: return
        print(color.green('--> back to your profile...'))
        # back to user profile
        self.browser.get('https://www.instagram.com/' + str(self.username) + '/')
        time.sleep(3) # pause for loading page data
        self.browser.find_element_by_class_name('AFWDX').click()
        print(color.green('--> exiting from your profile...'))
        # click by button exit
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()

    def close_browser(self):
        print(color.green('--> closing browser...'))
        self.browser.quit() # close browser
