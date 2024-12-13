import streamlit as st
import pandas as pd
import plotly.express as px
from loader import data

# Streamlit Page Configuration
st.set_page_config(
    page_title="HH Vacance Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)


data['Publication Time'] = pd.to_datetime(data['Publication Time'])

# Unique site options
unique_sites = data['Creation Site'].unique().tolist()
unique_sites.insert(0, 'All')
default_index = unique_sites.index('hh.uz') if 'hh.uz' in unique_sites else 0

# Columns for Site Selection
col1, col2, col3 = st.columns(3)

# Pie Chart 1: Experience Requirement Distribution
selected_site_exp = col1.selectbox("Select a Site for Experience", options=unique_sites)
filtered_data_exp = data if selected_site_exp == 'All' else data[data['Creation Site'] == selected_site_exp]

exp_counts = filtered_data_exp['Work Experience'].value_counts().reset_index()
exp_counts.columns = ['Experience Level', 'Count']

fig_exp = px.pie(
    exp_counts,
    values='Count',
    names='Experience Level',
    title=f"Experience Requirement Distribution for {selected_site_exp}",
    hole=0.1
)
fig_exp.update_traces(textinfo='percent+label', marker=dict(line=dict(color='white', width=2)))
col1.plotly_chart(fig_exp)

# Pie Chart 2: Internship Distribution
selected_site_intern = col2.selectbox("Select a Site for Internship", options=unique_sites)
filtered_data_intern = data if selected_site_intern == 'All' else data[data['Creation Site'] == selected_site_intern]

intern_counts = filtered_data_intern['Internship'].value_counts().reset_index()
intern_counts.columns = ['Internship', 'Count']

fig_intern = px.pie(
    intern_counts,
    values='Count',
    names='Internship',
    title=f"Internship Distribution for {selected_site_intern}",
    hole=0.1
)
fig_intern.update_traces(textinfo='percent+label', marker=dict(line=dict(color='white', width=2)))
col2.plotly_chart(fig_intern)

# Pie Chart 3: Work Schedule Distribution
selected_site_schedule = col3.selectbox("Select a Site for Work Schedule", options=unique_sites)
filtered_data_schedule = data if selected_site_schedule == 'All' else data[data['Creation Site'] == selected_site_schedule]

schedule_counts = filtered_data_schedule['Work_Schedule'].value_counts().reset_index()
schedule_counts.columns = ['Work Schedule', 'Count']

fig_schedule = px.pie(
    schedule_counts,
    values='Count',
    names='Work Schedule',
    title=f"Work Schedule Distribution for {selected_site_schedule}",
    hole=0.1
)
fig_schedule.update_traces(textinfo='percent+label', marker=dict(line=dict(color='white', width=2)))
col3.plotly_chart(fig_schedule)

# Line Chart: Trends of Selected Roles Over Time
col1, col2 = st.columns(2)

# Role Selection
selected_site_roles = col1.selectbox("Select a Site for Trends", options=unique_sites)
unique_roles = data['Role Name'].unique().tolist()
selected_roles = col1.multiselect("Select Roles", options=unique_roles, default=['Data Analyst', 'Q/A testing'])

filtered_data_roles = data.copy()
if selected_site_roles != 'All':
    filtered_data_roles = filtered_data_roles[filtered_data_roles['Creation Site'] == selected_site_roles]

filtered_data_roles = filtered_data_roles[filtered_data_roles['Role Name'].isin(selected_roles)]
grouped_data_roles = filtered_data_roles.groupby([filtered_data_roles['Publication Time'].dt.date, 'Role Name']).size().reset_index(name='Count')

if not grouped_data_roles.empty:
    fig_roles = px.line(
        grouped_data_roles,
        x='Publication Time',
        y='Count',
        color='Role Name',
        markers=True,
        title="Trends of Selected Roles Over Time",
        labels={'Publication Time': 'Publication Time', 'Count': 'Number of Entries', 'Role Name': 'Role'}
    )
    fig_roles.update_layout(xaxis_title="Publication Time", yaxis_title="Number of Entries", legend_title="Roles")
    col1.plotly_chart(fig_roles)
else:
    col1.write("No data available for the selected roles and years.")

# Bar Chart: Number of Entries by Role
selected_site_bar = col2.selectbox("Select a Site for Role Count", options=unique_sites, index=default_index)
filtered_data_bar = data if selected_site_bar == 'All' else data[data['Creation Site'] == selected_site_bar]

role_counts_bar = filtered_data_bar['Role Name'].value_counts().reset_index()
role_counts_bar.columns = ['Role Name', 'Count']

fig_bar = px.bar(
    role_counts_bar,
    x='Role Name',
    y='Count',
    color='Role Name',
    title=f"Number of Entries by Role for {selected_site_bar}",
    labels={'Role Name': 'Role', 'Count': 'Number of Entries'}
)
col2.plotly_chart(fig_bar)

df = pd.read_csv("processed_roles.csv")
df['City'] = df['City'].str.replace(r'Ташкент\s[0-9.,\s]+', 'Ташкент', regex=True)
selected_site_city = st.selectbox("Select a Site for City Count", options=unique_sites, index=default_index)
filtered_data_city = df if selected_site_city == 'All' else df[df['Creation Site'] == selected_site_city]

city_counts = filtered_data_city['City'].value_counts().reset_index()
city_counts.columns = ['City', 'Count']

fig_city = px.bar(
    city_counts,
    x='City',
    y='Count',
    color='City',
    title=f"Number of Entries by City for {selected_site_city}",
    labels={'City': 'City', 'Count': 'Number of Entries'}
)
st.plotly_chart(fig_city)

# Display Filtered Data Table
selected_site_table = st.selectbox("Select a Site for Data Table", options=unique_sites)
selected_roles_table = st.multiselect("Select Roles for Data Table", options=unique_roles, default=['Data Analyst', 'Q/A testing'])

filtered_data_table = data.copy()
if selected_site_table != 'All':
    filtered_data_table = filtered_data_table[filtered_data_table['Creation Site'] == selected_site_table]

filtered_data_table = filtered_data_table[filtered_data_table['Role Name'].isin(selected_roles_table)]

st.dataframe(filtered_data_table)
