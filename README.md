# Retail Pipeline 🚀

A modern **end-to-end data pipeline** for processing retail sales data from **Tier-2 & Tier-3 Indian cities**, powered by **Apache Spark**, **PostgreSQL**, and a lightweight **FastAPI service**.

This project automates the journey from **raw CSV retail transactions** → **cleaned & aggregated data** → **database storage** → **REST API for insights**.

---

## ✨ Features
- **ETL with Apache Spark**: Cleans, transforms, and aggregates sales data.
- **Data Persistence**: Stores processed results in PostgreSQL.
- **API Layer**: FastAPI serves processed data for analytics & dashboards.
- **Volume Management**: Ensures repeatable Spark runs with atomic writes.
- **Health Checks**: PostgreSQL service monitored for readiness before load.

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
- **Apache Spark 3.5** (via Bitnami image) – Scalable ETL processing
- **PostgreSQL 15** – Robust relational database
- **FastAPI** – Modern async Python API

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- Basic knowledge of Python & SQL (optional)

### 2️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/retail-pipeline.git
cd retail-pipeline
```

### 3️⃣ Environment Setup
Create a `.env` file with database credentials:
```env
DB_USER=retail_user
DB_PASS=retail_pass
DB_NAME=retail_db
DB_PORT=5433   # default mapped port
```


### 4 Access the services
- **API** → [http://localhost:8000](http://localhost:8000)
- **Postgres** → Host: `localhost`, Port: `5433`

---

## 🔄 Workflow
1. **Spark Job**
   - Reads raw CSV from `/app/data`
   - Cleans missing values & transforms schema
   - Aggregates sales per city & product
   - Writes processed parquet → `/app/processed_sales/current`

2. **Loader**
   - Reads parquet files from shared volume
   - Loads aggregated data into PostgreSQL

3. **API**
   - Exposes endpoints to query processed data
   - Ready to integrate with BI dashboards or frontends

---

## 📊 Example Output
**Aggregated Sales (per city & product):**

| StoreCity | ProductID | Total_Sales | Avg_Sales |
|-----------|-----------|-------------|-----------|
| Delhi     | P123      | 150000.00   | 250.50    |
| Jaipur    | P456      |  78000.00   | 180.30    |

---

## 🔧 Development Notes
- The pipeline uses **atomic writes** (`/processed_sales/current`) to avoid Spark overwrite errors.
- Spark job uses **temporary directories** for safe concurrent runs.
- To reset everything (including volumes):


---

## 📌 Future Enhancements
- ✅ Add multi-tenant system (will be given api key and shop id to every shop)
- ✅ Expand API with filtering & analytics endpoints
- ✅ Add dashboard UI with React/Next.js
- ✅ Integrate monitoring (Prometheus + Grafana)
