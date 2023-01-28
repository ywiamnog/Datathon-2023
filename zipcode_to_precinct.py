import pandas as pd

vote_sheet = pd.read_csv("cleaned_nov_votes.csv")

# dict maps zip to a set of precincts in that zip
zip_to_prec_dict = {}

# the reverse lol - doct that maps precincts to the zipcodes that they are in
prec_to_zip_dict = {}

for idx, row in vote_sheet.iterrows():

    zipcode = row.loc["ZIP"]
    if zipcode not in zip_to_prec_dict.keys():
        zip_to_prec_dict[zipcode] = {row.loc["Voting Precinct"]}
    else:
        zip_to_prec_dict[zipcode].add(row.loc["Voting Precinct"])

    precinct = row.loc["Voting Precinct"]

    if precinct not in prec_to_zip_dict.keys():
        prec_to_zip_dict[precinct] = {row.loc["ZIP"]}
    else:
        prec_to_zip_dict[precinct].add(row.loc["ZIP"])