import color as color

from Parser import YouTube_comment_parser

path_to_driver = "chromedriver.exe"
base_url = input("Input url to YouTube video:  ")
print(color.blue('--> save url...'))

parser = YouTube_comment_parser(base_url, path_to_driver)
parser.run_parser()
parser.save_csv()
parser.close()
