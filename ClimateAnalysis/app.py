# importing dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

@app.route('/api/v1.0/stations')
def stations():
    # starting session
    session = Session(engine)

    # retrieving station names
    station_names = session.query(station.station)

    session.close()

    return jsonify(station_names)

@app.route('/api/v1.0/tobs')
def tobs():
    # calculating date from 12 months ago
    max_date = session.query(func.max(measurement.date))
    for dates in max_date:
        recent_date = dt.datetime.strptime(dates[0], '%Y-%m-%d')
    one_year_ago = recent_date - dt.timedelta(days = 365)

    session = Session(engine)

    # retrieving past 12 months temperature data from the most active station
    results = session.query(measurement.date, measurement.tobs).\
                filter((measurement.station == 'USC00519281').\
                filter(measurement.date >= one_year_ago))
    
    session.close()

    return jsonify(results)

@app.route('/api/v1.0/<start>')
def start_analysis(start):
    session = Session(engine)

    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                    filter(measurement.station == 'USC00519281').filter(measurement.date >= start)
    
    session.close()

    return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def range_analysis(start, end):
    session = Session(engine)

    results = session.query(measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                    filter(measurement.station == 'USC00519281').filter(measurement.date >= start).filter(measurement.date <= end)
    
    session.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)













