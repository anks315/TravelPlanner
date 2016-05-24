import time

class TrainOption:
    """Entity Defining all properties of a Train Option
       Note:A Journey can have a train option for a particular segment of a journey"""
    srcStation=""
    destStation=""
    srcDepartureTime=time.time()
    destArrivalTime=time.time()
    fare=0.0
    trainName=""


class StationToTrainRelation:
    sourceDepartureTime=time.time()
    destinationArrivalTime=time.time()
    sourceDayNumber=-1
    destinationDayNumber=-1
    fare_1A=0.0
    fare_2A=0.0
    fare_3A=0.0
    fare_GN=0.0
    fare_SL=0.0
    fare_CC=0.0
    fare_2S=0.0
    fare_FC=0.0
    fare_3E=0.0
    sourceStationCode=""
    destinationStationCode=""
    trainNumber=""

