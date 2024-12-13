import pandas as pd


data = pd.read_csv('processed_roles.csv')

data = data[data['Role Name'] != 'other']
data['City'] = data['City'].str.replace(r'Ташкент\s[0-9.,\s]+', 'Ташкент', regex=True)
