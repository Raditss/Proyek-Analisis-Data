
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
hourly_data = pd.read_csv('./data/hour.csv')
daily_data = pd.read_csv('./data/day.csv')


# Convert date columns to datetime
hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

st.title('Bike Sharing Dashboard')

# Sidebar for dataset and filters
dataset_choice = st.sidebar.selectbox('Choose a dataset', ['Daily Data', 'Hourly Data'])
date_range = st.sidebar.date_input("Select date range", [daily_data['dteday'].min(), daily_data['dteday'].max()])

# Convert date_range to datetime format for comparison
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Filter the data based on the selected dataset
if dataset_choice == 'Hourly Data':
    filtered_data = hourly_data[(hourly_data['dteday'] >= start_date) & (hourly_data['dteday'] <= end_date)]
else:
    filtered_data = daily_data[(daily_data['dteday'] >= start_date) & (daily_data['dteday'] <= end_date)]



# KPIs
st.header('Key Performance Indicators')
total_rentals = filtered_data['cnt'].sum()
average_rentals = filtered_data['cnt'].mean()
st.metric(label="Total Bike Rentals", value=f"{total_rentals:,.0f}")
st.metric(label="Average Rentals per Period", value=f"{average_rentals:,.2f}")

# Peak Rental Hours (for hourly data)
if dataset_choice == 'Hourly Data':
    st.subheader('Peak Rental Hours')
    peak_hours = filtered_data.groupby('hr')['cnt'].sum().sort_values(ascending=False).head(5)
    st.write(peak_hours)

# Impact of Weather on Rentals
st.header('Weather Impact on Bike Rentals')
fig, ax = plt.subplots()
sns.scatterplot(x=filtered_data['temp'], y=filtered_data['cnt'], ax=ax)
ax.set_title('Temperature vs Bike Rentals')
ax.set_xlabel('Temperature')
ax.set_ylabel('Rentals')
st.pyplot(fig)

# Casual vs Registered Users
if dataset_choice == 'Daily Data':
    st.header('Casual vs Registered Users')
    fig, ax = plt.subplots()
    ax.plot(filtered_data['dteday'], filtered_data['casual'], label='Casual Users', color='green')
    ax.plot(filtered_data['dteday'], filtered_data['registered'], label='Registered Users', color='purple')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Casual vs Registered Bike Rentals Over Time')
    ax.legend()
    st.pyplot(fig)

# Display summary statistics
st.subheader('Summary Statistics')
st.write(filtered_data.describe())
