__author__ = 'ankur'

import sets
from datetime import timedelta
import json, copy, time, datetime, urllib2
import distanceutil, busapi, loggerUtil, dateTimeUtility, googleapiparser, models, minMaxUtil, miscUtility, TravelPlanner.trainUtil
from entity import BreakingStations

today = datetime.date.today().strftime("%Y-%m-%d")
skipvalues = sets.Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])
bigcities = sets.Set(['NEW DELHI', 'MUMBAI', 'BANGALORE', 'KOLKATA', 'HYDERABAD', 'CHENNAI', 'JAIPUR', 'AHMEDABAD', 'BHOPAL', 'LUCKNOW', 'PATNA', 'CHANDIGARH', 'PUNE', 'DELHI', 'AGRA', 'LUDHIANA', 'SURAT', 'KANPUR', 'NAGPUR', 'VISHAKHAPATNAM', 'INDORE', 'THANE','COIMBATORE', 'VADODARA', 'MADURAI', 'VARANASI', 'AMRITSAR', 'ALLAHABAD','KOTA', 'GUWAHATI', 'SOLAPUR', 'TRIVANDRUM'])

logger = loggerUtil.getlogger("TrainApiNeo4j")


def convertspartstofulljson(part_1, part_2):
    """
    This method is used to combine train journey data from part_1 and part_2 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    try:
        duration = dateTimeUtility.gettotalduration(part_2["full"][0]["arrival"],part_1["full"][0]["departure"],part_2["full"][0]["arrivalDate"],part_1["full"][0]["departureDate"])
        price = part_1["full"][0]["price"] + part_2["full"][0]["price"]
        part = {"carrierName": "Train","duration": duration, "id": part_1["full"][0]["id"] + "_" +part_2["full"][0]["id"] + str(1), "mode": "train", "site": "IRCTC", "source": part_1["full"][0]["source"],
                "destination": part_2["full"][0]["destination"], "arrival": part_2["full"][0]["arrival"], "departure": part_1["full"][0]["departure"], "departureDate": part_1["full"][0]["departureDate"],
                "arrivalDate": part_2["full"][0]["arrivalDate"], "route" : part_1["full"][0]["source"] + ",train," + part_2["full"][0]["source"] + ",train," + part_2["full"][0]["destination"],
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
        full = {"id": part_1["full"][0]["id"]+ "_" +part_2["full"][0]["id"], "minPrice": price, "maxPrice": price, "minDuration": duration, "maxDuration": duration, "minArrival": part_2["full"][0]["arrival"],"maxArrival": part_2["full"][0]["arrival"],
                "minDeparture": part_1["full"][0]["departure"], "maxDeparture": part_1["full"][0]["departure"], "route": part["route"], "duration": duration, "price": price, "destination": part["destination"], "source": part["arrival"],
                "departureDate": part["departureDate"], "departureDay": models.getdayabbrevationfromdatestr(part["departureDate"], 0), "arrivalDate": part["arrivalDate"], "arrivalDay" : models.getdayabbrevationfromdatestr(part["arrivalDate"], 0),
                "departure": part["departure"], "arrival": part["arrival"]}

        route["full"].append(full)
    except Exception as e:
        logger.error("Error while combining data for Train[%s] and Train[%s], reason [%s]", part_1["full"]["id"], part_2["full"]["id"], e.message)

    return route


def convertmultipleparttofulljourney(part_1, part_2, part_3):
    """
    This method is used to combine train journey data from part_1, part_2 and part_3 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :param part_3: part 3 of the journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    try:
        duration = dateTimeUtility.gettotalduration(part_3["full"][0]["arrival"],part_1["full"][0]["departure"],part_3["full"][0]["arrivalDate"],part_1["full"][0]["departureDate"])
        price = part_1["full"][0]["price"] + part_2["full"][0]["price"] + part_3["full"][0]["price"]
        part = {"carrierName": "Train","duration": duration, "id": part_1["full"][0]["id"] + "_" + part_2["full"][0]["id"] + part_3["full"][0]["id"] + str(1), "mode": "train", "site": "IRCTC", "source": part_1["full"][0]["source"],
                "destination": part_3["full"][0]["destination"], "arrival": part_3["full"][0]["arrival"], "departure": part_1["full"][0]["departure"], "departureDate": part_1["full"][0]["departureDate"],
                "arrivalDate": part_3["full"][0]["arrivalDate"], "route" : part_1["full"][0]["source"] + ",train," + part_2["full"][0]["source"] + ",train," + part_2["full"][0]["destination"] + ",train," + part_3["full"][0]["destination"],
                "prices": {"1A": part_1["full"][0]["prices"]["1A"] + part_2["full"][0]["prices"]["1A"] + part_3["full"][0]["prices"]["1A"],
                           "2A": part_1["full"][0]["prices"]["2A"] + part_2["full"][0]["prices"]["2A"] + part_3["full"][0]["prices"]["2A"],
                           "3A": part_1["full"][0]["prices"]["3A"] + part_2["full"][0]["prices"]["3A"] + part_3["full"][0]["prices"]["3A"],
                           "3E": part_1["full"][0]["prices"]["3E"] + part_2["full"][0]["prices"]["3E"] + part_3["full"][0]["prices"]["3E"],
                           "FC": part_1["full"][0]["prices"]["FC"] + part_2["full"][0]["prices"]["FC"] + part_3["full"][0]["prices"]["FC"],
                           "CC": part_1["full"][0]["prices"]["CC"] + part_2["full"][0]["prices"]["CC"] + part_3["full"][0]["prices"]["CC"],
                           "SL": part_1["full"][0]["prices"]["SL"] + part_2["full"][0]["prices"]["SL"] + part_3["full"][0]["prices"]["SL"],
                           "2S": part_1["full"][0]["prices"]["2S"] + part_2["full"][0]["prices"]["2S"] + part_3["full"][0]["prices"]["2S"],
                           "GN": part_1["full"][0]["prices"]["GN"] + part_2["full"][0]["prices"]["GN"] + part_3["full"][0]["prices"]["GN"]},
                "price": price, "priceClass": part_1["full"][0]["priceClass"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"] = part["id"] + str(1)

        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(2)

        part["subParts"].append(copy.deepcopy(part_3["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(3)

        route["parts"].append(part)
        route["full"] = []
        full = {"id": part_1["full"][0]["id"] + "_" + part_2["full"][0]["id"] + "_" + part_3["full"][0]["id"], "minPrice": price, "maxPrice": price, "minDuration": duration, "maxDuration": duration, "minArrival": part_3["full"][0]["arrival"],"maxArrival": part_3["full"][0]["arrival"],
                "minDeparture": part_1["full"][0]["departure"], "maxDeparture": part_1["full"][0]["departure"], "route": part["route"], "duration": duration, "price": price, "destination": part["destination"], "source": part["arrival"],
                "departureDate": part["departureDate"], "departureDay": models.getdayabbrevationfromdatestr(part["departureDate"], 0), "arrivalDate": part["arrivalDate"], "arrivalDay" : models.getdayabbrevationfromdatestr(part["arrivalDate"], 0),
                "departure": part["departure"], "arrival": part["arrival"]}

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
                logger.info("Added city [%s] in citytostationcodesmap with [%s] stations", cityname, stationlist)
                TravelPlanner.trainUtil.citytostationcodesmap[cityname] = stationlist
            return stationlist


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetostationcodescache = PlaceToStationCodesCache()

    def gettrainroutes(self, sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass='3A', numberofadults=1, nextday=False, directtrainset=sets.Set()):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param destinationstationset: set of destination city's stations
        :param journeydate: journey date in 'dd-mm-yyyy' format
        :param trainid: train route id
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity, destinationstationset)
        start = time.time()
        traindata = models.gettrainsbetweenstation(sourcecity, destinationstationset, logger, journeydate, destinationcity, trainid, priceclass, numberofadults, nextday, directtrainset)
        logger.info("Time taken [%s]", time.time() - start)
        return traindata

    def gettrainroutesbetweenmultiplecities(self, sourcecity, firstbreakingstationset, journeydate, trainid, firstbreakingcity, secondbreakingstationset, secondbreakingcity, destinationstationset, destinationcity, priceclass='3A', numberofadults=1, directtrainset=sets.Set()):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param firstbreakingstationset: set of first breaking city's stations
        :param journeydate: journey date in 'dd-mm-yyyy' format
        :param trainid: train route id
        :param firstbreakingcity: first breaking city of the journey
        :param secondbreakingstationset: list of all available railway stations in second breaking station city
        :param secondbreakingcity: second breaking city of the journey
        :param destinationstationset: list of all available railway stations in first breaking station city
        :param destinationcity: destination city of the journey
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity, firstbreakingstationset)
        start = time.time()
        traindata = models.gettrainsbetweenmultiplestation(sourcecity, firstbreakingstationset, logger, journeydate, firstbreakingcity, secondbreakingstationset, secondbreakingcity, destinationstationset, destinationcity, trainid, priceclass, numberofadults, directtrainset)
        logger.info("Time taken [%s]", time.time() - start)
        return traindata

    def findtrainsbetweenstations(self, sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, nextday=False, directtrainset=sets.Set()):

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
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: trains
        """
        resultjsondata = {"train": []}
        numberofadults = int(numberofadults)
        try:
            routedata = self.gettrainroutes(sourcecity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, nextday, directtrainset)
        except Exception as e:
            logger.error("Error while fetching train data from db for source [%s] and destination [%s], reason [%s]", sourcecity, destinationcity, e.message)
            return resultjsondata
        if len(routedata) > 0:
            resultjsondata["train"].extend(routedata)
        return resultjsondata

    def findtrainsbetweenmultiplestations(self, sourcecity, firstbreakingstationset, journeydate, trainid, firstbreakingcity, secondbreakingstationset, secondbreakingcity, destinationstationset, destinationcity, priceclass, numberofadults, directtrainset=sets.Set()):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param firstbreakingstationset: list of all available railway stations in first breaking station city
        :param journeydate: date of journey
        :param trainid: id of the train route
        :param firstbreakingcity: first breaking city of the journey
        :param secondbreakingstationset: list of all available railway stations in second breaking station city
        :param secondbreakingcity: second breaking city of the journey
        :param destinationstationset: list of all available railway stations in first breaking station city
        :param destinationcity: destination city of the journey
        :param priceclass: class preferred by user
        :param numberofadults: no. of adults travelling
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: trains
        """
        resultjsondata = {"train": []}
        numberofadults = int(numberofadults)
        try:
            routedata = self.gettrainroutesbetweenmultiplecities(sourcecity, firstbreakingstationset, journeydate, trainid, firstbreakingcity, secondbreakingstationset, secondbreakingcity, destinationstationset, destinationcity, priceclass, numberofadults, directtrainset)
        except Exception as e:
            logger.error("Error while fetching train data from db for source [%s] and destination [%s], reason [%s]", sourcecity, firstbreakingcity, e.message)
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
        for route1 in sourcetobreakingstationjson["train"]:
            for route2 in breakingtodestinationjson["train"]:
                if dateTimeUtility.isjourneypossible(route1["parts"][0]["arrival"], route2["parts"][0]["departure"], route1["parts"][0]["arrivalDate"], route2["parts"][0]["departureDate"]):
                    combinedjson = convertspartstofulljson(route1, route2)
                    resultjsondata["train"].append(combinedjson)
        return resultjsondata

    def combinemultipletraindata(self, sourcetofirstbreakingstationjson, firsttosecondbreakingstationjson, secondbreakingstationtodestinationjson):

        """
        To combine data from 3 train journey parts into one
        :param sourcetofirstbreakingstationjson: journey data from source to first breaking city
        :param firsttosecondbreakingstationjson: journey data from first breaking station to second one
        :param secondbreakingstationtodestinationjson: journey data from second breaking city to destination
        :return: combined data from 3 independent journeys
        """
        resultjsondata = {"train": []}
        for route1 in sourcetofirstbreakingstationjson["train"]:
            for route2 in firsttosecondbreakingstationjson["train"]:
                if dateTimeUtility.isjourneypossible(route1["parts"][0]["arrival"], route2["parts"][0]["departure"], route1["parts"][0]["arrivalDate"], route2["parts"][0]["departureDate"]):
                    for route3 in secondbreakingstationtodestinationjson["train"]:
                        if dateTimeUtility.isjourneypossible(route2["parts"][0]["arrival"], route3["parts"][0]["departure"], route2["parts"][0]["arrivalDate"], route3["parts"][0]["departureDate"]):
                            combinedjson = convertmultipleparttofulljourney(route1, route2, route3)
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
                    if possiblecity not in skipvalues:
                        city = models.getbreakingcity(possiblecity, logger)
                        if city:
                            breakingcitylist.append(city)
                except:
                    logger.error("Error getting city for breakingstation[%s]", possiblecity.upper())
        return breakingcitylist

    def getroutes(self, source, destination, journeydate, isonlydirect=1, priceclass='3A', numberofadults=1, nextday=False):

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
            directjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(source), destinationstationset, journeydate, "train0",TravelPlanner.trainUtil.gettraincity(destination),priceclass,numberofadults, nextday)
        else:
            directjson = {"train": []}
        if isonlydirect == 1 or len(directjson["train"]) >= 5:  # return in case we have more than 8 direct trains
            return directjson
        # set of direct trainnumbers, used for filtering in breaking city journey
        directtrainset = sets.Set()
        for train in directjson["train"]:
            directtrainset.add(train["full"][0]["trainNumber"])
        logger.info("Direct train number set [%s]", str(directtrainset))
        logger.debug("Calling google api parser for Source[%s] to Destination[%s] on journeyDate[%s]", source, destination,journeydate)
        breakingcitieslist = googleapiparser.getpossiblebreakingplacesfortrain(source, destination, logger, journeydate, TravelPlanner.trainUtil.googleplacesexecutor)
        logger.debug("Call To google api parser successful for Source[%s] and Destination[%s]", source, destination)
        breakingcityset = sets.Set()
        if len(breakingcitieslist) > 0:
            futures = []
            breakingcityset = (self.getbreakingcityset(breakingcitieslist))
            logger.info("Breaking cities between source [%s] to destination [%s] are [%s]", source, destination, breakingcityset)
            if len(breakingcityset) > 0:
                traincounter = [1]
                for breakingcity in breakingcityset:
                    traincounter[0] += 1
                    if breakingcity != TravelPlanner.trainUtil.gettraincity(source) and breakingcity != TravelPlanner.trainUtil.gettraincity(destination):
                        logger.info("Getting train journey from source [%s] to destination [%s] via breaking city [%s]", source, destination, breakingcity)
                        futures.append(TravelPlanner.trainUtil.trainexecutor.submit(self.fetchtraindatafrombreakingcities, breakingcity, destination, destinationstationset, journeydate, source, directtrainset, priceclass, numberofadults, traincounter))

            for future in futures:
                logger.info("Adding breaking journey into final train journey result")
                if future:
                    jsonresult = future.result()
                    if jsonresult and len(jsonresult) > 0:
                        directjson["train"].extend(jsonresult)
                else:
                    logger.error("Breaking journey call fails")

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
                traincounter = [1]
                futures = []
                for breakingcity in breakingcityset:
                    traincounter[0] += 1
                    logger.info("Getting train journey from source [%s] to destination [%s] via breaking city [%s]", source, destination, breakingcity)
                    futures.append(TravelPlanner.trainUtil.trainexecutor.submit(self.fetchtraindatafrombreakingcities, breakingcity.upper(), destination, destinationstationset, journeydate, source, directjson, directtrainset, priceclass, numberofadults, traincounter))

                for future in futures:
                    logger.info("Adding breaking journey into final train journey result")
                    if future:
                        jsonresult = future.result()
                        if jsonresult and len(jsonresult) > 0:
                            directjson["train"].extend(jsonresult)
                    else:
                        logger.error("Breaking journey call fails")

            except Exception as e:
                logger.error("Error in fetching longitude and latitude for [%s], reason [%s]", source, e.message)

        if len(directjson["train"]) == 0 and len(breakingcityset) != 0:
            logger.info("Journey not feasible from source [%s] to destination [%s] via breaking stations [%s], need to further break journey.", source, destination, breakingcityset)
            breakingcitylist = []
            if len(breakingcitieslist) > 0:
                futures = []
                breakingcitylist = (self.getlistoftwobreakingcityset(breakingcitieslist))
                logger.info("Breaking cities between source [%s] to destination [%s] are [%s]", source, destination, breakingcitylist)
                if len(breakingcitylist) > 0:
                    traincounter = [1]
                    for breakingcities in breakingcitylist:
                        traincounter[0] += 1
                        firstbreakingcity = breakingcities.first
                        secondbreakingcity = breakingcities.second
                        if firstbreakingcity != TravelPlanner.trainUtil.gettraincity(source) and firstbreakingcity != TravelPlanner.trainUtil.gettraincity(destination)\
                                and secondbreakingcity != TravelPlanner.trainUtil.gettraincity(source) and secondbreakingcity != TravelPlanner.trainUtil.gettraincity(destination):
                            logger.info("Getting train journey from source [%s] to destination [%s] via two breaking city [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                            futures.append(TravelPlanner.trainUtil.trainexecutor.submit(self.fetchtraindatafrommultiplebreakingcities, firstbreakingcity, secondbreakingcity, TravelPlanner.trainUtil.gettraincity(destination), destinationstationset, journeydate, TravelPlanner.trainUtil.gettraincity(source), directtrainset, priceclass, numberofadults, traincounter))

                for future in futures:
                    logger.info("Adding breaking journey into final train journey result")
                    if future:
                        jsonresult = future.result()
                        if jsonresult and len(jsonresult) > 0:
                            directjson["train"].extend(jsonresult)
                    else:
                        logger.error("Breaking journey call fails")

        logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", source, destination, journeydate)
        return directjson

    def fetchtraindatafrombreakingcities(self, breakingcity, destination, destinationstationset, journeydate, source, directtrainset, priceclass, numberofadults, traincounter):

        """
        :param breakingcity: city from where journey needs to be broken
        :param destination: final destination
        :param destinationstationset: set of all railway stations of destination city
        :param journeydate: date of journey
        :param source: source station of journey
        :param traincounter: global train counter used for route ID generation
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        """

        breakingcitystationset = self.placetostationcodescache.getstationsbycityname(breakingcity)
        if (len(breakingcitystationset)) != 0:
            # only call for train if breaking city has train stations
            sourcetobreakingstationtrainjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(source), breakingcitystationset, journeydate, "train"+str(traincounter[0]), TravelPlanner.trainUtil.gettraincity(breakingcity), priceclass, numberofadults, directtrainset=directtrainset)
        else:
            logger.error("Breaking city [%s] has no train stations", breakingcity)
            sourcetobreakingstationtrainjson = {"train": []}

        buscontroller = busapi.BusController()
        sourcetobreakingstationbusjson = buscontroller.getresults(source, breakingcity, journeydate,numberofadults)

        combinedjson = { "train" : []}
        if len(sourcetobreakingstationtrainjson["train"]) > 0 or len(sourcetobreakingstationbusjson["bus"]) > 0:
            nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')

            if (len(destinationstationset)) != 0:
                # only call for train if breaking city has train stations
                breakingtodestinationtrainjson = self.findtrainsbetweenstations(TravelPlanner.trainUtil.gettraincity(breakingcity), destinationstationset,journeydate, "train"+str(traincounter[0])+str(traincounter[0]), TravelPlanner.trainUtil.gettraincity(destination),priceclass,numberofadults, nextday=True, directtrainset=directtrainset)
            else:
                breakingtodestinationtrainjson = {"train": []}

            if len(breakingtodestinationtrainjson["train"]) > 0 and len(sourcetobreakingstationtrainjson["train"]) > 0:
                # merge train data from source - breakingcity - destination
                combinedjson = self.combinedata(sourcetobreakingstationtrainjson, breakingtodestinationtrainjson)
                if len(combinedjson["train"]) > 0:
                    # return if any breaking train journey is present, no need for bus journey
                    logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, breakingcity)
                    return combinedjson["train"]

            breakingtodestinationbusjson = buscontroller.getresults(breakingcity,destination, journeydate,numberofadults)
            breakingtodestinationbusjson["bus"].extend(buscontroller.getresults(breakingcity, destination, nextday, numberofadults)["bus"])

            if len(sourcetobreakingstationbusjson["bus"]) > 0 and len(breakingtodestinationtrainjson["train"]) > 0:
                # merge bus data (initial) and train data from source -(bus) - breakingcity -(train) - destination
                combinedjson["train"].extend(self.combinebusandtraininit(sourcetobreakingstationbusjson,breakingtodestinationtrainjson)["train"])

            if len(sourcetobreakingstationtrainjson["train"]) > 0 and len(breakingtodestinationbusjson["bus"]) > 0:
                # merge bus data (end) and train data from source -(train) - breakingcity -(bus) - destination
                combinedjson["train"].extend(self.combinebusandtrainend(sourcetobreakingstationtrainjson,breakingtodestinationbusjson)["train"])

            logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, breakingcity)
            return combinedjson["train"]

        else:
            logger.warning("No journey possible between [%s] and [%s] via [%s], return empty list", source, destination, breakingcity)
            return combinedjson["train"]

    def fetchtraindatafrommultiplebreakingcities(self, firstbreakingcity, secondbreakingcity, destination, destinationstationset, journeydate, source, directtrainset, priceclass, numberofadults, traincounter):

        """
        :param firstbreakingcity: first city from where journey needs to be broken
        :param secondbreakingcity: second city from where journey needs to be broken
        :param destination: final destination
        :param destinationstationset: set of all railway stations of destination city
        :param journeydate: date of journey
        :param source: source station of journey
        :param traincounter: global train counter used for route ID generation
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        """
        firstbreakingcitystationset = self.placetostationcodescache.getstationsbycityname(firstbreakingcity)
        secondbreakingcitystationset = self.placetostationcodescache.getstationsbycityname(secondbreakingcity)
        combinedjson = {"train": []}
        if len(firstbreakingcitystationset) != 0 and len(secondbreakingcitystationset) != 0:
            # only call for train if breaking city has train stations
            trainjson = self.findtrainsbetweenmultiplestations(source, firstbreakingcitystationset, journeydate, "train"+str(traincounter[0]), firstbreakingcity, secondbreakingcitystationset, secondbreakingcity, destinationstationset, destination, priceclass, numberofadults, directtrainset=directtrainset)
            srctofirstbrkstationtrainjson = {"train": []}
            srctofirstbrkstationtrainjsonroute = []
            firsttosecondbrkstationtrainjson = {"train": []}
            firsttosecondbrkstationtrainjsonroute = []
            secondbrkstationtodesttrainjson = {"train": []}
            secondbrkstationtodesttrainjsonroute = []
            if len(trainjson["train"]) >= 2:
                for trainroute in trainjson["train"]:
                    if trainroute["full"][0]["source"].upper() == source:
                        srctofirstbrkstationtrainjsonroute.append(trainroute)
                    if trainroute["full"][0]["source"].upper() == firstbreakingcity:
                        firsttosecondbrkstationtrainjsonroute.append(trainroute)
                    if trainroute["full"][0]["source"].upper() == secondbreakingcity:
                        secondbrkstationtodesttrainjsonroute.append(trainroute)
                srctofirstbrkstationtrainjson["train"].extend(srctofirstbrkstationtrainjsonroute)
                firsttosecondbrkstationtrainjson["train"].extend(firsttosecondbrkstationtrainjsonroute)
                secondbrkstationtodesttrainjson["train"].extend(secondbrkstationtodesttrainjsonroute)
            else:
                logger.warning("No journey possible between source [%s] and destination [%s], via Breaking cities [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                return combinedjson["train"]
        else:
            logger.warning("Neither Breaking city [%s] & [%s] has train stations", firstbreakingcity, secondbreakingcity)
            return combinedjson["train"]

        if len(firsttosecondbrkstationtrainjson["train"]) == 0:
            logger.warning("No train between Breaking cities [%s] & [%s]", firstbreakingcity, secondbreakingcity)
            return combinedjson["train"]

        if len(srctofirstbrkstationtrainjson["train"]) > 0 and len(secondbrkstationtodesttrainjson["train"]) > 0 and len(secondbrkstationtodesttrainjson["train"]) > 0:
            # merge onl train journey from source - first breakingstation - second breakingstation - destination
            combinedjson = self.combinemultipletraindata(srctofirstbrkstationtrainjson, firsttosecondbrkstationtrainjson, secondbrkstationtodesttrainjson)
            if len(combinedjson["train"]) > 0:
                logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                return combinedjson["train"]

        if len(srctofirstbrkstationtrainjson["train"]) > 0 or len(secondbrkstationtodesttrainjson["train"]) > 0:
            # merge train data from source - firstbreakingcity - secondbreakingcity
            sourcetobreakingstationtrainjson = self.combinedata(srctofirstbrkstationtrainjson, firsttosecondbrkstationtrainjson)
            if len(sourcetobreakingstationtrainjson["train"]) > 0:
                # return and merge secondbreakingcity - destination data
                combinedjson = self.combinedata(sourcetobreakingstationtrainjson, secondbrkstationtodesttrainjson)
                if len(combinedjson["train"]) > 0:
                    logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                    return combinedjson["train"]
                else:
                    # only train journey not possible, fetch bus data and try to create journey
                    buscontroller = busapi.BusController()
                    breakingstationtodestinationbusjson = buscontroller.getresults(secondbreakingcity, destination, journeydate, numberofadults)
                    nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
                    dayaftertomorrow = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=2)).strftime('%d-%m-%Y')
                    breakingstationtodestinationbusjson["bus"].extend(buscontroller.getresults(secondbreakingcity, destination, nextday, numberofadults)["bus"])
                    breakingstationtodestinationbusjson["bus"].extend(buscontroller.getresults(secondbreakingcity, destination, dayaftertomorrow, numberofadults)["bus"])
                    if len(breakingstationtodestinationbusjson["bus"]) > 0:
                        # merge bus data (end) and train data from source -(train) - breakingcity -(bus) - destination
                        combinedjson["train"].extend(self.combinebusandtrainend(sourcetobreakingstationtrainjson, breakingstationtodestinationbusjson)["train"])

            # merge train data from firstbreakingcity - secondbreakingcity - destination
            breakingstationtodestinationtrainjson = self.combinedata(firsttosecondbrkstationtrainjson, secondbrkstationtodesttrainjson)
            if len(breakingstationtodestinationtrainjson["train"]) > 0:
                # only train journey not possible, fetch bus data and try to create journey
                buscontroller = busapi.BusController()
                sourcetobreakingstationbusjson = buscontroller.getresults(source, firstbreakingcity, journeydate, numberofadults)
                if len(sourcetobreakingstationbusjson["bus"]) > 0:
                    # merge bus data (end) and train data from source -(bus) - breakingcities -(train) - destination
                    combinedjson["train"].extend(self.combinebusandtraininit(sourcetobreakingstationbusjson, breakingstationtodestinationtrainjson)["train"])

            logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, firstbreakingcity)
            return combinedjson["train"]
        else:
            logger.warning("No journey possible between [%s] and [%s] via [%s] & [%s], return empty list", source, destination, firstbreakingcity, secondbreakingcity)
            return combinedjson["train"]

    def getlistoftwobreakingcityset(self, breakingcitieslist):
        """
        To get list of those breaking cities which have 2 breaking stations
        :param breakingcitieslist: list of all possible breaking city list
        :return: list of those 2 breaking cities list
        """
        breakingcitylist = []
        for breakingcities in breakingcitieslist:
            if len(breakingcities) == 2:
                brkstations = BreakingStations()
                brkstations.first = breakingcities[0]
                brkstations.second = breakingcities[1]
                self.addtobreakingcitylist(brkstations, breakingcitylist)
        return breakingcitylist

    def addtobreakingcitylist(self, breakingstations, breakingcitylist):
        """
        Add breaking stations to breakingcitylist only if already not exists
        :param breakingstations: list of breaking stations with 2 breaking cities
        """

        if len(breakingcitylist) == 0:
            breakingcitylist.append(breakingstations)

        else:
            for brkstations in breakingcitylist:
                if brkstations.first == breakingstations.first and brkstations.second == breakingstations.second:
                    return
            breakingcitylist.append(breakingstations)

    def getbreakingcityset(self, breakingcitieslist):

        """
        To get set of all breaking cities
        :param breakingcitieslist: list of breaking city sets
        :return: breaking city sets
        """
        breakingcityset = sets.Set()

        """
        this method is used to get relevant breaking cities from all the breaking cities list.
        First prefernece is given to list having only one element then so on
        :param breakingcitieslist: list of breaking cities
        :return: breaking city set
        """
        for breakingcities in breakingcitieslist:
            breakingcities = sets.Set(breakingcities)
            if len(breakingcities) == 1:
                breakingcityset.add(breakingcities.pop())
            else:
                for breakingcity in breakingcities:
                    if breakingcity.upper() in bigcities:
                        breakingcityset.add(breakingcity)
        return breakingcityset

    def combinebusandtraininit(self, sourcetobreakingbusjson, breakingtodestinationtrainjson):

        """
        To combine bus and train data. bus data is inserted before train journey.
        :param sourcetobreakingbusjson: bus data from source to breaking staion
        :param breakingtodestinationtrainjson: train data from breaking to destination
        :return: combined data (Source - Bus - Breaking City - Train - Destination)
        """

        combinedjson = {"train": []}

        for j in range(len(breakingtodestinationtrainjson["train"])):
            trainpart = breakingtodestinationtrainjson["train"][j]["parts"][0]
            subparts = []
            for k in range(len(sourcetobreakingbusjson["bus"])):
                subpart = sourcetobreakingbusjson["bus"][k]["parts"][0]
                if dateTimeUtility.isjourneypossible(subpart["arrival"], trainpart["departure"], subpart["arrivalDate"], trainpart["departureDate"], 2, 24):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], trainpart["departure"],subpart["arrivalDate"],trainpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(trainpart["departure"], subpart["departure"], trainpart["departureDate"], subpart["departureDate"])
                    subparts.append(copy.deepcopy(subpart))

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": "bus","id": breakingtodestinationtrainjson["train"][j]["full"][0]["id"] + str(0), "destination": subparts[0]["destination"],
                           "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                breakingtodestinationtrainjson["train"][j]["parts"].insert(0, newpart)
                breakingtodestinationtrainjson["train"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",train," + breakingtodestinationtrainjson["train"][j]["full"][0]["destination"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["price"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
                breakingtodestinationtrainjson["train"][j]["full"][0]["minPrice"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                breakingtodestinationtrainjson["train"][j]["full"][0]["maxPrice"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                breakingtodestinationtrainjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
                breakingtodestinationtrainjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
                breakingtodestinationtrainjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                breakingtodestinationtrainjson["train"][j]["full"][0]["minDeparture"] = minmax["minDep"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["source"] = newpart["source"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["departure"] = subparts[0]["departure"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["departureDate"] = subparts[0]["departureDate"]
                breakingtodestinationtrainjson["train"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(subparts[0]["departureDate"], 0)
                breakingtodestinationtrainjson["train"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(breakingtodestinationtrainjson["train"][j]["full"][0]["arrivalDate"], 0)

        combinedjson["train"] = [x for x in breakingtodestinationtrainjson["train"] if len(x["parts"]) == 2]
        return combinedjson

    def combinebusandtrainend(self, sourcetobreakingtrainjson, breakingtodestinationbusjson):

        """
        To combine train and bus data. Bus data is inserted after train journey.
        :param sourcetobreakingtrainjson: train data from source to breaking station
        :param breakingtodestinationbusjson: bus data from breaking to destination
        :return: combined data (Source - Train - Breaking City - Bus - Destination)
        """
        combinedjson = {"train": []}

        for j in range(len(sourcetobreakingtrainjson["train"])):
            trainpart = sourcetobreakingtrainjson["train"][j]["parts"][0]
            subparts = []
            for k in range(len(breakingtodestinationbusjson["bus"])):
                subpart = breakingtodestinationbusjson["bus"][k]["parts"][0]
                if dateTimeUtility.isjourneypossible(trainpart["arrival"], subpart["departure"], trainpart["arrivalDate"], subpart["departureDate"], 2, 10):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(trainpart["arrival"], subpart["departure"],trainpart["arrivalDate"],subpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], trainpart["arrival"], subpart["arrivalDate"], trainpart["arrivalDate"])
                    subparts.append(copy.deepcopy(subpart))

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": "bus", "id": sourcetobreakingtrainjson["train"][j]["full"][0]["id"] + str(2), "destination": subparts[0]["destination"],
                           "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
                sourcetobreakingtrainjson["train"][j]["parts"].append(newpart)
                sourcetobreakingtrainjson["train"][j]["full"][0]["route"] = sourcetobreakingtrainjson["train"][j]["full"][0]["source"] + ",train," + newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["price"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
                sourcetobreakingtrainjson["train"][j]["full"][0]["minPrice"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                sourcetobreakingtrainjson["train"][j]["full"][0]["maxPrice"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                sourcetobreakingtrainjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
                sourcetobreakingtrainjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
                sourcetobreakingtrainjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                sourcetobreakingtrainjson["train"][j]["full"][0]["minArrival"] = minmax["minArr"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["destination"] = subparts[0]["destination"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                sourcetobreakingtrainjson["train"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
                sourcetobreakingtrainjson["train"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(sourcetobreakingtrainjson["train"][j]["full"][0]["departureDate"], 0)

        combinedjson["train"] = [x for x in sourcetobreakingtrainjson["train"] if len(x["parts"]) == 2]
        return combinedjson
