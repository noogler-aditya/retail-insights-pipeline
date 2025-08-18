

import os
import pandas as pd
from sqlalchemy import create_engine, URL

# --- Path to your data ---
DATA_PATH = "data/processed_sales/"

# --- Data Loading Logic ---
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"The specified path does not exist: {DATA_PATH}")

print(f"Reading partitioned Parquet dataset from folder: {DATA_PATH}")
df = pd.read_parquet(DATA_PATH)
df.columns = [col.lower() for col in df.columns] # Standardize to lowercase
print(f"Loaded and standardized {len(df)} rows.")

# --- PostgreSQL Connection and Data Load Logic ---
print("Connecting to PostgreSQL database...")

try:
    # This is the most robust way to define the connection,
    # preventing interference from external environment variables.
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="password",
        host="localhost",
        port="5432",
        database="Your_DATABASE"
    )

    engine = create_engine(db_url)

    df.to_sql("sales", engine, if_exists="replace", index=False)
    
    print("✅ Data loaded successfully into PostgreSQL table 'sales'.")

except Exception as e:
    print(f"❌ An error occurred during database operation: {e}")
