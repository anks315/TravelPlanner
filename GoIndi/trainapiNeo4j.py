__author__ = 'ankur'

import time
import logging
import models
import googleapiparser
import datetime
from sets import Set

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT'])

logger = logging.getLogger("TravelPlanner.TrainController.Routes")
fileHandler = logging.FileHandler('C:/Users/Ankit Kumar/Downloads/TrainRoutes_' + today + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

trainNumberstoDurationMap = {}


def parseAndReturnFare(trainroutes, logger):
    """
    to return map of train routes in either full or by parts journey
    :param trainroutes: list of trainroutes
    :param logger: to log information
    :return: map of full and part journey of train
    """

    logger.info("Generating route map with full & parts journey")
    route = {"full": [], "parts": []}
    for trainRoute in trainroutes:
        try:
            full = {"carrierName": trainRoute.trainName, "price": trainRoute.fare, "duration": trainRoute.duration,
                    "id": trainRoute.trainNumber, "mode": "train", "site": "IRCTC", "source": trainRoute.srcStation,
                    "destination": trainRoute.destStation, "arrival": trainRoute.destArrivalTime,
                    "departure": trainRoute.srcDepartureTime}
            route["full"].append(full)
        except ValueError:
            logger.error("Error while route map with full & parts journey")
            return route
    return route


def convertsPartsToFullJson(part_1, part_2):

    route = {"full": [], "parts": []}
    try:
        full = {"carrierName": "Train", "price": part_1["full"]["price"] + part_2["full"]["price"], "duration": "",
                "id": "train" + part_1["full"]["id"] + "_" + part_2["full"]["id"], "mode": "train", "site": "IRCTC",
                "source": part_1["full"]["source"], "destination": part_2["full"]["destination"],
                "arrival": part_1["full"]["arrival"], "departure": part_1["full"]["departure"]}
        route["parts"].append(part_1)
        route["parts"].append(part_2)
        route["full"].append(full)
    except ValueError:
        return route
    return route


class PlaceToStationCodesCache:
    """Class returs all stations corresponding to a city"""

    cityToStationsMap = {}

    def getStationsByCityName(self, cityname):
        if cityname in PlaceToStationCodesCache.cityToStationsMap:
            return PlaceToStationCodesCache.cityToStationsMap[cityname]
        else:
            stationList = models.getStationCodesByCityName(cityname, logger)
            if stationList:
                PlaceToStationCodesCache.cityToStationsMap[cityname] = stationList
            return stationList


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetoStationCodesCache = PlaceToStationCodesCache()

    def getTrainFare(self, sourcecity, destinationstationset):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param destinationstationset: set of destination city's stations
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity,
                    destinationstationset)
        start = time.time()
        trainroute = models.getTrainsBetweenStation(sourcecity, destinationstationset, logger)
        faredata = parseAndReturnFare(trainroute, logger)
        logger.info("Time taken [%s]", time.time() - start)
        if not faredata:
            return
        else:
            return faredata

    def findTrainsBetweenStations(self, sourcecity, destinationstationset):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param destinationstationset: list of all available railway stations in destination city
        :param journeyDate: date of journey
        :return:
        """
        resultjsondata = {"train": []}
        faredata = self.getTrainFare(sourcecity, destinationstationset)
        resultjsondata["train"].append(faredata)
        return resultjsondata


    def combineData(self, sourcetobreakingstationjson, breakingtodestinationjson):
        resultJsonData = {}
        resultJsonData["train"] = []
        for possibleSrcToBreakRoute in sourcetobreakingstationjson["train"]:
            for possibleBreakToDestRoute in breakingtodestinationjson["train"]:
                combinedJson = convertsPartsToFullJson(possibleSrcToBreakRoute, possibleBreakToDestRoute)
                resultJsonData["train"].append(combinedJson)
        return resultJsonData

    def convertBreakingStationToCity(self, breakingstation):

        """
        to fetch breaking city from DB, based on breaking station/city
        :param breakingstation: either breaking city or station
        :return: breaking city
        """

        possibleCities = breakingstation.split()
        logger.debug("Possible cities[%s]", breakingstation)

        for possibleCity in possibleCities:
            if possibleCity.upper not in skipValues:
                return models.getBreakingCity(possibleCity.upper, logger)
        return

    def getRoutes(self, source, destination, dateofjourney):

        """
        This method is used to fetch all possible route between source & destination stations via train and train/bus combined.

        :param source: source station of the journey
        :param destination: destination station of the journey
        :param dateofjourney: date of the journey
        :return: all possible routes from source to destination via direct train or combination of train-bus
        """
        source = str(source).upper()
        destination = str(destination).upper()

        sourceStations = self.placetoStationCodesCache.getStationsByCityName(source)
        destinationStations = self.placetoStationCodesCache.getStationsByCityName(destination)
        destinationStationSet = Set(destinationStations)
        if not sourceStations or not destinationStations:
            return
        directjson = self.findTrainsBetweenStations(source, destinationStationSet)
        breakingStations = googleapiparser.getPossibleBreakingPlacesForTrain(source, destination, logger)
        if len(breakingStations) > 0:
            breakingCity = self.convertBreakingStationToCity(breakingStations[0])
            breakingStationsStations = self.placetoStationCodesCache.getStationsByCityName(breakingCity)
            sourceToBreakingStationJson = self.findTrainsBetweenStations(source, breakingStationsStations)
            breakingToDestinationJson = self.findTrainsBetweenStations(breakingStationsStations, destinationStations)
            combinedJson = self.combineData(sourceToBreakingStationJson, breakingToDestinationJson)
            return directjson["train"].append(combinedJson["train"])
        return directjson["train"]
