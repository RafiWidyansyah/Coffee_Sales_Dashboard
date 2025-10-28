import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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

## Location Filter
with st.sidebar:
     st.sidebar.header("Location:")
     option = st.multiselect(label="Choose Location", location)

## Link Filter to Data

data = data[(data["transaction_date"] >= start_date) & (data["transaction_date"] <= end_date)]

## Dashboard Page

st.title("Coffee Sales Dashboard")
                    
