import csv
from bs4 import BeautifulSoup as bs
from color import color
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class YouTube_comment_parser(object):

    def __init__(self, url, path_to_driver):
        print(color.green("--> setting browser options..."))
        options = webdriver.FirefoxOptions()  # create option Firefox
        options.headless = True  # set headless mode
        print(color.green("--> loading firefox driver..."))
        # create "browser" object
        self.browser = webdriver.Firefox(executable_path=path_to_driver, options=options)
        self.url = url
        self.comment_info = []  # result comment list
        self.code_error = 0  # 1 if url invalid
        self.number_error_save = 0  # number not saved comment
        self.number_comments = 0  # number all comment

    def run_parser(self):  # main parser method
        comment_blocks = self.load_data()
        self.parser(comment_blocks)

    def get_video_name(self):
        if self.code_error == 1: return
        print(color.green("--> finding video name..."))
        soup = bs(self.browser.page_source, 'lxml')  # get html code
        # find name video
        for video_name in soup.find_all('h1', attrs={'class': 'title style-scope ytd-video-primary-info-renderer'}):
            return video_name.find('yt-formatted-string',
                                   attrs={'class': 'style-scope ytd-video-primary-info-renderer'}).text

    def save_csv(self, path=None):
        if self.code_error == 1: return
        if path is None:  # set default name csv file
            path = self.get_video_name() + ".csv"
        with open(path, 'w+', encoding='cp1251', newline='') as file:
            print(color.green("--> creating csv file..."))
            writer = csv.writer(file, delimiter=';')  # create csv file
            print(color.green("--> saving..."))
            for i in range(len(self.comment_info)):
                try:
                    writer.writerow(self.comment_info[i])  # write comment in file
                except:
                    self.number_error_save += 1
                    print(color.yellow("--> ops..., comment save error :("))

    def load_data(self):
        if self.code_error == 1: return  # check open url error
        number_comment, counter_pause = 0, 0
        print(color.green("--> opening url..."))
        try:
            self.browser.get(self.url)  # open page in browser
        except:
            print(color.red("--> invalid url..."))
            self.browser.quit()  # close browser
            self.code_error = 1
        if self.code_error == 1: return
        print(color.green("--> start parsing..."))
        scroll = self.browser.find_element_by_tag_name('html')  # find button scroll
        while True:
            for i in range(100):
                scroll.send_keys(Keys.END)  # down scrolling

            soup = bs(self.browser.page_source, 'lxml')  # get html code
            # finding comment blocks
            comment_blocks = soup.find_all('ytd-comment-thread-renderer',
                                           attrs={'class': 'style-scope ytd-item-section-renderer'})
            if len(comment_blocks) > number_comment:  # check loading comment on page
                number_comment = len(comment_blocks)
                counter_pause = 0
            else:
                counter_pause += 1
            if counter_pause == 5: break  # pause for load comment
        return comment_blocks

    def parser(self, comment_blocks):
        if self.code_error == 1: return
        self.comment_info = [["AUTHOR", "COMMENT", "LIKES"]]  # name columns in csv file
        print(color.green("--> finding data..."))
        for block in comment_blocks:
            user = block.find('a', attrs={'id': 'author-text'}).text  # username
            text = block.find('yt-formatted-string', attrs={'id': 'content-text'}).text  # comment text
            likes = block.find('span', attrs={'id': 'vote-count-middle'}).text  # number likes
            likes = ' '.join(likes.split())  # delete superfluous spaces
            user = ' '.join(user.split())  # delete superfluous spaces
            self.comment_info.append([user, text, likes])  # save in comment list
        self.number_comments = len(self.comment_info)  # set number comments

    def close(self):
        print(color.green("--> close browser..."))  # log
        self.browser.quit()  # close browser
