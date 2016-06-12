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
import json
import urllib2
import distanceutil
import minMaxUtil
import miscUtility
import TravelPlanner.trainUtil

today = datetime.date.today().strftime("%Y-%m-%d")
skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])
bigcities = Set(['NEW DELHI', 'MUMBAI', 'BANGALORE', 'KOLKATA', 'HYDERABAD', 'CHENNAI', 'JAIPUR', 'AHMEDABAD', 'BHOPAL', 'LUCKNOW', 'PATNA', 'CHANDIGARH', 'PUNE', 'DELHI', 'AGRA', 'LUDHIANA', 'SURAT', 'KANPUR', 'NAGPUR', 'VISHAKHAPATNAM', 'INDORE', 'THANE','COIMBATORE', 'VADODARA', 'MADURAI', 'VARANASI', 'AMRITSAR', 'ALLAHABAD','KOTA', 'GUWAHATI', 'SOLAPUR', 'TRIVANDRUM'])

logger = loggerUtil.getLogger("TrainApi", logging.DEBUG)

def convertspartstofulljson(part_1, part_2, traincounter):
    """
    This method is used to combine train journey data from part_1 and part_2 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    traincounter[0] += 1
    try:
        duration = dateTimeUtility.gettotalduration(part_2["full"][0]["arrival"],part_1["full"][0]["departure"],part_2["full"][0]["arrivalDate"],part_1["full"][0]["departureDate"])
        price = part_1["full"][0]["price"] + part_2["full"][0]["price"]
        part = {"carrierName": "Train","duration": duration, "id": part_1["full"][0]["id"] + str(1), "mode": "train", "site": "IRCTC", "source": part_1["full"][0]["source"],
                "destination": part_2["full"][0]["destination"], "arrival": part_2["full"][0]["arrival"], "departure": part_1["full"][0]["departure"], "departureDate": part_1["full"][0]["departureDate"],
                "arrivalDate": part_2["full"][0]["arrivalDate"], "route" : part_1["full"][0]["source"] + ",train," + part_2["full"][0]["destination"],
                "prices": {"1A": part_1["full"][0]["prices"]["1A"] + part_2["full"][0]["prices"]["1A"],
                           "2A": part_1["full"][0]["prices"]["2A"] + part_2["full"][0]["prices"]["2A"],
                           "3A": part_1["full"][0]["prices"]["3A"] + part_2["full"][0]["prices"]["3A"],
                           "3E": part_1["full"][0]["prices"]["3E"] + part_2["full"][0]["prices"]["3E"],
                           "FC": part_1["full"][0]["prices"]["FC"] + part_2["full"][0]["prices"]["FC"],
                           "CC": part_1["full"][0]["prices"]["CC"] + part_2["full"][0]["prices"]["CC"],
                           "SL": part_1["full"][0]["prices"]["SL"] + part_2["full"][0]["prices"]["SL"],
                           "2S": part_1["full"][0]["prices"]["2S"] + part_2["full"][0]["prices"]["2S"],
                           "GN": part_1["full"][0]["prices"]["GN"] + part_2["full"][0]["prices"]["GN"]},
                "price": price, "priceClass": part_1["full"][0]["priceClass"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"] = part["id"] + str(1)

        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(2)
        route["parts"].append(part)
        route["full"] = []
        full = {"id": part_1["full"][0]["id"], "minPrice": price, "maxPrice": price, "minDuration": duration, "maxDuration": duration, "minArrival": part_2["full"][0]["arrival"],"maxArrival": part_2["full"][0]["arrival"],
                "minDeparture": part_1["full"][0]["departure"], "maxDeparture": part_1["full"][0]["departure"], "route": part["route"], "duration":duration, "price":price}
        route["full"].append(full)
    except Exception as e:
        logger.error("Error while combining data for Train[%s] and Train[%s], reason [%s]", part_1["full"]["id"], part_2["full"]["id"], e.message)

    return route


class PlaceToStationCodesCache:
    """Class returs all stations corresponding to a city"""

    def getstationsbycityname(self, cityname):

        """
        This method is used to get stations corrsponding to city given
        :param cityname: name of city for which all railway station are to be found
        :return: station for cityname
        """
        if cityname in TravelPlanner.trainUtil.citytostationcodesmap:
            return TravelPlanner.trainUtil.citytostationcodesmap[cityname]
        else:
            stationlist = models.getstationcodesbycityname(cityname, logger)
            if stationlist:
                TravelPlanner.trainUtil.citytostationcodesmap[cityname] = stationlist
            return stationlist


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetostationcodescache = PlaceToStationCodesCache()

    def gettrainroutes(self, sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass='3A', numberOfAdults=1, nextday=False):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param destinationstationset: set of destination city's stations
        :param journeydate: journey date in 'dd-mm-yyyy' format
        :param trainid: train route id
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity, destinationstationset)
        start = time.time()
        traindata = models.gettrainsbetweenstation(sourcecity, destinationstationset, logger, journeydate, destinationcity, trainid, priceclass, numberOfAdults, nextday)
        logger.info("Time taken [%s]", time.time() - start)
        return traindata

    def findtrainsbetweenstations(self, sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, nextday=False):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param destinationstationset: list of all available railway stations in destination city
        :param journeydate: date of journey
        :param trainid: id of the train route
        :param destinationcity: destination city of the journey
        :param priceclass: class preferred by user
        :param numberofadults: no. of adults travelling
        :param nextday: wish to see next day trains from breaking stations
        :return: trains
        """
        resultjsondata = {"train": []}
        try:
            routedata = self.gettrainroutes(sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, nextday)
        except Exception as e:
            logger.error("Error while fetching train data from db for source [%s] and destination [%s], reason [%s]", sourcecity, destinationcity, e.message)
            return resultjsondata
        if len(routedata) > 0:
            resultjsondata["train"].extend(routedata)
        return resultjsondata

    def combinedata(self, sourcetobreakingstationjson, breakingtodestinationjson):

        """
        To combine data from 2 parts into one
        :param sourcetobreakingstationjson: journey data from source to breaking city
        :param breakingtodestinationjson: journey data from breaking city to destination
        :return: combined data
        """
        resultjsondata = {"train": []}
        for possiblesrctobreakroute in sourcetobreakingstationjson["train"]:
            for possiblebreaktodestroute in breakingtodestinationjson["train"]:
                if dateTimeUtility.checkIfApplicable(possiblesrctobreakroute["parts"][0]["arrival"],
                                                     possiblesrctobreakroute["parts"][0]["arrivalDate"],
                                                     possiblebreaktodestroute["parts"][0]["departure"],
                                                     possiblebreaktodestroute["parts"][0]["departureDate"], 3):
                    combinedjson = convertspartstofulljson(possiblesrctobreakroute, possiblebreaktodestroute)
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
                city = models.getbreakingcity(breakingstation.upper(), logger)
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
                        city = models.getbreakingcity(possiblecity, logger)
                        if city:
                            breakingcitylist.append(city)
                except:
                    logger.error("Error getting city for breakingstation[%s]", possiblecity.upper())
        return breakingcitylist

    def getroutes(self, source, destination, journeydate, isonlydirect=1, priceclass='3A', numberofadults=1):

        """
        This method is used to fetch all possible route between source & destination stations via train and train/bus combined.

        :param source: source station of the journey
        :param destination: destination station of the journey
        :param journeydate: date of the journey
        :param isonlydirect: if only direct trains are required
        :param priceclass: default price class selected by user
        :param numberofadults: no. of adult passenger
        :return: all possible routes from source to destination via direct train or combination of train-bus
        """
        logger.debug("[START]-Get Results From TrainApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", source,destination, journeydate)
        source = str(source).upper()
        destination = str(destination).upper()
        destinationstationset = self.placetostationcodescache.getstationsbycityname(TravelPlanner.trainUtil.gettraincity(destination))

        if len(destinationstationset) != 0:
            directjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(source), destinationstationset, journeydate, "train0",TravelPlanner.trainUtil.gettraincity(destination),priceclass,numberofadults)
        else:
            directjson = {"train": []}
        if isonlydirect == 1 or len(directjson["train"]) >= 7:  # return in case we have more than 8 direct trains
            return directjson
        logger.debug("Calling google api parser for Source[%s] to Destination[%s] on journeyDate[%s]", source, destination,journeydate)
        breakingcitieslist = googleapiparser.getpossiblebreakingplacesfortrain(source, destination, logger, journeydate, TravelPlanner.trainUtil.googleplacesexecutor)
        logger.debug("Call To google api parser successful for Source[%s] and Destination[%s]", source, destination)

        breakingcityset = Set()
        if len(breakingcitieslist) > 0:
            breakingcityset = (self.getbreakingcityset(breakingcitieslist))
            logger.info("Breaking cities between source [%s] to destination [%s] are [%s]", source, destination, breakingcityset)
            if len(breakingcityset) > 0:
                for breakingcity in breakingcityset:
                    if breakingcity != TravelPlanner.trainUtil.gettraincity(source) and breakingcity != TravelPlanner.trainUtil.gettraincity(destination):
                        logger.info("Getting train journey from source [%s] to destination [%s] via breaking city [%s]", source, destination, breakingcity)
                        TravelPlanner.trainUtil.trainexecutor.submit(self.fetchtraindatafrombreakingcities(breakingcity, destination, destinationstationset, journeydate, source, directjson,priceclass,numberofadults))

        if len(breakingcitieslist) == 0 or len(breakingcityset) == 0:
            try:
                logger.debug("Getting nearest railway station to source [%s]", source)
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ source.title()
                url = url.replace(' ', '%20')
                response = urllib2.urlopen(url)
                sourcelatlong = json.loads(response.read())
                response.close()
                sourcelat = sourcelatlong["results"][0]["geometry"]["location"]["lat"]
                sourcelong = sourcelatlong["results"][0]["geometry"]["location"]["lng"]
                logger.info("Co-ordinates for source [%s] are Lat[%s]-Long[%s]", source, sourcelat, sourcelong)
                breakingcity = distanceutil.findnearestrailwaystation(sourcelat, sourcelong, TravelPlanner.trainUtil.gettraincity(source)).upper()
                if breakingcity == source or breakingcity in source or source in breakingcity:
                    logger.warning("Breaking city is same as source [%s], calculating breaking city from destination [%s]'s co-ordinates", source, destination)
                else:
                    breakingcityset.add(breakingcity)
                logger.debug("Getting nearest railway station to destination [%s]", destination)
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ destination.title()
                url = url.replace(' ', '%20')
                response = urllib2.urlopen(url)
                destlatlong = json.loads(response.read())
                response.close()
                destlat = destlatlong["results"][0]["geometry"]["location"]["lat"]
                destlong = destlatlong["results"][0]["geometry"]["location"]["lng"]
                logger.info("Co-ordinates for destination [%s] are Lat[%s]-Long[%s]", destination, destlat, destlong)
                breakingcity = distanceutil.findnearestrailwaystation(destlat, destlong, TravelPlanner.trainUtil.gettraincity(destination)).upper()
                if breakingcity == destination or breakingcity in destination or destination in breakingcity:
                    logger.warning("No breaking journey city possible between source [%s] and destination [%s]", source, destination)
                    return directjson
                else:
                    breakingcityset.add(breakingcity)

                for breakingcity in breakingcityset:
                    logger.info("Getting train journey from source [%s] to destination [%s] via breaking city [%s]", source, destination, breakingcity)
                    TravelPlanner.trainUtil.trainexecutor.submit(self.fetchtraindatafrombreakingcities(breakingcity.upper(), destination, destinationstationset, journeydate,source, directjson,priceclass,numberofadults))
            except Exception as e:
                logger.error("Error in fetching longitude and latitude for [%s], reason [%s]", source, e.message)

        logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", source,destination)

        return directjson


    def fetchtraindatafrombreakingcities(self, breakingcity, destination, destinationstationset, journeydate, source, directjson, priceclass, numberffadults):
        """

        :param breakingcity: city from where journey needs to be broken
        :param destination: final destination
        :param destinationstationset: set of all railway stations of destination city
        :param journeydate: date of journey
        :param source: source station of journey
        :param traincounter: global train counter used for route ID generation
        :param directjson: final result
        """
        breakingcitystationset = self.placetostationcodescache.getstationsbycityname(breakingcity)
        if (len(breakingcitystationset)) != 0:
            # only call for train if breaking city has train stations
            sourcetobreakingstationjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(source), breakingcitystationset, journeydate, "train1", TravelPlanner.trainUtil.gettraincity(breakingcity),priceclass,numberffadults)
        else:
            logger.warning("Breaking city [%s] has no train stations", breakingcity)
            sourcetobreakingstationjson = {"train": []}

        buscontroller = busapi.BusController()
        sourcetobreakingstationbusjson = buscontroller.getResults(source, breakingcity, journeydate,numberffadults)

        if len(sourcetobreakingstationjson["train"]) > 0 or len(sourcetobreakingstationbusjson["bus"]) > 0:
            nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')

            if (len(destinationstationset)) != 0:
                # only call for train if breaking city has train stations
                breakingtodestinationjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(breakingcity), destinationstationset,journeydate, "train2", TravelPlanner.trainUtil.gettraincity(destination),priceclass,numberffadults, nextday=True)
            else:
                breakingtodestinationjson = {"train": []}

            breakingtodestinationbusjson = buscontroller.getResults(breakingcity,destination, journeydate,numberffadults)
            breakingtodestinationbusjson["bus"].extend(buscontroller.getResults(breakingcity, destination, nextday,numberffadults)["bus"])

            if len(breakingtodestinationjson["train"]) > 0 and len(sourcetobreakingstationjson["train"]) > 0:
                # merge train data from source - breakingcity - destination
                combinedjson = self.combinedata(sourcetobreakingstationjson, breakingtodestinationjson)
                if len(combinedjson["train"]) > 0:
                    directjson["train"].extend(combinedjson["train"])

            if len(sourcetobreakingstationbusjson["bus"]) > 0 and len(breakingtodestinationjson["train"]) > 0:
                # merge bus data (initial) and train data from source -(bus) - breakingcity -(train) - destination
                combinedjson = self.combinebusandtraininit(sourcetobreakingstationbusjson,breakingtodestinationjson)
                directjson["train"].extend(combinedjson["train"])

            if len(sourcetobreakingstationjson["train"]) > 0 and len(breakingtodestinationbusjson["bus"]) > 0:
                # merge bus data (end) and train data from source -(train) - breakingcity -(bus) - destination
                combinedjson = self.combinebusandtrainend(sourcetobreakingstationjson,breakingtodestinationbusjson)
                directjson["train"].extend(combinedjson["train"])

    def getbreakingcityset(self, breakingcitieslist):

        """
        To get set of all breaking cities
        :param breakingcitieslist: list of breaking city sets
        :return: breaking city sets
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
            else:
                for breakingcity in breakingcities:
                    if breakingcity.upper() in bigcities:
                        breakingcityset.add(breakingcity)
        return breakingcityset

    def combinebusandtraininit(self, sourcetobreakingbusjson, breakingtodestinationjson):

        """
        To combine bus an train data.
        :param sourcetobreakingbusjson: bus data from source to breaking staion
        :param breakingtodestinationjson: train data from breaking to destination
        :return: combined data
        """

        combinedjson = {"train": []}

        for j in range(len(breakingtodestinationjson["train"])):
            trainpart = breakingtodestinationjson["train"][j]["parts"][0]
            subparts = []
            for k in range(len(sourcetobreakingbusjson["bus"])):
                subpart = sourcetobreakingbusjson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subpart["arrival"], subpart["arrivalDate"], trainpart["departure"],trainpart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], trainpart["departure"],subpart["arrivalDate"],trainpart["departureDate"])
                    subparts.append(subpart)

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortOnWaitingTime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": "bus","id": breakingtodestinationjson["train"][j]["full"][0]["id"] + str(0),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                breakingtodestinationjson["train"][j]["parts"].insert(0, newpart)
                breakingtodestinationjson["train"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",train," + breakingtodestinationjson["train"][j]["full"][0]["destination"]
                breakingtodestinationjson["train"][j]["full"][0]["price"] = int(breakingtodestinationjson["train"][j]["full"][0]["price"]) + int(minmax["minPrice"])
                breakingtodestinationjson["train"][j]["full"][0]["minPrice"] = int(breakingtodestinationjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                breakingtodestinationjson["train"][j]["full"][0]["maxPrice"] = int(breakingtodestinationjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                breakingtodestinationjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(breakingtodestinationjson["train"][j]["full"][0]["duration"], minmax["minDuration"])
                breakingtodestinationjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(breakingtodestinationjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
                breakingtodestinationjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(breakingtodestinationjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                breakingtodestinationjson["train"][j]["full"][0]["minDeparture"] = minmax["minDep"]
                breakingtodestinationjson["train"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]

        combinedjson["train"] = [x for x in breakingtodestinationjson["train"] if len(x["parts"]) == 2]
        return combinedjson

    def combinebusandtrainend(self, sourcetobreakingjson, breakingtodestinationbusjson):

        """
        To combine train and bus data
        :param sourcetobreakingjson: train data from source to breaking station
        :param breakingtodestinationbusjson: bus data from breaking to destination
        :return: combined train and bus data
        """
        combinedjson = {"train": []}

        for j in range(len(sourcetobreakingjson["train"])):
            trainpart = sourcetobreakingjson["train"][j]["parts"][0]
            subparts = []
            for k in range(len(breakingtodestinationbusjson["bus"])):
                subpart = breakingtodestinationbusjson["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(trainpart["arrival"], trainpart["arrivalDate"],subpart["departure"], subpart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(trainpart["arrival"], subpart["departure"],trainpart["arrivalDate"],subpart["departureDate"])
                    subparts.append(subpart)

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortOnWaitingTime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": "bus", "id": sourcetobreakingjson["train"][j]["full"][0]["id"] + str(2),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
                sourcetobreakingjson["train"][j]["parts"].append(newpart)
                sourcetobreakingjson["train"][j]["full"][0]["route"] = sourcetobreakingjson["train"][j]["full"][0]["source"] + ",train," + newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                sourcetobreakingjson["train"][j]["full"][0]["price"] = int(sourcetobreakingjson["train"][j]["full"][0]["price"]) + int(minmax["minPrice"])
                sourcetobreakingjson["train"][j]["full"][0]["minPrice"] = int(sourcetobreakingjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                sourcetobreakingjson["train"][j]["full"][0]["maxPrice"] = int(sourcetobreakingjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                sourcetobreakingjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(sourcetobreakingjson["train"][j]["full"][0]["duration"], minmax["minDuration"])
                sourcetobreakingjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(sourcetobreakingjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
                sourcetobreakingjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(sourcetobreakingjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                sourcetobreakingjson["train"][j]["full"][0]["minArrival"] = minmax["minArr"]
                sourcetobreakingjson["train"][j]["full"][0]["maxArrival"] = minmax["maxArr"]

        combinedjson["train"] = [x for x in sourcetobreakingjson["train"] if len(x["parts"]) == 2]
        return combinedjson

