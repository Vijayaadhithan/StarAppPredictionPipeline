import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
import time
import joblib

#time_start = time.time() #
models = {} #Dictionary of models

# Step 1: Load and prepare the dataset for model training
dataset = pd.read_csv('raw_data.csv')

# Sort the dataset based on the 'stars' column in descending order
sorted_dataset = dataset.sort_values('stars', ascending=False)

# Select the top 10 repositories based on star count
top_10_repositories = sorted_dataset.head(10)

# Save the top 10 repositories in the 'best_model.txt' file
top_10_repositories[['name', 'stars']].to_csv('top10_github_repos.txt', index=False, sep='\t', header=False)

# Step 2: Load and prepare the modified dataset for model training
data = pd.read_csv('modified_data.csv')
filtered_data = data.dropna()  # Remove any rows with missing values

# Split the dataset into features and target variable
X = filtered_data.drop('stars', axis=1)
y = filtered_data['stars']

# Step 3: Train and evaluate the Linear Regression model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
linreg_model = LinearRegression()
linreg_model.fit(X_train, y_train)
y_pred_linreg = linreg_model.predict(X_test)
models["Linear Regression"] = linreg_model


# Calculate R-squared score for Linear Regression
r2_linreg = r2_score(y_test, y_pred_linreg)

# Step 4: Train and evaluate the Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
models["Random Forest"] = rf_model


# Calculate R-squared score for Random Forest
r2_rf = r2_score(y_test, y_pred_rf)

# Step 5: Train and evaluate the Decision Tree model
dt_model = tree.DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)
models["Decision Tree"] = dt_model


# Calculate R-squared score for Decision Tree
r2_dt = r2_score(y_test, y_pred_dt)

# Step 6: Train and evaluate the K-Nearest Neighbors model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train_scaled, X_test_scaled, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

k = 5  # Number of nearest neighbors to consider
knn_model = KNeighborsRegressor(n_neighbors=k)
knn_model.fit(X_train_scaled, y_train)
y_pred_knn = knn_model.predict(X_test_scaled)
models["K-Nearest Neighbors"] = knn_model


# Calculate R-squared score for K-Nearest Neighbors
r2_knn = r2_score(y_test, y_pred_knn)

# Step 7: Pick the best model based on R-squared scores
r2_scores = {"Linear Regression": r2_linreg, "Random Forest": r2_rf, "Decision Tree": r2_dt, "K-Nearest Neighbors": r2_knn}
best_model = max(r2_scores, key=r2_scores.get)
print(best_model)

with open('best_model_name.txt', 'w') as file:
    file.write(f"Best model: {best_model}\n")

best_model = models[best_model]
joblib.dump(best_model, 'best_model.joblib') # New

# Save the best model information and scores in a text file
with open('best_model_and_top10_github_tepos.txt', 'w') as file:
#    file.write(f"Best model: {best_model}\n")
#    file.write("R-squared scores:\n")
    for model, score in r2_scores.items():
        file.write(f"{model}: {score}\n")
    file.write("\nTop 10 repositories based on star count:\n")
    file.write(top_10_repositories[['name', 'stars']].to_string(index=False))

# Step 8: Visualize the correlation matrix
correlation_matrix = filtered_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix.png')
plt.close()

# Step 9: Compute the covariance matrix
covariance_matrix = np.cov(X.T)
sns.heatmap(covariance_matrix, annot=True, cmap='coolwarm')
plt.title('Covariance Matrix')
plt.savefig('covariance_matrix.png')
plt.close()

# Step 10: Plot predicted vs actual values for the best model
if best_model == "Linear Regression":
    plot_indices = np.random.choice(len(y_test), size=min(len(y_test), len(y_pred_linreg)), replace=False)
    plt.scatter(y_test.iloc[plot_indices], y_pred_linreg.flatten()[plot_indices])
elif best_model == "Random Forest":
    plt.scatter(y_test, y_pred_rf)
elif best_model == "Decision Tree":
    plt.scatter(y_test, y_pred_dt)
elif best_model == "K-Nearest Neighbors":
    plt.scatter(y_test, y_pred_knn)

plt.xlabel('Actual Stars', color='blue')
plt.ylabel('Predicted Stars', color='green')
plt.title('Actual vs Predicted Stars')
plt.show()
plt.savefig('predicted_vs_actual.png')
plt.close()
