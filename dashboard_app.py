
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Section 8 Reports Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("fake_property_listings.csv", parse_dates=["ListingDate"])

df = load_data()

st.title("🏠 Section 8 Report Dashboard")
st.markdown("This dashboard simulates the results of 20 key SQL queries defined in Section 6.")

# 1. BETWEEN
st.subheader("1. BETWEEN: Security Deposits Between $1500 and $2000")
between_df = df[(df["SecurityDeposit"] >= 1500) & (df["SecurityDeposit"] <= 2000)]
st.dataframe(between_df[["PropertyID", "SecurityDeposit"]])

# 2. ALIASES
st.subheader("2. ALIASES: Agent Names and Phone Numbers")
st.dataframe(df[["AgentName", "AgentPhoneNumber"]].drop_duplicates())

# 3. AND
st.subheader("3. AND: Properties with ≥ 3 Bedrooms and ≥ 2 Bathrooms")
st.dataframe(df[(df["Bedrooms"] >= 3) & (df["Bathrooms"] >= 2)][["PropertyID", "Bedrooms", "Bathrooms"]])

# 4. LIKE
st.subheader("4. LIKE: Agents Whose Names Start With 'J'")
like_df = df[df["AgentName"].str.startswith("J")]
st.dataframe(like_df[["AgentName", "AgentEmail"]].drop_duplicates())

# 5. IN
st.subheader("5. IN: Available Houses and Condos")
st.dataframe(df[df["PropertyType"].isin(["House", "Condo"])])

# 6. GROUP BY
st.subheader("6. GROUP BY: Count of Listings by Property Type")
grouped = df["PropertyType"].value_counts().reset_index()
grouped.columns = ["PropertyType", "Count"]
st.bar_chart(grouped.set_index("PropertyType"))

# 7. HAVING
st.subheader("7. HAVING: Property Types With More Than 2 Listings")
having_df = grouped[grouped["Count"] > 2]
st.dataframe(having_df)

# 8. COMPARISON
st.subheader("8. COMPARISON: Properties Listed After March 2022")
st.dataframe(df[df["ListingDate"] >= "2022-03-01"])

# 9. AGGREGATE
st.subheader("9. AGGREGATE: Average Square Footage")
avg_sqft = int(df["SqFt"].mean())
st.metric(label="Average SqFt", value=f"{avg_sqft:,} sq ft")

# 10. INNER JOIN (2 tables)
st.subheader("10. INNER JOIN: Property and Assigned Agent Info")
st.dataframe(df[["PropertyID", "AgentName"]])

# 11. INNER JOIN (3 tables)
st.subheader("11. INNER JOIN 3: Property, Agent, and Security Deposit")
st.dataframe(df[["PropertyID", "AgentName", "SecurityDeposit"]])

# 12. LEFT OUTER JOIN
st.subheader("12. OUTER JOIN: All Agents and the Properties They Are Assigned To")
st.dataframe(df[["AgentName", "PropertyType"]].drop_duplicates())

# 13. UNION
st.subheader("13. UNION: Unit Numbers for Apartments and Condos")
st.dataframe(df[df["PropertyType"].isin(["Apartment", "Condo"])][["PropertyID", "PropertyType"]])

# 14. SELF JOIN
st.subheader("14. SELF JOIN: Pairs of Properties with the Same Type")
joined = df[["PropertyID", "PropertyType"]].merge(
    df[["PropertyID", "PropertyType"]], on="PropertyType")
self_join_df = joined[joined["PropertyID_x"] != joined["PropertyID_y"]]
st.dataframe(self_join_df.head(10))

# 15. EQUI JOIN
st.subheader("15. EQUI JOIN: Agent Name and Property Type")
st.dataframe(df[["AgentName", "PropertyType"]].drop_duplicates())

# 16. EXISTS
st.subheader("16. EXISTS: Agents Assigned to at Least One Property")
st.dataframe(df[["AgentName"]].drop_duplicates())

# 17. NON-CORRELATED SUBQUERY
st.subheader("17. NON-CORRELATED SUBQUERY: Property Types with Price Over $1800")
st.dataframe(df[df["Amount"] > 1800][["PropertyType", "Amount"]])

# 18. CORRELATED SUBQUERY
st.subheader("18. CORRELATED SUBQUERY: Agents Assigned to Houses")
st.dataframe(df[df["PropertyType"] == "House"][["AgentName", "PropertyType"]].drop_duplicates())

# 19. NOT IN
st.subheader("19. NOT IN: Agents Not in Agencies 501 and 502")
st.write("Note: Since we don't have agency IDs, simulating with AgentName not starting with J")
st.dataframe(df[~df["AgentName"].str.startswith("J")][["AgentName", "AgentEmail"]].drop_duplicates())

# 20. OR
st.subheader("20. OR: Properties That Are Apartments or Condos")
st.dataframe(df[df["PropertyType"].isin(["Apartment", "Condo"])])

st.markdown("---")
st.caption("Simulated Section 6 SQL Queries · Powered by Streamlit and Pandas")
