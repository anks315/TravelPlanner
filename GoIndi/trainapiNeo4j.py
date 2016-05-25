
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

    def getStationsByCityName(self,cityName):
        if cityName in PlaceToStationCodesCache.cityToStationsMap:
            return PlaceToStationCodesCache.cityToStationsMap[cityName]
        else:
            stationList = models.getStationCodesByCityName(cityName, logger)
            if stationList:
                PlaceToStationCodesCache.cityToStationsMap[cityName]=stationList
            return stationList


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetoStationCodesCache = PlaceToStationCodesCache()

    def getTrainFare(self,sourceCity,destinationStationSet,journeyDate):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourceCity: source of the journey
        :param destinationStationSet: set of destination city's stations
        :param journeyDate: date of journey
        :param trainCounter:
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourceCity[%s] and destination Stations[%s] for [%s]", sourceCity, destinationStationSet, journeyDate)
        start = time.time()
        destinationStationPipeSeperated = self.getPipeSeperatedStationCodes(destinationStationSet)
        trainRoute = models.getTrainsBetweenStation(sourceCity,destinationStationSet)
        fareData=parseAndReturnFare(trainRoute,1)
        print("--- %s api---" % (time.time() - start))
        if not fareData:
            return
        else:
            return fareData



    def findTrainsBetweenStations(self,sourceCity,destinationStationSet,journeyDate):

        """
        find the trains between the sourceCity & destination cities stations
        :param sourceCity: source of the journey
        :param destinationStationSet: list of all available railway stations in destination city
        :param journeyDate: date of journey
        :return:
        """
        resultJsonData = {}
        resultJsonData["train"]=[]
        start_time = time.time()
        farefutures=[]
        trainCounter=0

        self.getTrainFare(sourceCity, destinationStationSet, journeyDate)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for srcStation in sourceCity:
                for destStation in destinationStationSet:
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

        sourceStations = self.placetoStationCodesCache.getStationsByCityName(source)
        destinationStations = self.placetoStationCodesCache.getStationsByCityName(destination)
        destinationStationSet = Set(destinationStations)
        if not sourceStations or not destinationStations:
            return
        directJson = self.findTrainsBetweenStations(source,destinationStationSet,dateOfJourney)
        breakingStations = googleapiparser.getPossibleBreakingPlacesForTrain(source,destination, logger)
        if breakingStations:
            breakingCity = self.convertBreakingStationToCity(breakingStations[0])
            breakingStationsStations = self.placetoStationCodesCache.getStationsByCityName(breakingCity)
            sourceToBreakingStationJson=self.findTrainsBetweenStations(source,breakingStationsStations,dateOfJourney)
            breakingToDestinationJson =self.findTrainsBetweenStations(breakingStationsStations,destinationStations,dateOfJourney)
            combinedJson = self.combineData(sourceToBreakingStationJson,breakingToDestinationJson)
            return directJson["train"].append(combinedJson["train"])
        return directJson["train"]


    def getPipeSeperatedStationCodes(self, destinationStationSet):

        pipeSeperatedCodes = ""
        for code in destinationStationSet:
            pipeSeperatedCodes.join(code)
        print pipeSeperatedCodes
        return





