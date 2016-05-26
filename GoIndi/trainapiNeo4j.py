__author__ = 'ankur'

import time
import logging
import models
import googleapiparser
import datetime
from sets import Set

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])

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
            full = {"carrierName": trainRoute.trainName, "duration": trainRoute.duration,
                    "id": trainRoute.trainNumber, "mode": "train", "site": "IRCTC", "source": trainRoute.srcStation,
                    "destination": trainRoute.destStation, "arrival": trainRoute.destArrivalTime,
                    "departure": trainRoute.srcDepartureTime, "fare_1A": trainRoute.fare_1A, "fare_2A": trainRoute.fare_2A,
                    "fare_3A": trainRoute.fare_3A, "fare_3E": trainRoute.fare_3E, "fare_FC": trainRoute.fare_FC,
                    "fare_CC": trainRoute.fare_CC, "fare_2S": trainRoute.fare_2S, "fare_SL": trainRoute.fare_SL,
                    "fare_GN": trainRoute.fare_GN}
            route["full"].append(full)
        except ValueError:
            logger.error("Error while route map with full & parts journey")
            return route
    return route


def convertsPartsToFullJson(part_1, part_2):

    route = {"full": [], "parts": []}
    try:
        full = {"carrierName": "Train", "duration": "",
                "id": part_1["full"]["id"] + "_" + part_2["full"]["id"], "mode": "train", "site": "IRCTC",
                "source": part_1["full"]["source"], "destination": part_2["full"]["destination"],
                "arrival": part_1["full"]["arrival"], "departure": part_1["full"]["departure"],
                "fare_1A": part_1["full"]["fare_1A"] + part_2["full"]["fare_1A"],
                "fare_2A": part_1["full"]["fare_2A"] + part_2["full"]["fare_2A"],
                "fare_3A": part_1["full"]["fare_3A"] + part_2["full"]["fare_3A"],
                "fare_3E": part_1["full"]["fare_3E"] + part_2["full"]["fare_3E"],
                "fare_FC": part_1["full"]["fare_FC"] + part_2["full"]["fare_FC"],
                "fare_CC": part_1["full"]["fare_CC"] + part_2["full"]["fare_CC"],
                "fare_SL": part_1["full"]["fare_SL"] + part_2["full"]["fare_SL"],
                "fare_2S": part_1["full"]["fare_2S"] + part_2["full"]["fare_2S"],
                "fare_GN": part_1["full"]["fare_GN"] + part_2["full"]["fare_GN"]}
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
        routedata = parseAndReturnFare(trainroute, logger)
        logger.info("Time taken [%s]", time.time() - start)
        return routedata

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
        resultjsondata = {"train": []}
        for possibleSrcToBreakRoute in sourcetobreakingstationjson["train"]:
            for possibleBreakToDestRoute in breakingtodestinationjson["train"]:
                combinedjson = convertsPartsToFullJson(possibleSrcToBreakRoute, possibleBreakToDestRoute)
                resultjsondata["train"].append(combinedjson)
        return resultjsondata

    def convertBreakingStationToCity(self, breakingstationlist):

        """
        to fetch breaking city from DB, based on breaking station/city
        :param breakingstationlist: either breaking city or station
        :return: breaking city
        """
        logger.debug("Possible cities[%s]", breakingstationlist)
        breakingcitylist = []
        for breakingstation in breakingstationlist:
            possiblecities = breakingstation.split()
            for possiblecity in possiblecities:
                if possiblecity.upper() not in skipValues:
                    city = models.getBreakingCity(possiblecity.upper(), logger)
                    if city:
                        breakingcitylist.append(city)
        return breakingcitylist

    def getRoutes(self, source, destination):

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
            return {"train": []}
        directjson = self.findTrainsBetweenStations(source, destinationStationSet)
        breakingstationlist = googleapiparser.getPossibleBreakingPlacesForTrain(source, destination, logger)
        if len(breakingstationlist) > 0:
            breakingcitylist = self.convertBreakingStationToCity(self.getBreakingStation(breakingstationlist))
            if len(breakingcitylist) > 0:
                breakingcitystations = self.placetoStationCodesCache.getStationsByCityName(breakingcitylist[0])
                sourceToBreakingStationJson = self.findTrainsBetweenStations(source, breakingcitystations)
                breakingToDestinationJson = self.findTrainsBetweenStations(breakingcitylist[0], destinationStations)
                combinedJson = self.combineData(sourceToBreakingStationJson, breakingToDestinationJson)
                return directjson["train"].append(combinedJson["train"])
        return directjson["train"]
    

    def getBreakingStation(self, breakingstationlist):

        """
        this method is used to get relevant breaking station list from all the breaking station lists.
        First prefernece is given to list having only one element then so on
        :param breakingstationlist: list of breaking station list
        :return: breaking list with one or two elements
        """
        for breakingstations in breakingstationlist:
            if len(breakingstations) == 1:
                return breakingstations

        for breakingstations in breakingstationlist:
            if len(breakingstations) == 2:
                return breakingstations