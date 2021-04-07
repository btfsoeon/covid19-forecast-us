#!/usr/bin/env python
# coding: utf-8

import json
import os

import pandas as  pd


file_dir = './'
files_csv = ['infection_by_county', 'population_by_county', 'vaccination_by_state']
files_json = ['variants_by_state']


df = {}
for f in files_csv:
    df[f] = pd.read_csv(file_dir + f + '.csv')

for d in df:
    print(df[d].head(5))

dj = {}
for f in files_json:
    with open(file_dir + f + '.json') as j:
        dj[f] = json.load(j)


### data preprocessing ###

## population ##

# drop columns
df['population_by_county'].drop(columns = ['OBJECTID', 'GEO_ID', 'GEO_LAND_AREA_SQ_KM', 'FIPS_CODE', 'B01001_001M', 'B09020_021E', 'B09020_021M'], inplace=True)
df['population_by_county'].info()

# rename B01001_001E to population from population_by_county
df['population_by_county'] = df['population_by_county'].rename(columns={'B01001_001E': 'population'})

# delete ' County' in'*** County' column from population_by_county
for i, row in df['population_by_county'].iterrows():
    if ' County' in row['GEO_NAME']:
        df['population_by_county'].at[i, 'GEO_NAME'] = row['GEO_NAME'].replace(' County', '')

# df.replace({'A': r'^ba.$'}, {'A': 'new'}, regex=True)
# see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.replace.html

df['population_by_county'] = df['population_by_county'].rename(columns={
    'GEO_NAME': 'county',
    'GEO_PARENT_NAME': 'state'})

# merge 'infection_by_county' and 'population_by_county'
infection_by_county =  pd.merge(df['infection_by_county'], df['population_by_county'], on=['state', 'county'], how='left')

# add column 'cases/population' , 'deaths/population'
infection_by_county['cases_ptc'] = infection_by_county['cases'] / infection_by_county['population']
infection_by_county['deaths_ptc'] = infection_by_county['deaths'] / infection_by_county['population']


## vaccination ##

# drop columns
df['vaccination_by_state'].drop(columns = ['total_distributed', 'people_vaccinated', 'people_vaccinated_per_hundred', 'daily_vaccinations_raw', 'daily_vaccinations', 'share_doses_used', 'distributed_per_hundred'],  inplace=True)

# join on state
df['vaccination_by_state'] = df['vaccination_by_state'].rename(columns={'location': 'state'})

# create
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




