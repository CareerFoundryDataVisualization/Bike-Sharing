import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt




#########################33 Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')

st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")
st.sidebar.title("Aspect Selector")
st.sidebar.markdown("Select an aspect of the analysis:")

page = st.sidebar.selectbox('Select page',
  ["Most popular stations",
    "Weather component and bike usage",
    "Interactive map"])


df = pd.read_csv('df_to_plot_dashboard.csv', index_col = 0)


######################################### DEFINE THE CHARTS #####################################################################


## Create the bar chart

if page == 'Most popular stations':

    ## Bar chart

    df['value'] = 1 
    df_groupby_bar = df.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig.update_layout(
        title = 'Most popular stations',
        xaxis_title = 'Start stations',
        yaxis_title='Sum of trips'
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == 'Weather component and bike usage':

    ### Create the dual axis line chart ###

    fig = make_subplots(specs = [[{"secondary_y": True}]])

    fig.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides'),
    secondary_y = False
    )

    fig.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature'),
    secondary_y=True
    )
    st.plotly_chart(fig, use_container_width=True)


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