from selenium import webdriver
from bs4 import BeautifulSoup as bs

from selenium.webdriver.common.keys import Keys

base_url = "https://www.youtube.com/watch?v=0q2eqmjHdUg"

options = webdriver.ChromeOptions()  # option Chrome
options.add_argument('headless')  # to open the browser in Headless mode
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
browser.get(base_url)
html = browser.find_element_by_tag_name('html')
number_comment, comment_blocks = 0, []
counter_pause = 0
while True:
    for i in range(100):
        html.send_keys(Keys.END)

    soup = bs(browser.page_source, 'lxml')
    comment_blocks = soup.find_all('ytd-comment-thread-renderer',
                                   attrs={'class': 'style-scope ytd-item-section-renderer'})
    if len(comment_blocks) > number_comment:
        number_comment = len(comment_blocks)
        counter_pause = 0
    else:counter_pause+=1
    if counter_pause == 5: break

for block in comment_blocks:
    user = block.find('a', attrs={'id': 'author-text'}).text  # user
    text = block.find('yt-formatted-string', attrs={'id': 'content-text'}).text  # user
    likes = block.find('span', attrs={'id': 'vote-count-middle'}).text  # user
    print(user, likes, text)

browser.quit()
