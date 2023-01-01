import pandas as pd
import numpy as np

# Read in the data
df = pd.read_csv(r"dataset_original/dataset_number_of_people_all.csv", header=0)
df_death = pd.read_csv(r"dataset_original/death_dataset.csv", header=0)


# Remove all lines where "age" is not 0, contains '-' or '+'
def check_if_age_is_valid(x):
    if x in (0, '0',):
        return True
    elif x in (
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
            "80 - 84",
            "85 +",

    ):
        return True
    elif '-' in str(x):
        return True
    elif '+' in str(x):
        return True
    elif x in ("Total",):
        return False

    return False


df = df[df['Age'].apply(check_if_age_is_valid)]

# Remove all lines where "Area" is "Semi-urban"
df = df[df['Area'] != 'Semi-urban']

# Remove column "Value Footnotes"
df = df.drop(columns=['Value Footnotes'])

# Remove all lines with countries that are not in the death dataset
df = df[df['Country or Area'].isin(df_death['Country or Area'])]


# save the cleaned data to a new file
df.to_csv(r"dataset_raw/dataset_number_of_people_all_cleaned.csv", index=False)

# Print the percent of data belonging to each country in death dataset (top 10)
# print(df_death['Country or Area'].value_counts(normalize=True).head(30))

# Hungary        0.037801
# Poland         0.036744
# Finland        0.035120
# Bulgaria       0.033795
# New Zealand    0.030805
# El Salvador    0.030292
# Ireland        0.029523
# France         0.029480
# Israel         0.028551
# Greece         0.028498