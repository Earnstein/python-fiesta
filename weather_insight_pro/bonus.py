import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv("happy.csv")
data_header = list(df.columns)
options = tuple(data_header[1:])
st.title("In search of happiness")
option_1 = st.selectbox("Select the data to view", options=options, key="select1")
option_2 = st.selectbox("Select the data to view", options=options, key="select2")
st.subheader(f"{option_1.title()} VS {option_2.title()}")

x_axis = list(df[option_1])
y_axis = list(df[option_2])

figure = px.scatter(x=x_axis, y=y_axis, labels={"x": f"{option_2}", "y": f"{option_1}"})
st.plotly_chart(figure)