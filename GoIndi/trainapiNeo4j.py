__author__ = 'ankur'

import time
import logging
import models
import googleapiparser
import calendar
from sets import Set
import dateTimeUtility
import busapi
import copy
from datetime import datetime

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])

logger = logging.getLogger("TravelPlanner.TrainController.Routes")
#fileHandler = logging.FileHandler('/home/ankur/TrainRoutes_' + today + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#fileHandler.setFormatter(formatter)
#logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

trainNumberstoDurationMap = {}


def parseandreturnroute(trainroutes, logger,journeyDate,trainCounter):
    """
    to return map of train routes in either full or by parts journey
    :param trainroutes: list of trainroutes
    :param logger: to log information
    :return: map of full and part journey of train
    """

    logger.info("Generating route map with full & parts journey")
    routes = []

    for trainRoute in trainroutes:
        route = {"full": [], "parts": []}
        trainCounter[0]=trainCounter[0]+1
        try:
            part ={}
            full = {"carrierName": trainRoute.trainName, "duration": trainRoute.duration,
                    "id": "train"+str(trainCounter[0]), "mode": "train", "site": "IRCTC", "source": trainRoute.srcStation,
                    "destination": trainRoute.destStation, "arrival": trainRoute.destArrivalTime,
                    "arrivalDate":dateTimeUtility.calculateArrivalTimeAndDate(journeyDate,trainRoute.srcDepartureTime,trainRoute.duration)["arrivalDate"],
                    "departure": trainRoute.srcDepartureTime,"departureDate":journeyDate,
                    "fare_1A": trainRoute.fare_1A, "fare_2A": trainRoute.fare_2A,
                    "fare_3A": trainRoute.fare_3A, "fare_3E": trainRoute.fare_3E, "fare_FC": trainRoute.fare_FC,
                    "fare_CC": trainRoute.fare_CC, "fare_2S": trainRoute.fare_2S, "fare_SL": trainRoute.fare_SL,
                    "fare_GN": trainRoute.fare_GN,"price":trainRoute.fare_1A}
            part = copy.deepcopy(full)
            part["id"]="train" + str(trainCounter[0]) + str(1)
            part["subParts"]=[]
            part["subParts"].append(copy.deepcopy(full))
            part["subParts"][0]["id"]="train" + str(trainCounter[0]) + str(1)+str(1)

            route["full"].append(full)
            route["parts"].append(part)
            routes.append(route)
        except ValueError:
            logger.error("Error while route map with full & parts journey")
            return routes
    return routes


