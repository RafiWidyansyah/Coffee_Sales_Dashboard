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
col2.metric(label="Total Product Sold", value=total_prod)

### Total Customers
total_cust = data['transaction_id'].count()
col3.metric(label="Total Customer", value=total_cust)
                    
## Plot
col1, col2 = st.columns(2) ## Row 1

## Total Revenue Over Month
revenue_by_month = data.groupby(['transaction_month','transaction_day'])['total_revenue'].sum().reset_index()
with col1:
  st.subheader('Total Revenue By Month')

  fig, ax = plt.subplots(figsize=(16, 8))

  sns.lineplot(
    x='transaction_month',
    y='total_revenue',
    data=revenue_by_month,
    color='tab:blue',
    ax=ax
  )

  plt.xlabel("Month")
  plt.ylabel("Total Revenue")

  st.pyplot(fig)

## Total Revenue Over Location
revenue_by_loc = data.groupby(['store_location'])['total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
with col2:
  st.subheader('Total Revenue By Location')

  fig, ax = plt.subplots(figsize=(16, 8))

  sns.barplot(
    x='store_location',
    y='total_revenue',
    data=revenue_by_loc,
    color='tab:blue',
    ax=ax
  )

  st.pyplot(fig)

## Row 2
col1, col2 = st.columns(2)

## Total Revenue By Product Category
revenue_by_cat = data.groupby('product_category')['total_revenue'].sum().reset_index()
with col1:
  st.subheader("Total Revenue By Product Category")

  fig, ax = plt.subplots(figsize=(16, 8))

  sns.barplot(
    x='product_category',
    y='total_revenue',
    data=revenue_by_cat,
    color='tab:blue',
    ax=ax
  )

  plt.xlabel("Product Category")
  plt.ylabel("Total Revenue")

  st.pyplot(fig)

## Top 5 Coffee Product By Revenue
coffee = data[data['product_category'] == 'Coffee']
coffee_rev = data.groupby('product_type')['total_revenue'].sum().reset_index()
coffee_rev = coffee_rev.sort_values('total_revenue', ascending=False).head(5)

with col2:
  st.subheader('Top 5 Coffee Product By Revenue')

  fig, ax = plt.subplots(figsize=(16, 8))

  sns.barplot(
    x='product_type',
    y='total_revenue',
    data=coffee_rev,
    color='tab:blue',
    ax=ax
  )

  plt.xlabel("Product Type")
  plt.ylabel("Total Revenue")

  st.pyplot(fig)
