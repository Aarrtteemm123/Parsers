from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, re, time

def get_html_all_vac(dictionary):
    header = """ <html> <body> <h3 style="font-weight: bolder;color:black;">
                Hello!<br>See vacancies on Dou.ua</h3>"""
    html=header
    for language in list(dictionary.keys()):
        title = """ <br><h3 style="font-weight: bolder;color:black;">
                Language  """ + language + """<br>
                </h3><br><hr><br>"""
        body = ""
        for vac in dictionary[language]:
            body += """<p style="font-weight: normal;color:black;"> """ + vac + """ </p>"""
        html+=title+body
    end = "</body> </html>"
    return html + end

def get_html_new_vac(key, lst):
    title = """ <html> <body> <h3 style="font-weight: bolder;color:black;">
        Hello,good news!<br>See new vacancies from """ + key + """ on Dou.ua
        </h3><br><hr><br>"""
    body = ""
    for vac in lst:
        body += """<p style="font-weight: normal;color:black;"> """ + vac + """ </p>"""
    end = "</body> </html>"
    return title + body + end


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def send_email(from_email, to_email, password, message, title):
    msg = MIMEMultipart()
    msg['Subject'] = "Dou-jobs(Python,Java)"  # title don't work
    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)

base_urls = {'Java': 'https://jobs.dou.ua/vacancies/?city=%D0%92%D0%B8%D0%BD%D0%BD%D0%B8%D1%86%D0%B0&category=Java',
             'Python':'https://jobs.dou.ua/vacancies/?city=%D0%97%D0%B0%D0%BF%D0%BE%D1%80%D0%BE%D0%B6%D1%8C%D0%B5&category=Python'}
base_urls_keys = list(base_urls.keys())
vac_list = []
vac_by_lan={}

from_email = read_file('from_email.txt')
to_email = read_file('to_email.txt')
password = read_file('password.txt')
title = 'Dou-jobs(Python,Java)'
fl_update = True
start_time = time.time()

while True:
    for key in base_urls_keys:
        browser.get(base_urls[key])
        soup = BeautifulSoup(browser.page_source, 'lxml')
        # шукаєм потрібні блоки
        title_block = soup.find_all('div', attrs={'class': 'b-inner-page-header'})
        title = title_block[0].find('h1').text
        first_word = re.split(' ', title)[0]
        if first_word != 'Нет':
            number_vacancies = int(first_word)
            print(number_vacancies)
            while True:
                try:
                    browser.find_element_by_link_text('Больше вакансий').click()
                    time.sleep(1)
                except:
                    break
            soup = BeautifulSoup(browser.page_source, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'vacancy'})  # шукаєм потрібні блоки
            print(len(divs))
            new_vac = []
            for div in divs:
                try:
                    title = div.find('a', attrs={'class': 'vt'}).text  # назва вакансій
                    city = div.find('span', attrs={'class': 'cities'}).text  # місто
                    link = div.find('a', attrs={'class': 'vt'})['href']  # силка
                    vacancy = title + " (" + city + ")" + " " + link
                    if not vac_list.__contains__(vacancy):
                        new_vac.append(vacancy)
                        vac_list.append(vacancy)
                except:
                    pass
            if len(new_vac) != 0 and fl_update:
                send_email(from_email, to_email, password, get_html_new_vac(key, new_vac), title)
            now = time.time()
            vac_by_lan[key]=vac_list
            fl_update = True
            if now-start_time>1728000:#20 days
                start_time = now
                send_email(from_email, to_email, password, get_html_all_vac(vac_by_lan), title)
                vac_list.clear()
                fl_update = False
    time.sleep(60)

#browser.quit()
