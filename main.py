import streamlit as st
from loader import *
import plotly.express as px


st.set_page_config(page_title="HH vacance Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

col1, col2, col3 = st.columns(3)

unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = col1.selectbox("Select a Site   ", 
                            options=unique_site,
                            )

if selected_site == 'All':
    experience_counts = data['Work Experience'].value_counts().reset_index()
    experience_counts.columns = ['experience', 'count']
    fig = px.pie(experience_counts, values='count', names='experience',
                title=f"Experience Requirement Distribution for {selected_site}",
                labels={'experience': 'Experience Level', 'count': 'Number of Jobs'},
                hole=0.1)
    
else:
    filtered_data = data[data['Creation Site'] == selected_site]
    experience_counts = filtered_data['Work Experience'].value_counts().reset_index()
    experience_counts.columns = ['experience', 'count']
    fig = px.pie(experience_counts, values='count', names='experience',
                title=f"Experience Requirement Distribution for {selected_site}",
                labels={'experience': 'Experience Level', 'count': 'Number of Jobs'},
                hole=0.1)

fig.update_traces(pull=[0.02, 0.05, 0.01, 0.0605],
                            textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
col1.plotly_chart(fig)


unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = col2.selectbox("Select a Site", 
                            options=unique_site,
                            )

if selected_site == 'All':
    experience_counts = data['Internship'].value_counts().reset_index()
    experience_counts.columns = ['Internship', 'count']
    fig = px.pie(experience_counts, values='count', names='Internship',
                title=f"Internship Requirement Distribution for {selected_site}",
                labels={'Internship': 'Internship', 'count': 'Number of Jobs'},
                hole=0.1)
    
else:
    filtered_data = data[data['Creation Site'] == selected_site]
    experience_counts = filtered_data['Internship'].value_counts().reset_index()
    experience_counts.columns = ['Internship', 'count']
    fig = px.pie(experience_counts, values='count', names='Internship',
                title=f"Internship Distribution for {selected_site}",
                labels={'Internship': 'Internship', 'count': 'Number of Jobs'},
                hole=0.1)

fig.update_traces(pull=[0.02, 0.05, 0.01, 0.0605],
                            textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
col2.plotly_chart(fig)


unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = col3.selectbox("Select a Site ", 
                            options=unique_site,
                            )

if selected_site == 'All':
    experience_counts = data['Work_Schedule'].value_counts().reset_index()
    experience_counts.columns = ['Work_Schedule', 'count']
    fig = px.pie(experience_counts, values='count', names='Work_Schedule',
                title=f"Work_Schedule Distribution for {selected_site}",
                labels={'Work_Schedule': 'Work_Schedule', 'count': 'Number of Jobs'},
                hole=0.1)
    
else:
    filtered_data = data[data['Creation Site'] == selected_site].copy()
    experience_counts = filtered_data['Work_Schedule'].value_counts().reset_index()
    experience_counts.columns = ['Work_Schedule', 'count']
    fig = px.pie(experience_counts, values='count', names='Work_Schedule',
                title=f"Work_Schedule Distribution for {selected_site}",
                labels={'Work_Schedule': 'Work_Schedule', 'count': 'Number of Jobs'},
                hole=0.1)

fig.update_traces(pull=[0.02, 0.05, 0.01, 0.0605],
                            textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
col3.plotly_chart(fig)

col1, col2 = st.columns(2)
unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = col1.selectbox("Select a Site  ", 
                            options=unique_site,
                            )

data['Publication Time'] = pd.to_datetime(data['Publication Time'])

unique_roles = data['Role Name'].unique().tolist()
selected_roles = col1.multiselect("Select Roles", options=unique_roles, default=['Data Analyst', 'Q/A testing'])

if selected_site == 'All':
    filtered_data = data[data['Role Name'].isin(selected_roles)].copy()
else:
    filtered_data = data[data['Role Name'].isin(selected_roles) & (data['Creation Site'] == selected_site)].copy()

grouped_data = filtered_data.groupby([filtered_data['Publication Time'].dt.date, 'Role Name']).size().reset_index(name='count')
grouped_data['Publication Time'] = pd.to_datetime(grouped_data['Publication Time'])

if not grouped_data.empty:
    fig = px.line(grouped_data, x='Publication Time', y='count', color='Role Name', markers=True,
                    title="Trends of Selected Roles Over Time",
                    labels={'Publication Time': 'Publication Time', 'count': 'Number of Entries', 'Role Name': 'Role'})
    fig.update_layout(xaxis_title="Publication Time", yaxis_title="Number of Entries", legend_title="Roles")
    col1.plotly_chart(fig)
else:
    col1.write("No data available for the selected roles and years.")


unique_sites = data['Creation Site'].unique().tolist()
unique_sites.insert(0, 'All')

default_index = unique_sites.index('hh.uz') if 'hh.uz' in unique_sites else 0


selected_site = col2.selectbox(
    "Select a Site.",
    options=unique_sites,
    index=default_index
)

filtered_data = data.copy()
if selected_site != 'All':
    filtered_data = filtered_data[filtered_data['Creation Site'] == selected_site]

role_counts = filtered_data['Role Name'].value_counts().reset_index()
role_counts.columns = ['Role Name', 'count']

fig = px.bar(
    role_counts,
    x='Role Name',
    y='count',
    color='Role Name',
    title=f"Number of Entries by Role for {selected_site}",
    labels={'Role Name': 'Role', 'count': 'Number of Entries'}
)

col2.plotly_chart(fig)


unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = st.selectbox(
    "Select a Site.    ",
    options=unique_sites,
    index=default_index
)

filtered_data = data.copy()
if selected_site != 'All':
    filtered_data = filtered_data[filtered_data['Creation Site'] == selected_site]

role_counts = filtered_data['City'].value_counts().reset_index()
role_counts.columns = ['City', 'count']

fig = px.bar(
    role_counts,
    x='City',
    y='count',
    color='City',
    title=f"Number of Entries by Role for {selected_site}",
    labels={'City': 'City', 'count': 'Number of Entries'}
)

st.plotly_chart(fig)





unique_site = data['Creation Site'].unique().tolist()
unique_site.insert(0, 'All')
selected_site = st.selectbox("Select a Site.  ", 
                            options=unique_site,
                            )

unique_roles = data['Role Name'].unique().tolist()
selected_roles = st.multiselect("Select Roles     ", 
                                options=unique_roles, 
                                default=['Data Analyst', 'Q/A testing'])


show_data = data.copy()

if selected_site != 'All':
    show_data = show_data[data['Creation Site'] == selected_site]

show_data = show_data[show_data['Role Name'].isin(selected_roles)]

st.dataframe(show_data)