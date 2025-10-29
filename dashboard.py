import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

# Load Dataset
data = pd.read_csv('coffee_shop_sales.csv')

# Dashboard Configuration
st.set_page_config(page_title="Coffee Sales Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

## Filter Component
min_date = data['transaction_date'].min()
max_date = data['transaction_date'].max()
location = data['store_location'].unique()
product_cat = data['product_category'].unique()

## Date Filter
with st.sidebar:
     st.sidebar.header("Date:")
     start_date, end_date = st.date_input(label="Date Filter",
                                          min_value=min_date,
                                          max_value=max_date,
                                          value=[min_date, max_date])
     data = data[(data["transaction_date"] >= str(start_date)) & (data["transaction_date"] <= str(end_date))]

## Location Filter
with st.sidebar:
     st.sidebar.header("Location:")
     loc = st.multiselect(label="Choose Location", options=location, default=location)

## Product Category Filter
with st.sidebar:
     st.sidebar.header("Product Category:")
     cat = st.multiselect(label="Choose Category Product", options=product_cat, default=product_cat)

## Link Filter to Data
data = data[(data["store_location"].isin(loc)) & (data["product_category"].isin(cat))]

## Dashboard Page

st.title("Coffee Sales Dashboard")

## KPI Metrics
col1, col2, col3 = st.columns(3)

### Total Revenue Metrics
total_revenue = data['total_revenue'].sum()
col1.metric(label="Total Revenue", value=total_revenue)

### Total Products Sales
total_prod = data['transaction_qty'].sum()
col2.metric(label="Total Product", value=total_prod)

### Total Customers
total_cust = data['transaction_id'].count()
col3.metric(label="Total Customer", value=total_cust)
                    
## Plot
col1, col2 = st.columns(2)

### Sales Revenue Trend Over Time
with col1:
  st.subheader('Sales Revenue Over Time')
  fig, ax = plt.subplots(figsize=(20, 15))
  sns.lineplot(x='transaction_date',
               y='total_revenue',
               data=data,
               ax=ax)

  plt.xlabel("Date")
  plt.ylabel("Sales Revenue")

  st.pyplot(fig)

### Total Customers Over Time
with col2:
  st.subheader('Total Customers Over Time')
  fig, ax = plt.subplots(figsize=(20, 15))
  
