# Credit Risk Modeling

## Loan Default Prediction, Probability of Default & Risk Monitoring

Credit Risk Modeling is an end-to-end machine learning portfolio project focused on predicting credit default risk and turning model outputs into practical risk-monitoring information.

The project covers the full workflow from data understanding and feature engineering to model development, probability calibration, explainability, PostgreSQL integration and Power BI reporting.

> This project is for educational and portfolio purposes only. It is not intended to support real-world lending decisions.

---

# 1. Business Problem

A lending institution needs to identify customers who are more likely to default and understand the factors associated with higher credit risk.

The project was developed to answer questions such as:

- Which customers are more likely to default?
- How well can historical payment behavior predict future default?
- Which variables contribute most strongly to model predictions?
- Can predicted probabilities be converted into meaningful risk bands?
- How closely do predicted default probabilities match observed default rates?
- Which customers should be prioritized for further risk review?

The final output combines machine learning predictions with a customer-level risk monitoring dashboard.

---

# 2. Dataset

The project uses the **Default of Credit Card Clients** dataset from the UCI Machine Learning Repository.

The dataset contains:

- **30,000 customers**
- **25 original variables**
- Credit limit information
- Customer characteristics
- Six months of payment status
- Six months of bill amounts
- Six months of payment amounts
- Default payment target

Target variable:

```text
0 = Non-default
1 = Default
```

Target distribution:

```text
Non-default: 23,364 customers (77.88%)
Default:      6,636 customers (22.12%)
```

Because the target is moderately imbalanced, model evaluation does not rely on Accuracy alone.

---

# 3. Project Workflow

```text
Raw Credit Data
        ↓
Data Understanding
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Train / Validation / Test Split
        ↓
Logistic Regression Baseline
        ↓
XGBoost Challenger
        ↓
Threshold Analysis
        ↓
Final Test Evaluation
        ↓
Probability Calibration
        ↓
Probability of Default
        ↓
Risk Score & Risk Band
        ↓
SHAP Explainability
        ↓
PostgreSQL
        ↓
Power BI Risk Dashboard
```

---

# 4. Data Cleaning

The raw dataset was first validated for:

- Missing values
- Duplicate rows
- Duplicate customer IDs
- Invalid categorical values
- Unusual payment-status codes
- Extreme bill and payment values

Main cleaning decisions:

- No missing values were found in the original dataset.
- No duplicate customer IDs were found.
- The target column was renamed to `TARGET`.
- Undocumented `EDUCATION` values 0, 5 and 6 were grouped into `Others`.
- Undocumented `MARRIAGE` value 0 was grouped into `Others`.
- Original payment-status variables were preserved.
- Negative bill amounts were not automatically removed.
- Customer `ID` was retained for identification but excluded from model training.

Final cleaned dataset:

```text
30,000 rows
25 columns
```

---

# 5. Exploratory Data Analysis

EDA focused on identifying patterns associated with default risk.

## Payment History

Payment behavior showed one of the strongest relationships with default.

Observed default rate by number of delayed months:

```text
0 delayed months → 11.71%
1 delayed month  → 29.82%
2 delayed months → 38.76%
3 delayed months → 50.87%
4 delayed months → 57.31%
5 delayed months → 57.38%
6 delayed months → 70.32%
```

This suggests that repeated payment delinquency contains strong predictive information.

## Payment-to-Bill Ratio

Customers making very low payments relative to their outstanding bills showed higher observed default rates:

```text
0–10% payment ratio   → 26.97%
10–25%                → 19.78%
25–50%                → 14.75%
50–100%               → 15.47%
>100%                 → 14.56%
```

These findings informed the feature engineering stage.

---

# 6. Feature Engineering

Thirteen additional behavioral and financial features were created.

## Payment Behavior Features

```text
DELAYED_MONTHS
MAX_DELAY
AVG_DELAY
HAS_DELAY
RECENT_DELAY
```

## Financial Behavior Features

```text
AVG_BILL_AMT
AVG_PAY_AMT
TOTAL_BILL_AMT
TOTAL_PAY_AMT
CREDIT_UTILIZATION
PAYMENT_TO_BILL
```

## Trend Features

```text
BILL_TREND
PAYMENT_TREND
```

