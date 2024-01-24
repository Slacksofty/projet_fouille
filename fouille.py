#!/usr/bin/env python

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Parameters for the URL
base_url = 'https://data.bordeaux-metropole.fr/geojson/aggregate/PC_CAPTE_P'
key = '14566AHIOY'
attributes = '{"comptage_5m":"sum","ident":"first"}'
year_start = 2021
month_start = 1
day_start = 1
hour_start = 8
year_end = 2021
month_end = 2
day_end = 1
hour_end = 8
range_step = 'hour'
data_filter = '{"ident": "Z30CT22"}'

def assemble_url(base_url, key, attributes, year_start, month_start, day_start, hour_start, year_end, month_end, day_end, hour_end, range_step, data_filter):
    range_start = f"{year_start}-{month_start:02d}-{day_start:02d}T{hour_start:02d}:00:00"
    range_end = f"{year_end}-{month_end:02d}-{day_end:02d}T{hour_end:02d}:00:00"
    
    assembled_url = f"{base_url}?key={key}&attributes={attributes}&rangeStart={range_start}&rangeEnd={range_end}&rangeStep={range_step}&filter={data_filter}"
    return assembled_url

def plot_graph(df, title, x_label, y_label, save_path):
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_label], df[y_label], marker='o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

def fetch_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        features = json_data.get('features', [])

        data = []
        for feature in features:
            properties = feature.get('properties', {})
            time = properties.get('time', '')
            ident = properties.get('ident', '')
            comptage_5m = properties.get('comptage_5m', None)

            if comptage_5m is not None:
                data.append({
                    'year': int(time[:4]),
                    'month': int(time[5:7]),
                    'day': int(time[8:10]),
                    'hour': int(time[11:13]),
                    'ident': ident,
                    'comptage_5m': comptage_5m,
                })

        df = pd.DataFrame(data)

        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def group_by_day(df):
    # Group by day and sum the 'comptage_5m'
    grouped_df = df.groupby(['year', 'month', 'day']).agg({'comptage_5m': 'sum'}).reset_index()
    return grouped_df

def group_by_month(df):
    # Group by month and sum the 'comptage_5m'
    grouped_df = df.groupby(['year', 'month']).agg({'comptage_5m': 'sum'}).reset_index()
    return grouped_df

def group_by_year(df):
    # Group by year and sum the 'comptage_5m'
    grouped_df = df.groupby(['year']).agg({'comptage_5m': 'sum'}).reset_index()
    return grouped_df


url = assemble_url(base_url, key, attributes, year_start, month_start, day_start, hour_start, year_end, month_end, day_end, hour_end, range_step, data_filter)

df = fetch_data(url)

day_grouped_df = group_by_day(df)

print(day_grouped_df.head())

month_end = 12

url = assemble_url(base_url, key, attributes, year_start, month_start, day_start, hour_start, year_end, month_end, day_end, hour_end, range_step, data_filter)

df = fetch_data(url)

month_grouped_df = group_by_month(df)

print(month_grouped_df.head())

year_end = 2023

url = assemble_url(base_url, key, attributes, year_start, month_start, day_start, hour_start, year_end, month_end, day_end, hour_end, range_step, data_filter)

df = fetch_data(url)

year_grouped_df = group_by_year(df)

print(year_grouped_df.head())

plot_graph(day_grouped_df, 'Comptage_5m by Day', 'day', 'comptage_5m', 'comptage_by_day.png')
plot_graph(month_grouped_df, 'Comptage_5m by Month', 'month', 'comptage_5m', 'comptage_by_month.png')
plot_graph(year_grouped_df, 'Comptage_5m by Year', 'year', 'comptage_5m', 'comptage_by_year.png')