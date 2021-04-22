import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# Now that everything has been declared, run/launch the application...
#if __name__ == '__main__':
    #app.run()

#precipitation analysis
@app.route("/api/v1.0/precipitation")
#precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #calculates data one year ago from most recent date on db 
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#stations route
@app.route("/api/v1.0/stations")
#new function stations
def stations():
    results = session.query(Station.station).all() #query that will allow us to get all of the stations in our database.
    stations = list(np.ravel(results)) #one-dimensional array, results parameter, convert results to list
    return jsonify(stations=stations)

#monthly temparture route
@app.route("/api/v1.0/tobs")
#new function temp monthly 
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #calculate the date 1 yr ago from last date
    #query the primary station for all the temp observations from the prev year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results)) #unravel w/ 1 dim array, convert array to a list
    return jsonify(temps=temps)
#statistics route, report on minimum, average, and maximum temperatures, provide start and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None): #add parameters to function
    #query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

#if not statement. * used to indicate there will be multiple results for our query: minimum, average, and max temps
    if not end:
       results = session.query(*sel).\
          filter(Measurement.date >= start).\
          filter(Measurement.date <= end).all()
       temps = list(np.ravel(results))
       return jsonify(temps=temps)
#cal the temp min, avg and max w/ start and end dates. sel list simply data points we need to collect
    results = session.query(*sel).\
       filter(Measurement.date >= start).\
       filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps) 
     
