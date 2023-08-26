import streamlit as st

st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
day = st.slider("Forecast Days  ", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select the data to view", ("Temperature", "Sky"))
st.subheader(f"{option} forecast for the next {day} in {place}")

