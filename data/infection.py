import requests

URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
DIR = '/Users/JG20021/Desktop/soeon/HSU/2021_spring/CS_480/MLproject/data/'
FILE = 'infection_by_county.csv'

req = requests.get(URL)
url_content = req.content
csv_file = open(DIR + FILE, 'wb')

csv_file.write(url_content)
csv_file.close()
