import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
# import dropbox
# from dropbox.exceptions import AuthError


########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")
st.sidebar.title("Aspect Selector")
# st.sidebar.markdown("Select an aspect of the analysis:")

page = st.sidebar.selectbox('Select a page',
  ["Most popular stations",
    "Weather component and bike usage",
    "Interactive map"])

# DROPBOX_ACCESS_TOKEN = 'gyqy3sl5f2zjvd5'


# def dropbox_connect():
#     """Create a connection to Dropbox."""

#     try:
#         dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
#     except AuthError as e:
#         print('Error connecting to Dropbox with access token: ' + str(e))
#     return dbx


# dropbox_url = "https://www.dropbox.com/s/ms9t7qx5spi9pof/reduced_data_to_plot.csv?dl=0"

# def dropbox_download_file(dropbox_file_path, local_file_path):
#     """Download a file from Dropbox to the local machine."""

#     try:
#         dbx = dropbox_connect()

#         with open(local_file_path, 'wb') as f:
#             metadata, result = dbx.files_download(path=dropbox_file_path)
#             f.write(result.content)
#     except Exception as e:
#         print('Error downloading file from Dropbox: ' + str(e))

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)

# @st.cache_data(ttl=600)
# def load_data(sheets_url):
#     csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#     return pd.read_csv(csv_url)

# df = pd.read_csv(st.secrets["dropbox_url"])


######################################### DEFINE THE CHARTS #####################################################################


## Create the bar chart

if page == 'Most popular stations':

    ## Bar chart

    df['value'] = 1 
    df_groupby_bar = df.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in Chicago',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == 'Weather component and bike usage':

    ### Create the dual axis line chart ###

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
        title = 'Daily bike trips and temperatures in 2018',
        height = 600
    )

    st.plotly_chart(fig_2, use_container_width=True)


else: 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over Chicago")

    path_to_html = "Divvy Bike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in Chicago")
    st.components.v1.html(html_data,height=1000)
