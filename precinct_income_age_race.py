# PURPOSE: to determine the zipcodes that are most similar
# imports
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as stats
from scipy.stats import chi2_contingency

sns.set()
import math
import re

# Read in data. Data is already clean.
precinct_data = pd.read_csv("ExternalDataByZipcode.csv")
income_age_data = precinct_data[["Zip Codesort column", "Median Household Income", "Median Age"]]
income_age_data = income_age_data.set_index('Zip Codesort column')

# Create matrix where every entry is the absolute difference in med household income in precinct
incomes = pd.DataFrame(columns=income_age_data.index, index=income_age_data.index)
max_income_diff = 0  # keep track of max diff for normalization purposes later on
for zipcode2 in incomes.columns:
    for zipcode1 in incomes.index:
        med_income1_str = income_age_data.loc[zipcode1, "Median Household Income"]
        med_income2_str = income_age_data.loc[zipcode2, "Median Household Income"]
        # remove non-numeric vals from med_income1 and med_income2
        med_income1 = re.sub('[^0-9]', '', med_income1_str)
        med_income2 = re.sub('[^0-9]', '', med_income2_str)

        incomes.loc[zipcode1, zipcode2] = abs(float(med_income1) - float(med_income2))
        max_income_diff = max(max_income_diff, abs(float(med_income1) - float(med_income2)))
    # cast to floats
    incomes[zipcode2] = pd.to_numeric(incomes[zipcode2])

# Normalize incomes matrix
for zipcode1 in incomes.index:
    for zipcode2 in incomes.columns:
        incomes.loc[zipcode1, zipcode2] = 1 - incomes.loc[zipcode1, zipcode2] / max_income_diff

# Create matrix where every entry is the absolute difference in med age in precinct
ages = pd.DataFrame(columns=income_age_data.index, index=income_age_data.index)
max_age_diff = 0  # keep track of max diff for normalization purposes later on
for zipcode2 in ages.columns:
    for zipcode1 in ages.index:
        med_age1 = income_age_data.loc[zipcode1, "Median Age"]
        med_age2 = income_age_data.loc[zipcode2, "Median Age"]
        ages.loc[zipcode1, zipcode2] = abs(float(med_age1) - float(med_age2))
        max_age_diff = max(max_age_diff, abs(float(med_age1) - float(med_age2)))
    # cast to floats
    ages[zipcode2] = pd.to_numeric(ages[zipcode2])

# Normalize ages matrix
for zipcode1 in ages.index:
    for zipcode2 in ages.columns:
        ages.loc[zipcode1, zipcode2] = 1 - ages.loc[zipcode1, zipcode2] / max_age_diff

# make side-by-side heat map of med household income and med age
income_hmap = sns.heatmap(incomes, robust=True, cmap=sns.color_palette("mako", as_cmap=True))

# make side-by-side heat map of med household income and med age
age_hmap = sns.heatmap(ages, robust=True, cmap=sns.color_palette("mako", as_cmap=True))

hmaps, axes = plt.subplots(1, 2, figsize=(28, 10))
hmaps.suptitle("Comparison of Zipcodes by Demographic")
sns.heatmap(ax=axes[0], data=incomes, robust=True, cmap=sns.color_palette("mako", as_cmap=True))
sns.heatmap(ax=axes[1], data=ages, robust=True, cmap=sns.color_palette("mako", as_cmap=True))
axes[0].set_title("Similarity in Median Household Income")
axes[1].set_title("Similarity in Median Age")

# Analyzing race percentages in zipcodes
race_data = precinct_data[['Zip Codesort column', 'White Percentage', 'Black/AfricanAmerican Percentage',
                           'Pacific Islander Percentage', 'Asian Percentage',
                           'Other Race Population', '2+ Races Percentage', 'Population']]
race_data = race_data.set_index('Zip Codesort column')

# clean data to change percentages to decimals
for column in race_data.columns:
    for zipcode in race_data.index:
        race_data.loc[zipcode, column] = re.sub('[^0-9|.]', '', race_data.loc[zipcode, column])
    race_data[column] = pd.to_numeric(race_data.loc[:, column])

# if entry == 0, change it to be 0.001
for column in race_data.columns:
    for zipcode in race_data.index:
        if race_data.loc[zipcode, column] == 0:
            race_data.loc[zipcode, column] = 0.00001

# calculate mean percentages and insert at top of df
white_perc = race_data.loc[:, 'White Percentage'].mean(),
black_perc = race_data.loc[:, 'Black/AfricanAmerican Percentage'].mean(),
pi_perc = race_data.loc[:, 'Pacific Islander Percentage'].mean(),
asian_perc = race_data.loc[:, 'Asian Percentage'].mean(),
other_perc = race_data.loc[:, 'Other Race Population'].mean(),
twomore_perc = race_data.loc[:, '2+ Races Percentage'].mean()
means = pd.Series([race_data.loc[:, 'White Percentage'].mean(),
                   race_data.loc[:, 'Black/AfricanAmerican Percentage'].mean(),
                   race_data.loc[:, 'Pacific Islander Percentage'].mean(),
                   race_data.loc[:, 'Asian Percentage'].mean(),
                   race_data.loc[:, 'Other Race Population'].mean(),
                   race_data.loc[:, '2+ Races Percentage'].mean()])

actual_race_pop = pd.DataFrame(columns=["White", "Black", "Pacific Islander", "Asian", "Other", "2+"],
                               index=race_data.index)
for row_idx in range(0, race_data.shape[0]):
    for col_idx in range(0, race_data.shape[1] - 1):
        # population is last column in race_data
        actual_race_pop.iloc[row_idx, col_idx] = np.round(
            race_data.iloc[row_idx, col_idx] * race_data.iloc[row_idx, race_data.shape[1] - 1] / 100, 0)

# create matrix of zipcodes vs zipcodes to determine p-value of how different two zipcodes are in terms of racial distribution
races_pvalue = pd.DataFrame(columns=race_data.index, index=race_data.index)

for zipcode2 in race_data.index:
    for zipcode1 in race_data.index:
        # make a df for fisher exact test:
        #       zipcode1    zipcode2
        # races     %           %
        compare_two_zipcodes = [[race_data.loc[zipcode1, "White Percentage"],
                                 race_data.loc[zipcode1, "Black/AfricanAmerican Percentage"],
                                 race_data.loc[zipcode1, "Pacific Islander Percentage"],
                                 race_data.loc[zipcode1, "Asian Percentage"],
                                 race_data.loc[zipcode1, "Other Race Population"],
                                 race_data.loc[zipcode1, "2+ Races Percentage"]],
                                [race_data.loc[zipcode2, "White Percentage"],
                                 race_data.loc[zipcode2, "Black/AfricanAmerican Percentage"],
                                 race_data.loc[zipcode2, "Pacific Islander Percentage"],
                                 race_data.loc[zipcode2, "Asian Percentage"],
                                 race_data.loc[zipcode2, "Other Race Population"],
                                 race_data.loc[zipcode2, "2+ Races Percentage"]]]
        result = chi2_contingency(compare_two_zipcodes)
        races_pvalue.loc[zipcode1, zipcode2] = result[1]
    races_pvalue[zipcode2] = pd.to_numeric(races_pvalue[zipcode2])

hmap_race_dist = sns.heatmap(races_pvalue, robust=True, cmap=sns.color_palette("mako", as_cmap=True))
hmap_race_dist.set_title("p-value of Racial Distribution between Zipcodes")
