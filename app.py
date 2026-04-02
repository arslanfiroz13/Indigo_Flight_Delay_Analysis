import streamlit as st
import pandas as pd
import mysql.connector

# ------------------ CONNECTION ------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1539",
    database="indigo_flight_analysis"
)


# ------------------ TITLE ------------------
st.set_page_config(layout="wide")
st.title("✈️ Indigo Flight Delay Dashboard")

# ------------------ LOAD DATA ------------------
df = pd.read_sql("SELECT * FROM indigo_flights", conn)

# ------------------ KPI ------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Flights", len(df))
col2.metric("Avg Arrival Delay", round(df['arrival_delay'].mean(), 2))
col3.metric("Avg Departure Delay", round(df['departure_delay'].mean(), 2))
col4.metric("Max Delay", df['arrival_delay'].max())

# ------------------ TOP DELAY ------------------
st.subheader("🚨 Top 10 Delayed Flights")
st.dataframe(df.sort_values(by='arrival_delay', ascending=False).head(10))

# ------------------ ROUTES ------------------
st.subheader("🛫 Top Routes")

routes = df.groupby(['origin','destination']).size().reset_index(name='total')
routes['route'] = routes['origin'] + " → " + routes['destination']

st.bar_chart(routes.set_index('route')['total'])

# ------------------ AIRPORT DELAY ------------------
st.subheader("🏢 Avg Delay by Airport")

airport = df.groupby('origin')['arrival_delay'].mean().reset_index()
st.bar_chart(airport.set_index('origin'))

# ------------------ MONTHLY ------------------
st.subheader("📅 Monthly Flights")

df['month'] = pd.to_datetime(df['date']).dt.month
monthly = df.groupby('month').size()

st.line_chart(monthly)

# ------------------ MONTHLY DELAY ------------------
st.subheader("📉 Monthly Avg Delay")

monthly_delay = df.groupby('month')['arrival_delay'].mean()
st.line_chart(monthly_delay)

# ------------------ DISTANCE VS DELAY ------------------
st.subheader("📏 Distance vs Delay")

distance_delay = df.groupby('distance')['arrival_delay'].mean()
st.line_chart(distance_delay)

# ------------------ NO DELAY FLIGHTS ------------------
st.subheader("✅ Flights with No Delay")

no_delay = df[df['arrival_delay'] <= 0]
st.write("Total No Delay Flights:", len(no_delay))
st.dataframe(no_delay.head(20))

# ------------------ LONG DISTANCE ------------------
st.subheader("🌍 Long Distance Flights (>1500 km)")

long_flights = df[df['distance'] > 1500]
st.dataframe(long_flights.head(20))

# ------------------ TOP DELAYED ROUTES ------------------
st.subheader("🔥 Top 5 Most Delayed Routes")

delay_routes = df.groupby(['origin','destination'])['arrival_delay'].mean().reset_index()
delay_routes = delay_routes.sort_values(by='arrival_delay', ascending=False).head(5)

delay_routes['route'] = delay_routes['origin'] + " → " + delay_routes['destination']

st.bar_chart(delay_routes.set_index('route')['arrival_delay'])

# ------------------ AIRLINE ANALYSIS ------------------
st.subheader("✈️ Flights by Airline")

airline = df['airline'].value_counts()
st.bar_chart(airline)

# ------------------ DEPARTURE VS ARRIVAL ------------------
st.subheader("📊 Departure vs Arrival Delay")

compare = df[['departure_delay','arrival_delay']].head(100)
st.line_chart(compare)

# ------------------ RAW DATA ------------------
st.subheader("📄 Raw Data")
st.dataframe(df)