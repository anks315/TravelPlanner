__author__ = 'ankur'

import time
import logging
import models
import googleapiparser
from sets import Set
import dateTimeUtility
import busapi
import copy
import datetime
import loggerUtil
from datetime import timedelta

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])

logger = loggerUtil.getLogger("TrainApi", logging.DEBUG)

trainNumberstoDurationMap = {}


def parseandreturnroute(trainroutes, logger, journeyDate, trainCounter):
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
        trainCounter[0] += 1
        try:
            full = {"carrierName": trainRoute.trainName, "duration": trainRoute.duration,
                    "id": "train" + str(trainCounter[0]), "mode": "train", "site": "IRCTC",
                    "source": trainRoute.srcStation,
                    "destination": trainRoute.destStation, "arrival": trainRoute.destArrivalTime,
                    "sourceStation": trainRoute.srcStationCode, "destinationStation": trainRoute.destStationCode,
                    "arrivalDate": dateTimeUtility.calculateArrivalTimeAndDate(journeyDate, trainRoute.srcDepartureTime,
                                                                               trainRoute.duration)["arrivalDate"],
                    "departure": trainRoute.srcDepartureTime, "departureDate": journeyDate,
                    "prices": trainRoute.prices, "price": trainRoute.price, "priceClass": trainRoute.priceClass}
            part = copy.deepcopy(full)
            part["id"] = "train" + str(trainCounter[0]) + str(1)
            part["subParts"] = []
            part["subParts"].append(copy.deepcopy(full))
            part["subParts"][0]["id"] = "train" + str(trainCounter[0]) + str(1) + str(1)

            route["full"].append(full)
            route["parts"].append(part)
            if hasprice(route):
                routes.append(route)
        except ValueError as e:
            logger.error("Error while route map with full & parts journey, reason [%s]", e.message)
            return routes
    return routes


