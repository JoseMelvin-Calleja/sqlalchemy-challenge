# importing dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# importing Flask 
from flask import Flask

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

@app.route('/api/v1.0/precipitation')
def precipitation():

@app.route('/api/v1.0/stations')
def stations():

@app.route('/api/v1.0/tobs')
def tabs():

@app.route('/api/v1.0/<start>')
def start_analysis(start):

@app.route('/api/v1.0/<start>/<end>')
def range_analysis(start, end):


if __name__ == "__main__":
    app.run(debug=True)













