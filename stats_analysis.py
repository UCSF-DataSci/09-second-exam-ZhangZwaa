import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from statsmodels.regression.mixed_linear_model import MixedLM
from scipy.stats import f_oneway
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


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
# Using one way ANOVA
groups = [group['costs'] for _, group in data.groupby('insurance_type')]
f_stat, p_value = f_oneway(*groups)

print(f"F-statistic: {f_stat:.2f}")
print(f"P-value: {p_value}")

plt.figure(figsize=(10, 6))
sns.boxplot(x="insurance_type",
                y="costs",
                data=data,
                order=['Basic', 'Premium', 'Platinum', 'NoInsurance'])
plt.xlabel("Insurance type")
plt.ylabel("Costs per visit")
plt.savefig('boxplot.png', format='png')
# Basic statistics
stats = data.groupby("insurance_type")["costs"].describe()

corr, _ = pearsonr(data["insurance_type"], data["costs"])