import time, datetime


class TrainOption:
    """Entity Defining all properties of a Train Option
       Note:A Journey can have a train option for a particular segment of a journey"""
    srcStation = ""
    srcStationCode = ""
    destStation = ""
    destStationCode = ""
    prices = {}
    price = 0
    priceClass = ""
    trainName = ""
    trainNumber = ""
    duration = time.time()
    numadults=1
    srcDepartureTime = time.time()
    destArrivalTime = time.time()
    srcDepartureDay = ""
    destArrivalDay = ""
    srcDepartureDate = datetime.date.today()
    destArrivalDate = datetime.date.today()


class StationToTrainRelation:
    sourceDepartureTime = time.time()
    destinationArrivalTime = time.time()
    sourceDayNumber = -1
    destinationDayNumber = -1
    fare_1A = 0.0
    fare_2A = 0.0
    fare_3A = 0.0
    fare_GN = 0.0
    fare_SL = 0.0
    fare_CC = 0.0
    fare_2S = 0.0
    fare_FC = 0.0
    fare_3E = 0.0
    sourceStationCode = ""
    destinationStationCode = ""
    trainNumber = ""


class TrainStation:
    """
    Entity class for train station
    """
    code = ""
    name = ""
    city = ""
    otherCity = ""

class FareData:
    """
    Entity class for train fare data
    """
    fare_1A = 0
    fare_2A = 0
    fare_3A = 0
    fare_3E = 0
    fare_FC = 0
    fare_CC = 0
    fare_SL = 0
    fare_2S = 0
    fare_GN = 0


class NearestAirports:
    """
    Entity for nearest airport & nearest big airport to given
    """
    near = ""
    big = ""


class Airports:
    """
    Entity for nearest airports to a given source & destination city
    """
    sourceairports = NearestAirports()
    destinationairports = NearestAirports()


class FlightRequest:
    """
    Entity for flight http request
    """
    sourcecity = ""
    destinationcity = ""
    journeydate = datetime.date.today()
    trainclass = '3A'
    flightclass = 'economy'
    numberofadults = 1


class BreakingStations:
    """
    Entity for breaking station.
    """
    first = ""
    second = ""

