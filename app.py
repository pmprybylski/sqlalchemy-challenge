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
def welcome():
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
    