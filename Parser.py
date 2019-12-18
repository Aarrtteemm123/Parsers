import csv
from bs4 import BeautifulSoup as bs
from color import color
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class YouTube_comment_parser(object):

    def __init__(self, url, path_to_driver):
        print(color.green("--> setting browser options..."))
        options = webdriver.FirefoxOptions()  # option Chrome
        options.headless = True
        print(color.green("--> loading firefox driver..."))
        self.browser = webdriver.Firefox(executable_path=path_to_driver, options=options)
        self.url = url
        self.comment_info = []
        self.code_error = 0
        self.number_error_save = 0
        self.number_comments = 0

    def run_parser(self):
        comment_blocks = self.load_data()
        self.parser(comment_blocks)

    def get_video_name(self):
        if self.code_error == 1: return
        print(color.green("--> finding video name..."))
        soup = bs(self.browser.page_source, 'lxml')
        for video_name in soup.find_all('h1', attrs={'class': 'title style-scope ytd-video-primary-info-renderer'}):
            return video_name.find('yt-formatted-string',
                                   attrs={'class': 'style-scope ytd-video-primary-info-renderer'}).text

    def save_csv(self, path=None):
        if self.code_error == 1: return
        if path is None:
            path = self.get_video_name() + ".csv"
        with open(path, 'w+', encoding='cp1251', newline='') as file:
            print(color.green("--> creating csv file..."))
            writer = csv.writer(file, delimiter=';')
            print(color.green("--> saving..."))
            for i in range(len(self.comment_info)):
                try:
                    writer.writerow(self.comment_info[i])
                except:
                    self.number_error_save+=1
                    print(color.yellow("--> ops..., comment save error :("))

    def load_data(self):
        if self.code_error == 1: return
        number_comment, counter_pause = 0, 0
        print(color.green("--> opening url..."))
        try:
            self.browser.get(self.url)
        except:
            print(color.red("--> invalid url..."))
            self.browser.quit()
            self.code_error = 1
        if self.code_error == 1: return
        print(color.green("--> start parsing..."))
        html = self.browser.find_element_by_tag_name('html')
        while True:
            for i in range(100):
                html.send_keys(Keys.END)

            soup = bs(self.browser.page_source, 'lxml')
            comment_blocks = soup.find_all('ytd-comment-thread-renderer',
                                           attrs={'class': 'style-scope ytd-item-section-renderer'})
            if len(comment_blocks) > number_comment:
                number_comment = len(comment_blocks)
                counter_pause = 0
            else:
                counter_pause += 1
            if counter_pause == 5: break
        return comment_blocks

    def parser(self, comment_blocks):
        if self.code_error == 1: return
        self.comment_info = [["AUTHOR", "COMMENT", "LIKES"]]
        print(color.green("--> finding data..."))
        for block in comment_blocks:
            user = block.find('a', attrs={'id': 'author-text'}).text  # user
            text = block.find('yt-formatted-string', attrs={'id': 'content-text'}).text  # user
            likes = block.find('span', attrs={'id': 'vote-count-middle'}).text  # user
            likes = ' '.join(likes.split())
            user = ' '.join(user.split())
            self.comment_info.append([user, text, likes])
        self.number_comments = len(self.comment_info)

    def close(self):
        print(color.green("--> close browser..."))
        self.browser.quit()
