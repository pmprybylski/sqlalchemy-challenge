# Dependencies & Setup
from flask import Flask, jsonify
import numpy as np
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# DATABASE SETUP

# Create engine and reflect exisitng database into new model
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
base = automap_base()
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create Session from Python to DB
session = Session(engine)

# FLASK SETUP
app = Flask(__name__)

# FLASK ROUTES

# Home 
@app.route('/')
def home():
    return """<html>
    <h1>Hawaii Climate App (Flask API)</h1>
    <hr>
    <img src='Images/surfs-up.png' alt="Surf's Up">
    <br><br>
    <p>Precipitation Analysis:</p>
    <ul>
        <li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a></li>
    </ul>
    <p>Station Analysis:</p>
    <ul>
    <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
    </ul>
    <p>Temperature Analysis:</p>
    <ul>
    <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
    </ul>
    <p>Start Day Analysis:</p>
    <ul>
    <li><a href="/api/v1.0/20160823">/api/v1.0/20160823</a></li>
    </ul>
    <p>Start & End Day Analysis:</p>
    <ul>
    <li><a href="/api/v1.0/20160823/20170823">/api/v1.0/20160823/20170823</a></li>
    </ul>
    </html>
    """

# Precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Convert query results to dictionary using 'date' as the key and 'prcp' as the value
    # Calculate the date one year ago from the last data point in the database
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query to retrieve last 12 months of precipation data selecting only the 'date' and 'prcp' values
    prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).\
        order_by(measurement.date).all()
    
    # Convert list of tuples into a dictionary
    prcp_dict = dict(prcp_data)

    # Return JSON representation of dictionary
    return jsonify(prcp_dict)

# Station Route
@app.route('/api/v1.0/stations')
def station_list():
    # Return a list of stations from the dataset
    active_stations = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    
    # Convert list of tuples into a regular list
    stations_list = list(active_stations)
    
    # Reurn JSON list of stations
    return jsonify(stations_list)

# TOBS Route
@app.route('/api/v1.0/tobs')
def tobs():
    # Calculate the date one year ago from the last data point in the database
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query for dates and temperature observations from a year from the last data point
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_ago).\
        filter(measurement.station == 'USC00519281').\
        order_by(measurement.date).all()

    # Convert to list
    tobs_list = list(tobs_data)

    # JSON list of temperature observations for the previous year
    return jsonify(tobs_list)
 
# Start Day Route
@app.route('/api/v1.0/20160823')
def start_day():
    start = dt.date(2017,8,23) - dt.timedelta(days=365)

    start_day = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        group_by(measurement.date).all()

    # Convert to list
    start_list = list(start_day)

    # Return JSON list of TMIN, TAVG, and TMAX for given start date
    return jsonify(start_list)
    
# Start-End Day Route
@app.route('/api/v1.0/20160823/20170823')
def start_end_day():
    end = dt.date(2017,8,23)
    start = dt.date(2016,8,23)
    
    start_end_day = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        group_by(measurement.date).all()
    
    # Convert to list
    start_end_list = list(start_end_day)

    # Return JSON list of TMIN, TAVG, AND TMAX for a given start-end range
    return jsonify(start_end_list)


# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)






