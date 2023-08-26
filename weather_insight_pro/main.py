import streamlit as st
import plotly.express as px


def get_data(days):
    dates = ["2020-10-08", "2020-10-13", "2020-10-15"]
    temperatures = [10, 11, 25]
    temperatures = [i * days for i in temperatures]
    return dates, temperatures


st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
day = st.slider("Forecast Days  ", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select the data to view", ("Temperature", "Sky"))
st.subheader(f"{option} forecast for the next {day} in {place}")

x_axis, y_axis = get_data(day)
figure = px.line(x=x_axis, y=y_axis, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)
