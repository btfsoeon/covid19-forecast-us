#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# processed infection in the US time-series(by date)
# calculate average

infection_us = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
infection_by_state = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
infection_us['date'] = pd.to_datetime(infection_us['date'], format='%Y-%m-%d', errors='raise')
infection_by_state['date'] = pd.to_datetime(infection_by_state['date'], format='%Y-%m-%d', errors='raise')
#population_us = pd.read_csv('')
population_by_state = pd.read_csv('./population_by_state.csv')[['GEO_NAME', 'B01001_001E']]
population_by_state = population_by_state.rename(columns={'GEO_NAME': 'state',
                                                          'B01001_001E': 'population'})
infection_by_state = pd.merge(infection_by_state, population_by_state, how="left", on=["state"])

# calculate infection percentage
infection_by_state.eval('cases_pct = cases / population', inplace=True)
infection_by_state.eval('deaths_pct = deaths / population', inplace=True)

infection_us.info()
infection_by_state.info()
infection_us.plot(x='date', y='cases')
infection_us.plot(x='date', y='deaths')


# average infection by state time-series(by date)
# variation or standard deviation by state compared to the averge of whole US

plt.figure(figsize=(20,10))
sns.lineplot(data = infection_by_state, x='date', y='cases_pct', hue='state')

plt.figure(figsize=(20,10))
sns.lineplot(data = infection_by_state, x='date', y='cases_pct')


# variance
# compare us total: state, us_total 

infection_us_avg = pd.DataFrame(infection_us)
for i, row in infection_us_avg.iterrows():
    infection_us_avg.at[i, 'cases'] = row['cases']/55
    infection_us_avg.at[i, 'deaths'] = row['deaths']/55
_agg = infection_by_state.append(infection_us_avg)
_agg.info()
_agg.head()
_agg['is_total'] = np.where(_agg['state'] != _agg['state'], 'US total', 'state')
plt.figure(figsize=(20,10))

sns.lineplot(data=_agg, x="date", y="cases", hue="is_total")

plt.figure(figsize=(20,10))
sns.lineplot(data = infection_by_state, x='date', y='deaths', hue='state')

plt.figure(figsize=(20,10))
sns.lineplot(data=_agg, x="date", y="deaths", hue="is_total")


# average infection by state time-series(by date)
# variation or standard deviation by count compared to average of the each state

infection_by_county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
infection_by_county['date'] = pd.to_datetime(infection_by_county['date'], format='%Y-%m-%d', errors='raise')

population_by_county = pd.read_csv('./population_by_county.csv')[['GEO_NAME', 'GEO_PARENT_NAME', 'B01001_001E']]
population_by_county = population_by_county.rename(columns={'GEO_NAME': 'county_tmp',
                                                          'GEO_PARENT_NAME': 'state',
                                                          'B01001_001E': 'population'})

def dropCounty(whole_county_name):
    if " County" in whole_county_name:
        return whole_county_name.replace(" County", "")
    return whole_county_name

population_by_county['county'] = dropCounty(population_by_county['county_tmp'])
infection_by_county = pd.merge(infection_by_county, population_by_county, how="left", on=["state", "county"])

infection_by_county.eval('cases_pct = cases / population', inplace=True)
infection_by_county.eval('deaths_pct = deaths / population', inplace=True)

infection_by_county.info()
infection_by_county.head()

# variance ranking


# california
infection_by_county_ca = infection_by_county.query("state == 'California'")
plt.figure(figsize=(20,10))
sns.lineplot(data=infection_by_county_ca, x="date", y="cases")


# infection - vaccination

vaccination_by_state = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
vaccination_by_state.drop(columns = ['total_distributed', 'people_vaccinated', 'people_vaccinated_per_hundred', 'daily_vaccinations_raw', 'daily_vaccinations', 'share_doses_used', 'distributed_per_hundred'],  inplace=True)
vaccination_by_state = vaccination_by_state.rename(columns={'location': 'state'})
vaccination_by_state['date'] = pd.to_datetime(vaccination_by_state['date'], format='%Y-%m-%d', errors='raise')
vaccination_by_state.info()
vaccination_by_state.head()

plt.figure(figsize=(20,10))
sns.lineplot(data=vaccination_by_state, x="date", y="people_fully_vaccinated_per_hundred", hue="state")


# aggregate infection - vaccination
_agg_iv = pd.merge(infection_by_state, vaccination_by_state, how="left", on=["date", "state"])

_agg_iv.info()
_agg_iv.head()

# calculate corr
pearsoncorr = _agg_iv.corr(method='pearson')

plt.figure(figsize=(10,8))
sns.heatmap(pearsoncorr, 
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5)


_agg_iv_simple = _agg_iv[['date','cases_pct', 'deaths_pct', 'people_fully_vaccinated_per_hundred']]

# calculate corr by date
pearsoncorr_by_date = _agg_iv_simple.groupby('date').corr(method='pearson')
print(pearsoncorr_by_date['cases_pct'])

