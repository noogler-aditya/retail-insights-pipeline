# Retail Pipeline 🚀

An **end-to-end data pipeline** for processing retail sales data from **Tier-2 & Tier-3 Indian cities**.It automates the flow from **raw CSVs to a REST API**, powered by **Apache Spark**, **PostgreSQL**, and **FastAPI**.

---

## ✨ Workflow & Features

This project implements a classic ETL pattern to deliver analysis-ready data.
**Raw CSV**→ **Spark (Clean & Aggregate)** → **PostgreSQL (Store)** → **FastAPI (Serve)**

- **Scalable ETL**: Cleans and aggregates data efficiently with Apache Spark.
- **Reliable Storage**: Persists processed data in PostgreSQL.
- **Fast API Layer**: Exposes data for dashboards via FastAPI.
- **Atomic Writes**: Ensures safe, repeatable Spark job execution.
- **Health Checks**: Waits for the database to be ready before loading data.

---

## 📂 Project Structure

```bash
.
├── api/
│   └── main.py               # FastAPI app
├── dashboard/
│   └── app.py                # Dashboard application (e.g., Streamlit)
├── data/
│   ├── processed_sales/       # Processed parquet data
│   └── indian_retail_tier2_tier3.csv  # Raw input dataset
├── data_ingestion/
│   └── fetch_sales.py        # Script for data ingestion
├── db/
│   └── load_to_db.py         # Loads processed parquet → Postgres
├── processing/
│   └── spark_etl.py          # Spark ETL job
├── venv/                     # Python virtual environment (ignored in Docker)
├── .env                      # Environment variables
├── .gitignore                # Git ignore rules
├── accuracy.ipynb            # Model evaluation notebook
├── initial_EDA.ipynb         # Exploratory Data Analysis notebook
├── requirement.txt           # Python dependencies
```

---

## ⚙️ Tech Stack

**Apache Spark 3.5 | PostgreSQL 15 | FastAPI | Docker**

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/retail-pipeline.git
cd retail-pipeline
```

### 2️⃣ Environment Setup

Create a file named `.env` in the root directory with your database credentials:

```env
DB_USER=retail_user
DB_PASS=retail_pass
DB_NAME=retail_db
DB_PORT=5433   # default mapped port
```

### 🔧 Access & Output

- **API Docs**: [http://localhost:8000](http://localhost:8000)
- **Postgres** → Host: `localhost`, Port: `5433`

## 📊 Example Output

**Aggregated Sales (per city & product):**

| StoreCity | ProductID | Total_Sales | Avg_Sales |
| --------- | --------- | ----------- | --------- |
| Delhi     | P123      | 150000.00   | 250.50    |
| Jaipur    | P456      | 78000.00    | 180.30    |
| Mumbai    | P789      | 210500.00   | 310.75    |

---

## 📌 Notes & Future Work

- The pipeline uses atomic writes to a current directory to prevent Spark overwrite errors.
- To completely reset the database and volumes, run docker-compose down -v.

**Future plans include**: adding multi-tenancy, expanding API endpoints with more analytics, and building a dashboard UI.
