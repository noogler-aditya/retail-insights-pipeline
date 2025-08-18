import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🇮🇳",
    layout="wide"
)

# --- API Configuration ---
API_URL = "http://localhost:8000"

# --- Helper Functions with Caching ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def get_cities():
    """Fetches the list of unique cities from the API."""
    try:
        response = requests.get(f"{API_URL}/cities")
        response.raise_for_status()
        return response.json().get("cities", [])
    except requests.exceptions.RequestException:
        return []

@st.cache_data(ttl=600)
def get_sales_data(city):
    """Fetches sales data for a specific city."""
    try:
        response = requests.get(f"{API_URL}/sales/{city}")
        response.raise_for_status()
        return response.json().get("sales", [])
    except requests.exceptions.RequestException:
        return None

# --- Main Dashboard UI ---
st.title("🇮🇳 Indian Retail Sales Dashboard")
st.markdown("An interactive dashboard to visualize sales insights from our PySpark pipeline.")

# --- Sidebar for User Input ---
st.sidebar.header("Dashboard Filters")
cities = get_cities()

if not cities:
    st.sidebar.error("Could not connect to the API to fetch cities. Please ensure the backend is running.")
else:
    selected_city = st.sidebar.selectbox(
        "Select a City",
        options=cities,
        index=cities.index("Nagpur") if "Nagpur" in cities else 0
    )

    # --- Main Content Area ---
    if selected_city:
        sales_data = get_sales_data(selected_city)

        if sales_data is not None:
            df = pd.DataFrame(sales_data)
            
            st.header(f"📈 Sales Performance in {selected_city}")

            # --- Key Metrics (KPIs) ---
            total_revenue = df['total_sales'].sum()
            avg_transaction_value = df['avg_sales'].mean()
            num_products = df['productid'].nunique()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
            col2.metric("Avg. Transaction Value", f"₹{avg_transaction_value:,.2f}")
            col3.metric("Number of Products", f"{num_products}")

            st.markdown("---")

            # --- Charts and Data Table ---
            col1, col2 = st.columns([2, 3])

            with col1:
                st.subheader("Top 10 Products by Sales")
                top_products = df.nlargest(10, 'total_sales')
                fig = px.bar(
                    top_products,
                    x='total_sales',
                    y='productid',
                    orientation='h',
                    title=f"Top 10 Products in {selected_city}",
                    labels={'total_sales': 'Total Sales (₹)', 'productid': 'Product ID'},
                    text='total_sales'
                )
                fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Full Sales Data")
                st.dataframe(df, use_container_width=True)
        else:
            st.error(f"Failed to fetch sales data for {selected_city}. The API might be down or the city has no data.")