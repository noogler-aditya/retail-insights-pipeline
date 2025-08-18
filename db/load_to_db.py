# import os
# import pandas as pd
# from sqlalchemy import create_engine, URL

# --- Path to your data ---
# DATA_PATH = "data/processed_sales/"

# --- Data Loading Logic ---
# if not os.path.exists(DATA_PATH):
#     raise FileNotFoundError(f"The specified path does not exist: {DATA_PATH}")

# print(f"Reading partitioned Parquet dataset from folder: {DATA_PATH}")
# df = pd.read_parquet(DATA_PATH)
# print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
# print(df.head())

# --- PostgreSQL Connection and Data Load Logic ---
# print("Connecting to PostgreSQL database...")

# try:
    # --- FOOLPROOF FIX: Create a URL object ---
    # This explicitly defines every part of the connection,
    # preventing SQLAlchemy from using any external environment variables.
    # db_url = URL.create(
    #     drivername="postgresql+psycopg2",
    #     username="postgres",
    #     password="Aditya@sql19",  # Use the password for your local postgres user
    #     host="localhost",
    #     port="5432",
    #     database="sales_db"
    # )
    
    # print("--- ATTEMPTING CONNECTION WITH THIS URL OBJECT ---")
    # print(db_url)
    # print("-------------------------------------------------")

    # Create the engine from the URL object
    # engine = create_engine(db_url)

    # Load DataFrame into the PostgreSQL database
#     df.to_sql("sales", engine, if_exists="replace", index=False)
    
#     print("✅ Data loaded successfully into PostgreSQL table 'sales'.")

# except Exception as e:
#     print(f"❌ An error occurred during database operation: {e}")




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
        password="Aditya@sql19",
        host="localhost",
        port="5432",
        database="sales_db"
    )

    engine = create_engine(db_url)

    df.to_sql("sales", engine, if_exists="replace", index=False)
    
    print("✅ Data loaded successfully into PostgreSQL table 'sales'.")

except Exception as e:
    print(f"❌ An error occurred during database operation: {e}")