from flask import Flask, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_variable = str(station).zfill(6)
    filename = f"data_small/TG_STAID{station_variable}.txt"
    formatted_date = datetime.strptime(date, "%Y%M%d").strftime("%Y-%M-%d")
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == formatted_date]["   TG"].squeeze()/10
    return {
        "station": station,
        "date": formatted_date,
        "temperature": temperature
    }


if __name__ == '__main__':
    app.run(debug=True, port=8080)
