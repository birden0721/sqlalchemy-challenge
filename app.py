# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt  # Import datetime module

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    stations_data = [{"station": station, "name": name} for station, name in results]
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = "USC00519281"
    one_year_ago = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station_id)\
        .filter(Measurement.date >= one_year_ago)\
        .all()
    tobs_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temperature_start(start):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .all()
    min_temp, max_temp, avg_temp = results[0]
    return jsonify({"min_temperature": min_temp, "max_temperature": max_temp, "avg_temperature": avg_temp})

@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .all()
    min_temp, max_temp, avg_temp = results[0]
    return jsonify({"min_temperature": min_temp, "max_temperature": max_temp, "avg_temperature": avg_temp})

if __name__ == '__main__':
    app.run(debug=True)
