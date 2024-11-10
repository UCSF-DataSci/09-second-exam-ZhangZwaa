# Summary of Q1
Total number of visits: 15409<br>
First few rows of file:<br>
patient_id,visit_date,age,education_level,walking_speed<br>
P0001,2020-01-19,66.33,Bachelors,3.51<br>
P0001,2020-05-02,66.62,Bachelors,3.55<br>
P0001,2020-07-25,66.85,Bachelors,3.47<br>
P0001,2020-10-21,67.09,Bachelors,3.93<br>
P0001,2021-01-28,67.36,Bachelors,3.21<br>
P0001,2021-04-22,67.59,Bachelors,3.81<br>
P0001,2021-07-12,67.81,Bachelors,3.37<br>
P0001,2021-10-24,68.1,Bachelors,3.67<br>
P0001,2022-04-21,68.59,Bachelors,2.93<br>
# Summary of Q2
Mean walking speed by education level:<br>
Bachelors       4.051125<br>
Graduate        4.447184<br>
High School     3.244856<br>
Some College    3.728234<br>
<br>
Mean costs by insurance type:<br>
Basic          10253.454426<br>
NoInsurance    20255.921483<br>
Platinum        2249.299552<br>
Premium         5246.521219<br>
<br>
Age effect on walking speed: -0.69<br>
# Summary of Q3
## Analyze walking speed
Model: OLS
Regression Coefficients: [ 0.19970344  0.5923656  -0.59814054 -0.1939285  -0.03021663]<br>
R2: 0.808<br>
RMSE for Baseline Model: 0.34<br>
F-statistic: 1673951.77<br>
P-value: 0.0000<br>
## Analyze costs
Simple analysis of insurance type effect<br>
![Simple analysis of insurance type effect](1.png)<br>
Box plots and basic statistics<br>
![Box plots and basic statistics](boxplot.png)<br>
Effect sizes using eta-squared: 0.9969, which means insurance type has a **strong** effect on costs<br>
## Advanced analysis
![interaction result with confounder](9.png)<br>
Analyze _education_ and _age_ interaction effects on _walking speed_. Control for relevant confounders _visit months_