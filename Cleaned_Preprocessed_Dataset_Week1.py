import pandas as pd

# Step 1: Load and Inspect Dataset
print(" ++ Load and Inspect Dataset ++")
df = pd.read_excel("SLU Opportunity Wise Data-1710158595043.xlsx", engine="openpyxl")

print(df.head())
df.info()
df.isnull().sum()

# Step 2: Data Cleaning
print(" ++ Data Cleaning ++ ")
# Converting date columns properly :
date_cols = [
    'Learner SignUp DateTime',
    'Opportunity Start Date',
    'Opportunity End Date',
    'Apply Date',
    'Entry created at',
    'Date of Birth'
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print("There Handling Missing Values ==>")

# for categorical columns:
categorical_cols = ['Gender', 'Country', 'Institution Name', 'Current/Intended Major']

df[categorical_cols] = df[categorical_cols].fillna("Unknown")
# Date of Birth missing values left as NaT (intentional)

print("There Removing Duplicates ==>")
df.drop_duplicates(inplace=True)

#  Step 3: Feature Engineering
print(" ++ Feature Engineering ++ ")
print("Calculating Age ==>")
df['Age'] = (
    (df['Learner SignUp DateTime'] - df['Date of Birth']).dt.days // 365
)


print("Opportunity Duration ==>")
df['Opportunity_Duration_Days'] = (
    df['Opportunity End Date'] - df['Opportunity Start Date']
).dt.days

print("Signup Month & Year ==>")
df['Signup_Month'] = df['Learner SignUp DateTime'].dt.month
df['Signup_Year'] = df['Learner SignUp DateTime'].dt.year


print("Application Delay Feature ==>")
df['Days_To_Apply'] = (
    df['Apply Date'] - df['Learner SignUp DateTime']
).dt.days

#
 # Step4: Data Validation
print(" ++ Data Validation ++ ")
df.isnull().sum()
df.describe()
df.sample(5)

df = df[df['Age'] > 0]

print(df)

# Step5: Save Cleaned Dataset
print(" ++ Save Cleaned Dataset ++ ")
df.to_csv("Cleaned_Preprocessed_Dataset_Week1.csv", index=False)

print