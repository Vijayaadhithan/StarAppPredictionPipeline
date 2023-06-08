import pandas as pd

# Read the five data sets
data_set1 = pd.read_csv('repo_features_1000..3000.csv')
data_set2 = pd.read_csv('repo_features_3000..5000.csv')
data_set3 = pd.read_csv('repo_features_5000..10000.csv')
data_set4 = pd.read_csv('repo_features_10000..20000.csv')
data_set5 = pd.read_csv('repo_features_500..1000.csv')
data_set6 = pd.read_csv('repo_features_1000..2000.csv')
data_set7 = pd.read_csv('repo_features_3000..4000.csv')
data_set8 = pd.read_csv('repo_features_5000..6000.csv')
data_set9 = pd.read_csv('repo_features_6000..7000.csv')
data_set10 = pd.read_csv('repo_features_20000..400000.csv')

# Combine the data sets
combined_data = pd.concat([data_set1, data_set2, data_set3, data_set4, data_set5, data_set6, data_set7, data_set8, data_set9,data_set10])

# Optional: Reset the index of the combined data set
combined_data.reset_index(drop=True, inplace=True)

if 'age' in combined_data.columns:
    combined_data = combined_data.drop(columns=['age'])
    print("The 'age' column has been removed.")
else:
    print("The 'age' column does not exist.")
combined_data.head()
print(combined_data.shape)
combined_data.to_csv('raw_data.csv', index=False)
unique_columns = combined_data.columns.unique()
print(unique_columns)
unique_columns = combined_data.columns[combined_data.nunique() == len(combined_data)]
print("Columns with only unique values:")
print(unique_columns)
combined_data.isnull().sum()
bool_columns = combined_data.select_dtypes(include='bool').columns

# Display the column names
print("Columns containing only True or False values:")
for column in bool_columns:
    print(column)
combined_data.describe()

# Replace NaN values with 0
dataset = combined_data.fillna(0)

# Verify if NaN values have been replaced with 0
print(dataset.isnull().sum())

dataset = dataset.replace({True: 1, False: 0})

non_numeric_columns = []
for column in dataset.columns:
    try:
        pd.to_numeric(dataset[column])
    except ValueError:
        non_numeric_columns.append(column)

# Print the columns with non-numeric values
print("Columns with non-numeric values:")
print(non_numeric_columns)

dataset.head()

# Remove columns from the combined data set
columns_to_remove = ['name', 'full_name', 'commits', 'forks_url', 'watchers_url', 'created_at']  
dataset = dataset.drop(columns=columns_to_remove)

dataset.head()

filtered_data = dataset.filter(regex=r'^(?!.*language).*$')

filtered_data.head()

print(filtered_data.shape)
filtered_data.to_csv('modified_data.csv', index=False)

print("Modified data set saved as 'modified_data.csv'")
