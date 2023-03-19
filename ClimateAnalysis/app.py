# importing dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np


# importing Flask 
from flask import Flask, jsonify

# creating database  
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# creating flask 
app = Flask(__name__)

# flask routes

@app.route('/')
def homepage():
    return(
        f"Welcome to Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    max_date = session.query(func.max(measurement.date))
    for dates in max_date:
        recent_date = dt.datetime.strptime(dates[0], '%Y-%m-%d')
    one_year_ago = recent_date - dt.timedelta(days = 365)

    results = session.query(measurement.date, measurement.prcp).\
                    filter(measurement.date >= one_year_ago).all()
    
    session.close()

    percip = []
    for date, precipitation in results:
        percip_dict = {}
        percip_dict['Date'] = date
        percip_dict['Precipitation'] = precipitation
        percip.append(percip_dict)

    return jsonify(percip)

@app.route('/api/v1.0/stations')
def stations():
    # starting session
    session = Session(engine)

    # retrieving station names
    results = session.query(station.station).all()

    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    # calculating date from 12 months ago
    max_date = session.query(func.max(measurement.date))
    for dates in max_date:
        recent_date = dt.datetime.strptime(dates[0], '%Y-%m-%d')
    one_year_ago = recent_date - dt.timedelta(days = 365)

    # retrieving past 12 months temperature data from the most active station
    results = session.query(measurement.date, measurement.tobs).\
                filter(measurement.station == 'USC00519281').\
                filter(measurement.date >= one_year_ago)
    
    session.close()

    data = []
    for date, tob in results:
        dict = {}
        dict['Date'] = date
        dict['TOBS'] = tob
        data.append(dict)

    return jsonify(data)

@app.route('/api/v1.0/<start>')
def start_analysis(start):
    session = Session(engine)

    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                    filter(measurement.station == 'USC00519281').filter(measurement.date >= start)
    
    session.close()

    data = []
    for date, tob in results:
        dict = {}
        dict['Date'] = date
        dict['TOBS'] = tob
        date.append(dict)

    return jsonify(data)

@app.route('/api/v1.0/<start>/<end>')
def range_analysis(start, end):
    session = Session(engine)

    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                    filter(measurement.station == 'USC00519281').filter(measurement.date >= start).filter(measurement.date <= end)
    
    session.close()

    data = []
    for date, tob in results:
        dict = {}
        dict['Date'] = date
        dict['TOBS'] = tob
        date.append(dict)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)













