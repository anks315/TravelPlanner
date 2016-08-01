import sets
import json, time, datetime, urllib2
import distanceutil, busapi, loggerUtil, googleapiparser, models, TravelPlanner.startuputil, trainapiutil, breakingcityutil

__author__ = 'ankur'
today = datetime.date.today().strftime("%Y-%m-%d")
skipvalues = sets.Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])

logger = loggerUtil.getlogger("TrainApiNeo4j")


class TrainController:

    """Entry point to get all routes with train as the major mode of transport"""
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

    def gettrainrouteviabreakingcity(self, sourcecity, breakingstationset, breakingcity, destinationstationset, journeydate, trainid, destinationcity, priceclass='3A', numberofadults=1, directtrainset=sets.Set()):

        """
        to get list of all possible routes along with fare between all stations of source city and destination stations
        :param sourcecity: source of the journey
        :param breakingstationset: list of all available railway stations in breaking city
        :param breakingcity: breaking city in journey
        :param destinationstationset: set of destination city's stations
        :param journeydate: journey date in 'dd-mm-yyyy' format
        :param trainid: train route id
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: list of all possible routes with fare
        """
        logger.info("Fetching train routes between sourcecity[%s] and destination Stations[%s]", sourcecity, destinationstationset)
        start = time.time()
        traindata = models.gettrainsbetweenstationviabreaking(sourcecity, breakingstationset, breakingcity, destinationstationset, logger, journeydate, destinationcity, trainid, priceclass, numberofadults, directtrainset)
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

    def findtrainsviabreakingstation(self, sourcecity, breakingstationset, breakingcity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, directtrainset=sets.Set()):

        """
        find the trains between the sourcecity & destination cities stations
        :param sourcecity: source of the journey
        :param breakingstationset: list of all available railway stations in breaking city
        :param breakingcity: breaking city in journey
        :param destinationstationset: list of all available railway stations in destination city
        :param journeydate: date of journey
        :param trainid: id of the train route
        :param destinationcity: destination city of the journey
        :param priceclass: class preferred by user
        :param numberofadults: no. of adults travelling
        :param directtrainset: set of direct train numbers from source to destination, used for filtering out all direct trains in breaking journey
        :return: trains
        """
        resultjsondata = {"train": []}
        numberofadults = int(numberofadults)
        try:
            routedata = self.gettrainrouteviabreakingcity(sourcecity, breakingstationset, breakingcity, destinationstationset, journeydate, trainid, destinationcity, priceclass, numberofadults, directtrainset)
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
        destinationstationset = breakingcityutil.getstationsbycityname(TravelPlanner.startuputil.gettraincity(destination))

        if len(destinationstationset) != 0:
            directjson = self.findtrainsbetweenstations(TravelPlanner.startuputil.gettraincity(source), destinationstationset, journeydate, "train0",TravelPlanner.startuputil.gettraincity(destination),priceclass,numberofadults, nextday)
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
        breakingcitieslist = googleapiparser.getpossiblebreakingplacesfortrain(source, destination, logger, journeydate, TravelPlanner.startuputil.googleplacesexecutor)
        logger.debug("Call To google api parser successful for Source[%s] and Destination[%s]", source, destination)
        breakingcityset = sets.Set()
        if len(breakingcitieslist) > 0:
            futures = []
            breakingcityset = (breakingcityutil.getbreakingcityset(breakingcitieslist))
            logger.info("Breaking cities between source [%s] to destination [%s] are [%s]", source, destination, breakingcityset)
            if len(breakingcityset) > 0:
                traincounter = [1]
                for breakingcity in breakingcityset:
                    traincounter[0] += 1
                    if breakingcity != TravelPlanner.startuputil.gettraincity(source) and breakingcity != TravelPlanner.startuputil.gettraincity(destination):
                        logger.info("Getting train journey from source [%s] to destination [%s] via breaking city [%s]", source, destination, breakingcity)
                        futures.append(TravelPlanner.startuputil.trainexecutor.submit(self.fetchtraindatafrombreakingcities, breakingcity, destination, destinationstationset, journeydate, source, directtrainset, priceclass, numberofadults, traincounter))

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
                breakingcity = distanceutil.findnearestrailwaystation(sourcelat, sourcelong, TravelPlanner.startuputil.gettraincity(source)).upper()
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
                breakingcity = distanceutil.findnearestrailwaystation(destlat, destlong, TravelPlanner.startuputil.gettraincity(destination)).upper()
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
                    futures.append(TravelPlanner.startuputil.trainexecutor.submit(self.fetchtraindatafrombreakingcities, breakingcity.upper(), destination, destinationstationset, journeydate, source, directjson, directtrainset, priceclass, numberofadults, traincounter))

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
            if len(breakingcitieslist) > 0:
                futures = []
                breakingcitylist = (breakingcityutil.getlistoftwobreakingcityset(breakingcitieslist))
                logger.info("Breaking cities between source [%s] to destination [%s] are [%s]", source, destination, breakingcitylist)
                if len(breakingcitylist) > 0:
                    traincounter = [1]
                    for breakingcities in breakingcitylist:
                        traincounter[0] += 1
                        firstbreakingcity = breakingcities.first
                        secondbreakingcity = breakingcities.second
                        if firstbreakingcity != TravelPlanner.startuputil.gettraincity(source) and firstbreakingcity != TravelPlanner.startuputil.gettraincity(destination)\
                                and secondbreakingcity != TravelPlanner.startuputil.gettraincity(source) and secondbreakingcity != TravelPlanner.startuputil.gettraincity(destination):
                            logger.info("Getting train journey from source [%s] to destination [%s] via two breaking city [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                            futures.append(TravelPlanner.startuputil.trainexecutor.submit(self.fetchtraindatafrommultiplebreakingcities, firstbreakingcity, secondbreakingcity, TravelPlanner.startuputil.gettraincity(destination), destinationstationset, journeydate, TravelPlanner.startuputil.gettraincity(source), directtrainset, priceclass, numberofadults, traincounter))

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

        combinedjson = {"train": []}
        buscontroller = busapi.BusController()
        breakingcitystationset = breakingcityutil.getstationsbycityname(breakingcity)
        sourcestationset = breakingcityutil.getstationsbycityname(TravelPlanner.startuputil.gettraincity(source))

        if (len(breakingcitystationset) == 0) or (len(sourcestationset) == 0 and len(destinationstationset) == 0):
            logger.info("No train journey possible from source [%s] to destination [%s] via [%s], since breaking city has no train stations", source, destination, breakingcity)
            return combinedjson["train"]

        if len(destinationstationset) == 0:
            # destination station has no railway station, only bus journey possible from breaking city to destination
            sourcetobreakingstationtrainjson = self.findtrainsbetweenstations(TravelPlanner.startuputil.gettraincity(source), breakingcitystationset, journeydate, "train" + str(traincounter[0]), breakingcity, priceclass, numberofadults, nextday=False, directtrainset=directtrainset)
            if len(sourcetobreakingstationtrainjson["train"]) > 0:
                breakingstationtodestinationbusjson = trainapiutil.getnextdaybusresults(buscontroller, breakingcity, destination, journeydate, numberofadults)
                if len(breakingstationtodestinationbusjson["bus"]) > 0:
                    # merge bus data (end) and train data from source -(train) - breakingcity -(bus) - destination
                    combinedjson["train"].extend(trainapiutil.combinebusandtrainend(sourcetobreakingstationtrainjson, breakingstationtodestinationbusjson)["train"])

        elif len(breakingcitystationset) > 0 and len(destinationstationset) > 0:
            # only call multiple trains query if both breaking city and destination has train stations
            trainjson = self.findtrainsviabreakingstation(TravelPlanner.startuputil.gettraincity(source), breakingcitystationset, TravelPlanner.startuputil.gettraincity(breakingcity), destinationstationset, journeydate, "train" + str(traincounter[0]), TravelPlanner.startuputil.gettraincity(destination), priceclass, numberofadults, directtrainset=directtrainset)
            sourcetobreakingstationtrainjson = {"train": []}
            sourcetobreakingstationtrainjsonroute = []
            breakingstationtodestinationtrainjson = {"train": []}
            breakingstationtodestinationtrainjsonroute = []
            for trainroute in trainjson["train"]:
                if trainroute["full"][0]["source"].upper() == source:
                    sourcetobreakingstationtrainjsonroute.append(trainroute)
                if trainroute["full"][0]["source"].upper() == breakingcity:
                    breakingstationtodestinationtrainjsonroute.append(trainroute)
            sourcetobreakingstationtrainjson["train"].extend(sourcetobreakingstationtrainjsonroute)
            breakingstationtodestinationtrainjson["train"].extend(breakingstationtodestinationtrainjsonroute)

            if len(sourcetobreakingstationtrainjson["train"]) == 0 and len(breakingstationtodestinationtrainjson["train"]) == 0:
                logger.warning("No train between source [%s] and breaking city [%s] and breaking city [%s] and destination [%s]", source, breakingcity, breakingcity, destination)
                return combinedjson["train"]

            if len(sourcetobreakingstationtrainjson["train"]) > 0 and len(breakingstationtodestinationtrainjson) > 0:
                # merge train data from source - breakingcity - destination
                combinedjson = trainapiutil.combinedata(sourcetobreakingstationtrainjson, breakingstationtodestinationtrainjson)
                if len(combinedjson["train"]) > 0:
                    # return if any breaking train journey is present, no need for bus journey
                    logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, breakingcity)
                    return combinedjson["train"]

            if len(sourcetobreakingstationtrainjson["train"]) > 0:
                breakingstationtodestinationbusjson = trainapiutil.getnextdaybusresults(buscontroller, breakingcity, destination, journeydate, numberofadults)
                if len(breakingstationtodestinationbusjson["bus"]) > 0:
                    # merge bus data (end) and train data from source -(train) - breakingcity -(bus) - destination
                    combinedjson["train"].extend(trainapiutil.combinebusandtrainend(sourcetobreakingstationtrainjson, breakingstationtodestinationbusjson)["train"])

            if len(breakingstationtodestinationtrainjson["train"]) > 0:
                sourcetobreakingstationbusjson = buscontroller.getresults(source, breakingcity, journeydate, numberofadults)
                if len(sourcetobreakingstationbusjson["bus"]) > 0:
                    # merge bus data (initial) and train data from source -(bus) - breakingcity -(train) - destination
                    combinedjson["train"].extend(trainapiutil.combinebusandtraininit(sourcetobreakingstationbusjson, breakingstationtodestinationtrainjson)["train"])

        logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, breakingcity)
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
        combinedjson = {"train": []}
        firstbreakingcitystationset = breakingcityutil.getstationsbycityname(firstbreakingcity)
        secondbreakingcitystationset = breakingcityutil.getstationsbycityname(secondbreakingcity)
        sourcestationset = breakingcityutil.getstationsbycityname(TravelPlanner.startuputil.gettraincity(source))

        if len(firstbreakingcitystationset) == 0 or len(secondbreakingcitystationset) == 0 or (len(sourcestationset) == 0 and len(destinationstationset) == 0):
            logger.info("Train journey not possible between source [%s] and dstination [%s] via Breaking cities [%s] & [%s], cause either brekaing city has no train stations", source, destination, firstbreakingcity, secondbreakingcity)
            return combinedjson["train"]

        buscontroller = busapi.BusController()
        srctofirstbrkstationtrainjson = {"train": []}
        srctofirstbrkstationtrainjsonroute = []
        firsttosecondbrkstationtrainjson = {"train": []}
        firsttosecondbrkstationtrainjsonroute = []
        secondbrkstationtodesttrainjson = {"train": []}
        secondbrkstationtodesttrainjsonroute = []

        # now train journey is possible cause we are sure that any two of first breaking/second breaking/destination has railway stations
        if len(destinationstationset) == 0:
            # since destination has no railway stations, only bus journey possible from second breaking city to destination
            trainjson = self.findtrainsviabreakingstation(TravelPlanner.startuputil.gettraincity(source), firstbreakingcitystationset, TravelPlanner.startuputil.gettraincity(firstbreakingcity), secondbreakingcitystationset, journeydate, "train" + str(traincounter[0]), TravelPlanner.startuputil.gettraincity(secondbreakingcity), priceclass, numberofadults, directtrainset=directtrainset)
            for trainroute in trainjson["train"]:
                if trainroute["full"][0]["source"].upper() == source:
                    srctofirstbrkstationtrainjsonroute.append(trainroute)
                if trainroute["full"][0]["source"].upper() == firstbreakingcity:
                    firsttosecondbrkstationtrainjsonroute.append(trainroute)
            srctofirstbrkstationtrainjson["train"].extend(srctofirstbrkstationtrainjsonroute)
            firsttosecondbrkstationtrainjson["train"].extend(firsttosecondbrkstationtrainjsonroute)

            if len(srctofirstbrkstationtrainjson["train"]) == 0 or len(firsttosecondbrkstationtrainjson["train"]) == 0:
                logger.info("Train journey not possible between source [%s] and dstination [%s] via Breaking cities [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                return combinedjson["train"]

            # merge train data from source - breakingcity - destination
            combinedjson = trainapiutil.combinedata(srctofirstbrkstationtrainjson, firsttosecondbrkstationtrainjson)
            if len(combinedjson["train"]) == 0:
                logger.info("Train journey not possible between source [%s] and dstination [%s] via Breaking cities [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                return combinedjson["train"]

            secondbrkstationtodestbusjson = trainapiutil.getnextdaybusresults(buscontroller, secondbreakingcity, destination, journeydate, numberofadults)
            if len(secondbrkstationtodestbusjson["bus"]) > 0:
                # merge bus data (end) and train data from source -(train) - first breakingcity - (train) second breaking city -(train) - destination
                withbustrainend = trainapiutil.combinebusandtrainend(combinedjson, secondbrkstationtodestbusjson)
                fullroute = source.title() + ",train," + firstbreakingcity.title() + ",train," + secondbreakingcity.title() + ",bus," + destination.title()
                for trainroute in withbustrainend["train"]:
                    trainroute["full"][0]["route"] = fullroute
                combinedjson["train"].extend(withbustrainend["train"])

        elif len(firstbreakingcitystationset) > 0 and len(secondbreakingcitystationset) > 0 and len(destinationstationset) > 0:
            # only call for train if breaking city has train stations
            trainjson = self.findtrainsbetweenmultiplestations(source, firstbreakingcitystationset, journeydate, "train"+str(traincounter[0]), firstbreakingcity, secondbreakingcitystationset, secondbreakingcity, destinationstationset, destination, priceclass, numberofadults, directtrainset=directtrainset)
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

            if len(firsttosecondbrkstationtrainjson["train"]) == 0:
                logger.warning("No train between Breaking cities [%s] & [%s]", firstbreakingcity, secondbreakingcity)
                return combinedjson["train"]

            if len(srctofirstbrkstationtrainjson["train"]) > 0 and len(secondbrkstationtodesttrainjson["train"]) > 0 and len(secondbrkstationtodesttrainjson["train"]) > 0:
                # merge onl train journey from source - first breakingstation - second breakingstation - destination
                combinedjson = trainapiutil.combinemultipletraindata(srctofirstbrkstationtrainjson, firsttosecondbrkstationtrainjson, secondbrkstationtodesttrainjson)
                if len(combinedjson["train"]) > 0:
                    logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                    return combinedjson["train"]

            if len(srctofirstbrkstationtrainjson["train"]) > 0 or len(secondbrkstationtodesttrainjson["train"]) > 0:
                # merge train data from source - firstbreakingcity - secondbreakingcity
                sourcetobreakingstationtrainjson = trainapiutil.combinedata(srctofirstbrkstationtrainjson, firsttosecondbrkstationtrainjson)
                if len(sourcetobreakingstationtrainjson["train"]) > 0:
                    # return and merge secondbreakingcity - destination data
                    combinedjson = trainapiutil.combinedata(sourcetobreakingstationtrainjson, secondbrkstationtodesttrainjson)
                    if len(combinedjson["train"]) > 0:
                        logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s] & [%s]", source, destination, firstbreakingcity, secondbreakingcity)
                        return combinedjson["train"]
                    else:
                        # only train journey not possible, fetch bus data and try to create journey
                        breakingstationtodestinationbusjson = trainapiutil.getnextdaybusresults(buscontroller, secondbreakingcity, destination, journeydate, numberofadults)
                        if len(breakingstationtodestinationbusjson["bus"]) > 0:
                            # merge bus data (end) and train data from source -(train) - first breakingcity -(train)- second breaking city -(train)- destination
                            withbustrainend = trainapiutil.combinebusandtrainend(sourcetobreakingstationtrainjson, breakingstationtodestinationbusjson)
                            fullroute = source.title() + ",train," + firstbreakingcity.title() + ",train," + secondbreakingcity.title() + ",bus," + destination.title()
                            for trainroute in withbustrainend["train"]:
                                trainroute["full"][0]["route"] = fullroute
                            combinedjson["train"].extend(withbustrainend["train"])

                # merge train data from firstbreakingcity - secondbreakingcity - destination
                breakingstationtodestinationtrainjson = trainapiutil.combinedata(firsttosecondbrkstationtrainjson, secondbrkstationtodesttrainjson)
                if len(breakingstationtodestinationtrainjson["train"]) > 0:
                    # only train journey not possible, fetch bus data and try to create journey
                    buscontroller = busapi.BusController()
                    sourcetobreakingstationbusjson = buscontroller.getresults(source, firstbreakingcity, journeydate, numberofadults)
                    if len(sourcetobreakingstationbusjson["bus"]) > 0:
                        # merge bus data (init) and train data from source -(bus) - first breaking city -(train)- second breaking city -(train)- destination
                        withbustraininit = trainapiutil.combinebusandtraininit(sourcetobreakingstationbusjson, breakingstationtodestinationtrainjson)
                        fullroute = source.title() + ",bus," + firstbreakingcity.title() + ",train," + secondbreakingcity.title() + ",train," + destination.title()
                        for trainroute in withbustraininit["train"]:
                            trainroute["full"][0]["route"] = fullroute
                        combinedjson["train"].extend(withbustraininit["train"])

        logger.info("Return success for Call to Fetch breaking journey route from [%s] to [%s] via [%s]", source, destination, firstbreakingcity)
        return combinedjson["train"]