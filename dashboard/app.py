import os
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="retaildb",
        user="postgres",
        password="postgres"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def load_sql(filename):
    project_root = "/Users/karanveersingh/online_retail_pipeline" #Change to your path address
    sql_path = os.path.join(project_root, "queries", filename)
    print("Loading SQL file from:", sql_path)

    with open(sql_path, "r", encoding="utf-8-sig") as f:
        sql = f.read().strip()
    
    if not sql:
        raise ValueError(f"SQL file {filename} is empty!")
    
    return sql




st.set_page_config(page_title="Online Retail Dashboard", layout="wide")
st.title("Online Retail Dashboard")


year_df = run_query(load_sql("distinct_years.sql"))
countries_df = run_query(load_sql("distinct_countries.sql"))

selected_year = st.sidebar.selectbox("Select Year", year_df['year'].tolist())
selected_country = st.sidebar.multiselect("Select Country", countries_df['country'].tolist(), default=countries_df['country'].tolist())


kpi_query_template = load_sql("kpis.sql")
kpi_query = kpi_query_template.replace("{YEAR}", str(int(selected_year))) \
                              .replace("{COUNTRIES}", ",".join([f"'{c}'" for c in selected_country]))
kpi_df = run_query(kpi_query)

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (£)", f"{kpi_df['total_revenue'][0]:,.2f}")
col2.metric("Avg Order Value (£)", f"{kpi_df['avg_order_value'][0]:,.2f}")
col3.metric("Cancelled Orders", kpi_df['cancelled_orders'][0])


monthly_query_template = load_sql("monthly_revenue.sql")
monthly_query = monthly_query_template.replace("{YEAR}", str(int(selected_year))) \
                                     .replace("{COUNTRIES}", ",".join([f"'{c}'" for c in selected_country]))
df_monthly = run_query(monthly_query)

df_monthly['month'] = df_monthly['month'].astype(int)
df_monthly['month_year'] = df_monthly.apply(lambda row: f"{int(row['month']):02d}-{int(selected_year)}", axis=1)

fig1 = px.line(df_monthly, x='month_year', y='monthly_sales', markers=True,
               title=f"Monthly Revenue Trend ({int(selected_year)})",
               labels={"month_year": "Month-Year", "monthly_sales": "Revenue (£)"},
               template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)


top_customers_query_template = load_sql("top_customers.sql")
top_customers_query = top_customers_query_template.replace("{YEAR}", str(int(selected_year))) \
                                                  .replace("{COUNTRIES}", ",".join([f"'{c}'" for c in selected_country]))
df_customers = run_query(top_customers_query)

fig2 = px.bar(df_customers, x='customer_id', y='revenue',
              title="Top 10 Customers by Revenue",
              labels={"customer_id": "Customer ID", "revenue": "Revenue (£)"},
              template="plotly_white", color='revenue')
st.plotly_chart(fig2, use_container_width=True)


top_products_query_template = load_sql("top_products.sql")
top_products_query = top_products_query_template.replace("{YEAR}", str(int(selected_year))) \
                                                .replace("{COUNTRIES}", ",".join([f"'{c}'" for c in selected_country]))
df_products = run_query(top_products_query)

fig3 = px.bar(df_products, x='description', y='total_sold',
              title="Top 10 Products by Quantity Sold",
              labels={"description": "Product", "total_sold": "Quantity Sold"},
              template="plotly_white", color='total_sold')
st.plotly_chart(fig3, use_container_width=True)
