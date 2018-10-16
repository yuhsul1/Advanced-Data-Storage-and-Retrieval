import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind = engine)


@app.route("/")
def Welcome():
    return (
    f"Welcome to Hawaii Weather Percipitation API <br \>" 
    f"For Percipitation by Dates please visit: /api/v1.0/precipitation<br \>"
    f"For all Station list please visit:/api/v1.0/stations<br \>"
    f"For all Temperature list from past year, please visit: /api/v1.0/tobs<br \>"
    f"For all Temperature data for given starting time, please type yyyy-mm-dd at the end using: /api/v1.0/start/<br \>"
    f"For all Temperature data for given starting time, please enter starting and end date yyyy-mm-dd/yyyy-mm-dd at the end using: /api/v1.0/start/end<br \>"

    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>"2016-08-23").all()

   
    list = []
    
    for result in results:
        prcp = {"Date":[], "Percipitation":[]}
        prcp["Percipitation"].append(result[1])
        prcp["Date"].append(result[0])
        list.append(prcp)

    return jsonify(list)


@app.route("/api/v1.0/stations")
def station():
    results = session.query(Station.name).all()
    all_station = list(np.ravel(results))
    
    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date>"2016-08-23").all()

    list = []
    
    for result in results:
        tobs = {"Date":[], "Tobs":[]}
        tobs["Tobs"].append(result[0])
        tobs["Date"].append(result[1])
        list.append(tobs)

    return jsonify(list)

@app.route("/api/v1.0/start/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).all()

    list = []
    
    for result in results:
        tobs = { "Min Temp":[], "Avg Temp":[], "Max Temp":[]}
      
        tobs["Min Temp"].append(result[0])
        tobs["Avg Temp"].append(result[1])
        tobs["Max Temp"].append(result[2])
        list.append(tobs)

    return jsonify(list)

@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start, Measurement.date<=end).all()

    list = []
    
    for result in results:
        tobs = {"Min Temp":[], "Avg Temp":[], "Max Temp":[]}
        
        tobs["Min Temp"].append(result[0])
        tobs["Avg Temp"].append(result[1])
        tobs["Max Temp"].append(result[2])
        list.append(tobs)

    return jsonify(list)


if __name__ == "__main__":
    app.run(debug=True)