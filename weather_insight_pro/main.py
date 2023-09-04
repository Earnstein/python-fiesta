import streamlit as st
import plotly.express as px
from backend import get_weather_data

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ").title()
day = st.slider("Forecast Days  ", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select the data to view", ("Temperature", "Sky"))
st.subheader(f"{option} forecast for the next {day} days in {place}")

if place:
    try:
        weather_data = get_weather_data(city_name=place, forecast_days=day, kind=option)
        dates = [entry["dt_txt"] for entry in weather_data]

        if option == "Temperature":
            temperature_data = [entry["main"]["temp"] for entry in weather_data]
            figure = px.line(x=dates, y=temperature_data, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            sky_conditions = {
                "Clear": "assets/clear.png",
                "Clouds": "assets/cloud.png",
                "Rain": "assets/rain.png",
                "Snow": "assets/snow.png"
            }
            sky_data = [entry["weather"][0]["main"] for entry in weather_data]
            image_paths = [sky_conditions[key] for key in sky_data]
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, (image_path, sky_condition) in enumerate(zip(image_paths, sky_data)):
                if i < 8:
                    col1.image(image_path, width=115)
                    col1.text(sky_condition)
                elif i < 16:
                    col2.image(image_path, width=115)
                    col2.text(sky_condition)
                elif i < 24:
                    col3.image(image_path, width=115)
                    col3.text(sky_condition)
                elif i < 32:
                    col4.image(image_path, width=115)
                    col4.text(sky_condition)
                else:
                    col5.image(image_path, width=115)
                    col5.text(sky_condition)
    except KeyError:
        st.info(f"{place} does not exists")