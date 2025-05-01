
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("fake_property_listings.csv", parse_dates=["ListingDate"])
    return df

df = load_data()

# Title and description
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")
st.title("🏠 Property Listings Dashboard")
st.markdown("""
This interactive dashboard allows real estate professionals, renters, and buyers to explore available listings.
Use the filters to customize your search and gain insights into the housing market.
""")

# Sidebar filters
st.sidebar.header("Filter Listings")

property_types = st.sidebar.multiselect(
    "Select Property Type", options=df["PropertyType"].unique(), default=df["PropertyType"].unique()
)

markets = st.sidebar.multiselect(
    "Select Market", options=df["PropertyMarket"].unique(), default=df["PropertyMarket"].unique()
)

bedrooms = st.sidebar.slider("Minimum Bedrooms", min_value=1, max_value=5, value=1)
bathrooms = st.sidebar.slider("Minimum Bathrooms", min_value=1, max_value=3, value=1)

min_price, max_price = st.sidebar.slider(
    "Price Range", min_value=int(df["Amount"].min()), max_value=int(df["Amount"].max()),
    value=(1000, 500000)
)

date_range = st.sidebar.date_input(
    "Listing Date Range",
    value=[df["ListingDate"].min(), df["ListingDate"].max()]
)

# Apply filters
filtered_df = df[
    (df["PropertyType"].isin(property_types)) &
    (df["PropertyMarket"].isin(markets)) &
    (df["Bedrooms"] >= bedrooms) &
    (df["Bathrooms"] >= bathrooms) &
    (df["Amount"] >= min_price) &
    (df["Amount"] <= max_price) &
    (df["ListingDate"] >= pd.to_datetime(date_range[0])) &
    (df["ListingDate"] <= pd.to_datetime(date_range[1]))
]

# Display filtered data
st.subheader(f"📋 Filtered Listings: {len(filtered_df)} Found")
st.dataframe(filtered_df.style.format({
    "Amount": "${:,.0f}",
    "SecurityDeposit": "${:,.0f}",
    "SqFt": "{:,.0f} sq ft"
}))

# KPI Metrics
st.markdown("### 📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Price", f"${int(filtered_df['Amount'].mean()):,}")
col2.metric("Average SqFt", f"{int(filtered_df['SqFt'].mean()):,} sq ft")
col3.metric("Average Deposit", f"${int(filtered_df['SecurityDeposit'].mean()):,}")

# Charts
st.markdown("### 📊 Visual Insights")
col4, col5 = st.columns(2)

with col4:
    fig1 = px.histogram(filtered_df, x="PropertyType", title="Listings by Property Type")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.pie(filtered_df, names="PropertyMarket", title="Market Distribution")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 💰 Top 10 Most Expensive Listings")
top10 = filtered_df.sort_values(by="Amount", ascending=False).head(10)
st.table(top10[["PropertyID", "PropertyType", "Amount", "Bedrooms", "Bathrooms", "SqFt"]])

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit · Data: fake_property_listings.csv")
