#!/usr/bin/env python
# coding: utf-8

import json
import os
import shutil
import urllib.request

import pandas as pd

CSV_SRC = {
           'infection_by_county':
                'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
           'vaccination_by_state':
                'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv'
          }

JSON_SRC = {
            'variants_by_state':
                'https://raw.githubusercontent.com/USATODAY/covid-variants/master/combined.json'
           }

CSV_LOCAL = {
            'population_by_county':
                './population_by_county.csv'
            }

df = {}
for cs in CSV_SRC:
    try:
        df[cs] = pd.read_csv(CSV_SRC[cs])
    except Exception as e:
        print('Error: ', e)

dj = {}
for js in JSON_SRC:
    with urllib.request.urlopen(JSON_SRC[js]) as j:
        dj[js] = json.loads(j.read().decode())

print('Completed downloading!')

for cl in CSV_LOCAL:
    df[cl] = pd.read_csv(CSV_LOCAL[cl])

# for check
for d in df:
    print(df[d].head(5))

print('Completed data loading!')


### data preprocessing ###

## population ##
df['population_by_county'].drop(columns = ['OBJECTID', 'GEO_ID', 'GEO_LAND_AREA_SQ_KM', 'FIPS_CODE', 'B01001_001M', 'B09020_021E', 'B09020_021M'], inplace=True)
df['population_by_county'].info()

df['population_by_county'] = df['population_by_county'].rename(columns={
    'B01001_001E': 'population',
    'POP_DENSITY': 'pop_density'})

for i, row in df['population_by_county'].iterrows():
    if ' County' in row['GEO_NAME']:
        df['population_by_county'].at[i, 'GEO_NAME'] = row['GEO_NAME'].replace(' County', '')

# df.replace({'A': r'^ba.$'}, {'A': 'new'}, regex=True)
# see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html

df['population_by_county'] = df['population_by_county'].rename(columns={
    'GEO_NAME': 'county',
    'GEO_PARENT_NAME': 'state'})

infection_by_county =  pd.merge(df['infection_by_county'], df['population_by_county'], on=['state', 'county'], how='left')

infection_by_county['cases_pct'] = infection_by_county['cases'] / infection_by_county['population']
infection_by_county['deaths_pct'] = infection_by_county['deaths'] / infection_by_county['population']


## vaccination ##
df['vaccination_by_state'].drop(columns = ['total_distributed', 'people_vaccinated', 'people_vaccinated_per_hundred', 'daily_vaccinations_raw', 'daily_vaccinations', 'share_doses_used', 'distributed_per_hundred'],  inplace=True)

df['vaccination_by_state'] = df['vaccination_by_state'].rename(columns={'location': 'state'})

vaccination_by_state = df['vaccination_by_state']

# merge
#infection_by_county =  pd.merge(infection_by_county, data['vaccination_by_state'], on=['date', 'state'], how='left')


## variant ##
variants_by_state = []
for dl1 in dj['variants_by_state']:
    for dl2 in dj['variants_by_state'][dl1]:
        variants_by_state.append(dj['variants_by_state'][dl1][dl2])

variants_by_state  = pd.json_normalize(variants_by_state)
variants_by_state = variants_by_state.rename(columns = {
    'filedate': 'date',
    'State': 'state',
    'mytotal': 'total'})


### export ###
sfiles_dir = './processed'
if not os.path.exists(sfiles_dir):
    os.mkdir(sfiles_dir)

infection_by_county.to_csv(os.path.join(sfiles_dir, 'infection_by_county.csv'), index=False)
vaccination_by_state.to_csv(os.path.join(sfiles_dir, 'vaccination_by_state.csv'), index=False)
variants_by_state.to_csv(os.path.join(sfiles_dir, 'variants_by_state.csv'), index=False)


### compress ###
shutil.make_archive('processed', 'zip',  sfiles_dir)

print('Completed exporting!')
