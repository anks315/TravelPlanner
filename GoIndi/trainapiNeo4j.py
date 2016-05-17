__author__ = 'ankur'


import hmac
import json
import trainConstants
import urllib
import concurrent.futures
import time
import  logging
import models



trainNumberstoDurationMap ={}



def parseAndReturnFare(trainOption,trainCounter):
    route={}
    try:
        full={}
        full["carrierName"]=trainOption.trainName
        full["price"]=trainOption.fare
        full["duration"]=""
        full["id"]= "train"+str(trainCounter)
        full["mode"]="train"
        full["site"]="IRCTC"
        full["source"]=trainOption.srcStation
        full["destination"]=trainOption.destStation
        full["arrival"]= trainOption.destArrivalTime
        full["departure"]=trainOption.srcDepartureTime
        route["full"]=[]
        route["parts"]=[]
        route["full"].append(full)
        parts=full
        parts["id"]="train"+str(trainCounter)+str(1)
        route["parts"].append(parts)
    except ValueError:
        return route
    return route


class PlaceToStationCodesCache:
    """Class returs all stations corresponding to a city"""

    cityToStationsMap={}

    def getStationsByCode(self,stationName):
        if stationName in PlaceToStationCodesCache.cityToStationsMap:
            return PlaceToStationCodesCache.cityToStationsMap[stationName]
        else:
            stationList = models.getStationCodesByName(stationName)
            if stationList:
                PlaceToStationCodesCache.cityToStationsMap[stationName]=stationList
            return stationList


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetoStationCodesCache = PlaceToStationCodesCache()

    def getTrainFare(self,sourceStation,destinationStation,journeyDate,trainCounter):
        start = time.time()
        trainRoute = models.getTrainsBetweenStation(sourceStation,destinationStation,journeyDate)
        fareData=parseAndReturnFare(trainRoute,trainCounter)
        print("--- %s api---" % (time.time() - start))
        if not fareData:
            return
        else:
            return fareData



    def findTrainsBetweenStations(self,sourceStationList,destinationStationList,journeyDate):
        resultJsonData = {}
        resultJsonData["train"]=[]
        start_time = time.time()
        farefutures=[]
        trainCounter=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for srcStation in sourceStationList:
                for destStation in destinationStationList:
                    trainCounter=trainCounter+1
                    farefutures.append(executor.submit(self.getTrainFare,srcStation,destStation,journeyDate,trainCounter))

        for future in farefutures:
            fareData = future.result()
            if not fareData:
                pass
            else:
                resultJsonData["train"].append(future.result())
        print("--- %s seconds ---" % (time.time() - start_time))
        logging.error(time.time() - start_time)
        return resultJsonData


    def getRoutes(self,source,destination,dateOfJourney):

        sourceStations = self.placetoStationCodesCache.getStationsByCode(source)
        destinationStations = self.placetoStationCodesCache.getStationsByCode(destination)
        if not sourceStations or not destinationStations:
            return
        else:
            return self.findTrainsBetweenStations(sourceStations,destinationStations,dateOfJourney)



