from color import color

from Parser import Insta_followers_parser
from colorama import init

init()  # init color code for logs

login = input('username ')  # username your page
password = input('password ')  # password your page
profile_url = input('profile url ')  # profile url user where parse followers
fl_graphics_mode = input('run program with graphics mode?[y/n]') == 'y'
print(color.green('--> saving your data...'))
parser = Insta_followers_parser(profile_url, login, password, not fl_graphics_mode)
parser.run()  # starting main parser method
parser.save_csv()  # saving result
