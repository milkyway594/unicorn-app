import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px

# st.title("demo app")
# st.write("welcome to streamlit")

def load_data():
    df= pd.read_csv("Unicorn_Companies.csv")
    df.loc[:,"Valuation ($)"] =df.loc[:,"Valuation"].str.replace("$","").str.replace("B","000000000").astype("int64")
    df.loc[:,"Funding ($)"] = df.loc[:,"Funding"].str.replace("Unknown","-1").str.replace("$","").str.replace("M","00000").str.replace("B","00000000").astype("int64")
    df.drop(columns=["Valuation","Funding"],axis=1,inplace=True)
    df["Date Joined"] =pd.to_datetime(df["Date Joined"])
    df.loc[:,"year joined"]=df["Date Joined"].dt.year
    df.loc[:,"count"] = 1


    return df

df =load_data()
st.title("Unicorn Companies App")

# st.dataframe(df)

# create filter

industry_list = df["Industry"].unique()
selected_industry = st.sidebar.multiselect("Industry",industry_list)
filtered_industry = df[df["Industry"].isin(selected_industry)]

city_list = df["City"].unique()
selected_city = st.sidebar.multiselect("City",city_list)
filtered_city = df[df["City"].isin(selected_city)]

continent_list = df["Continent"].unique()
selected_continent = st.sidebar.multiselect("Continent",continent_list)
filtered_continent = df[df["Continent"].isin(selected_continent)]

year_founded_list = df["Year Founded"].unique()
selected_year = st.sidebar.multiselect("Year Founded",year_founded_list)
filtered_year = df[df["Year Founded"].isin(selected_year)]

# this is the data if industry is selected and/if none
if selected_industry and selected_city:
    combined_table =df[df["Industry"].isin(selected_industry) & df["City"].isin(selected_city)]
    st.dataframe(combined_table)

elif selected_industry :
    st.dataframe(filtered_industry)

elif  selected_city:

    st.dataframe(filtered_city)

# elif selected_continent:
#     st.dataframe(filtered_continent)

# elif selected_year:
#     st.dataframe(filtered_year)


else:

    st.dataframe(df)

# calculate some metrics
total_valuation=F"$ {round(df["Valuation ($)"].sum()/1000000000,2)} B"
total_funding=f"$ {df["Funding ($)"].sum() :.04f} B"
no_of_companies=len(df)


# display these metrics
# using streamlit container / column components

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("no of companies",no_of_companies)

with col2:
    st.metric("Total valuation",total_valuation)

with col3:
    st.metric("Total funding",total_funding)


con =st.container()
# Create different charts
with con:
    st.subheader("charts section")
    bar_plot_1 = sns.countplot(data=df,x=df["Industry"])
    plt.xticks(rotation=45)
    plt.ylabel("No of companies")
    st.pyplot(bar_plot_1.get_figure())


    # plotly charts
    # line chart
    line_1= px.bar(
        df,x="Industry",y="count")
    st.plotly_chart(line_1)