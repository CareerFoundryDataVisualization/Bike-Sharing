import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.sidebar.title("Aspect Selector")
# st.sidebar.markdown("Select an aspect of the analysis:")

page = st.sidebar.selectbox('Select a page',
  ["Intro page","Most popular stations",
    "Weather component and bike usage",
    "Interactive map with aggregated bike trips", "Recommendations"])


df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
df['month'] = df['date'].dt.month
df['month'] = df['month'].astype('int')
df['season'] = [
    "winter" if (month == 12 or 1 <= month <= 4)
    else "spring" if (4 < month <= 5)
    else "summer" if (6 <= month <= 9)
    else "fall"
    for month in df['month']
]



# st.dataframe(df1)
######################################### DEFINE THE CHARTS #####################################################################
if page == "Intro page":
    st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
    st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")
    
    myImage = Image.open("Divvy_Bikes.jpg")
    #source: https://ride.divvybikes.com/blog/new-divvy-ebike
    st.image(myImage)#, caption='Enter any caption here')


## Create the season fiter

elif page == 'Most popular stations':
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')    
    total_rides = float(df1['bike_rides_daily'].sum())    

    total1 = st.columns(1,gap='large')
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
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
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see Streeter Dr/Grand Avenue, Canal Street/St. Addams streat as well as Clinton Street/Madison Street. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map in the last page of the dashboard.")

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
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their effect on the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to November.")


elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over Chicago")

    path_to_html = "Divvy Bike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in Chicago")
    st.components.v1.html(html_data,height=1000)
    st.markdown("Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips. The most popular start stations are: Streeter Dr/Grand Avenue, Canal Street/Adams Street as well as Clinton Street/Madison Street. While having the aggregated bike trips filter enabled, we can see that even though Clinton Street/Madison Street is a popular start stations, it doesn't account for the most commonly taken trips. The most common routes (>2,000) are between Theater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street.")

else:
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs_page.png")  #source: Midjourney
    st.image(bikes)
    st.markdown("Our analysis has shown that Divvy Bikes needs to focus on the following points: <br> - Add more stations to the locations around the water line, such as heater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street <br> - These stations don't need to be fully stocked with bikes in winter and late autumn to reduce logistics costs")