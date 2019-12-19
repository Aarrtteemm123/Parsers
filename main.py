import color as color
import time
from colorama import init
from Parser import YouTube_comment_parser

init()  # init color code for logs

path_to_driver = "geckodriver.exe"  # path to Firefox webdriver
base_url = input("Input url to YouTube video: ")  # input url
print(color.green('--> save url...'))  # log

start = time.time()  # start time
parser = YouTube_comment_parser(base_url, path_to_driver)
parser.run_parser()
parser.save_csv()
parser.close()  # close browser

print(color.cyan("All comments: " + str(parser.number_comments)))
print(color.yellow("No comments saved: " + str(parser.number_error_save)))
print(color.cyan("Time parsing: " + str(round((time.time() - start), 3)) + " s"))
input("Press any key to exit")
