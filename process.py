import pandas as pd
import numpy as np

country = 'Hungary'
remove_born = False

# Read in the data
df_all = pd.read_csv(r"dataset_raw/dataset_number_of_people_all_cleaned.csv", header=0)
df = df_all[df_all['Country or Area'] == country]

# If some year has both "Census - de jure - complete tabulation" and "Estimate - de jure" in column Record Type, remove the "Estimate - de jure" row
years_census_dublicates = {
    # 2010: {"Census - de jure - complete tabulation":False, "Estimate - de jure":False},
}

# iterate over all rows
for index, row in df.iterrows():
    now_year = years_census_dublicates.get(row['Year'],
                                           {"Census - de jure - complete tabulation": False,
                                            "Census - de facto - complete tabulation": False,
                                            "Estimate - de jure": False}
                                           )
    now_year[row['Record Type']] = True
    years_census_dublicates[row['Year']] = now_year

for i, el in years_census_dublicates.items():
    if ((el["Census - de jure - complete tabulation"] and el["Estimate - de jure"]) or
            (el["Census - de facto - complete tabulation"] and el["Estimate - de jure"])):
        # remove all rows with "Estimate - de jure"
        df = df.drop(df[(df['Year'] == i) & (df['Record Type'] == "Estimate - de jure")].index)
        print(f"Removed all rows with 'Estimate - de jure' for year {i}")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove duplicate rows (when Value can be different, but all other columns are the same)
df = df.drop_duplicates(subset=["Country or Area", "Year", "Area", "Sex", "Age", "Record Type", "Reliability", ])

# Remove Reliability column
df = df.drop(columns=['Reliability'])


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
else:
    for index, row in df.iterrows():
        # if "Age" is "0 - 4" - and there is no row with "Age" "0" or "1 - 4" - remove year
        if row['Age'] == '0 - 4':
            if len(get_age_group(df, row, '0')) == 0 or len(get_age_group(df, row, '1 - 4')) == 0:
                df = df.drop(df[(df['Year'] == row['Year'])].index)
                print(f"Removed year {row['Year']}")
            else:
                df = remove_age_group(df, row, '0 - 4')

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
        row_85_99 = get_age_group(df, row, '85 - 99')

        row_new = row
        row_new['Age'] = '80 +'
        if len(row_90_99) > 0:
            row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
                               row_90_99['Value'].values[0]
        elif len(row_85_99) > 0:
            row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_99['Value'].values[0]
        else:
            row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
                               row_90_94['Value'].values[0] + row_95_99['Value'].values[0]
        df = df.append(row_new, ignore_index=True)

        df = remove_age_group(df, row, '80 - 84')
        df = remove_age_group(df, row, '85 - 89')
        df = remove_age_group(df, row, '90 - 94')
        df = remove_age_group(df, row, '95 - 99')
        df = remove_age_group(df, row, '90 - 99')
        df = remove_age_group(df, row, '85 - 99')
        df = remove_age_group(df, row, '100 +')

bad_age_groups = {}
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
        print(f"Found bad age group {row['Age']}. Year: {row['Year']}")
        bad_age_groups[row['Year']] = row['Age']

# Remove years with bad age groups
for index, row in df.iterrows():
    if row['Year'] in bad_age_groups.keys():
        df = df.drop(index)

# Sort the data
df = df.sort_values(by=['Year', 'Area', 'Sex', 'Age'])

# Save the data
df.to_csv(f"dataset_raw/{country}_cleaned.csv", index=False)
