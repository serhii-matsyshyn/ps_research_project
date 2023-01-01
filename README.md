# Original dataset processed

## How to use
Run step by step, 1 country at a time.  
Data is saved in `dataset_raw` folder and `final_datasets` folders.  
Final datasets are saved in `final_datasets` folder.

- dataset_clean.py: clean the original dataset
- process.py: process the cleaned dataset
  - choose the country you want to process
  - remove born - means to summarize the data of age 0 and 1 - 4 and create 1 age group 0 - 4
- death_extract.py: extract the death data from the second dataset
  - choose the country you want to process
  - remove born - means to summarize the data of age 0 and 1 - 4 and create 1 age group 0 - 4
- combine.py: combine the processed data and death data
  - choose the country you want to process
  - drop_nan_deaths - drop years where there is no death data available
  - remove born - means to summarize the data of age 0 and 1 - 4 and create 1 age group 0 - 4


## Common errors
```
Traceback (most recent call last):
  File "...\process.py", line 153, in <module>
    row_new['Value'] = row['Value'] + row_80_84['Value'].values[0] + row_85_89['Value'].values[0] + \
IndexError: index 0 is out of bounds for axis 0 with size 0

Process finished with exit code 1
```
Some data is missing in the original dataset or it is duplicated.
Or age groups are like 85 - 95 (instead of 85 - 89 and 90 - 95)
