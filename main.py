from color import color

from Parser import Insta_followers_parser
from colorama import init
init()  # init color code for logs
def read_file(filename):  # read data from file
    with open(filename, 'r') as file:
        return file.read()

login = read_file('login.txt')
password = read_file('password.txt')
profile_url = read_file('profile_url.txt')
print(color.green('--> saving your data...'))
parser = Insta_followers_parser(profile_url,login,password)
parser.run()
parser.save_csv()