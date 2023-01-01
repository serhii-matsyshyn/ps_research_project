import pandas as pd
import numpy as np

country = 'Hungary'
remove_born = False

# Read in the data
df = pd.read_csv(r"dataset_original/death_dataset.csv", header=0)

# Extract only Finland
df = df[df['Country or Area'] == country]
df = df.drop(columns=['Value Footnotes'])


def check_if_age_is_valid(x):
    if x in (0, '0',):
        return True
    elif '-' in str(x):
        return True
    elif '+' in str(x):
        return True
    return False


df = df[df['Age'].apply(check_if_age_is_valid)]


def remove_age_group(df, row, age_group):
    return df.drop(df[(df['Country or Area'] == row['Country or Area']) & (df['Year'] == row['Year']) &
                      (df['Area'] == row['Area']) & (df['Sex'] == row['Sex']) & (df['Age'] == age_group)].index)


def get_age_group(df, row, age_group):
    return df[(df['Country or Area'] == row['Country or Area']) & (df['Year'] == row['Year']) &
              (df['Area'] == row['Area']) & (df['Sex'] == row['Sex']) & (df['Age'] == age_group)]


if remove_born:
    # If Country or Area,Year,Area,Sex and "Age" is "0 - 4" - remove all rows with "Age" "0" and "1 - 4"
    for index, row in df.iterrows():
        if row['Age'] == '0 - 4':
            df = remove_age_group(df, row, '0')
            df = remove_age_group(df, row, '1 - 4')

    # If Country or Area,Year,Area,Sex and "Age" is "0" - add row with "Age" "0 - 4" and Value = Value of "1 - 4" + Value of "0"
    # remove all rows with "Age" "0" and "1 - 4"

    for index, row in df.iterrows():
        if row['Age'] == '0':
            row_1_4 = get_age_group(df, row, '1 - 4')

            row_new = row
            row_new['Age'] = '0 - 4'
            row_new['Value'] = row['Value'] + row_1_4['Value'].values[0]
            df = df.append(row_new, ignore_index=True)

            df = remove_age_group(df, row, '0')
            df = remove_age_group(df, row, '1 - 4')

for index, row in df.iterrows():
    if row['Age'] == '80 +':
        df = remove_age_group(df, row, '85 +')
        df = remove_age_group(df, row, '90 +')
        df = remove_age_group(df, row, '95 +')
        df = remove_age_group(df, row, '100 +')

for index, row in df.iterrows():
    if row['Age'] == '85 +':
        row_80_84 = get_age_group(df, row, '80 - 84')

        row_new = row
        row_new['Age'] = '80 +'
        row_new['Value'] = row['Value'] + row_80_84['Value'].values[0]
        df = df.append(row_new, ignore_index=True)

        df = remove_age_group(df, row, '80 - 84')
        df = remove_age_group(df, row, '85 +')
        df = remove_age_group(df, row, '90 +')
        df = remove_age_group(df, row, '95 +')
        df = remove_age_group(df, row, '100 +')

for index, row in df.iterrows():
    if row['Age'] == '90 +':
        row_80_84 = get_age_group(df, row, '80 - 84')
        row_85_89 = get_age_group(df, row, '85 - 89')

        row_new = row
        row_new['Age'] = '80 +'
        row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0]
        df = df.append(row_new, ignore_index=True)

        df = remove_age_group(df, row, '80 - 84')
        df = remove_age_group(df, row, '85 - 89')
        df = remove_age_group(df, row, '90 +')
        df = remove_age_group(df, row, '95 +')
        df = remove_age_group(df, row, '100 +')

for index, row in df.iterrows():
    if row['Age'] == '95 +':
        row_80_84 = get_age_group(df, row, '80 - 84')
        row_85_89 = get_age_group(df, row, '85 - 89')
        row_90_94 = get_age_group(df, row, '90 - 94')

        row_new = row
        row_new['Age'] = '80 +'
        row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
                           row_90_94['Value'].values[0]
        df = df.append(row_new, ignore_index=True)

        df = remove_age_group(df, row, '80 - 84')
        df = remove_age_group(df, row, '85 - 89')
        df = remove_age_group(df, row, '90 - 94')
        df = remove_age_group(df, row, '95 +')
        df = remove_age_group(df, row, '100 +')

for index, row in df.iterrows():
    if row['Age'] == '100 +':
        row_80_84 = get_age_group(df, row, '80 - 84')
        row_85_89 = get_age_group(df, row, '85 - 89')
        row_90_94 = get_age_group(df, row, '90 - 94')
        row_95_99 = get_age_group(df, row, '95 - 99')
        row_90_99 = get_age_group(df, row, '90 - 99')

        row_new = row
        row_new['Age'] = '80 +'
        if len(row_90_99) > 0:
            row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
                               row_90_99['Value'].values[0]
        else:
            row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
                               row_90_94['Value'].values[0] + row_95_99['Value'].values[0]
        df = df.append(row_new, ignore_index=True)

        df = remove_age_group(df, row, '80 - 84')
        df = remove_age_group(df, row, '85 - 89')
        df = remove_age_group(df, row, '90 - 94')
        df = remove_age_group(df, row, '95 - 99')
        df = remove_age_group(df, row, '90 - 99')
        df = remove_age_group(df, row, '100 +')

# Check the data
for index, row in df.iterrows():
    if row['Age'] not in (
            "0",
            "0 - 4",
            "1 - 4",
            "5 - 9",
            "10 - 14",
            "15 - 19",
            "20 - 24",
            "25 - 29",
            "30 - 34",
            "35 - 39",
            "40 - 44",
            "45 - 49",
            "50 - 54",
            "55 - 59",
            "60 - 64",
            "65 - 69",
            "70 - 74",
            "75 - 79",
            "80 +",
    ):
        print(f"Found age group {row['Age']}")

# Sort the data
df = df.sort_values(by=['Year', 'Area', 'Sex', 'Age'])

# Save to csv
df.to_csv(f"dataset_raw/death_dataset_{country}.csv", index=False)
