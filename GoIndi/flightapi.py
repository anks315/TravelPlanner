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
import logging, copy
import loggerUtil, models
import TravelPlanner.trainUtil


logger = loggerUtil.getLogger("FlightApi",logging.WARNING)


class FlightController:
    """Class returns all stations corresponding to a city"""

    stationToCityMap = {'JSA':'Jaisalmer','RJA':'Rajahmundry','PGH':'Pantnagar','IXP':'Pathankot','KUU':'Kullu','SLV':'Shimla','IXA':'Agartala','AGR':'Agra','AMD':'Ahmedabad','IXD':'Allahabad','ATQ':'Amritsar','IXU':'Aurangabad','IXB':'Bagdogra','BLR':'Bangalore','BHU':'Bhavnagar','BHO':'Bhopal','BBI':'Bhubaneswar','BHJ':'Bhuj','CCU':'Kolkata','IXC':'Chandigarh','MAA':'Chennai','COK':'Cochin','CJB':'Coimbatore','NMB':'Daman','DED':'Dehradun','DIB':'Dibrugarh','DMU':'Dimapur','DIU':'Diu','GAU':'Gauhati','GOI':'Goa','GWL':'Gwalior','HBX':'Hubli','HYD':'Hyderabad','IMF':'Imphal','IDR':'Indore','JAI':'Jaipur','IXJ':'Jammu','JGA':'Jamnagar','IXW':'Jamshedpur','JDH':'Jodhpur','JRH':'Jorhat','KNU':'Kanpur','HJR':'Khajuraho','CCJ':'Kozhikode','IXL':'Leh','LKO':'Lucknow','LUH':'Ludhiana','IXM':'Madurai','IXE':'Mangalore','BOM':'Mumbai','NAG':'Nagpur','NDC':'Nanded','ISK':'Nasik','DEL':'New Delhi','PAT':'Patna','PNY':'Pondicherry','PNQ':'Poona','PNQ':'Pune','PBD':'Porbandar','IXZ':'Port Blair','PUT':'PuttasubParthi','BEK':'Rae Bareli','RAJ':'Rajkot','IXR':'Ranchi','SHL':'Shillong','IXS':'Silchar','SXR':'Srinagar','STV':'Surat','TEZ':'Tezpur','TRZ':'Tiruchirapally','TIR':'Tirupati','TRV':'Trivandrum','UDR':'Udaipur','BDQ':'Vadodara','VNS':'Varanasi','VGA':'Vijayawada','VTZ': 'Vishakhapatnam'}

    def getResults(self, sourcecity,sourcestate, destinationcity,destinationstate, journeyDate,trainClass,flightClass,numberOfAdults):

        logger.debug("[START]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",sourcecity,destinationcity,journeyDate)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + source
            url = url.replace(' ', '%20')
            response = urllib2.urlopen(url)
            sourceLatLong = json.loads(response.read())
            response.close()
            sourceLat = sourceLatLong["results"][0]["geometry"]["location"]["lat"]
            sourceLong = sourceLatLong["results"][0]["geometry"]["location"]["lng"]
            sourceAirport = distanceutil.findNearestAirport(sourceLat,sourceLong)
            bigSourceAirport = distanceutil.findNearestBigAirport(sourceLat,sourceLong)
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination
            url = url.replace(' ', '%20')
            response2 = urllib2.urlopen(url)
            destLatLong = json.loads(response2.read())
            destLat = destLatLong["results"][0]["geometry"]["location"]["lat"]
            destLong = destLatLong["results"][0]["geometry"]["location"]["lng"]
            destAirport = distanceutil.findNearestAirport(destLat, destLong)
            bigDestinationAirport = distanceutil.findNearestBigAirport(destLat, destLong)
            bigSource = FlightController.stationToCityMap[bigSourceAirport]
            bigDestination = FlightController.stationToCityMap[bigDestinationAirport]
            sourceFlight = FlightController.stationToCityMap[sourceAirport]
            destinationFlight = FlightController.stationToCityMap[destAirport]

            if source!=sourceFlight:
                othermodessminitfuture = executor.submit(self.getothermodes,sourcecity, sourceFlight, journeyDate,trainClass,numberOfAdults)
                othermodessminit2future = executor.submit(self.getothermodes, sourcecity, sourceFlight, dateTimeUtility.getPreviousDate(journeyDate),trainClass,numberOfAdults)
            if destination != destinationFlight:
                othermodessmendfuture = executor.submit(self.getothermodes, destinationFlight, destinationcity, journeyDate,trainClass,numberOfAdults)
                othermodessmend2future = executor.submit(self.getothermodes, destinationFlight, destinationcity, dateTimeUtility.getNextDate(journeyDate),trainClass,numberOfAdults)

            onlyflightfuture = executor.submit(flightSkyScanner.getApiResults,sourceFlight,destinationFlight,journeyDate,"flight0",flightClass,numberOfAdults)




            finalList = {}
            mixedFlight = {}
            if (bigSource!='empty')and(bigDestination!='empty')and(bigSource!=destinationFlight)and(bigDestination!=sourceFlight):
                mixedFlight = {"flight": []}
                mixedFlightEnd = {"flight": []}
                mixedFlightInit = {"flight": []}
                otherModesInit=[]
                otherModesEnd=[]
                otherModesInitFuture = []
                otherModesEndFuture = []
                #if there is only one big airport in between or both source and destination are big airports
                if((bigSource!=bigDestination) and ((bigSource != sourceFlight)and(bigDestination!=destinationFlight))):
                    mixedFlightFuture = executor.submit(flightSkyScanner.getApiResults,bigSource,bigDestination,journeyDate,"flight1",flightClass,numberOfAdults)
                    otherModesInitFuture = executor.submit(self.getothermodes, sourcecity, bigSource, journeyDate,trainClass,numberOfAdults)
                    otherModesInit2Future = executor.submit(self.getothermodes, sourcecity, bigSource, dateTimeUtility.getPreviousDate(journeyDate),trainClass,numberOfAdults)
                    otherModesEndFuture = executor.submit(self.getothermodes, bigDestination, destinationcity, journeyDate,trainClass,numberOfAdults)
                    otherModesEnd2Future = executor.submit(self.getothermodes, bigDestination, destinationcity,
                                                          dateTimeUtility.getNextDate(journeyDate),trainClass,numberOfAdults)
                if (bigSource != sourceFlight):
                    mixedFlightEndFuture =executor.submit(flightSkyScanner.getApiResults,bigSource,destinationFlight,journeyDate,"flight2",flightClass,numberOfAdults)
                    if otherModesInitFuture==[]:
                        otherModesInitFuture = executor.submit(self.getothermodes,sourcecity, bigSource, journeyDate,trainClass,numberOfAdults)
                        otherModesInit2Future = executor.submit(self.getothermodes, sourcecity, bigSource,
                                                        dateTimeUtility.getPreviousDate(journeyDate),trainClass,numberOfAdults)

                if (bigDestination != destinationFlight):
                    mixedFlightInitFuture =executor.submit(flightSkyScanner.getApiResults,sourceFlight,bigDestination,journeyDate,"flight3",flightClass,numberOfAdults)
                    if otherModesEndFuture==[]:
                        otherModesEndFuture = executor.submit(self.getothermodes,bigDestination, destinationcity, journeyDate,trainClass,numberOfAdults)
                        otherModesEnd2Future = executor.submit(self.getothermodes, bigDestination, destinationcity,
                                                       dateTimeUtility.getNextDate(journeyDate),trainClass,numberOfAdults)
                onlyFlight = onlyflightfuture.result()
                onlyFlight = miscUtility.limitResults(onlyFlight, "flight")
                if source != sourceFlight and destination !=destinationFlight:
                    otherModesSmInit = othermodessminitfuture.result()
                    otherModesSmInit2 = othermodessminit2future.result()
                    otherModesSmEnd = othermodessmendfuture.result()
                    otherModesSmEnd2 = othermodessmend2future.result()
                    onlyFlight = self.mixandmatch(onlyFlight, otherModesSmInit,otherModesSmInit2, otherModesSmEnd,otherModesSmEnd2)
                elif source != sourceFlight:
                    otherModesSmInit = othermodessminitfuture.result()
                    otherModesSmInit2 = othermodessminit2future.result()
                    onlyFlight = self.mixAndMatchEnd(onlyFlight, otherModesSmInit, otherModesSmInit2)
                elif destination != destinationFlight:
                    otherModesSmEnd = othermodessmendfuture.result()
                    otherModesSmEnd2 = othermodessmend2future.result()
                    onlyFlight = self.mixAndMatchInit(onlyFlight, otherModesSmEnd, otherModesSmEnd2)


                if ((bigSource!=bigDestination) and ((bigSource != sourceFlight)and(bigDestination!=destinationFlight))):
                    otherModesInit=otherModesInitFuture.result()
                    otherModesInit2 = otherModesInit2Future.result()
                    otherModesEnd= otherModesEndFuture.result()
                    otherModesEnd2 = otherModesEnd2Future.result()
                    mixedFlight = self.mixandmatch(mixedFlightFuture.result(), otherModesInit,otherModesInit2, otherModesEnd,otherModesEnd2)
                if(bigSource != sourceFlight):
                    if otherModesInit==[]:
                        otherModesInit = otherModesInitFuture.result()
                        otherModesInit2 = otherModesInit2Future.result()
                    if destination != destinationFlight:
                        mixedFlightEnd = self.mixandmatch(mixedFlightEndFuture.result(), otherModesInit, otherModesInit2,
                                                   otherModesSmEnd, otherModesSmEnd2)
                    else:
                        mixedFlightEnd = self.mixAndMatchEnd(mixedFlightEndFuture.result(), otherModesInit, otherModesInit2)
                if(bigDestination != destinationFlight):
                    if otherModesEnd==[]:
                        otherModesEnd = otherModesEndFuture.result()
                        otherModesEnd2 = otherModesEnd2Future.result()
                    if source != sourceFlight:
                        mixedFlightInit = self.mixandmatch(mixedFlightInitFuture.result(), otherModesSmInit,
                                                          otherModesSmInit2,
                                                           otherModesEnd, otherModesEnd2)
                    else:
                        mixedFlightInit = self.mixAndMatchInit(mixedFlightInitFuture.result(), otherModesEnd,otherModesEnd2)

                finalList["flight"]=onlyFlight["flight"]+mixedFlight["flight"]+mixedFlightInit["flight"]+mixedFlightEnd["flight"]
            else:
                onlyFlight = onlyflightfuture.result()
                onlyFlight = miscUtility.limitResults(onlyFlight, "flight")
                if source != sourceFlight and destination != destinationFlight:
                    otherModesSmInit = othermodessminitfuture.result()
                    otherModesSmInit2 = othermodessminit2future.result()
                    otherModesSmEnd = othermodessmendfuture.result()
                    otherModesSmEnd2 = othermodessmend2future.result()
                    onlyFlight = self.mixandmatch(onlyFlight, otherModesSmInit, otherModesSmInit2, otherModesSmEnd,
                                                  otherModesSmEnd2)
                elif source != sourceFlight:
                    otherModesSmInit = othermodessminitfuture.result()
                    otherModesSmInit2 = othermodessminit2future.result()
                    onlyFlight = self.mixAndMatchEnd(onlyFlight, otherModesSmInit, otherModesSmInit2)
                elif destination != destinationFlight:
                    otherModesSmEnd = othermodessmendfuture.result()
                    otherModesSmEnd2 = othermodessmend2future.result()
                    onlyFlight = self.mixAndMatchInit(onlyFlight, otherModesSmEnd, otherModesSmEnd2)

                finalList["flight"] = onlyFlight["flight"]
            logger.debug("[END]-Get Results From FlightApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",sourcecity,destinationcity,journeyDate)
            return finalList

    def getothermodes(self, source,destination, journeydate,trainClass='3A',numberOfAdults=1):

        traincontrollerneo = trainapiNeo4j.TrainController()
        logger.debug("[START] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
        resultjsondata = traincontrollerneo.getroutes(source, destination, journeydate, priceclass=trainClass,
                                                      numberofadults=numberOfAdults)["train"]
        if not resultjsondata:
            logger.debug("No Data From Train,Retrieving From Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
            buscontroller = busapi.BusController()
            resultjsondata = buscontroller.getResults(source, destination, journeydate,numberOfAdults)["bus"]
        if not resultjsondata:
            logger.debug("No Data From Train and Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)

        logger.debug("[END] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)

        return resultjsondata

    def mixandmatch(self, mixedflight,otherModesInit,otherModesInit2,otherModesEnd,otherModesEnd2):
        logger.debug("[START]")
        otherModesEnd = otherModesEnd + otherModesEnd2
        otherModesInit = otherModesInit + otherModesInit2
        mixedflight = miscUtility.limitResults(mixedflight, "flight")
        for j in range(len(mixedflight["flight"])):
            flightpart = mixedflight["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(otherModesInit)):
                subpart = otherModesInit[k]["parts"][0]
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
                duration1 = subparts[0]["duration"]
                waitingtime1 = subparts[0]["waitingTime"]
                departuredate1 = subpart[0]["departureDate"]
                source = subparts[0]["source"]
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflight["flight"][j]["full"][0]["id"] + str(0),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                flightpart["id"] = mixedflight["flight"][j]["full"][0]["id"] + str(1)
                mixedflight["flight"][j]["parts"].insert(0, newpart)
                mixedflight["flight"][j]["full"][0]["route"] = newpart["source"] + ","+newpart["mode"]+"," + newpart["destination"] + ",flight," + flightpart["destination"]
            subparts = []
            for k in range(len(otherModesEnd)):
                subpart = otherModesEnd[k]["parts"][0]
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
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflight["flight"][j]["full"][0]["id"] + str(2),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                mixedflight["flight"][j]["parts"].append(newpart)
                mixedflight["flight"][j]["full"][0]["route"] = mixedflight["flight"][j]["full"][0]["route"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                mixedflight["flight"][j]["full"][0]["price"] = int(mixedflight["flight"][j]["full"][0]["price"]) + price1 + price2
                mixedflight["flight"][j]["full"][0]["minPrice"] = int(mixedflight["flight"][j]["full"][0]["minPrice"]) + int(minmax1["minPrice"]) + int(minmax2["minPrice"])
                mixedflight["flight"][j]["full"][0]["maxPrice"] = int(mixedflight["flight"][j]["full"][0]["maxPrice"]) + int(minmax1["maxPrice"]) + int(minmax2["maxPrice"])
                mixedflight["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(mixedflight["flight"][j]["full"][0]["duration"], duration1),duration2)
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
                mixedflight["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                mixedflight["flight"][j]["full"][0]["departureDate"] = departuredate1
                mixedflight["flight"][j]["full"][0]["arrivalDay"] = models.getdayfromdate(subparts[0]["arrivalDate"], 0)
                mixedflight["flight"][j]["full"][0]["departureDay"] = models.getdayfromdate(departuredate1, 0)

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
                mixedFlightInit["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["duration"], subparts[0]["duration"])
                mixedFlightInit["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedFlightInit["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedFlightInit["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedFlightInit["flight"][j]["full"][0]["minArrival"] = minmax["minArr"]
                mixedFlightInit["flight"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
                mixedFlightInit["flight"][j]["full"][0]["destination"] = subparts[0]["destination"]
                mixedFlightInit["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                mixedFlightInit["flight"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
                mixedFlightInit["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                mixedFlightInit["flight"][j]["full"][0]["arrivalDay"] = models.getdayfromdate(subparts[0]["arrivalDate"], 0)
                mixedFlightInit["flight"][j]["full"][0]["departureDay"] = models.getdayfromdate(flightpart["departureDate"], 0)

        mixedFlightInit["flight"] = [x for x in mixedFlightInit["flight"] if len(x["parts"]) == 2]
        logger.debug("[FlightApi.mixAndMatchInit]-[END]")
        return mixedFlightInit

    def mixAndMatchEnd(self, mixedflightend, otherModesInit,otherModesInit2):

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
                mixedflightend["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["duration"], subparts[0]["duration"])
                mixedflightend["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
                mixedflightend["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
                mixedflightend["flight"][j]["full"][0]["minDeparture"] = minmax["minDep"]
                mixedflightend["flight"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
                mixedflightend["flight"][j]["full"][0]["source"] = subparts[0]["source"]
                mixedflightend["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
                mixedflightend["flight"][j]["full"][0]["departure"] = subparts[0]["departure"]
                mixedflightend["flight"][j]["full"][0]["departureDate"] = subparts[0]["departureDate"]
                mixedflightend["flight"][j]["full"][0]["departureDay"] = models.getdayfromdate(subparts[0]["departureDate"], 0)
                mixedflightend["flight"][j]["full"][0]["arrivalDay"] = models.getdayfromdate(flightpart["arrivalDate"], 0)

        mixedflightend["flight"] = [x for x in mixedflightend["flight"] if len(x["parts"]) == 2]
        logger.debug("[END]")
        return mixedflightend


