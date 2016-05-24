
__author__ = 'ankur'


import concurrent.futures
import time
import logging
import models
import googleapiparser
import datetime
from sets import Set

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT'])

logger = logging.getLogger("TravelPlanner.TrainController.Routes")
fileHandler = logging.FileHandler('C:/Users/Ankit Kumar/Downloads/TrainRoutes_' + today +'.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

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
    except ValueError:
        return route
    return route

def convertsPartsToFullJson(part_1,part_2):
    route={}
    try:
        full={}
        full["carrierName"]="Train"
        full["price"]=part_1["full"]["price"]+part_2["full"]["price"]
        full["duration"]=""
        full["id"]= "train"+part_1["full"]["id"] + "_" + part_2["full"]["id"]
        full["mode"]="train"
        full["site"]="IRCTC"
        full["source"]=part_1["full"]["source"]
        full["destination"]=part_2["full"]["destination"]
        full["arrival"]= part_1["full"]["arrival"]
        full["departure"]=part_1["full"]["departure"]
        route["full"]=[]
        route["parts"]=[]
        route["parts"].append(part_1)
        route["parts"].append(part_2)
        route["full"].append(full)
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
            stationList = models.getStationCodesByName(stationName, logger)
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

        """
        find the trains between the
        :param sourceStationList:
        :param destinationStationList:
        :param journeyDate:
        :return:
        """
        resultJsonData = {}
        resultJsonData["train"]=[]
        start_time = time.time()
        farefutures=[]
        trainCounter=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for srcStation in sourceStationList:
                for destStation in destinationStationList:
                    trainCounter += 1
                    farefutures.append(executor.submit(self.getTrainFare,srcStation,destStation,journeyDate,trainCounter))

        for future in farefutures:
            fareData = future.result()
            if not fareData:
                pass
            else:
                resultJsonData["train"].append(future.result())
        print("--- %s seconds ---" % (time.time() - start_time))
        logger.error(time.time() - start_time)
        return resultJsonData


    def combineData(self,sourceToBreakingStationJson,breakingToDestinationJson):
        resultJsonData ={}
        resultJsonData["train"]=[]
        for possibleSrcToBreakRoute in sourceToBreakingStationJson["train"]:
            for possibleBreakToDestRoute in breakingToDestinationJson["train"]:
                combinedJson=convertsPartsToFullJson(possibleSrcToBreakRoute,possibleBreakToDestRoute)
                resultJsonData["train"].append(combinedJson)
        return resultJsonData


    def convertBreakingStationToCity(self,breakingStation):

        """
        to fetch breaking city from DB, based on breaking station/city
        :param breakingStation: either breaking city or station
        :return: breaking city
        """

        possibleCities = breakingStation.split()
        logger.debug("Possible cities[%s]", breakingStation)

        for possibleCity in possibleCities:
            if possibleCity.upper not in skipValues:
                return models.getBreakingCity(possibleCity.upper, logger)
        return



    def getRoutes(self,source,destination,dateOfJourney):

        """
        This method is used to fetch all possible route between source & destination stations via train and train/bus combined.

        :param source: source station of the journey
        :param destination: destination station of the journey
        :param dateOfJourney: date of the journey
        :return: all possible routes from source to destination via direct train or combination of train-bus
        """
        source = str(source).upper()
        destination = str(destination).upper()

        sourceStations = self.placetoStationCodesCache.getStationsByCode(source)
        destinationStations = self.placetoStationCodesCache.getStationsByCode(destination)
        if not sourceStations or not destinationStations:
            return
        breakingStations = googleapiparser.getPossibleBreakingPlacesForTrain(source,destination, logger)
        breakingCity= self.convertBreakingStationToCity(breakingStations[0])
        breakingStationsStations = self.placetoStationCodesCache.getStationsByCode(breakingCity)
        sourceToBreakingStationJson=self.findTrainsBetweenStations(sourceStations,breakingStationsStations,dateOfJourney)
        breakingToDestinationJson =self.findTrainsBetweenStations(breakingStationsStations,destinationStations,dateOfJourney)
        combinedJson = self.combineData(sourceToBreakingStationJson,breakingToDestinationJson)
        directJson = self.findTrainsBetweenStations(sourceStations,destinationStations,dateOfJourney)
        return directJson["train"].append(combinedJson["train"])








