# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI, HTTPException
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import os
# from contextlib import contextmanager

# app = FastAPI(
#     title="Indian Retail Sales API",
#     description="An API to serve sales insights processed by PySpark.",
#     version="1.0.0"
# )

# --- Database Connection Settings ---
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS]):
#     raise RuntimeError("One or more database environment variables are not set. Please check your .env file.")

# @contextmanager
# def get_db_connection():
#     """A context manager for safely handling database connections."""
#     conn = None
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
#             user=DB_USER, password=DB_PASS, cursor_factory=RealDictCursor
#         )
#         yield conn
#     except psycopg2.OperationalError as e:
#         print(f"Database connection error: {e}")
#         raise HTTPException(status_code=503, detail="Could not connect to the database.")
#     finally:
#         if conn:
#             conn.close()

# @app.get("/", tags=["General"])
# def read_root():
#     """A welcome endpoint for the API."""
#     return {"message": "Welcome to the Indian Retail Sales API!"}

# @app.get("/cities", tags=["Sales Data"])
# async def get_all_cities():
#     """Returns a list of all unique store cities."""
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cur:
#                 # CORRECTED: Use quotes to enforce case-sensitivity
#                 cur.execute('SELECT DISTINCT "StoreCity" FROM sales ORDER BY "StoreCity";')
#                 # The key from RealDictCursor will be lowercase by default
#                 cities = [row['storecity'] for row in cur.fetchall()]
#         return {"cities": sorted(cities)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/sales/{city}", tags=["Sales Data"])
# async def get_sales_by_city(city: str):
#     """Returns all product sales data for a specific city."""
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cur:
#                 # CORRECTED: Use quotes to enforce case-sensitivity
#                 cur.execute(
#                     'SELECT * FROM sales WHERE LOWER("StoreCity") = LOWER(%s);',
#                     (city,)
#                 )
#                 results = cur.fetchall()
        
    #     if not results:
    #         raise HTTPException(status_code=404, detail=f"No sales data found for city: {city}")
        
    #     return {"city": city, "sales": results}

    # except HTTPException:
    #     raise
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    #     raise HTTPException(status_code=500, detail="An internal server error occurred.")













from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from contextlib import contextmanager

app = FastAPI(
    title="Indian Retail Sales API",
    description="An API to serve sales insights processed by PySpark.",
    version="1.0.0"
)

# --- Database Connection Settings ---
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS]):
    raise RuntimeError("One or more database environment variables are not set. Please check your .env file.")

@contextmanager
def get_db_connection():
    """A context manager for safely handling database connections."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASS, cursor_factory=RealDictCursor
        )
        yield conn
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=503, detail="Could not connect to the database.")
    finally:
        if conn:
            conn.close()

@app.get("/", tags=["General"])
def read_root():
    """A welcome endpoint for the API."""
    return {"message": "Welcome to the Indian Retail Sales API!"}

@app.get("/cities", tags=["Sales Data"])
async def get_all_cities():
    """Returns a list of all unique store cities."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT DISTINCT storecity FROM sales ORDER BY storecity;')
                cities = [row['storecity'] for row in cur.fetchall()]
        return {"cities": sorted(cities)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sales/{city}", tags=["Sales Data"])
async def get_sales_by_city(city: str):
    """Returns all product sales data for a specific city."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # FOOLPROOF FIX: Compare both the column and the input in lowercase
                cur.execute(
                    'SELECT * FROM sales WHERE LOWER(storecity) = LOWER(%s);',
                    (city,)
                )
                results = cur.fetchall()
        
        if not results:
            raise HTTPException(status_code=404, detail=f"No sales data found for city: {city}")
        
        return {"city": city, "sales": results}

    except HTTPException:
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