def convertsPartsToFullJson(part_1, part_2,trainCounter):

    """
    This method is used to combine train journey data from part_1 and part_2 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    trainCounter[0]=trainCounter[0]+1
    try:
        part = {"carrierName": "Train", "duration": "", "id": "train" + str(trainCounter[0]) + str(1), "mode": "train",
                "site": "IRCTC", "source": part_1["full"][0]["source"], "destination": part_2["full"][0]["destination"],
                "arrival": part_1["full"][0]["arrival"], "departure": part_1["full"][0]["departure"],
                "departureDate": part_1["full"][0]["departureDate"], "arrivalDate": part_2["full"][0]["arrivalDate"],
                "fare_1A": part_1["full"][0]["fare_1A"] + part_2["full"][0]["fare_1A"],
                "fare_2A": part_1["full"][0]["fare_2A"] + part_2["full"][0]["fare_2A"],
                "fare_3A": part_1["full"][0]["fare_3A"] + part_2["full"][0]["fare_3A"],
                "fare_3E": part_1["full"][0]["fare_3E"] + part_2["full"][0]["fare_3E"],
                "fare_FC": part_1["full"][0]["fare_FC"] + part_2["full"][0]["fare_FC"],
                "fare_CC": part_1["full"][0]["fare_CC"] + part_2["full"][0]["fare_CC"],
                "fare_SL": part_1["full"][0]["fare_SL"] + part_2["full"][0]["fare_SL"],
                "fare_2S": part_1["full"][0]["fare_2S"] + part_2["full"][0]["fare_2S"],
                "fare_GN": part_1["full"][0]["fare_GN"] + part_2["full"][0]["fare_GN"],
                "price": part_1["full"][0]["price"] + part_2["full"][0]["price"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"]="train" +str(trainCounter[0])+str(1)+str(1)

        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"]="train"+str(trainCounter[0])+str(1)+str(2)
        route["parts"].append(part)
        route["full"]=[]
        full = {"id": "train" + str(trainCounter[0])}
        route["full"].append(full)
    except ValueError:
        logger.error("Error while combining data for Train[%s] and Train[%s]", part_1["full"]["id"], part_2["full"]["id"])
        return route
    return route


class PlaceToStationCodesCache:
    """Class returs all stations corresponding to a city"""

    cityToStationsMap = {}

    def getStationsByCityName(self, cityname):

        """
        This method is used to get stations corrsponding to city given
        :param cityname: name of city for which all railway station are to be found
        :return: station for cityname
        """
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

    def gettrainroutes(self, sourcecity, destinationstationset,journeydate,trainCounter):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param destinationstationset: set of destination city's stations
        :param journeydate: journey date in 'dd-mm-yyyy' format
        :param trainCounter: global train counter used for id generation
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity,
                    destinationstationset)
        start = time.time()
        trains = models.getTrainsBetweenStation(sourcecity, destinationstationset, logger, journeydate)
        routedata = parseandreturnroute(trains, logger,journeydate,trainCounter)
        logger.info("Time taken [%s]", time.time() - start)
        return routedata

    def findTrainsBetweenStations(self, sourcecity, destinationstationset,journeyDate,trainCounter):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param destinationstationset: list of all available railway stations in destination city
        :param journeyDate: date of journey
        :return:
        """
        resultjsondata = {"train": []}
        routedata = self.gettrainroutes(sourcecity, destinationstationset,journeyDate,trainCounter)
        if len(routedata)>0:
            resultjsondata["train"].extend(routedata)
        return resultjsondata


    def combineData(self, sourcetobreakingstationjson, breakingtodestinationjson, traincounter):

        """
        To combine data from 2 parts into one
        :param sourcetobreakingstationjson: journey data from source to breaking city
        :param breakingtodestinationjson: journey data from breaking city to destination
        :return: combined data
        """
        resultjsondata = {"train": []}
        for possibleSrcToBreakRoute in sourcetobreakingstationjson["train"]:
            for possibleBreakToDestRoute in breakingtodestinationjson["train"]:
                if dateTimeUtility.checkIfApplicable(possibleSrcToBreakRoute["parts"][0]["arrival"],possibleSrcToBreakRoute["parts"][0]["arrivalDate"],possibleBreakToDestRoute["parts"][0]["departure"],possibleBreakToDestRoute["parts"][0]["departureDate"],3):
                    combinedjson = convertsPartsToFullJson(possibleSrcToBreakRoute, possibleBreakToDestRoute, traincounter)
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
            try:
                city = models.getBreakingCity(breakingstation.upper(), logger)
                if city:
                    breakingcitylist.append(city)
                    continue # continue to other list
            except:
                logger.error("Error getting city for breakingstation[%s]", breakingstation)
            possiblecities = breakingstation.split()  # split by space and search on indiviual words
            for possiblecity in possiblecities:
                try:
                    if possiblecity.upper() not in skipValues:
                        city = models.getBreakingCity(possiblecity.upper(), logger)
                        if city:
                            breakingcitylist.append(city)
                except:
                    logger.error("Error getting city for breakingstation[%s]", possiblecity.upper())
        return breakingcitylist

    def getRoutes(self, source, destination,journeyDate,isOnlyDirect=1):

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
        trainCounter =[0]
        directjson = self.findTrainsBetweenStations(source, destinationStationSet,journeyDate,trainCounter)
        if isOnlyDirect==1:
            return directjson
        breakingstationlist = googleapiparser.getPossibleBreakingPlacesForTrain(source, destination, logger,journeyDate)
        if len(breakingstationlist) > 0:
            breakingcitylist = self.convertBreakingStationToCity(self.getBreakingStation(breakingstationlist))
            if len(breakingcitylist) > 0:
                for breakingcity in breakingcitylist:
                    breakingcitystations = self.placetoStationCodesCache.getStationsByCityName(breakingcity)
                    sourceToBreakingStationJson = self.findTrainsBetweenStations(source, breakingcitystations,journeyDate,trainCounter)
                    busController= busapi.BusController()
                    sourceToBreakingStationBusJson=busController.getResults(source,breakingcity,journeyDate)

                    if len(sourceToBreakingStationJson["train"]) > 0 or len(sourceToBreakingStationBusJson["bus"])>0:
                        breakingToDestinationJson = self.findTrainsBetweenStations(breakingcity, destinationStations,journeyDate,trainCounter)
                        breakingToDestinationBusJson=busController.getResults(breakingcity,destination,journeyDate)
                        if len(breakingToDestinationJson["train"]) > 0 and len(sourceToBreakingStationJson["train"])>0:
                            combinedJson = self.combineData(sourceToBreakingStationJson, breakingToDestinationJson, trainCounter)
                            if len(combinedJson["train"])>0:
                                directjson["train"].extend(combinedJson["train"])
                        if len(sourceToBreakingStationBusJson["bus"])>0 and len(breakingToDestinationJson["train"]) >0:
                            combinedJson = self.combineBusAndTrainInit(sourceToBreakingStationBusJson, breakingToDestinationJson)
                            directjson["train"].extend(combinedJson["train"])
                        if len(sourceToBreakingStationJson["train"])>0 and  len(breakingToDestinationBusJson["bus"]) >0:
                            combinedJson = self.combineBusAndTrainEnd(sourceToBreakingStationJson, breakingToDestinationBusJson)
                            directjson["train"].extend(combinedJson["train"])

        return directjson
    

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

        #for breakingstations in breakingstationlist:
         #   if len(breakingstations) == 2:
          #       return breakingstations
        return []

    def combineBusAndTrainInit(self,sourceToBreakingBusJson,breakingToDestinationJson):

        combinedjson = {"train" : []}

        for j in range(len(breakingToDestinationJson["train"])):
            trainPart = breakingToDestinationJson["train"][j]["parts"][0]
            subParts = []
            for k in range(len(sourceToBreakingBusJson["bus"])):
                subPart = sourceToBreakingBusJson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subPart["arrival"],subPart["arrivalDate"],trainPart["departure"],trainPart["departureDate"],3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(subPart["arrival"],trainPart["departure"],subPart["arrivalDate"],trainPart["departureDate"])
                    subParts.append(subPart)
            if subParts:
                newPart = {"subParts": subParts, "mode": "bus",
                           "id": breakingToDestinationJson["train"][j]["full"][0]["id"] + str(0),
                           "destination": subParts[0]["destination"], "source": subParts[0]["source"],
                           "carrierName": subParts[0]["carrierName"]}
                breakingToDestinationJson["train"][j]["parts"].insert(0,newPart)

        combinedjson["train"] = [x for x in breakingToDestinationJson["train"] if len(x["parts"]) == 2]
        return combinedjson

    def combineBusAndTrainEnd(self,sourceToBreakingJson,breakingToDestinationBusJson):

        combinedjson = {"train" : []}

        for j in range(len(sourceToBreakingJson["train"])):
            trainPart = sourceToBreakingJson["train"][j]["parts"][0]
            subParts = []
            for k in range(len(breakingToDestinationBusJson["bus"])):
                subPart = breakingToDestinationBusJson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(trainPart["arrival"],trainPart["arrivalDate"],subPart["departure"],subPart["departureDate"],3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(trainPart["arrival"],subPart["departure"],trainPart["arrivalDate"],subPart["departureDate"])
                    subParts.append(subPart)
            if subParts:
                newPart = {"subParts": subParts, "mode": "bus",
                           "id": sourceToBreakingJson["train"][j]["full"][0]["id"] + str(2),
                           "destination": subParts[0]["destination"], "source": subParts[0]["source"],
                           "carrierName": subParts[0]["carrierName"]}
                sourceToBreakingJson["train"][j]["parts"].append(newPart)

        combinedjson["train"] = [x for x in sourceToBreakingJson["train"] if len(x["parts"]) == 2]
        return combinedjson
