# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, sum as spark_sum, avg, round, to_date, month, year

# spark = SparkSession.builder \
#     .appName("Retail Sales ETL") \
#     .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
#     .getOrCreate()

# === Extract ===
# input_path = "/app/data/indian_retail_tier2_tier3.csv"
# df = spark.read.csv(input_path, header=True, inferSchema=True)

# Show schema for debugging
# print("===== Schema Loaded =====")
# df.printSchema()

# === Transform ===
# Fill only columns that actually exist
# fill_values = {}
# if "Item_Visibility" in df.columns:
#     fill_values["Item_Visibility"] = 0
# if "Item_Weight" in df.columns:
#     avg_weight = df.select(avg("Item_Weight")).first()[0]
#     fill_values["Item_Weight"] = avg_weight

# if fill_values:
#     df = df.na.fill(fill_values)

# Convert date column to proper format (if exists)
# if "TransactionDate" in df.columns:
#     df = df.withColumn("TransactionDate", to_date(col("TransactionDate"), "yyyy-MM-dd"))
#     df = df.withColumn("Year", year(col("TransactionDate")))
#     df = df.withColumn("Month", month(col("TransactionDate")))

# Example aggregation: Total sales per product & city
# if set(["ProductID", "StoreCity", "TotalPrice"]).issubset(df.columns):
#     sales_per_city = df.groupBy("StoreCity", "ProductID") \
#         .agg(
#             round(spark_sum("TotalPrice"), 2).alias("Total_Sales"),
#             round(avg("TotalPrice"), 2).alias("Avg_Sales")
#         )

#     sales_per_city.show(10, truncate=False)

    # === Load ===
#     output_path = "/app/processed_sales"
#     sales_per_city.write.mode("overwrite").parquet(output_path)
#     print(f"ETL completed. Processed data saved at {output_path}")
# else:
#     print("Required columns for aggregation not found. Skipping aggregation step.")

# Stop Spark session
# spark.stop()






# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, sum as spark_sum, avg, round, to_date, month, year
# import os  # NEW
# import sys  # NEW

# Initialize Spark session
# spark = SparkSession.builder \
#     .appName("Retail Sales ETL") \
#     .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
#     .getOrCreate()

# === Extract ===
# input_path = "data/indian_retail_tier2_tier3.csv"
# df = spark.read.csv(input_path, header=True, inferSchema=True)

# Show schema for debugging
# print("===== Schema Loaded =====")
# df.printSchema()

# === Transform ===
# Fill only columns that actually exist
# fill_values = {}
# if "Item_Visibility" in df.columns:
#     fill_values["Item_Visibility"] = 0
# if "Item_Weight" in df.columns:
#     avg_weight = df.select(avg("Item_Weight")).first()[0]
#     fill_values["Item_Weight"] = avg_weight

# if fill_values:
#     df = df.na.fill(fill_values)

# Convert date column to proper format (if exists)
# if "TransactionDate" in df.columns:
#     df = df.withColumn("TransactionDate", to_date(col("TransactionDate"), "yyyy-MM-dd"))
#     df = df.withColumn("Year", year(col("TransactionDate")))
#     df = df.withColumn("Month", month(col("TransactionDate")))

# Example aggregation: Total sales per product & city
# if set(["ProductID", "StoreCity", "TotalPrice"]).issubset(df.columns):
#     sales_per_city = df.groupBy("StoreCity", "ProductID") \
#         .agg(
#             round(spark_sum("TotalPrice"), 2).alias("Total_Sales"),
#             round(avg("TotalPrice"), 2).alias("Avg_Sales")
#         )

#     sales_per_city.show(10, truncate=False)

    # === Load ===
    # NEW: allow output_path to be passed as first CLI arg or env var
#     output_path = sys.argv[1] if len(sys.argv) > 1 else "/data/processed_sales"
#     output_path = os.environ.get("OUTPUT_PATH", output_path)

#     sales_per_city.write.mode("overwrite").parquet(output_path)
#     print(f"ETL completed. Processed data saved at {output_path}")
# else:
#     print("Required columns for aggregation not found. Skipping aggregation step.")

# Stop Spark session
# spark.stop()















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