def convertsPartsToFullJson(part_1, part_2, trainCounter):
    """
    This method is used to combine train journey data from part_1 and part_2 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    trainCounter[0] += 1
    try:
        part = {"carrierName": "Train",
                "duration": dateTimeUtility.gettotalduration(part_2["full"][0]["arrival"], part_1["full"][0]["departure"],
                                                           part_2["full"][0]["arrivalDate"],
                                                           part_1["full"][0]["departureDate"]),
                "id": "train" + str(trainCounter[0]) + str(1), "mode": "train",
                "site": "IRCTC", "source": part_1["full"][0]["source"], "destination": part_2["full"][0]["destination"],
                "arrival": part_2["full"][0]["arrival"], "departure": part_1["full"][0]["departure"],
                "departureDate": part_1["full"][0]["departureDate"], "arrivalDate": part_2["full"][0]["arrivalDate"],
                "prices": {"1A": part_1["full"][0]["prices"]["1A"] + part_2["full"][0]["prices"]["1A"],
                           "2A": part_1["full"][0]["prices"]["2A"] + part_2["full"][0]["prices"]["2A"],
                           "3A": part_1["full"][0]["prices"]["3A"] + part_2["full"][0]["prices"]["3A"],
                           "3E": part_1["full"][0]["prices"]["3E"] + part_2["full"][0]["prices"]["3E"],
                           "FC": part_1["full"][0]["prices"]["FC"] + part_2["full"][0]["prices"]["FC"],
                           "CC": part_1["full"][0]["prices"]["CC"] + part_2["full"][0]["prices"]["CC"],
                           "SL": part_1["full"][0]["prices"]["SL"] + part_2["full"][0]["prices"]["SL"],
                           "2S": part_1["full"][0]["prices"]["2S"] + part_2["full"][0]["prices"]["2S"],
                           "GN": part_1["full"][0]["prices"]["GN"] + part_2["full"][0]["prices"]["GN"]},
                "price": part_1["full"][0]["price"] + part_2["full"][0]["price"],
                "priceClass": part_1["full"][0]["priceClass"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"] = "train" + str(trainCounter[0]) + str(1) + str(1)

        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = "train" + str(trainCounter[0]) + str(1) + str(2)
        route["parts"].append(part)
        route["full"] = []
        full = {"id": "train" + str(trainCounter[0])}
        route["full"].append(full)
    except ValueError as e:
        logger.error("Error while combining data for Train[%s] and Train[%s], reason [%s]", part_1["full"]["id"],
                     part_2["full"]["id"], e.message)
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
            return Set(stationList)


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetoStationCodesCache = PlaceToStationCodesCache()

    def gettrainroutes(self, sourcecity, destinationstationset, journeydate, trainCounter, destinationcity):

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
        trains = models.getTrainsBetweenStation(sourcecity, destinationstationset, logger, journeydate, destinationcity)
        routedata = parseandreturnroute(trains, logger, journeydate, trainCounter)
        logger.info("Time taken [%s]", time.time() - start)
        return routedata

    def findTrainsBetweenStations(self, sourcecity, destinationstationset, journeyDate, trainCounter, destinationcity):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param destinationstationset: list of all available railway stations in destination city
        :param journeyDate: date of journey
        :return:
        """
        resultjsondata = {"train": []}
        routedata = self.gettrainroutes(sourcecity, destinationstationset, journeyDate, trainCounter, destinationcity)
        if len(routedata) > 0:
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
                if dateTimeUtility.checkIfApplicable(possibleSrcToBreakRoute["parts"][0]["arrival"],
                                                     possibleSrcToBreakRoute["parts"][0]["arrivalDate"],
                                                     possibleBreakToDestRoute["parts"][0]["departure"],
                                                     possibleBreakToDestRoute["parts"][0]["departureDate"], 3):
                    combinedjson = convertsPartsToFullJson(possibleSrcToBreakRoute, possibleBreakToDestRoute,
                                                           traincounter)
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
                    continue  # continue to other list
            except:
                logger.error("Error getting city for breakingstation[%s]", breakingstation)
            possiblecities = breakingstation.split()  # split by space and search on indiviual words
            for possiblecity in possiblecities:
                possiblecity = possiblecity.upper()
                try:
                    if possiblecity not in skipValues:
                        city = models.getBreakingCity(possiblecity, logger)
                        if city:
                            breakingcitylist.append(city)
                except:
                    logger.error("Error getting city for breakingstation[%s]", possiblecity.upper())
        return breakingcitylist

    def getRoutes(self, source, destination, journeydate, isOnlyDirect=1):

        """
        This method is used to fetch all possible route between source & destination stations via train and train/bus combined.

        :param source: source station of the journey
        :param destination: destination station of the journey
        :param dateofjourney: date of the journey
        :return: all possible routes from source to destination via direct train or combination of train-bus
        """
        logger.debug("[START]-Get Results From TrainApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", source,
                     destination, journeydate)
        source = str(source).upper()
        destination = str(destination).upper()

        destinationstationset = self.placetoStationCodesCache.getStationsByCityName(destination)
        traincounter = [0]
        directjson = self.findTrainsBetweenStations(source, destinationstationset, journeydate, traincounter,
                                                    destination)
        if isOnlyDirect == 1 or len(directjson["train"]) > 8:  # return in case we have more than 8 direct trains
            return directjson
        logger.debug("Calling google api parser for Source[%s] an Destination[%s],journeyDate", source, destination,
                     journeydate)
        breakingcitieslist = googleapiparser.getPossibleBreakingPlacesForTrain(source, destination, logger, journeydate)
        logger.debug("Call To google api parser successful for Source[%s] and Destination[%s]", source, destination)

        if len(breakingcitieslist) > 0:
            breakingcityset = (self.getBreakingCitySet(breakingcitieslist))
            if len(breakingcityset) > 0:
                for breakingcity in breakingcityset:
                    breakingcitystationset = self.placetoStationCodesCache.getStationsByCityName(breakingcity)
                    sourceToBreakingStationJson = self.findTrainsBetweenStations(source, breakingcitystationset,
                                                                                 journeydate, traincounter,
                                                                                 breakingcity)
                    busController = busapi.BusController()
                    sourceToBreakingStationBusJson = busController.getResults(source.title(), breakingcity.title(),
                                                                              journeydate)

                    if len(sourceToBreakingStationJson["train"]) > 0 or len(sourceToBreakingStationBusJson["bus"]) > 0:
                        breakingToDestinationJson = self.findTrainsBetweenStations(breakingcity, destinationstationset,
                                                                                   journeydate, traincounter,
                                                                                   destination)
                        nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime(
                            '%d-%m-%Y')
                        breakingToDestinationJson["train"].extend(
                            self.findTrainsBetweenStations(breakingcity, destinationstationset, nextday, traincounter,
                                                           destination)["train"])
                        breakingToDestinationBusJson = busController.getResults(breakingcity.title(),
                                                                                destination.title(), journeydate)
                        breakingToDestinationBusJson["bus"].extend(
                            busController.getResults(breakingcity.title(), destination.title(), nextday)["bus"])
                        if len(breakingToDestinationJson["train"]) > 0 and len(
                                sourceToBreakingStationJson["train"]) > 0:
                            combinedjson = self.combineData(sourceToBreakingStationJson, breakingToDestinationJson,
                                                            traincounter)
                            if len(combinedjson["train"]) > 0:
                                directjson["train"].extend(combinedjson["train"])
                        if len(sourceToBreakingStationBusJson["bus"]) > 0 and len(
                                breakingToDestinationJson["train"]) > 0:
                            combinedjson = self.combineBusAndTrainInit(sourceToBreakingStationBusJson,
                                                                       breakingToDestinationJson)
                            directjson["train"].extend(combinedjson["train"])
                        if len(sourceToBreakingStationJson["train"]) > 0 and len(
                                breakingToDestinationBusJson["bus"]) > 0:
                            combinedjson = self.combineBusAndTrainEnd(sourceToBreakingStationJson,
                                                                      breakingToDestinationBusJson)
                            directjson["train"].extend(combinedjson["train"])

        logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", source,
                     destination)

        return directjson

    def getBreakingCitySet(self, breakingcitieslist):

        """

        :param breakingcitieslist:
        :return:
        """

        breakingcityset = Set()

        """
        this method is used to get relevant breaking cities from all the breaking cities list.
        First prefernece is given to list having only one element then so on
        :param breakingcitieslist: list of breaking cities
        :return: breaking city set
        """
        for breakingcities in breakingcitieslist:
            if len(breakingcities) == 1:
                breakingcityset.add(breakingcities.pop())

                # for breakingcities in breakingstationlist:
                #   if len(breakingcities) == 2:
                #       return breakingcities
        return breakingcityset

    def combineBusAndTrainInit(self, sourceToBreakingBusJson, breakingToDestinationJson):

        combinedjson = {"train": []}

        for j in range(len(breakingToDestinationJson["train"])):
            trainPart = breakingToDestinationJson["train"][j]["parts"][0]
            subParts = []
            for k in range(len(sourceToBreakingBusJson["bus"])):
                subPart = sourceToBreakingBusJson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subPart["arrival"], subPart["arrivalDate"], trainPart["departure"],
                                                     trainPart["departureDate"], 3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(subPart["arrival"], trainPart["departure"],
                                                                            subPart["arrivalDate"],
                                                                            trainPart["departureDate"])
                    subParts.append(subPart)
            if subParts:
                newPart = {"subParts": subParts, "mode": "bus",
                           "id": breakingToDestinationJson["train"][j]["full"][0]["id"] + str(0),
                           "destination": subParts[0]["destination"], "source": subParts[0]["source"],
                           "carrierName": subParts[0]["carrierName"]}
                breakingToDestinationJson["train"][j]["parts"].insert(0, newPart)

        combinedjson["train"] = [x for x in breakingToDestinationJson["train"] if len(x["parts"]) == 2]
        return combinedjson

    def combineBusAndTrainEnd(self, sourceToBreakingJson, breakingToDestinationBusJson):

        combinedjson = {"train": []}

        for j in range(len(sourceToBreakingJson["train"])):
            trainPart = sourceToBreakingJson["train"][j]["parts"][0]
            subParts = []
            for k in range(len(breakingToDestinationBusJson["bus"])):
                subPart = breakingToDestinationBusJson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(trainPart["arrival"], trainPart["arrivalDate"],
                                                     subPart["departure"], subPart["departureDate"], 3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(trainPart["arrival"], subPart["departure"],
                                                                            trainPart["arrivalDate"],
                                                                            subPart["departureDate"])
                    subParts.append(subPart)
            if subParts:
                newPart = {"subParts": subParts, "mode": "bus",
                           "id": sourceToBreakingJson["train"][j]["full"][0]["id"] + str(2),
                           "destination": subParts[0]["destination"], "source": subParts[0]["source"],
                           "carrierName": subParts[0]["carrierName"]}
                sourceToBreakingJson["train"][j]["parts"].append(newPart)

        combinedjson["train"] = [x for x in sourceToBreakingJson["train"] if len(x["parts"]) == 2]
        return combinedjson


def hasprice(route):
    """
    Check whether any price exists for the train or not. Ignore train if no price data is present
    :param route: train route
    :return: True if price exists else False
    """

    prices = route["full"][0]["prices"]
    trainname = route["full"][0]["carrierName"]

    if prices["1A"] == 0 and prices["2A"] == 0 and prices["3A"] == 0 and prices["3E"] == 0 and prices["FC"] == 0 and \
                    prices["CC"] == 0 and prices["SL"] == 0 and prices["2S"] == 0 and prices["GN"] == 0:
        logger.warning("Ignoring train [%s] since all prices are 0", trainname)
        return False
    return True
