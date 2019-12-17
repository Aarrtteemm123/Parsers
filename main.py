from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time, requests

# base urls for parse
base_url = "https://www.youtube.com/watch?v=wf62R6yQXmM"

options = webdriver.ChromeOptions()  # option Chrome
options.add_argument('headless')  # to open the browser in Headless mode
options.add_argument("window-size=1051,806")
# create browser
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
# create browser
browser.get(base_url)
time.sleep(5)
browser.execute_script("window.scrollTo(0, 800)")
time.sleep(3)
soup = bs(browser.page_source, 'lxml')
comment_blocks = soup.find_all('ytd-comment-thread-renderer', attrs={'class': 'style-scope ytd-item-section-renderer'})
for block in comment_blocks:
    user = block.find('a', attrs={'id': 'author-text'}).text  # user
    text = block.find('yt-formatted-string', attrs={'id': 'content-text'}).text  # user
    likes = block.find('span', attrs={'id': 'vote-count-middle'}).text  # user
    print(user,likes,text)
browser.quit()
