from Parser import YouTube_comment_parser

base_url = "https://www.youtube.com/watch?v=MDi05WQd6ZM&list=PLPWylTRFeg-BVCSwZM_CazmOAPKRk9l6o"
path_to_driver = "chromedriver.exe"

parser = YouTube_comment_parser(base_url, path_to_driver)
parser.run_parser()
parser.save_csv()
parser.close()
