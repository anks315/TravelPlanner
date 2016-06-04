__author__ = 'ankur'
import busapi
import json
import urllib2
import flightSkyScanner
import concurrent.futures
import dateTimeUtility
import miscUtility
import distanceutil
import trainapiNeo4j
import minMaxUtil
import logging
import loggerUtil


logger = loggerUtil.getLogger("FlightApi",logging.DEBUG)


class FlightController:
    """Class returns all stations corresponding to a city"""

    stationToCityMap = {'KUU':'Kullu','SLV':'Shimla','IXA':'Agartala','AGR':'Agra','AMD':'Ahmedabad','IXD':'Allahabad','ATQ':'Amritsar','IXU':'Aurangabad','IXB':'Bagdogra','BLR':'Bangalore','BHU':'Bhavnagar','BHO':'Bhopal','BBI':'Bhubaneswar','BHJ':'Bhuj','CCU':'Kolkata','IXC':'Chandigarh','MAA':'Chennai','COK':'Cochin','CJB':'Coimbatore','NMB':'Daman','DED':'Dehradun','DIB':'Dibrugarh','DMU':'Dimapur','DIU':'Diu','GAU':'Gauhati','GOI':'Goa','GWL':'Gwalior','HBX':'Hubli','HYD':'Hyderabad','IMF':'Imphal','IDR':'Indore','JAI':'Jaipur','IXJ':'Jammu','JGA':'Jamnagar','IXW':'Jamshedpur','JDH':'Jodhpur','JRH':'Jorhat','KNU':'Kanpur','HJR':'Khajuraho','CCJ':'Kozhikode','IXL':'Leh','LKO':'Lucknow','LUH':'Ludhiana','IXM':'Madurai','IXE':'Mangalore','BOM':'Mumbai','BOM':'Mumbai','NAG':'Nagpur','NDC':'Nanded','ISK':'Nasik','DEL':'Delhi','PAT':'Patna','PNY':'Pondicherry','PNQ':'Poona','PNQ':'Pune','PBD':'Porbandar','IXZ':'Port Blair','PUT':'PuttasubParthi','BEK':'Rae Bareli','RAJ':'Rajkot','IXR':'Ranchi','SHL':'Shillong','IXS':'Silchar','SXR':'Srinagar','STV':'Surat','TEZ':'Tezpur','TRZ':'Tiruchirapally','TIR':'Tirupati','TRV':'Trivandrum','UDR':'Udaipur','BDQ':'Vadodara','VNS':'Varanasi','VGA':'Vijayawada','VTZ': 'Vishakhapatnam'}

    def getResults(self, sourcecity,sourcestate, destinationcity,destinationstate, journeyDate):

        logger.debug("[START]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",sourcecity,destinationcity,journeyDate)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            flightCounter = 0
            source = sourcecity
            destination = destinationcity
            response = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+ source)
            sourceLatLong = json.loads(response.read())
            response.close()
            sourceLat = sourceLatLong["results"][0]["geometry"]["location"]["lat"]
            sourceLong = sourceLatLong["results"][0]["geometry"]["location"]["lng"]
            sourceAirport = distanceutil.findNearestAirport(sourceLat,sourceLong)
            bigSourceAirport = distanceutil.findNearestBigAirport(sourceLat,sourceLong)
            response2 = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + destination)
            destLatLong = json.loads(response2.read())
            destLat = destLatLong["results"][0]["geometry"]["location"]["lat"]
            destLong = destLatLong["results"][0]["geometry"]["location"]["lng"]
            destAirport = distanceutil.findNearestAirport(destLat, destLong)
            bigDestinationAirport = distanceutil.findNearestBigAirport(destLat, destLong)
            bigSource = FlightController.stationToCityMap[bigSourceAirport]
            bigDestination = FlightController.stationToCityMap[bigDestinationAirport]
            sourceFlight = FlightController.stationToCityMap[sourceAirport]
            destinationFlight = FlightController.stationToCityMap[destAirport]

            if(source!=sourceFlight):
                otherModesSmInitFuture = executor.submit(self.getOtherModes,sourcecity, sourceFlight, journeyDate)
                otherModesSmInit2Future = executor.submit(self.getOtherModes, sourcecity, sourceFlight, dateTimeUtility.getPreviousDate(journeyDate))
            if (destination != destinationFlight):
                otherModesSmEndFuture = executor.submit(self.getOtherModes, destinationFlight, destinationcity, journeyDate)
                otherModesSmEnd2Future = executor.submit(self.getOtherModes, destinationFlight, destinationcity,
                                                          dateTimeUtility.getNextDate(journeyDate))

            onlyFlightFuture = executor.submit(flightSkyScanner.getApiResults,sourceFlight,destinationFlight,journeyDate,"flight0")




            finalList = {}
            mixedFlight = {}
            if((bigSource!='empty')and(bigDestination!='empty')and(bigSource!=destinationFlight)and(bigDestination!=sourceFlight)):
                mixedFlight = {}
                mixedFlight["flight"] = []
                mixedFlightEnd = {}
                mixedFlightEnd["flight"] = []
                mixedFlightInit = {}
                mixedFlightInit["flight"] = []
                otherModesInit=[]
                otherModesEnd=[]
                otherModesInitFuture = []
                otherModesEndFuture = []
                #if there is only one big airport in between or both source and destination are big airports
                if((bigSource!=bigDestination) and ((bigSource != sourceFlight)and(bigDestination!=destinationFlight))):
                    mixedFlightFuture = executor.submit(flightSkyScanner.getApiResults,bigSource,bigDestination,journeyDate,"flight1")
                    otherModesInitFuture = executor.submit(self.getOtherModes, sourcecity, bigSource, journeyDate)
                    otherModesInit2Future = executor.submit(self.getOtherModes, sourcecity, bigSource, dateTimeUtility.getPreviousDate(journeyDate))
                    otherModesEndFuture = executor.submit(self.getOtherModes, bigDestination, destinationcity, journeyDate)
                    otherModesEnd2Future = executor.submit(self.getOtherModes, bigDestination, destinationcity,
                                                          dateTimeUtility.getNextDate(journeyDate))
                if (bigSource != sourceFlight):
                    mixedFlightEndFuture =executor.submit(flightSkyScanner.getApiResults,bigSource,destinationFlight,journeyDate,"flight2")
                    if otherModesInitFuture==[]:
                        otherModesInitFuture = executor.submit(self.getOtherModes,sourcecity, bigSource, journeyDate)
                        otherModesInit2Future = executor.submit(self.getOtherModes, sourcecity, bigSource,
                                                        dateTimeUtility.getPreviousDate(journeyDate))

                if (bigDestination != destinationFlight):
                    mixedFlightInitFuture =executor.submit(flightSkyScanner.getApiResults,sourceFlight,bigDestination,journeyDate,"flight3")
                    if otherModesEndFuture==[]:
                        otherModesEndFuture = executor.submit(self.getOtherModes,bigDestination, destinationcity, journeyDate)
                        otherModesEnd2Future = executor.submit(self.getOtherModes, bigDestination, destinationcity,
                                                       dateTimeUtility.getNextDate(journeyDate))
                onlyFlight = onlyFlightFuture.result()
                onlyFlight = miscUtility.limitResults(onlyFlight, "flight")
                if source != sourceFlight and destination !=destinationFlight:
                    otherModesSmInit = otherModesSmInitFuture.result()
                    otherModesSmInit2 = otherModesSmInit2Future.result()
                    otherModesSmEnd = otherModesSmEndFuture.result()
                    otherModesSmEnd2 = otherModesSmEnd2Future.result()
                    onlyFlight = self.mixAndMatch(onlyFlight, otherModesSmInit,otherModesSmInit2, otherModesSmEnd,otherModesSmEnd2)
                elif source != sourceFlight:
                    otherModesSmInit = otherModesSmInitFuture.result()
                    otherModesSmInit2 = otherModesSmInit2Future.result()
                    onlyFlight = self.mixAndMatchEnd(onlyFlight, otherModesSmInit, otherModesSmInit2)
                elif destination != destinationFlight:
                    otherModesSmEnd = otherModesSmEndFuture.result()
                    otherModesSmEnd2 = otherModesSmEnd2Future.result()
                    onlyFlight = self.mixAndMatchInit(onlyFlight, otherModesSmEnd, otherModesSmEnd2)


                if ((bigSource!=bigDestination) and ((bigSource != sourceFlight)and(bigDestination!=destinationFlight))):
                    otherModesInit=otherModesInitFuture.result()
                    otherModesInit2 = otherModesInit2Future.result()
                    otherModesEnd= otherModesEndFuture.result()
                    otherModesEnd2 = otherModesEnd2Future.result()
                    mixedFlight = self.mixAndMatch(mixedFlightFuture.result(), otherModesInit,otherModesInit2, otherModesEnd,otherModesEnd2)
                if(bigSource != sourceFlight):
                    if otherModesInit==[]:
                        otherModesInit = otherModesInitFuture.result()
                        otherModesInit2 = otherModesInit2Future.result()
                    if destination != destinationFlight:
                        mixedFlightEnd = self.mixAndMatch(mixedFlightEndFuture.result(), otherModesInit, otherModesInit2,
                                                   otherModesSmEnd, otherModesSmEnd2)
                    else:
                        mixedFlightEnd = self.mixAndMatchEnd(mixedFlightEndFuture.result(), otherModesInit, otherModesInit2)
                if(bigDestination != destinationFlight):
                    if otherModesEnd==[]:
                        otherModesEnd = otherModesEndFuture.result()
                        otherModesEnd2 = otherModesEnd2Future.result()
                    if source != sourceFlight:
                        mixedFlightInit = self.mixAndMatch(mixedFlightInitFuture.result(), otherModesSmInit,
                                                          otherModesSmInit2,
                                                           otherModesEnd, otherModesEnd2)
                    else:
                        mixedFlightInit = self.mixAndMatchInit(mixedFlightInitFuture.result(), otherModesEnd,otherModesEnd2)

                finalList["flight"]=onlyFlight["flight"]+mixedFlight["flight"]+mixedFlightInit["flight"]+mixedFlightEnd["flight"]
            else:
                onlyFlight = onlyFlightFuture.result()
                onlyFlight = miscUtility.limitResults(onlyFlight, "flight")
                if source != sourceFlight and destination != destinationFlight:
                    otherModesSmInit = otherModesSmInitFuture.result()
                    otherModesSmInit2 = otherModesSmInit2Future.result()
                    otherModesSmEnd = otherModesSmEndFuture.result()
                    otherModesSmEnd2 = otherModesSmEnd2Future.result()
                    onlyFlight = self.mixAndMatch(onlyFlight, otherModesSmInit, otherModesSmInit2, otherModesSmEnd,
                                                  otherModesSmEnd2)
                elif source != sourceFlight:
                    otherModesSmInit = otherModesSmInitFuture.result()
                    otherModesSmInit2 = otherModesSmInit2Future.result()
                    onlyFlight = self.mixAndMatchEnd(onlyFlight, otherModesSmInit, otherModesSmInit2)
                elif destination != destinationFlight:
                    otherModesSmEnd = otherModesSmEndFuture.result()
                    otherModesSmEnd2 = otherModesSmEnd2Future.result()
                    onlyFlight = self.mixAndMatchInit(onlyFlight, otherModesSmEnd, otherModesSmEnd2)

                finalList["flight"] = onlyFlight["flight"]
            logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",sourcecity,destinationcity,journeyDate)
            return finalList

    def getOtherModes(self, source,destination, journeyDate):

        trainControllerneo = trainapiNeo4j.TrainController()
        logger.debug("[START] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeyDate)
        resultJsonData = trainControllerneo.getRoutes(source, destination, journeyDate)["train"]
        if(resultJsonData==[]):
            logger.debug("No Data From Train,Retrieving From Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeyDate)
            busController = busapi.BusController()
            resultJsonData = busController.getResults(source, destination, journeyDate)["bus"]
        if(resultJsonData==[]):
            logger.debug("No Data From Train and Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeyDate)

        logger.debug("[END] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeyDate)

        return resultJsonData

    def mixAndMatch(self, mixedFlight,otherModesInit,otherModesInit2,otherModesEnd,otherModesEnd2):
        logger.debug("[START]")
        otherModesEnd = otherModesEnd + otherModesEnd2
        otherModesInit = otherModesInit + otherModesInit2

        for j in range(len(mixedFlight["flight"])):
                flightPart = mixedFlight["flight"][j]["parts"][0]
                subparts = []
                for k in range(len(otherModesInit)):
                    subpart = otherModesInit[k]["parts"][0]
                    if dateTimeUtility.checkIfApplicable(subpart["arrival"], subpart["arrivalDate"],flightPart["departure"], flightPart["departureDate"], 3):
                        subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"],flightPart["departure"],subpart["arrivalDate"],flightPart["departureDate"])
                        subparts.append(subpart)
                if len(subparts) > 5:
                    subparts.sort(miscUtility.sortOnWaitingTime)
                    subparts = subparts[0:5]
                continueFurther = 0;
                if subparts:
                    continueFurther=1
                    minmax1 = minMaxUtil.getMinMaxValues(subparts)
                    newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedFlight["flight"][j]["full"][0]["id"] + str(0),
                               "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                    flightPart["id"] = mixedFlight["flight"][j]["full"][0]["id"] + str(1)
                    mixedFlight["flight"][j]["parts"].insert(0, newpart)
                    mixedFlight["flight"][j]["full"][0]["route"] = newpart["source"] + ","+newpart["mode"]+"," + newpart["destination"] + ",flight," + flightPart["destination"]
                subparts = []
                for k in range(len(otherModesEnd)):
                    subpart = otherModesEnd[k]["parts"][0]
                    if dateTimeUtility.checkIfApplicable(flightPart["arrival"], flightPart["arrivalDate"],subpart["departure"], subpart["departureDate"], 3):
                        subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightPart["arrival"], subpart["departure"],flightPart["arrivalDate"],subpart["departureDate"])
                        subparts.append(subpart)
                if len(subparts) > 5:
                    subparts.sort(miscUtility.sortOnWaitingTime)
                    subparts = subparts[0:5]

                if subparts and continueFurther==1:
                    minmax2 = minMaxUtil.getMinMaxValues(subparts)
                    newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedFlight["flight"][j]["full"][0]["id"] + str(2),
                               "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                    mixedFlight["flight"][j]["parts"].append(newpart)
                    mixedFlight["flight"][j]["full"][0]["route"] = mixedFlight["flight"][j]["full"][0]["route"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                    mixedFlight["flight"][j]["full"][0]["price"] = int(mixedFlight["flight"][j]["full"][0]["price"]) + int(minmax1["minPrice"]) + int(minmax2["minPrice"])
                    mixedFlight["flight"][j]["full"][0]["minPrice"] = int(mixedFlight["flight"][j]["full"][0]["minPrice"]) + int(minmax1["minPrice"]) + int(minmax2["minPrice"])
                    mixedFlight["flight"][j]["full"][0]["maxPrice"] = int(mixedFlight["flight"][j]["full"][0]["maxPrice"]) + int(minmax1["maxPrice"]) + int(minmax2["maxPrice"])
                    mixedFlight["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedFlight["flight"][j]["full"][0]["duration"], minmax1["minDuration"]),minmax2["minDuration"])
                    mixedFlight["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedFlight["flight"][j]["full"][0]["minDuration"], minmax1["minDuration"]),minmax2["minDuration"])
                    mixedFlight["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedFlight["flight"][j]["full"][0]["maxDuration"], minmax1["maxDuration"]),minmax2["maxDuration"])
                    mixedFlight["flight"][j]["full"][0]["minDeparture"] = minmax1["minDep"]
                    mixedFlight["flight"][j]["full"][0]["maxDeparture"] = minmax1["maxDep"]
                    mixedFlight["flight"][j]["full"][0]["minArrival"] = minmax2["minArr"]
                    mixedFlight["flight"][j]["full"][0]["maxArrival"] = minmax2["maxArr"]
        mixedFlight["flight"] = [x for x in mixedFlight["flight"] if len(x["parts"]) == 3]
        logger.debug("[END]")
        return mixedFlight

    def mixAndMatchInit(self, mixedFlightInit, otherModesEnd,otherModesEnd2):
        logger.debug("[START]")
        mixedFlightInit = miscUtility.limitResults(mixedFlightInit,"flight")
        otherModesEnd=otherModesEnd+otherModesEnd2

        for j in range(len(mixedFlightInit["flight"])):
            flightPart = mixedFlightInit["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(otherModesEnd)):
                subpart = otherModesEnd[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(flightPart["arrival"],flightPart["arrivalDate"],subpart["departure"],subpart["departureDate"],3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightPart["arrival"],subpart["departure"],flightPart["arrivalDate"],subpart["departureDate"])
                    subparts.append(subpart)
            if len(subparts) > 5:
                subparts.sort(miscUtility.sortOnWaitingTime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedFlightInit["flight"][j]["full"][0]["id"] + str(1),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
                mixedFlightInit["flight"][j]["parts"].append(newpart)
                mixedFlightInit["flight"][j]["full"][0]["route"]=flightPart["source"]+",flight,"+flightPart["destination"]+","+subparts[0]["mode"]+","+newpart["destination"]
                mixedFlightInit["flight"][j]["full"][0]["price"] = int(mixedFlightInit["flight"][j]["full"][0]["price"]) + int(minmax["minPrice"])
                mixedFlightInit["flight"][j]["full"][0]["minPrice"] = int(mixedFlightInit["flight"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
                mixedFlightInit["flight"][j]["full"][0]["maxPrice"] = int(mixedFlightInit["flight"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
                mixedFlightInit["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["duration"], minmax["minDuration"])
                mixedFlightInit["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedFlightInit["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedFlightInit["flight"][j]["full"][0]["minArrival"] = minmax["minArr"]
                mixedFlightInit["flight"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
        mixedFlightInit["flight"] = [x for x in mixedFlightInit["flight"] if len(x["parts"]) == 2]
        logger.debug("[FlightApi.mixAndMatchInit]-[END]")
        return mixedFlightInit

    def mixAndMatchEnd(self, mixedFlightEnd, otherModesInit,otherModesInit2):
        logger.debug("[START]")
        mixedFlightEnd = miscUtility.limitResults(mixedFlightEnd, "flight")
        otherModesInit=otherModesInit+otherModesInit2
        for j in range(len(mixedFlightEnd["flight"])):
            flightPart = mixedFlightEnd["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(otherModesInit)):
                subpart = otherModesInit[k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subpart["arrival"], subpart["arrivalDate"],flightPart["departure"], flightPart["departureDate"], 3):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], flightPart["departure"],subpart["arrivalDate"],flightPart["departureDate"])
                    subparts.append(subpart)

            if len(subparts) > 5:
                subparts.sort(miscUtility.sortOnWaitingTime)
                subparts = subparts[0:5]

            if subparts:
                minmax = minMaxUtil.getMinMaxValues(subparts)
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedFlightEnd["flight"][j]["full"][0]["id"] + str(0),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                flightPart["id"]=mixedFlightEnd["flight"][j]["full"][0]["id"] + str(1)
                mixedFlightEnd["flight"][j]["parts"].insert(0,newpart)
                mixedFlightEnd["flight"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",flight," + flightPart["destination"]
                mixedFlightEnd["flight"][j]["full"][0]["price"] = int(mixedFlightEnd["flight"][j]["full"][0]["price"]) + int(minmax["minPrice"])
                mixedFlightEnd["flight"][j]["full"][0]["minPrice"] = int(mixedFlightEnd["flight"][j]["full"][0]["minPrice"]) +  int(minmax["minPrice"])
                mixedFlightEnd["flight"][j]["full"][0]["maxPrice"] = int(mixedFlightEnd["flight"][j]["full"][0]["maxPrice"] ) + int(minmax["maxPrice"])
                mixedFlightEnd["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedFlightEnd["flight"][j]["full"][0]["duration"], minmax["minDuration"])
                mixedFlightEnd["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedFlightEnd["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedFlightEnd["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedFlightEnd["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedFlightEnd["flight"][j]["full"][0]["minDeparture"] = minmax["minDep"]
                mixedFlightEnd["flight"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
        mixedFlightEnd["flight"] = [x for x in mixedFlightEnd["flight"] if len(x["parts"]) == 2]
        logger.debug("[END]")
        return mixedFlightEnd