After feature engineering:

```text
30,000 rows
38 columns
```

Customer ID and selected demographic variables were not included in the primary predictive model.

---

# 7. Machine Learning Strategy

The data was divided into:

```text
70% Training
15% Validation
15% Test
```

Stratified splitting was used to preserve the default/non-default distribution.

The Test Set remained untouched during model selection and threshold analysis.

Two models were developed:

1. Logistic Regression
2. XGBoost

---

# 8. Logistic Regression Baseline

Logistic Regression was used as an interpretable baseline model.

Validation performance:

```text
Accuracy  : 81.56%
Precision : 65.42%
Recall    : 35.18%
F1 Score  : 45.75%
ROC-AUC   : 76.15%
PR-AUC    : 52.00%
```

At the default threshold of 0.50, recall was relatively low.

Threshold analysis showed the trade-off between detecting more default customers and generating additional false positives.

A working baseline threshold of **0.25** produced:

```text
Precision : 46.28%
Recall    : 58.19%
F1 Score  : 51.56%
```

---

# 9. XGBoost Champion Model

XGBoost was developed as the challenger model and handled class imbalance using `scale_pos_weight`.

After validation comparison, XGBoost was selected as the champion classification model.

Final performance on the held-out Test Set:

| Metric | Result |
|---|---:|
| Accuracy | 75.27% |
| Precision | 45.71% |
| Recall | 62.55% |
| F1 Score | 52.82% |
| ROC-AUC | 77.99% |
| PR-AUC | 55.67% |

Test confusion matrix:

```text
True Negative  : 2,764
False Positive :   740
False Negative :   373
True Positive  :   623
```

The model correctly detected **623 of 996 actual default customers** in the Test Set.

---

# 10. Probability Calibration

The raw XGBoost probability output was calibrated before being interpreted as Probability of Default.

A calibrated model was used for:

```text
Probability of Default
Risk Band
Risk Score
```

The classification model and calibrated probability model were kept conceptually separate:

```text
Raw XGBoost
→ Classification & SHAP explanation

Calibrated XGBoost
→ Probability of Default
→ Risk Band
→ Risk Score
```

---

# 11. Risk Segmentation

Customers were assigned into three project-level risk bands:

```text
PD < 10%        → Low Risk
10% ≤ PD < 25%  → Medium Risk
PD ≥ 25%        → High Risk
```

Observed results on the Test portfolio:

| Risk Band | Customers | Defaults | Actual Default Rate |
|---|---:|---:|---:|
| Low | 1,493 | 106 | 7.10% |
| Medium | 1,696 | 272 | 16.04% |
| High | 1,311 | 618 | 47.14% |

The segmentation produced a clear separation in observed risk.

Predicted vs actual default rates were also closely aligned:

```text
Low
Actual: 7.10%
Average PD: 6.85%

Medium
Actual: 16.04%
Average PD: 15.55%

High
Actual: 47.14%
Average PD: 47.91%
```

---

# 12. Risk Score

A simple internal project risk score was created from calibrated PD:

```text
Risk Score = (1 - PD) × 100
```

Interpretation:

```text
Higher score → Lower estimated risk
Lower score  → Higher estimated risk
```

This score is used only as an internal project metric and is not intended to represent an official credit score such as FICO.

---

# 13. Explainable AI with SHAP

SHAP was used to explain the XGBoost model.

Two levels of explainability were implemented.

## Global Explainability

SHAP feature importance was used to identify variables with the strongest influence across the scored portfolio.

Important drivers included payment behavior, repayment persistence, bill/payment variables and credit utilization.

## Local Explainability

Individual customer predictions were also explained.

For each scored customer, the project generates:

```text
Main Risk Driver
Second Risk Driver
Third Risk Driver
```

Positive SHAP contributions represent features pushing the classification model toward default.

This allows the dashboard to show not only:

```text
Customer risk level
```

but also:

```text
Why the model considers the customer risky
```

---

# 14. PostgreSQL Integration

Machine learning outputs were loaded into PostgreSQL.

Database:

```text
credit_risk_modeling
```

Main tables:

```text
credit_features
model_predictions
```

Records:

