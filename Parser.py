import csv
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class YouTube_parser_comment(object):

    def __init__(self, url, path_to_driver):
        options = webdriver.ChromeOptions()  # option Chrome
        options.add_argument('headless')  # to open the browser in Headless mode
        self.browser = webdriver.Chrome(executable_path=path_to_driver)
        self.url = url
        self.comment_info = []

    def run_parser(self):
        comment_bloks = self.load_data()
        self.parser(comment_bloks)
        self.browser.quit()

    def get_video_name(self):
        soup = bs(self.browser.page_source, 'lxml')
        for video_name in soup.find_all('h1', attrs={'class': 'title style-scope ytd-video-primary-info-renderer'}):
            return video_name.find('yt-formatted-string',
                                   attrs={'class': 'style-scope ytd-video-primary-info-renderer'}).text

    def save_csv(self, path=None):
        if path is None:
            path = self.get_video_name() + ".csv"
        with open(path, 'w+', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for i in range(len(self.comment_info)):
                try:
                    writer.writerow(self.comment_info[i])
                except:
                    print("Ooopppsss...")

    def load_data(self):
        number_comment, counter_pause = 0, 0
        self.browser.get(self.url)
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

    def parser(self, comment_bloks):
        self.comment_info = [["AUTHOR", "COMMENT", "LIKES"]]
        for block in comment_bloks:
            user = block.find('a', attrs={'id': 'author-text'}).text  # user
            text = block.find('yt-formatted-string', attrs={'id': 'content-text'}).text  # user
            likes = block.find('span', attrs={'id': 'vote-count-middle'}).text  # user
            likes = ' '.join(likes.split())
            user = ' '.join(user.split())
            self.comment_info.append([user, text, likes])
