import pandas as pd
import random

random.seed(1)

msdata = pd.read_csv("ms_data.csv")
print(msdata.head())
# handle missing data, but there's no Na here
print(msdata.isna().sum())

# Convert visit_date to datetime
msdata["visit_date"] = pd.to_datetime(msdata["visit_date"], format="%Y-%m-%d")

ms_sorted = msdata.sort_values(by=["patient_id", "visit_date"])

# Read insurance types
with open("insurance.lst", "r") as i:
    ins_type = i.readlines()
    ins_type = [line.rstrip("\n") for line in ins_type[1:]]

ins_rec = {}
patient_ids = msdata["patient_id"].unique()

# Each patient_id should always have the same insurance type
for patient_id in patient_ids:
    ran_ind = random.randint(0, len(ins_type) - 1)
    ins_rec[patient_id] = ins_type[ran_ind]

msdata["insurance_type"] = msdata["patient_id"].map(ins_rec)

# Add cost and variation
cost_base = {"Basic": 10000, "Premium": 5000, "Platinum": 2000, "NoInsurance": 20000}
# Consider seasonal variations: suppose in fall and winter (Aug-Jan next year),
# it will cost more for each visit on average
for ind, _ in msdata.iterrows():
    month_visit = msdata.loc[ind, "visit_date"].month
    if month_visit in [1, 8, 9, 10, 11, 12]:
        ran = random.randint(0, 1000)
    else:
        ran = random.randint(-500, 500)
    msdata.loc[ind, "costs"] = cost_base[msdata.loc[ind, "insurance_type"]] + ran

print(msdata.head())

print(f"Mean walking speed by education level:\n{msdata.groupby("education_level")["walking_speed"].mean()}")
print(f"\nMean costs by insurance type:\n{msdata.groupby("insurance_type")["costs"].mean()}")
print(f"\nAge effect on walking speed: {msdata["age"].corr(msdata['walking_speed']):.2f}")

# with open("readme.md", "a") as file:
#     file.write("# Summary of Q2<br>")
#     file.write(f"\nMean walking speed by education level:\n{msdata.groupby("education_level")["walking_speed"].mean()}<br>")
#     file.write(f"\nMean costs by insurance type:\n{msdata.groupby("insurance_type")["costs"].mean()}<br>")
#     file.write(f"\nAge effect on walking speed: {msdata["age"].corr(msdata['walking_speed']):.2f}")

msdata.to_csv('ms_data_Q2.csv', index=False)