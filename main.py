from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, re, time


def get_html_all_vac(dictionary):  # return all vacancies in html code
    header = """ <html> <body> <h3 style="font-weight: bolder;color:black;">
                Hello!<br>See vacancies on Dou.ua</h3>"""
    html = header
    for language in list(dictionary.keys()):  # language with vacancies list
        title = """ <br><h3 style="font-weight: bolder;color:black;">
                Language  """ + language + """<br>
                </h3><br><hr><br>"""
        body = ""
        for vac in dictionary[language]:  # list vacancies concrete language
            body += """<p style="font-weight: normal;color:black;"> """ + vac + """ </p>"""
        html += title + body
    end = "</body> </html>"
    return html + end


def get_html_new_vac(key, lst):  # return new vacancies in html code
    title = """ <html> <body> <h3 style="font-weight: bolder;color:black;">
        Hello,good news!<br>See new vacancies from """ + key + """ on Dou.ua
        </h3><br><hr><br>"""
    body = ""
    for vac in lst:
        body += """<p style="font-weight: normal;color:black;"> """ + vac + """ </p>"""
    end = "</body> </html>"
    return title + body + end


def read_file(filename):  # read data from file
    with open(filename, 'r') as file:
        return file.read()


def send_email(from_email, to_email, password, message, title):
    msg = MIMEMultipart()  # create msg object
    msg['Subject'] = "Dou-jobs(Python,Java)"  # value title don't work
    msg.attach(MIMEText(message, 'html'))  # attach text to msg
    server = smtplib.SMTP('smtp.gmail.com: 587')  # create server
    server.starttls()  # always use TLS protocol
    server.login(from_email, password)  # login
    server.sendmail(from_email, to_email, msg.as_string())  # send msg
    server.quit()  # destroy connection


options = webdriver.ChromeOptions()  # option Chrome
options.add_argument('headless')  # to open the browser in Headless mode
# create browser
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)

# base urls for parse
base_urls = {'Python': 'https://jobs.dou.ua/vacancies/?category=Python',
             'Java': 'https://jobs.dou.ua/vacancies/?category=Java'}
base_urls_keys = list(base_urls.keys())  # keys (Python and Java)
vac_list = []  # list with vacancies
vac_by_lan = {}  # list vacancies concrete language

from_email = read_file('from_email.txt')  # bot email
to_email = read_file('to_email.txt')  # your email
password = read_file('password.txt')  # password from your email
title = 'Dou-jobs(Python,Java)'  # title msg in email
fl_update = True  # flag for update list vacancies
start_time = time.time()  # start time

while True:  # main loop
    for key in base_urls_keys:
        browser.get(base_urls[key])  # open page in browser
        soup = BeautifulSoup(browser.page_source, 'lxml')  # get html code (lxml parser)
        # find title
        title_block = soup.find_all('div', attrs={'class': 'b-inner-page-header'})
        title = title_block[0].find('h1').text  # get text from title block
        first_word = re.split(' ', title)[0]  # get first word
        if first_word != 'Нет':
            while True:
                try:
                    # find and click button "Больше вакансий"
                    browser.find_element_by_link_text('Больше вакансий').click()
                    time.sleep(1)  # pause between clicks
                except:
                    break  # all vacancies are displayed
            soup = BeautifulSoup(browser.page_source, 'lxml')  # get html code
            divs = soup.find_all('div', attrs={'class': 'vacancy'})  # find title needed blocks
            new_vac = []  # list for new vacancies
            for div in divs:
                try:
                    title = div.find('a', attrs={'class': 'vt'}).text  # name vacancy
                    city = div.find('span', attrs={'class': 'cities'}).text  # city
                    link = div.find('a', attrs={'class': 'vt'})['href']  # link to vacancy
                    vacancy = title + " (" + city + ")" + " " + link
                    if not vac_list.__contains__(vacancy):  # find this vacancy in all
                        new_vac.append(vacancy)
                        vac_list.append(vacancy)
                except:  # if any tag is not found
                    pass
            if len(new_vac) != 0 and fl_update:  # send new vacancy to your email
                send_email(from_email, to_email, password, get_html_new_vac(key, new_vac), title)
            now = time.time()  # update time
            vac_by_lan[key] = vac_list  # attach vacancies to concrete language
            fl_update = True  # miss first iteration after update lists
            if now - start_time > 1728000:  # period of mailing (20 days)
                start_time = now  # update timer
                send_email(from_email, to_email, password, get_html_all_vac(vac_by_lan), title)
                vac_list.clear()  # update vacancy list
                fl_update = False
    time.sleep(60)  # pause between parse pages

# browser.quit()  # close browser
