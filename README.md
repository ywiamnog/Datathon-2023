# Datathon-2023
## Inspiration
Rice Datathon 2023: The Baker Ripley Challenge.

## What it does
Who voted in the November election? What was the impact of each method? What about on different demographics? What was the cost of getting one person to vote? How did targeted precincts and non-targeted similar precincts compare to one another in terms of voter turnout?

## How we built it
Python: numpy, pandas, matplotlib, scipy, seaborn, re, openpyxl

## Challenges we ran into
We were unable to find demographic data from precincts. We were, however, able to find demographic data from zipcodes, so we mapped each precinct to its corresponding zipcode, computed the most similar zipcode, and mapped that back to the most similar untargeted precinct. Another challenge was to see how to best visualize the data to get as much insight as possible.

## Accomplishments that we're proud of
We are an underclassmen team, doing our first Datathon. We were challenged to find and compare similar precincts with the limited data that we had. We used Chi-squared contingency tests and Euclidean distance to compare median age, median household income, and racial demogrpahic distribution of each zipcode to determine the most similar precincts.

## What we learned
We learned to use pandas and other Python packages to clean, compute results, and extract useful information from large quantities of data.

## What's next for Baker Ripley Impact Analysis
Block walking had the best success of contacting a voter, but are also incredibly expensive. One solution would be to use walks to target specific areas or voters with demographics where voter turnout is the lowest. For example, older voters, or specific zip codes. Inexpensive texts and phone calls can be used to target lower priority voters.
