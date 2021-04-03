import requests

SRCS = {'infection_by_county.csv':
            'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
        'vaccination_by_state.csv':
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv'}
DIR = './'

for d in SRCS:
    req = requests.get(SRCS[d])
    url_content = req.content
    csv_file = open(DIR + d, 'wb')
    csv_file.write(url_content)
    csv_file.close()
