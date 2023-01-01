import pandas as pd
import numpy as np

country = 'Hungary'
drop_nan_deaths = True
remove_born = False

# Read in the data
df_death = pd.read_csv(f"dataset_raw/death_dataset_{country}.csv", header=0)
df_main = pd.read_csv(f"dataset_raw/{country}_cleaned.csv", header=0)

# Add column "Deaths" to df_main
df_main['Deaths'] = np.nan


def remove_age_group(df, row, age_group):
    return df.drop(df[(df['Country or Area'] == row['Country or Area']) & (df['Year'] == row['Year']) &
                      (df['Area'] == row['Area']) & (df['Sex'] == row['Sex']) & (df['Age'] == age_group)].index)


def get_age_group(df, row, age_group):
    return df[(df['Country or Area'] == row['Country or Area']) & (df['Year'] == row['Year']) &
              (df['Area'] == row['Area']) & (df['Sex'] == row['Sex']) & (df['Age'] == age_group)]


# Iterate over all rows in df_death
for index, row in df_death.iterrows():
    # Find row in df_main with same Country or Area, Year, Area, 'Sex' and 'Age'
    row_main = df_main[(df_main['Country or Area'] == row['Country or Area']) & (df_main['Year'] == row['Year']) &
                       (df_main['Area'] == row['Area']) & (df_main['Sex'] == row['Sex']) & (
                                   df_main['Age'] == row['Age'])]

    # If row_main is not empty
    if not row_main.empty:
        # Add Deaths to df_main
        df_main.loc[row_main.index, 'Deaths'] = row['Value']
    else:
        # If row_main is empty
        print(f"Could not find row in df_main with same Country or Area - year {row['Year']}")

# Print how many rows have NaN in Deaths column
print(f"Rows with NaN in Deaths column: {df_main['Deaths'].isna().sum()}")

# Remove whole years if NaN in Deaths column
if drop_nan_deaths:
    for year in df_main['Year'].unique():
        if df_main[df_main['Year'] == year]['Deaths'].isna().any():
            df_main = df_main.drop(df_main[df_main['Year'] == year].index)

# Save df_main to csv
df_main.to_csv(f"final_datasets/{country}_combined__years_with_nan_dropped_{drop_nan_deaths}{'_born_sum' if remove_born else ''}.csv", index=False)
