import time


class TrainOption:
    """Entity Defining all properties of a Train Option
       Note:A Journey can have a train option for a particular segment of a journey"""
    srcStation = ""
    srcStationCode = ""
    destStation = ""
    destStationCode = ""
    srcDepartureTime = time.time()
    destArrivalTime = time.time()
    prices = {}
    price = 0
    priceClass = ""
    trainName = ""
    trainNumber = ""
    duration = time.time()
    numadults=1


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
