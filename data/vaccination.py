import requests

URL = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv'
DIR = '/Users/JG20021/Desktop/soeon/HSU/2021_spring/CS_480/MLproject/data/'
FILE = 'vaccination_by_state.csv'

req = requests.get(URL)
url_content = req.content
csv_file = open(DIR + FILE, 'wb')

csv_file.write(url_content)
csv_file.close()
