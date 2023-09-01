import os
import requests


def get_weather_data(city_name: str, forecast_days=None, kind=None):
    num_of_data = 8 * forecast_days
    url = "https://api.openweathermap.org/data/2.5/forecast?"
    params = {
        "q": city_name,
        "appid": os.getenv("OWM_API_KEY")
    }
    request = requests.get(url, params=params)
    response = request.json()
    response_1 = response['list']
    weather_data = response_1[:num_of_data]
    return weather_data


if __name__ == "__main__":
    print(__name__)



