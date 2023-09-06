from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DATA_DIRECTORY = "data_small"


def load_station_data(filename, skip_rows):
    return pd.read_csv(filename, skiprows=skip_rows, parse_dates=["    DATE"])


@app.route("/")
def home():
    stations_columns = ["STAID", "STANAME                                 "]
    stations = load_station_data(f"{DATA_DIRECTORY}/stations.txt", skip_rows=17)
    stations_table = stations[stations_columns].to_html()
    return render_template("index.html", data=stations_table)


@app.route("/api/v1/<station>")
def station(station):
    station_variable = str(station).zfill(6)
    filename = f"{DATA_DIRECTORY}/TG_STAID{station_variable}.txt"
    df = load_station_data(filename, skip_rows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    station_data = df.to_dict(orient="records")
    return jsonify(station_data)


@app.route("")
def stations(station, date):
    station_variable = str(station).zfill(6)
    filename = f"{DATA_DIRECTORY}/TG_STAID{station_variable}.txt"
    df = load_station_data(filename, skip_rows=20)
    formatted_date = datetime.strptime(date, "%Y%M%d").strftime("%Y-%m-%d")
    temperature = df.loc[df["    DATE"] == formatted_date, "   TG"].squeeze() / 10
    return jsonify({
        "station": station,
        "date": formatted_date,
        "temperature": temperature
    })


@app.route("/api/v1/year/<station>/<year>")
def year(station, year):
    station_variable = str(station).zfill(6)
    filename = f"{DATA_DIRECTORY}/TG_STAID{station_variable}.txt"
    df = load_station_data(filename, skip_rows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    filtered_data = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return jsonify(filtered_data)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