# graph corr coff by date
date = []
cases_vacc_corr = []
deaths_vacc_corr = []
for cbd in pearsoncorr_by_date['cases_pct'].items():
    if cbd[1] == cbd[1]: # value exists
        if cbd[0][1] == 'people_fully_vaccinated_per_hundred':
            date.append(cbd[0][0])
            cases_vacc_corr.append(cbd[1])
for cbd in pearsoncorr_by_date['deaths_pct'].items():
    if cbd[1] == cbd[1]: # value exists
        if cbd[0][1] == 'people_fully_vaccinated_per_hundred':
            deaths_vacc_corr.append(cbd[1])

d = {'date': date, 'cases_corr': cases_vacc_corr, 'deaths_corr': deaths_vacc_corr}
plt.figure(figsize=(20,10))
sns.lineplot(data=d, x="date", y='cases_corr', legend='brief', label='cases_corr')
sns.lineplot(data=d, x="date", y='deaths_corr', legend='brief', label='deaths_corr')


# corr coff by state

import json
import urllib.request

# variants
with urllib.request.urlopen('https://raw.githubusercontent.com/USATODAY/covid-variants/master/combined.json') as j:
    d = json.loads(j.read().decode())

variants_by_state = []
for dl1 in d:
    for dl2 in d[dl1]:
        variants_by_state.append(d[dl1][dl2])

variants_by_state  = pd.json_normalize(variants_by_state)
variants_by_state = variants_by_state.rename(columns = {
    'filedate': 'date',
    'State': 'state',
    'mytotal': 'variants_total'})
variants_by_state['date'] = pd.to_datetime(variants_by_state['date'], format='%Y-%m-%d', errors='raise')

STATE_LIST = [
    "Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia",
    "Federated States of Micronesia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Marshall Islands", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
    "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands",
    "Ohio", "Oklahoma", "Oregon", "Palau", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Minor Outlying Islands",
    "Virgin Islands", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
STATE_ABBRE_LIST = [
    "AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC",
    "FM", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
    "ME", "MD", "MH", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "MP",
    "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UM",
    "VI", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

STATE_DIC = dict(zip(STATE_ABBRE_LIST, STATE_LIST))

for s in STATE_DIC:
    variants_by_state['state'] = variants_by_state['state'].replace(s, STATE_DIC[s])

variants_by_state.info()
variants_by_state.head()

plt.figure(figsize=(20,10))
sns.lineplot(data=variants_by_state, x='date', y='variants_total', hue='state')

# state ranking by recent date
variants_by_state_recent = variants_by_state[variants_by_state['date'] == variants_by_state['date'].max()]
variants_by_state_recent = variants_by_state_recent.sort_values(by=['variants_total'], ascending=False)


# correlation coefficient
_agg_iv = pd.merge(_agg_iv, variants_by_state, how="left", on=["date", "state"])

_agg_iv.info()
_agg_iv.head()


# calculate corr
pearsoncorr = _agg_iv.corr(method='pearson')

plt.figure(figsize=(10,8))
sns.heatmap(pearsoncorr, 
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5)


_agg_iv_simple = _agg_iv[['date','state','cases_pct', 'deaths_pct', 'people_fully_vaccinated_per_hundred', 'variants_total']]

# calculate corr by date
pearsoncorr_by_date = _agg_iv_simple.groupby('date').corr(method='pearson')

# graph corr coff by date
date = []
cases_vacc_corr = []
deaths_vacc_corr = []
variants_corr = []
for cbd in pearsoncorr_by_date['cases_pct'].items():
    if cbd[1] == cbd[1]: # value exists
        if cbd[0][1] == 'people_fully_vaccinated_per_hundred':
            date.append(cbd[0][0])
            cases_vacc_corr.append(cbd[1])
for cbd in pearsoncorr_by_date['deaths_pct'].items():
    if cbd[1] == cbd[1]: # value exists
        if cbd[0][1] == 'people_fully_vaccinated_per_hundred':
            deaths_vacc_corr.append(cbd[1])
for cbd in pearsoncorr_by_date['variants_total'].items():
    if cbd[1] == cbd[1]: # value exists
        if cbd[0][1] == 'people_fully_vaccinated_per_hundred':
            variants_corr.append(cbd[1])            

if len(variants_corr) < len(cases_vacc_corr):
    variants_corr = [None] * (len(cases_vacc_corr)-len(variants_corr)) + variants_corr

d = {'date': date, 'cases_corr': cases_vacc_corr, 'deaths_corr': deaths_vacc_corr, 'variants_corr': variants_corr}
plt.figure(figsize=(20,10))
plt.title( "Correlation coeffient with fully vaccinated percentage" , size = 24 )
sns.lineplot(data=d, x="date", y='cases_corr', legend='brief', label='cases_corr')
sns.lineplot(data=d, x="date", y='deaths_corr', legend='brief', label='deaths_corr')
sns.lineplot(data=d, x="date", y='variants_corr', legend='brief', label='variants_corr')


# clean data and export
_agg_iv_simple.to_csv('_agg_simple_by_state.csv', index=False)




