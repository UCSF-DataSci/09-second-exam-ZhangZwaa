import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from statsmodels.regression.mixed_linear_model import MixedLM
from scipy.stats import f_oneway
import seaborn as sns
import matplotlib.pyplot as plt


# Load data
data = pd.read_csv("ms_data_Q2.csv")

# Analyze walking speed
y = data["walking_speed"]
X = data[["education_level", "age"]]

# Change education_level into nominal data
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_encoded = encoder.fit_transform(X[["education_level"]])

new_edu = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(["education_level"]))

X = pd.concat([new_edu, X["age"]], axis=1)

# Create the regression model
regr = LinearRegression()
regr.fit(X, y)

# Output the regression coefficients
print("Regression Coefficients:", regr.coef_)

# If data has repeated measures (e.g., subject_id), we can fit a mixed-effects model
if "subject_id" in data.columns:
    mixed_model = MixedLM(y, X, groups=data["subject_id"])
    mixed_results = mixed_model.fit()
    print(mixed_results.summary())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)

model = sm.OLS(y_train, X_train).fit()
print(model.summary(alpha=0.05))
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print(f'\nRMSE for Baseline Model: {rmse:.2f}')


# Analysis costs
# Perform one-way ANOVA
groups = [group['costs'].values for _, group in data.groupby('insurance_type')]
f_stat, p_value = f_oneway(*groups)

# Print F-statistic and p-value
print(f"F-statistic: {f_stat:.2f}") #
print(f"P-value: {p_value:.4f}") #

# Boxplot for visualizing costs by insurance type
plt.figure(figsize=(10, 6))
sns.boxplot(
    x="insurance_type",
    y="costs",
    data=data,
    order=['Basic', 'Premium', 'Platinum', 'NoInsurance']
)
plt.xlabel("Insurance Type")
plt.ylabel("Costs per Visit")
plt.title("Costs per Visit by Insurance Type")
plt.savefig('boxplot.png', format='png') #
plt.show()

# Calculate basic statistics
stats = data.groupby("insurance_type")["costs"].describe()
print(stats) #

# Calculate SS_between and SS_total for eta-squared
grand_mean = data['costs'].mean()
ss_total = np.sum((data['costs'] - grand_mean) ** 2)
ss_between = sum([len(group) * (group.mean() - grand_mean) ** 2 for group in groups])

# Calculate eta-squared
eta_squared = ss_between / ss_total

# Print effect size
print(f"Eta-squared: {eta_squared:.4f}\n\n") #

# Advanced analysis
# Add confounder: visit month from visitdate
data["visit_date"] = pd.to_datetime(data["visit_date"], format="%Y-%m-%d")
data["visit_month"] = data["visit_date"].dt.month
model_mul = sm.OLS.from_formula('walking_speed ~ age * education_level + visit_month', data).fit()
print(model_mul.summary())
