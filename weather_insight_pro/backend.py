import os
import requests
def get_data(days):
    dates = ["2020-10-08", "2020-10-13", "2020-10-15"]
    temperatures = [10, 11, 25]
    temperatures = [i * days for i in temperatures]
    return dates, temperatures


url = "https://api.openweathermap.org/data/2.5/forecast?"
params = {
    "lat": float(os.getenv("MY_LAT")),
    "lon": float(os.getenv("MY_LONG")),
    "appid": os.getenv("OWM_API_KEY")
}

request = requests.get(url, params=params)
response = request.json()
print(response)