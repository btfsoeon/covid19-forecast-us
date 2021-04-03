# covid19-forecast-usa

## Purpose

This project aims to predict COVID-19 infection in the US, 
hoping schools are going to be open soon.

For now (4/2/2021), more than 31 million people are infected in the US.
Cases have slowed down as vaccination distribution has been sped up. 
However, there are still other risks such as variants.


## Literature Review

The standard epidemiological models such as SIR, SEIR, and etc. have been challenged 
regarding the delivery of higher accuracy for long-term prediction. 
Due to the complex nature of the COVID-19 outbreak and variation in its behavior from nation-to-nation, 
many studies suggest machine learning as an effective tool to model the outbreak.

[COVID-19 Pandemic Prediction for Hungary; a Hybrid Machine Learning Approach](https://assets.researchsquare.com/files/rs-27132/v1_stamped.pdf)

[COVID-19 growth prediction using multivariate long short term memory](https://ui.adsabs.harvard.edu/abs/2020arXiv200504809Y/abstract)

[A County-level Dataset for Informing the United States’ Response to COVID-19](https://arxiv.org/pdf/2004.00756.pdf)

[Analysis and Prediction of COVID-19 using SIR, SEIR, and Machine Learning Models: Australia, Italy, and UK Cases](https://www.researchgate.net/publication/344646923_Analysis_and_Prediction_of_COVID-19_using_SIR_SEIR_and_Machine_Learning_Models_Australia_Italy_and_UK_Cases)

[Machine learning model estimating number of COVID-19 infection cases over coming 24 days in every province of South Korea (XGBoost and MultiOutputRegressor)](https://www.researchgate.net/publication/341392108_Machine_learning_model_estimating_number_of_COVID-19_infection_cases_over_coming_24_days_in_every_province_of_South_Korea_XGBoost_and_MultiOutputRegressor)

[Machine Learning Models for Government to Predict COVID-19 Outbreak](https://dl.acm.org/doi/10.1145/3411761)

[Modeling COVID-19 scenarios for the United States](https://www.nature.com/articles/s41591-020-1132-9)

[COVID-19 Outbreak Prediction with Machine Learning](https://www.medrxiv.org/content/10.1101/2020.04.17.20070094v1)

<!-- https://covid19-projections.com/model-details/

https://arxiv.org/abs/2004.01574

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7643377/

https://dl.acm.org/doi/pdf/10.1145/3411761

https://link.springer.com/article/10.1007/s11071-020-05743-y -->


## Dataset

### Infection per county
https://github.com/nytimes/covid-19-data
+ date
+ county
+ state
+ fips
+ cases
+ deaths


### Population per county
https://covid19.census.gov/datasets/population-county-2018
+ county
+ state
+ population
+ density


### Vaccination per county
https://covid.cdc.gov/covid-data-tracker/#county-view

#### Vaccination per state (temporarily)
https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations
+ date
+ state
+ people_fully_vaccinated_per_hundred


### Variant infection (additional dataset needed)
+ https://www.cdc.gov/coronavirus/2019-ncov/transmission/variant-cases.html
    + Location (state)
    + B.1.1.7 Variant
    + P.1. Variant
    + B.1.351  Variant

+ https://github.com/USATODAY/covid-variants


## Modeling
(coming soon)


## Reference
+ SIR model - https://github.com/marisae/param-estimation-SIR
+ Forecasting Models - https://www.cdc.gov/coronavirus/2019-ncov/covid-data/forecasting-us.html
