__author__ = 'ankur'
import busapi
import json
import urllib2
import flightSkyScanner
import concurrent.futures
import dateTimeUtility
import miscUtility, flightutil
import distanceutil
import trainapineo4j
import minMaxUtil
import copy
import loggerUtil, models
import TravelPlanner.startuputil


logger = loggerUtil.getlogger("FlightApi")


class FlightController:
    """Class returns all stations corresponding to a city"""

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass, flightclass, numberofadults):

        logger.debug("[START]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",sourcecity,destinationcity,journeydate)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

            source = TravelPlanner.startuputil.gettraincity(sourcecity).title()
            destination = TravelPlanner.startuputil.gettraincity(destinationcity).title()
            # get nearest airport and nearest big airport to our source city
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + source
            url = url.replace(' ', '%20')
            response = urllib2.urlopen(url)
            sourcelatlong = json.loads(response.read())
            response.close()
            sourcelat = sourcelatlong["results"][0]["geometry"]["location"]["lat"]
            sourcelong = sourcelatlong["results"][0]["geometry"]["location"]["lng"]
            sourceairport = distanceutil.findnearestairport(sourcelat,sourcelong)
            bigsourceairport = distanceutil.findnearestbigairport(sourcelat,sourcelong)

            # get nearest airport and nearest big airport to our destination city
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination
            url = url.replace(' ', '%20')
            response2 = urllib2.urlopen(url)
            destlatlong = json.loads(response2.read())
            destlat = destlatlong["results"][0]["geometry"]["location"]["lat"]
            destlong = destlatlong["results"][0]["geometry"]["location"]["lng"]
            destairport = distanceutil.findnearestairport(destlat, destlong)
            bigdestinationairport = distanceutil.findnearestbigairport(destlat, destlong)
            
            bigsource = flightutil.stationtocitymap[bigsourceairport]
            bigdestination = flightutil.stationtocitymap[bigdestinationairport]
            sourceflight = flightutil.stationtocitymap[sourceairport]
            destinationflight = flightutil.stationtocitymap[destairport]

            if source != sourceflight:
                othermodessminitfuture = executor.submit(self.getothermodes,sourcecity, sourceflight, journeydate,trainclass,numberofadults)
                othermodessminit2future = executor.submit(self.getothermodes, sourcecity, sourceflight, dateTimeUtility.getPreviousDate(journeydate),trainclass,numberofadults)
            if destination != destinationflight:
                othermodessmendfuture = executor.submit(self.getothermodes, destinationflight, destinationcity, journeydate,trainclass,numberofadults)
                othermodessmend2future = executor.submit(self.getothermodes, destinationflight, destinationcity, dateTimeUtility.getNextDate(journeydate),trainclass,numberofadults)

            onlyflightfuture = executor.submit(flightSkyScanner.getApiResults,sourceflight,destinationflight,journeydate,"flight0",flightclass,numberofadults)

            finallist = {}
            if (bigsource != 'empty') and (bigdestination != 'empty') and (bigsource != destinationflight) and (bigdestination != sourceflight):
                mixedflight = {"flight": []}
                mixedflightend = {"flight": []}
                mixedflightinit = {"flight": []}
                othermodesinit=[]
                othermodesend=[]
                othermodesinitfuture = []
                othermodesendfuture = []

                # if there is only one big airport in between or both source and destination are big airports
                if (bigsource != bigdestination) and ((bigsource != sourceflight) and (bigdestination != destinationflight)):
                    mixedflightfuture = executor.submit(flightSkyScanner.getApiResults,bigsource,bigdestination,journeydate,"flight1",flightclass,numberofadults)
                    othermodesinitfuture = executor.submit(self.getothermodes, sourcecity, bigsource, journeydate,trainclass,numberofadults)
                    othermodesinit2future = executor.submit(self.getothermodes, sourcecity, bigsource, dateTimeUtility.getPreviousDate(journeydate),trainclass,numberofadults)
                    othermodesendfuture = executor.submit(self.getothermodes, bigdestination, destinationcity, journeydate,trainclass,numberofadults)
                    othermodesend2future = executor.submit(self.getothermodes, bigdestination, destinationcity, dateTimeUtility.getNextDate(journeydate),trainclass,numberofadults)

                if bigsource != sourceflight:
                    mixedflightendfuture = executor.submit(flightSkyScanner.getApiResults, bigsource, destinationflight, journeydate, "flight2", flightclass, numberofadults)
                    if not othermodesinitfuture:
                        othermodesinitfuture = executor.submit(self.getothermodes,sourcecity, bigsource, journeydate, trainclass,numberofadults)
                        othermodesinit2future = executor.submit(self.getothermodes, sourcecity, bigsource, dateTimeUtility.getPreviousDate(journeydate), trainclass, numberofadults)

                if bigdestination != destinationflight:
                    mixedflightinitfuture = executor.submit(flightSkyScanner.getApiResults,sourceflight,bigdestination,journeydate,"flight3",flightclass,numberofadults)
                    if not othermodesendfuture:
                        othermodesendfuture = executor.submit(self.getothermodes, bigdestination, destinationcity, journeydate,trainclass,numberofadults)
                        othermodesend2future = executor.submit(self.getothermodes, bigdestination, destinationcity, dateTimeUtility.getNextDate(journeydate),trainclass,numberofadults)

                onlyflight = onlyflightfuture.result()
                onlyflight = miscUtility.limitResults(onlyflight, "flight")
                if source != sourceflight and destination != destinationflight:
                    othermodessminit = othermodessminitfuture.result()
                    othermodessminit2 = othermodessminit2future.result()
                    othermodessmend = othermodessmendfuture.result()
                    othermodessmend2 = othermodessmend2future.result()
                    onlyflight = self.mixandmatch(onlyflight, othermodessminit,othermodessminit2, othermodessmend, othermodessmend2)
                elif source != sourceflight:
                    othermodessminit = othermodessminitfuture.result()
                    othermodessminit2 = othermodessminit2future.result()
                    onlyflight = self.mixAndMatchEnd(onlyflight, othermodessminit, othermodessminit2)
                elif destination != destinationflight:
                    othermodessmend = othermodessmendfuture.result()
                    othermodessmend2 = othermodessmend2future.result()
                    onlyflight = self.mixAndMatchInit(onlyflight, othermodessmend, othermodessmend2)

                if (bigsource != bigdestination) and ((bigsource != sourceflight) and (bigdestination != destinationflight)):
                    othermodesinit = othermodesinitfuture.result()
                    othermodesinit2 = othermodesinit2future.result()
                    othermodesend = othermodesendfuture.result()
                    othermodesend2 = othermodesend2future.result()
                    mixedflight = self.mixandmatch(mixedflightfuture.result(), othermodesinit,othermodesinit2, othermodesend,othermodesend2)

                if bigsource != sourceflight:
                    if not othermodesinit:
                        othermodesinit = othermodesinitfuture.result()
                        othermodesinit2 = othermodesinit2future.result()
                    if destination != destinationflight:
                        mixedflightend = self.mixandmatch(mixedflightendfuture.result(), othermodesinit, othermodesinit2, othermodessmend, othermodessmend2)
                    else:
                        mixedflightend = self.mixAndMatchEnd(mixedflightendfuture.result(), othermodesinit, othermodesinit2)

                if bigdestination != destinationflight:
                    if not othermodesend:
                        othermodesend = othermodesendfuture.result()
                        othermodesend2 = othermodesend2future.result()
                    if source != sourceflight:
                        mixedflightinit = self.mixandmatch(mixedflightinitfuture.result(), othermodessminit, othermodessminit2, othermodesend, othermodesend2)
                    else:
                        mixedflightinit = self.mixAndMatchInit(mixedflightinitfuture.result(), othermodesend,othermodesend2)

                finallist["flight"]=onlyflight["flight"]+mixedflight["flight"]+mixedflightinit["flight"]+mixedflightend["flight"]
            else:
                onlyflight = onlyflightfuture.result()
                onlyflight = miscUtility.limitResults(onlyflight, "flight")
                if source != sourceflight and destination != destinationflight:
                    othermodessminit = othermodessminitfuture.result()
                    othermodessminit2 = othermodessminit2future.result()
                    othermodessmend = othermodessmendfuture.result()
                    othermodessmend2 = othermodessmend2future.result()
                    onlyflight = self.mixandmatch(onlyflight, othermodessminit, othermodessminit2, othermodessmend, othermodessmend2)
                elif source != sourceflight:
                    othermodessminit = othermodessminitfuture.result()
                    othermodessminit2 = othermodessminit2future.result()
                    onlyflight = self.mixAndMatchEnd(onlyflight, othermodessminit, othermodessminit2)
                elif destination != destinationflight:
                    othermodessmend = othermodessmendfuture.result()
                    othermodessmend2 = othermodessmend2future.result()
                    onlyflight = self.mixAndMatchInit(onlyflight, othermodessmend, othermodessmend2)

                finallist["flight"] = onlyflight["flight"]
            logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)
            return finallist

    def getothermodes(self, source, destination, journeydate, trainclass='3A', numberofadults=1):

        traincontrollerneo = trainapineo4j.TrainController()
        logger.debug("[START] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
        resultjsondata = traincontrollerneo.getroutes(source, destination, journeydate, priceclass=trainclass, numberofadults=numberofadults)["train"]
        if not resultjsondata:
            logger.debug("No Data From Train,Retrieving From Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
            buscontroller = busapi.BusController()
            resultjsondata = buscontroller.getresults(source, destination, journeydate,numberofadults)["bus"]
        if not resultjsondata:
            logger.debug("No Data From Train and Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)

        logger.debug("[END] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)

        return resultjsondata

    def mixandmatch(self, mixedflight, othermodesinit, othermodesinit2, othermodesend, othermodesend2):
        logger.debug("[START]")
        othermodesend = othermodesend + othermodesend2
        othermodesinit = othermodesinit + othermodesinit2
        mixedflight = miscUtility.limitResults(mixedflight, "flight")
        for j in range(len(mixedflight["flight"])):
            flightpart = mixedflight["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(othermodesinit)):
                subpart = othermodesinit[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subpart["arrival"], subpart["arrivalDate"],flightpart["departure"], flightpart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"],flightpart["departure"],subpart["arrivalDate"],flightpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["departure"], flightpart["departureDate"], subpart["departureDate"])
                    subparts.append(copy.deepcopy(subpart))
            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]
            continueFurther = 0;
            if subparts:
                continueFurther=1
                minmax1 = minMaxUtil.getMinMaxValues(subparts)
                price1 = int(minMaxUtil.getprice(subparts[0]))
                subJourneyTime1 = subparts[0]["subJourneyTime"]
                waitingtime1 = subparts[0]["waitingTime"]
                departuredate1 = subparts[0]["departureDate"]
                departure1 = subparts[0]["departure"]
                source = subparts[0]["source"]
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflight["flight"][j]["full"][0]["id"] + str(0),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                flightpart["id"] = mixedflight["flight"][j]["full"][0]["id"] + str(1)
                mixedflight["flight"][j]["parts"].insert(0, newpart)
                mixedflight["flight"][j]["full"][0]["route"] = newpart["source"] + ","+newpart["mode"]+"," + newpart["destination"] + ",flight," + flightpart["destination"]
            subparts = []
            for k in range(len(othermodesend)):
                subpart = othermodesend[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(flightpart["arrival"], flightpart["arrivalDate"],subpart["departure"], subpart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightpart["arrival"], subpart["departure"],flightpart["arrivalDate"],subpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["arrivalDate"], flightpart["arrivalDate"])
                    subparts.append(copy.deepcopy(subpart))
            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]

            if subparts and continueFurther==1:
                minmax2 = minMaxUtil.getMinMaxValues(subparts)
                price2 = int(minMaxUtil.getprice(subparts[0]))
                destination = subparts[0]["destination"]
                duration2 = subparts[0]["duration"]
                subJourneyTime2 = subparts[0]["subJourneyTime"]
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflight["flight"][j]["full"][0]["id"] + str(2),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                mixedflight["flight"][j]["parts"].append(newpart)
                mixedflight["flight"][j]["full"][0]["route"] = mixedflight["flight"][j]["full"][0]["route"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                mixedflight["flight"][j]["full"][0]["price"] = int(mixedflight["flight"][j]["full"][0]["price"]) + price1 + price2
                mixedflight["flight"][j]["full"][0]["minPrice"] = int(mixedflight["flight"][j]["full"][0]["minPrice"]) + int(minmax1["minPrice"]) + int(minmax2["minPrice"])
                mixedflight["flight"][j]["full"][0]["maxPrice"] = int(mixedflight["flight"][j]["full"][0]["maxPrice"]) + int(minmax1["maxPrice"]) + int(minmax2["maxPrice"])
                mixedflight["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedflight["flight"][j]["full"][0]["duration"], subJourneyTime1),subJourneyTime2)
                mixedflight["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedflight["flight"][j]["full"][0]["minDuration"], minmax1["minDuration"]),minmax2["minDuration"])
                mixedflight["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedflight["flight"][j]["full"][0]["maxDuration"], minmax1["maxDuration"]),minmax2["maxDuration"])
                mixedflight["flight"][j]["full"][0]["minDeparture"] = minmax1["minDep"]
                mixedflight["flight"][j]["full"][0]["maxDeparture"] = minmax1["maxDep"]
                mixedflight["flight"][j]["full"][0]["minArrival"] = minmax2["minArr"]
                mixedflight["flight"][j]["full"][0]["maxArrival"] = minmax2["maxArr"]
                mixedflight["flight"][j]["full"][0]["destination"] = destination
                mixedflight["flight"][j]["full"][0]["source"] = source
                mixedflight["flight"][j]["full"][0]["waitingTime"] = dateTimeUtility.addDurations(waitingtime1, subparts[0]["waitingTime"])
                mixedflight["flight"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
                mixedflight["flight"][j]["full"][0]["departure"] = departure1
                mixedflight["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                mixedflight["flight"][j]["full"][0]["departureDate"] = departuredate1
                mixedflight["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
                mixedflight["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(departuredate1, 0)

        mixedflight["flight"] = [x for x in mixedflight["flight"] if len(x["parts"]) == 3]
        logger.debug("[END]")
        return mixedflight

    def mixAndMatchInit(self, mixedFlightInit, otherModesEnd,otherModesEnd2):

        """
        Join flight journey with other modes, with flight being first part of combined journey
        :param mixedFlightInit: flight part of journey
        :param otherModesEnd: other mode of journey
        :param otherModesEnd2: other mode of journey2
        :return: combined journey flight followed by other mode
        """
        logger.debug("[START]")
        mixedFlightInit = miscUtility.limitResults(mixedFlightInit,"flight")
        otherModesEnd=otherModesEnd+otherModesEnd2

        for j in range(len(mixedFlightInit["flight"])):
            flightpart = mixedFlightInit["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(otherModesEnd)):
                subpart = otherModesEnd[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(flightpart["arrival"],flightpart["arrivalDate"],subpart["departure"],subpart["departureDate"],3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightpart["arrival"],subpart["departure"],flightpart["arrivalDate"],subpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["arrivalDate"], flightpart["arrivalDate"])
                    subparts.append(copy.deepcopy(subpart))
            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedFlightInit["flight"][j]["full"][0]["id"] + str(1),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
                mixedFlightInit["flight"][j]["parts"].append(newpart)
                mixedFlightInit["flight"][j]["full"][0]["route"]=flightpart["source"]+",flight,"+flightpart["destination"]+","+subparts[0]["mode"]+","+newpart["destination"]
                mixedFlightInit["flight"][j]["full"][0]["price"] = int(mixedFlightInit["flight"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
                mixedFlightInit["flight"][j]["full"][0]["minPrice"] = int(mixedFlightInit["flight"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                mixedFlightInit["flight"][j]["full"][0]["maxPrice"] = int(mixedFlightInit["flight"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                mixedFlightInit["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
                mixedFlightInit["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedFlightInit["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedFlightInit["flight"][j]["full"][0]["minArrival"] = minmax["minArr"]
                mixedFlightInit["flight"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
                mixedFlightInit["flight"][j]["full"][0]["destination"] = subparts[0]["destination"]
                mixedFlightInit["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                mixedFlightInit["flight"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
                mixedFlightInit["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                mixedFlightInit["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
                mixedFlightInit["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(flightpart["departureDate"], 0)

        mixedFlightInit["flight"] = [x for x in mixedFlightInit["flight"] if len(x["parts"]) == 2]
        logger.debug("[FlightApi.mixAndMatchInit]-[END]")
        return mixedFlightInit

    def mixAndMatchEnd(self, mixedflightend, otherModesInit, otherModesInit2):

        """
        Join flight with other modes, with flight in the end
        :param mixedflightend: flight part of journey
        :param otherModesInit: other mode of journey
        :param otherModesInit2: other mode of jounrey2
        :return: combined journey with flight after other mode of total journey
        """
        logger.debug("[START]")
        mixedflightend = miscUtility.limitResults(mixedflightend, "flight")
        otherModesInit=otherModesInit+otherModesInit2
        for j in range(len(mixedflightend["flight"])):
            flightpart = mixedflightend["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(otherModesInit)):
                subpart = otherModesInit[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subpart["arrival"], subpart["arrivalDate"],flightpart["departure"], flightpart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], flightpart["departure"],subpart["arrivalDate"],flightpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["departure"], flightpart["departureDate"], subpart["departureDate"])
                    subparts.append(copy.deepcopy(subpart))

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortonsubjourneytime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflightend["flight"][j]["full"][0]["id"] + str(0), "destination": subparts[0]["destination"],
                           "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                flightpart["id"]=mixedflightend["flight"][j]["full"][0]["id"] + str(1)
                mixedflightend["flight"][j]["parts"].insert(0,newpart)
                mixedflightend["flight"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",flight," + flightpart["destination"]
                mixedflightend["flight"][j]["full"][0]["price"] = int(mixedflightend["flight"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
                mixedflightend["flight"][j]["full"][0]["minPrice"] = int(mixedflightend["flight"][j]["full"][0]["minPrice"]) +  int(minmax["minPrice"])
                mixedflightend["flight"][j]["full"][0]["maxPrice"] = int(mixedflightend["flight"][j]["full"][0]["maxPrice"] ) + int(minmax["maxPrice"])
                mixedflightend["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
                mixedflightend["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedflightend["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedflightend["flight"][j]["full"][0]["minDeparture"] = minmax["minDep"]
                mixedflightend["flight"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
                mixedflightend["flight"][j]["full"][0]["source"] = subparts[0]["source"]
                mixedflightend["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                mixedflightend["flight"][j]["full"][0]["departure"] = subparts[0]["departure"]
                mixedflightend["flight"][j]["full"][0]["departureDate"] = subparts[0]["departureDate"]
                mixedflightend["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(subparts[0]["departureDate"], 0)
                mixedflightend["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(flightpart["arrivalDate"], 0)

        mixedflightend["flight"] = [x for x in mixedflightend["flight"] if len(x["parts"]) == 2]
        logger.debug("[END]")
        return mixedflightend