from color import color

from Parser import Insta_followers_parser
from colorama import init
init()  # init color code for logs

login = input('username ') # username your page
password = input('password ') # password your page
profile_url = input('profile url ') # profile url user where parse followers
print(color.green('--> saving your data...'))
parser = Insta_followers_parser(profile_url,login,password)
parser.run() # starting main parser method
parser.save_csv() # saving result