# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)


#Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

engine.execute('SELECT * FROM measurement LIMIT 10').fetchall()

# Design a query to retrieve the last 12 months of precipitation data and plot the results
max_date = session.query(Measurement.prcp, Measurement.date).\
    order_by(Measurement.date.desc()).first()
print(max_date)

min_date = session.query(Measurement.prcp, Measurement.date).\
    order_by(Measurement.date.asc()).first()
print(min_date)

#api route set up

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all dates and precipitation in past year"""
    
#Calculate the date 1 year ago from the last data point in the database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
#Unpacking results by performing a query to retrieve the data and precipitation scores
    meas_prcp= session.query(Measurement.date, func.sum(Measurement.prcp).label("prcp")).filter(Measurement.date>query_date).\
        group_by(Measurement.date).order_by(Measurement.date).all()
    
# Create a dictionary from the row data and append to a list of total_rain
    total_rain = []
    for date, prcp in meas_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        total_rain.append(prcp_dict)

    return jsonify(total_rain)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    active_stations= session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station). \
    order_by(func.count(Measurement.station).desc()).all()
    active_stations

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in active_stations:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all dates and  in temperatures in past year"""
    
#Calculate the date 1 year ago from the last data point in the database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
#Unpacking results by performing a query to retrieve the data and precipitation scores
    meas_tobs= session.query(Measurement.date, func.sum(Measurement.tobs).label("tobs")).filter(Measurement.date>query_date).\
        group_by(Measurement.date).order_by(Measurement.date).all()
    
# Create a dictionary from the row data and append to a list of total_rain
    year_temps = []
    for date, tobs in meas_tobs:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        year_temps.append(temp_dict)

    return jsonify(year_temps)


# @app.route("/api/v1.0/<start>")
# def temp_info():
#     """Return minimum, maximum and average temperature for all date higher than start date"""
#     start_date = dt.date(2015, 5, 1)
#     temp_info = session.query(func.min(Measurement.tobs).label("TMIN"),func.max(Measurement.tobs).label("TMAX"),\
#                     func.avg(Measurement.tobs).label("TAVG")).filter(Measurement.date>=start_date).all()
    
#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_temp_info = []
    
#     for row in temp_info:
#         row_dict = {}
#         row_dict["minimum temperature"] = row.TMIN
#         row_dict["maximum temperature"] = row.TMAX
#         row_dict["average temperature"] = row.TAVG
#         all_temp_info.append(row_dict)

#     return jsonify(all_temp_info)


# @app.route("/api/v1.0/<start>/<end>")
# def temp_info2(start_date,end_date):
#     """Return minimum, maximum and average temperature for all date higher than start date and lower than end date"""
#     temp_info = session.query(func.min(Measurement.tobs).label("TMIN"),func.max(Measurement.tobs).label("TMAX"),\
#                     func.avg(Measurement.tobs).label("TAVG")).filter(Measurement.date>=start_date).\
#                     filter(Measurement.date<=end_date).all()
    
#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_temp_info = []
    
#     for row in temp_info:
#         row_dict = {}
#         row_dict["minimum temperature"] = row.TMIN
#         row_dict["maximum temperature"] = row.TMAX
#         row_dict["average temperature"] = row.TAVG
#         all_temp_info.append(row_dict)

#     return jsonify(all_temp_info)


if __name__ == '__main__':
    app.run(debug=True)

