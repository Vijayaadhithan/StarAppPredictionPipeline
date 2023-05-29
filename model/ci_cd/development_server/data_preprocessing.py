import pandas as pd

# Read the five data sets
data_set = pd.read_csv('repo_features.csv')
"""
data_set2 = pd.read_csv('repo_features_3000..5000.csv')
data_set3 = pd.read_csv('repo_featulsres_5000..10000.csv')
data_set4 = pd.read_csv('repo_features_10000..20000.csv')
data_set5 = pd.read_csv('repo_features_500..1000.csv')
data_set6 = pd.read_csv('repo_features_1000..2000.csv')
data_set7 = pd.read_csv('repo_features_3000..4000.csv')
data_set8 = pd.read_csv('repo_features_5000..6000.csv')
data_set9 = pd.read_csv('repo_features_6000..7000.csv')
data_set10 = pd.read_csv('repo_features_20000..400000.csv')
"""

# Combine the data sets
"""
combined_data = pd.concat([data_set1, data_set2, data_set3, data_set4, data_set5, data_set6, data_set7, data_set8, data_set9,data_set10])
"""
combined_data = pd.concat([data_set])

# Optional: Reset the index of the combined data set
combined_data.reset_index(drop=True, inplace=True)

combined_data.to_csv('raw_data.csv', index=False)

unique_columns = combined_data.columns.unique()

unique_columns = combined_data.columns[combined_data.nunique() == len(combined_data)]
combined_data.isnull().sum()

bool_columns = combined_data.select_dtypes(include='bool').columns

combined_data.describe()

# Replace NaN values with 0
dataset = combined_data.fillna(0)

dataset = dataset.replace({True: 1, False: 0})

non_numeric_columns = []
for column in dataset.columns:
    try:
        pd.to_numeric(dataset[column])
    except ValueError:
        non_numeric_columns.append(column)

# Remove columns from the combined data set
columns_to_remove = ['name', 'full_name', 'commits', 'forks_url', 'watchers_url', 'created_at']
dataset = dataset.drop(columns=columns_to_remove)

filtered_data = dataset.filter(regex=r'^(?!.*language).*$')

filtered_data.to_csv('modified_data.csv', index=False)
