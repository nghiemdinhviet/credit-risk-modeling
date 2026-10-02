from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine


# =========================================
# PROJECT PATHS
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "credit_default_features.csv"
)

RISK_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_risk_scores_explained.csv"
)


# =========================================
# LOAD DATA
# =========================================

credit_features = pd.read_csv(FEATURE_PATH)
model_predictions = pd.read_csv(RISK_PATH)

print("Credit features:", credit_features.shape)
print("Model predictions:", model_predictions.shape)


# =========================================
# POSTGRESQL CONNECTION
# =========================================

DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "credit_risk_modeling"
DB_USER = "postgres"

DB_PASSWORD = getpass("PostgreSQL password: ")

connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)


# =========================================
# IMPORT TABLE 1
# =========================================

print("\nImporting credit_features...")

credit_features.to_sql(
    "credit_features",
    engine,
    if_exists="replace",
    index=False,
    chunksize=5000,
    method="multi"
)

print("credit_features imported successfully.")


# =========================================
# IMPORT TABLE 2
# =========================================

print("\nImporting model_predictions...")

model_predictions.to_sql(
    "model_predictions",
    engine,
    if_exists="replace",
    index=False,
    chunksize=5000,
    method="multi"
)

print("model_predictions imported successfully.")


print("\nAll tables imported successfully.")