import pandas as pd
import openpyxl

# read datasets
df_atm = pd.read_csv("phone_attempts.xlsx.csv")
df_con = pd.read_csv("phone_contacts.xlsx.csv")


# contact data with voter id and contact outcome
df_con = df_con[["Voter ID", "Contact Outcome"]]
df_con.head()

# remove null Voter ID
df_con = df_con[(df_con['Voter ID'] != "--")]

df_con_talk = df_con[(df_con['Contact Outcome'] == "Talking to Correct Person")]
df_con_talk.head()



# attempt data with voter id and result
df_atm = df_atm[["Voter ID", "Result"]]

# remove null Voter ID
df_atm = df_atm[(df_atm['Voter ID'] != "--")]

# possible results = {'Answering Machine', 'Busy Signal', 'Deliverability Error', 'Fax', 'No Answer', 'No Contact', 'Talked to Correct Person', 'Remove number from list'}
df_atm_con = df_atm[(df_atm['Result'] == "Talked to Correct Person")]



# calculate those talked to of the people who answered their phone
talk_percent = df_con_talk.shape[0] / df_con.shape[0]
print("percent talked to of those contacted:", talk_percent)

# calculate those contacted to of the total phone call attempts
contact_percent = df_atm_con.shape[0] / df_atm.shape[0]
print("percent contacted:", contact_percent)

# calculate those talked to of the total phone call attempts
talk_total_percent = df_con_talk.shape[0] / df_atm.shape[0]
print("total percent talked to:", talk_total_percent)

# print(df_atm)
# print(df_con_talk)
# print(df_atm_con)
