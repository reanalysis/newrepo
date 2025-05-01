
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("fake_property_listings.csv")

# Dashboard Title
st.title("🏠 Property Listing Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Listings")

property_type = st.sidebar.multiselect(
    "Property Type", options=df["PropertyType"].unique(), default=df["PropertyType"].unique()
)

market_type = st.sidebar.multiselect(
    "Market", options=df["PropertyMarket"].unique(), default=df["PropertyMarket"].unique()
)

bedrooms = st.sidebar.slider("Minimum Bedrooms", 1, 5, 1)
bathrooms = st.sidebar.slider("Minimum Bathrooms", 1, 3, 1)
min_price, max_price = st.sidebar.slider("Price Range", int(df["Amount"].min()), int(df["Amount"].max()), (1000, 500000))

# Apply filters
filtered_df = df[
    (df["PropertyType"].isin(property_type)) &
    (df["PropertyMarket"].isin(market_type)) &
    (df["Bedrooms"] >= bedrooms) &
    (df["Bathrooms"] >= bathrooms) &
    (df["Amount"] >= min_price) &
    (df["Amount"] <= max_price)
]

# Main View
st.subheader("📋 Filtered Listings")
st.dataframe(filtered_df)

# Visualization 1: Listings by Property Type
st.subheader("📊 Listings by Property Type")
fig1 = px.histogram(filtered_df, x="PropertyType", title="Count of Listings by Type")
st.plotly_chart(fig1)

# Visualization 2: Market Breakdown
st.subheader("🥧 Rent vs Sale")
fig2 = px.pie(filtered_df, names="PropertyMarket", title="Market Distribution")
st.plotly_chart(fig2)

# Visualization 3: Top 5 Most Expensive Properties
st.subheader("💰 Top 5 Expensive Listings")
top5 = filtered_df.sort_values(by="Amount", ascending=False).head(5)
st.table(top5[["PropertyID", "PropertyType", "Amount", "Bedrooms", "Bathrooms"]])

# Visualization 4: Average Square Footage
st.subheader("📐 Average Square Footage")
avg_sqft = filtered_df["SqFt"].mean()
st.metric(label="Average SqFt", value=f"{int(avg_sqft)} sq ft")

# Footer
st.caption("Built with Streamlit · Data powered by fake_property_listings.csv")
