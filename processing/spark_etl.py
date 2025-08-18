
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, round, to_date, year, month

# --- Dynamic Path Configuration for Local Execution ---
# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to get the project's root directory
project_root = os.path.dirname(script_dir)

# Construct absolute paths for input and output relative to the project root
input_path = os.path.join(project_root, "data", "indian_retail_tier2_tier3.csv")
output_path = os.path.join(project_root, "data", "processed_sales")

print(f"--- Running Spark ETL Job Locally ---")
print(f"Using input file: {input_path}")
print(f"Using output directory: {output_path}")
# ----------------------------------------------------

# Initialize Spark session with the Java security fix
spark = SparkSession.builder \
    .appName("Retail Sales ETL") \
    .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
    .getOrCreate()

# === Extract ===
df = spark.read.csv(input_path, header=True, inferSchema=True)
print("===== Schema Loaded =====")
df.printSchema()

# === Transform ===
# Convert date column to proper format
if "TransactionDate" in df.columns:
    df = df.withColumn("TransactionDate", to_date(col("TransactionDate"), "yyyy-MM-dd"))

# Example aggregation: Total sales per product & city
if set(["ProductID", "StoreCity", "TotalPrice"]).issubset(df.columns):
    sales_per_city = df.groupBy("StoreCity", "ProductID") \
        .agg(
            round(spark_sum("TotalPrice"), 2).alias("Total_Sales"),
            round(avg("TotalPrice"), 2).alias("Avg_Sales")
        )
    sales_per_city.show(10, truncate=False)

    # === Load ===
    sales_per_city.write.mode("overwrite").parquet(output_path)
    print(f"✅ ETL completed. Processed data saved at {output_path}")
else:
    print("❌ Required columns for aggregation (ProductID, StoreCity, TotalPrice) not found.")

# Stop Spark session
spark.stop()