```text
credit_features   → 30,000 customers
model_predictions → 4,500 scored test customers
```

The `model_predictions` table contains:

```text
Customer_ID
Actual_Default
Probability_of_Default
Risk_Score
Risk_Band
Main_Risk_Driver
Second_Risk_Driver
Third_Risk_Driver
```

PostgreSQL is used as the data source for the Power BI dashboard.

---

# 15. Power BI Dashboard

The final report contains four pages.

## 01 — Credit Risk Overview

Key KPIs:

```text
Total Scored Customers
Actual Default Rate
Average PD
High Risk Customers
Average Risk Score
```

Main visuals:

- Risk Band Distribution
- Actual Default Rate by Risk Band
- PD Distribution
- Actual vs Predicted Default Rate

---

## 02 — Risk Drivers

The second page focuses on the main drivers associated with credit risk.

Visuals include:

- Top Main Risk Drivers
- Average PD by Main Risk Driver
- Default Rate by Delayed Months
- Average PD by Maximum Payment Delay

---

## 03 — Model Performance

The third page focuses on machine-learning performance.

KPIs:

```text
ROC-AUC
PR-AUC
Precision
Recall
F1 Score
```

Visuals include:

- XGBoost Test Performance
- Test Confusion Matrix
- Logistic Regression Threshold Trade-off
- Calibration by Risk Band

---

## 04 — Customer Risk Monitoring

The final page provides customer-level risk monitoring.

Features include:

- Risk Band filter
- Main Risk Driver filter
- High Risk Customers by Main Driver
- Average PD by Main Driver
- Customer-level monitoring table

Customer details include:

```text
Customer ID
Probability of Default
Risk Score
Risk Band
Actual Default
Main Risk Driver
Second Risk Driver
Third Risk Driver
```

---

# 16. Technology Stack

```text
Python
Pandas
NumPy
Matplotlib
scikit-learn
XGBoost
SHAP

PostgreSQL
SQL
SQLAlchemy
psycopg2

Power BI
Power Query
DAX

Jupyter Notebook
VS Code
Git
GitHub
```

---

# 17. Project Structure

```text
Credit_Risk_Modeling/
│
├── data/
│   ├── raw/
│   │   └── credit_default_raw.xls
│   │
│   └── processed/
│       ├── credit_default_clean.csv
│       ├── credit_default_features.csv
│       ├── customer_risk_scores.csv
│       └── customer_risk_scores_explained.csv
│
├── database/
│   └── import_to_postgres.py
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_training.ipynb
│   └── 06_explainability.ipynb
│
├── models/
│   ├── xgboost_champion.pkl
│   └── xgboost_calibrated_pd.pkl
│
├── powerbi/
│
├── images/
├── docs/
├── src/
│
├── .gitignore
└── README.md
```

---

# 18. Key Project Outcomes

The project demonstrates an end-to-end credit-risk analytics workflow combining:

- Data cleaning and exploratory analysis
- Financial and behavioral feature engineering
- Baseline and boosted-tree classification models
- Imbalanced classification evaluation
- Threshold analysis
- Probability calibration
- Probability of Default estimation
- Risk segmentation
- Customer risk scoring
- SHAP model explainability
- PostgreSQL integration
- Power BI monitoring

The main goal was not only to build a predictive model, but to convert model outputs into information that can be understood and monitored from a business perspective.

---

# 19. Limitations

This project has several important limitations:

- The dataset is historical and public rather than live banking data.
- Risk-band thresholds are project assumptions, not real lending-policy thresholds.
- Model performance should not be interpreted as sufficient for production lending decisions.
- Sensitive demographic variables require additional fairness and regulatory review before any real-world use.
- Model calibration and validation would need ongoing monitoring in a production environment.

---

# 20. Future Improvements

Possible future extensions include:

- Hyperparameter optimization
- Time-based validation
- Additional fairness analysis
- Model drift monitoring
- Champion/challenger model tracking
- More advanced probability calibration
- Cost-sensitive threshold optimization
- Automated model scoring pipeline
- Deployment through an API or batch scoring workflow

---

# Disclaimer

This project was created for educational and portfolio purposes.

The model, risk scores, risk bands and dashboard are not intended for real-world credit approval, rejection or lending decisions.