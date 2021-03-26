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
    <img src='Images/surfs-up.png' alt='Surf's Up'>
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
    <li><a href="/api/v1.0/<start>">/api/v1.0/<start></a></li>
    </ul>
    <p>Start & End Day Analysis:</p>
    <ul>
    <li><a href="/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end></a></li>
    </ul>
    </html>
    """

# Precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Convert query results to dictionary using 'date' as the key and 'prcp' as the value
    # Calculate the date one year ago from the last data point in the database
    one_year_ago = dt.date(2017, 89, 23) - dt.timedelta(days=365)

    # Query to retrieve last 12 months of precipation data selecting only the 'date' and 'prcp' values
    prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).\
        order_by(measurement.date).all()
    
    # Convert list of tuples into a dictionary
    prcp_dict = dict(prcp_data)

    # Return JSON representation of dictionary
    return jsonify(prcp_dict)
