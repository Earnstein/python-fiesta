import os
import requests


def get_data(days):
    dates = ["2020-10-08", "2020-10-13", "2020-10-15"]
    temperatures = [10, 11, 25]
    temperatures = [i * days for i in temperatures]
    return dates, temperatures


def get_weather_data(city_name: str, forecast_days=None, kind=None):
    num_of_weather_data = 8 * forecast_days
    url = "https://api.openweathermap.org/data/2.5/forecast?"
    params = {
        "q": city_name,
        "appid": os.getenv("OWM_API_KEY")
    }
    request = requests.get(url, params=params)
    response = request.json()
    response_1 = response['list']
    weather_data = response_1[:num_of_weather_data]
    return weather_data


if __name__ == "__main__":
    a = get_weather_data("akure", 5, "temperature")
    print(a)



