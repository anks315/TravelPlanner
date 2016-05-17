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
