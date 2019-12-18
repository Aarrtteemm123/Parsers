import color as color
import time

from Parser import YouTube_comment_parser

path_to_driver = "chromedriver.exe"
base_url = input("Input url to YouTube video: ")
print(color.blue('--> save url...'))

start = time.time()

parser = YouTube_comment_parser(base_url, path_to_driver)
parser.run_parser()
parser.save_csv()
parser.close()

print("Time parsing: "+str(round((time.time()-start), 3))+" s")
