__author__ = 'ankur'
import busapi
import json
import urllib2
from django.http import HttpResponse
import time
import flightSkyScanner
import concurrent.futures
import dateTimeUtility
import miscUtility
class FlightController:
    """Class returns all stations corresponding to a city"""


    cityAndStateToStationsMap={'Agartala':'IXA','Agra':'AGR','Ahmedabad':'AMD','Allahabad':'IXD','Amritsar':'ATQ','Aurangabad':'IXU','Bagdogra':'IXB','Bangalore':'BLR','Bhavnagar':'BHU','Bhopal':'BHO','Bhubaneswar':'BBI','Bhuj':'BHJ','Calcutta':'CCU','Kolkata':'CCU','Chandigarh':'IXC','Chennai':'MAA','Madras':'MAA','Cochin':'COK','Coimbatore':'CJB','Daman':'NMB','Dehradun':'DED','Dibrugarh':'DIB','Dimapur':'DMU','Diu':'DIU','Gauhati':'GAU','Goa':'GOI','Gwalior':'GWL','Hubli':'HBX','Hyderabad':'HYD','Imphal':'IMF','Indore':'IDR','Jaipur':'JAI','Jammu':'IXJ','Jamnagar':'JGA','Jamshedpur':'IXW','Jodhpur':'JDH','Jorhat':'JRH','Kanpur':'KNU','Khajuraho':'HJR','Kozhikode':'CCJ','calicut':'CCJ','Leh':'IXL','Lucknow':'LKO','Ludhiana':'LUH','Madurai':'IXM','Mangalore':'IXE','Mumbai':'BOM','Bombay':'BOM','Nagpur':'NAG','Nanded':'NDC','Nasik':'ISK','New Delhi':'DEL','Delhi':'DEL','Patna':'PAT','Pondicherry':'PNY','Poona':'PNQ','Pune':'PNQ','Porbandar':'PBD','Port Blair':'IXZ','PuttasubParthi':'PUT','Rae Bareli':'BEK','Rajkot':'RAJ','Ranchi':'IXR','Shillong':'SHL','Silchar':'IXS','Srinagar':'SXR','Surat':'STV','Tezpur':'TEZ','Tiruchirapally':'TRZ','Tirupati':'TIR','Trivandrum':'TRV','Udaipur':'UDR','Vadodara':'BDQ','Varanasi':'VNS','Vijayawada':'VGA','Vishakhapatnam':'VTZ','Gurgaon':'DEL','Noida':'DEL','Ghaziabad':'DEL','Tripura':'IXA','Uttar Pradesh':'AGR','Gujarat':'AMD','Uttar Pradesh':'IXD','Punjab':'ATQ','Maharashtra':'IXU','Sikkim':'IXB','Karnataka':'BLR','Gujarat':'BHU','Madhya Pradesh':'BHO','Orissa':'BBI','Gujarat':'BHJ','West Bengal':'CCU','Chandigarh':'IXC','Tamil Nadu':'MAA','Kerala':'COK','Coimbatore':'CJB','Daman':'NMB','Uttar Pradesh':'DED','Assam':'DIB','Nagaland':'DMU','Daman and Diu':'DIU','Assam':'GAU','Goa':'GOI','Madhya Pradesh':'GWL','Karnataka':'HBX','Andhra Pradesh':'HYD','Manipur':'IMF','Madhya Pradesh':'IDR','Rajasthan':'JAI','Jammu & Kashmir':'IXJ','Gujarat':'JGA','Jharkhand':'IXW','Rajasthan':'JDH','Assam':'JRH','Uttar Pradesh':'KNU','Madhya Pradesh':'HJR','Kerala':'CCJ','Jammu & Kashmir':'IXL','Utter Pradesh':'LKO','Punjab':'LUH','Tamil Nadu':'IXM','Karnataka':'IXE','Maharashtra':'BOM','Maharashtra':'NDC','Maharashtra':'ISK','Delhi':'DEL','Bihar':'PAT','Maharashtra':'PNQ','Gujarat':'PBD','Andaman and Nicobar Islands':'IXZ','Andhra Pradesh':'PUT','Uttar Pradesh':'BEK','Gujarat':'RAJ','Jharkhand':'IXR','Meghalaya':'SHL','Mizoram':'IXS','J & K':'SXR','Gujrat':'STV','Assam':'TEZ','Tamil Nadu':'TRZ','Andhra Pradesh':'TIR','Kerala':'TRV','Rajasthan':'UDR','Gujarat':'BDQ','Uttar Pradesh':'VNS','Andhra Pradesh':'VGA','Andhra Pradesh':'VTZ'}
    nearestBigAirportMap={'Jammu':'Delhi','Mangalore':'Bangalore','Delhi':'Delhi','Bangalore':'Bangalore'}

    def getResults(self, sourcecity,sourcestate, destinationcity,destinationstate, journeyDate):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            flightCounter = 0
            source = sourcecity
            destination = destinationcity

            onlyFlightFuture = executor.submit(flightSkyScanner.getApiResults,source,destination,journeyDate,"flight0")

            if sourcecity in FlightController.nearestBigAirportMap.keys():
                bigSource = FlightController.nearestBigAirportMap[sourcecity]
            else:
                bigSource='empty'
            if destinationcity in FlightController.nearestBigAirportMap.keys():
                 bigDestination = FlightController.nearestBigAirportMap[destinationcity]
            else:
                bigDestination='empty'
            finalList = {}
            mixedFlight = {}
            if((bigSource!='empty')and(bigDestination!='empty')and(bigSource!=destination)and(bigDestination!=source)):
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
                if((bigSource!=bigDestination) and ((bigSource != source)and(bigDestination!=destination))):
                    mixedFlightFuture = executor.submit(flightSkyScanner.getApiResults,bigSource,bigDestination,journeyDate,"flight1")
                    otherModesInitFuture = executor.submit(self.getOtherModes, sourcecity, bigSource, journeyDate)
                    otherModesInit2Future = executor.submit(self.getOtherModes, sourcecity, bigSource, dateTimeUtility.getPreviousDate(journeyDate))
                    otherModesEndFuture = executor.submit(self.getOtherModes, bigDestination, destinationcity, journeyDate)
                    otherModesEnd2Future = executor.submit(self.getOtherModes, bigDestination, destinationcity,
                                                          dateTimeUtility.getNextDate(journeyDate))
                if (bigSource != source):
                    mixedFlightEndFuture =executor.submit(flightSkyScanner.getApiResults,bigSource,destination,journeyDate,"flight2")
                    if otherModesInitFuture==[]:
                        otherModesInitFuture = executor.submit(self.getOtherModes,sourcecity, bigSource, journeyDate)
                        otherModesInit2Future = executor.submit(self.getOtherModes, sourcecity, bigSource,
                                                        dateTimeUtility.getPreviousDate(journeyDate))

                if (bigDestination != destination):
                    mixedFlightInitFuture =executor.submit(flightSkyScanner.getApiResults,source,bigDestination,journeyDate,"flight3")
                    if otherModesEndFuture==[]:
                        otherModesEndFuture = executor.submit(self.getOtherModes,bigDestination, destinationcity, journeyDate)
                        otherModesEnd2Future = executor.submit(self.getOtherModes, bigDestination, destinationcity,
                                                       dateTimeUtility.getNextDate(journeyDate))
                onlyFlight = onlyFlightFuture.result()
                if ((bigSource!=bigDestination) and ((bigSource != source)and(bigDestination!=destination))):
                    otherModesInit=otherModesInitFuture.result()
                    otherModesInit2 = otherModesInit2Future.result()
                    otherModesEnd= otherModesEndFuture.result()
                    otherModesEnd2 = otherModesEnd2Future.result()
                    mixedFlight = self.mixAndMatch(mixedFlightFuture.result(), otherModesInit,otherModesInit2, otherModesEnd,otherModesEnd2)
                if(bigSource != source):
                    if otherModesInit==[]:
                        otherModesInit = otherModesInitFuture.result()
                        otherModesInit2 = otherModesInit2Future.result()
                    mixedFlightEnd = self.mixAndMatchEnd(mixedFlightEndFuture.result(), otherModesInit, otherModesInit2)
                if(bigDestination != destination):
                    if otherModesEnd==[]:
                        otherModesEnd = otherModesEndFuture.result()
                        otherModesEnd2 = otherModesEnd2Future.result()
                    mixedFlightInit = self.mixAndMatchInit(mixedFlightInitFuture.result(), otherModesEnd,otherModesEnd2)

                onlyFlight = miscUtility.limitResults(onlyFlight,"flight")
                finalList["flight"]=onlyFlight["flight"]+mixedFlight["flight"]+mixedFlightInit["flight"]+mixedFlightEnd["flight"]
            else:
                onlyFlight = onlyFlightFuture.result()
                onlyFlight = miscUtility.limitResults(onlyFlight,"flight")
                finalList["flight"] = onlyFlight["flight"]
            return finalList

    def getOtherModes(self, source,destination, journeyDate):
        busController = busapi.BusController()
        resultJsonData = busController.getResults(source, destination, journeyDate)
        return resultJsonData

    def mixAndMatch(self, mixedFlight,otherModesInit,otherModesInit2,otherModesEnd,otherModesEnd2):
        mixedFlight = miscUtility.limitResults(mixedFlight, "flight")
        otherModesEnd["bus"] = otherModesEnd["bus"] + otherModesEnd2["bus"]
        otherModesInit["bus"] = otherModesInit["bus"] + otherModesInit2["bus"]

        for j in range(len(mixedFlight["flight"])):
                flightPart = mixedFlight["flight"][j]["parts"][0]
                subParts = []
                for k in range(len(otherModesInit["bus"])):
                    subPart = otherModesInit["bus"][k]["parts"][0]
                    if dateTimeUtility.checkIfApplicable(subPart["arrival"], subPart["arrivalDate"],
                                                         flightPart["departure"], flightPart["departureDate"], 3):
                        subPart["waitingTime"] = dateTimeUtility.getWaitingTime(subPart["arrival"],
                                                                                flightPart["departure"],
                                                                                subPart["arrivalDate"],
                                                                                flightPart["departureDate"])
                        subParts.append(subPart)
                if subParts != []:
                    newPart = {}
                    newPart["subParts"] = subParts
                    newPart["mode"] = "bus"
                    newPart["id"] = mixedFlight["flight"][j]["full"][0]["id"] + str(0)
                    newPart["destination"] = subParts[0]["destination"]
                    newPart["source"] = subParts[0]["source"]
                    newPart["carrierName"] = subParts[0]["carrierName"]
                    flightPart["id"] = mixedFlight["flight"][j]["full"][0]["id"] + str(1)
                    mixedFlight["flight"][j]["parts"].insert(0, newPart)
                subParts = []
                for k in range(len(otherModesEnd["bus"])):
                    subPart = otherModesEnd["bus"][k]["parts"][0]
                    if dateTimeUtility.checkIfApplicable(flightPart["arrival"], flightPart["arrivalDate"],
                                                         subPart["departure"], subPart["departureDate"], 3):
                        subPart["waitingTime"] = dateTimeUtility.getWaitingTime(flightPart["arrival"], subPart["departure"],
                                                                                flightPart["arrivalDate"],
                                                                                subPart["departureDate"])
                        subParts.append(subPart)
                if subParts != []:
                    newPart = {}
                    newPart["subParts"] = subParts
                    newPart["mode"] = "bus"
                    newPart["id"] = mixedFlight["flight"][j]["full"][0]["id"] + str(2)
                    newPart["destination"] = subParts[0]["destination"]
                    newPart["source"] = subParts[0]["source"]
                    newPart["carrierName"] = subParts[0]["carrierName"]
                    mixedFlight["flight"][j]["parts"].append(newPart)

        mixedFlight["flight"] = [x for x in mixedFlight["flight"] if len(x["parts"]) == 3]

        return mixedFlight

    def mixAndMatchInit(self, mixedFlightInit, otherModesEnd,otherModesEnd2):
        mixedFlightInit = miscUtility.limitResults(mixedFlightInit,"flight")
        otherModesEnd["bus"]=otherModesEnd["bus"]+otherModesEnd2["bus"]
        for j in range(len(mixedFlightInit["flight"])):
            flightPart = mixedFlightInit["flight"][j]["parts"][0]
            subParts = []
            for k in range(len(otherModesEnd["bus"])):
                subPart = otherModesEnd["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(flightPart["arrival"],flightPart["arrivalDate"],subPart["departure"],subPart["departureDate"],3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(flightPart["arrival"],subPart["departure"],flightPart["arrivalDate"],subPart["departureDate"])
                    subParts.append(subPart)
            if subParts!=[]:
                newPart = {}
                newPart["subParts"]=subParts
                newPart["mode"]="bus"
                newPart["id"]=mixedFlightInit["flight"][j]["full"][0]["id"]+str(1)
                newPart["destination"] = subParts[0]["destination"]
                newPart["source"] = subParts[0]["source"]
                newPart["carrierName"] = subParts[0]["carrierName"]
                mixedFlightInit["flight"][j]["parts"].append(newPart)

        mixedFlightInit["flight"] = [x for x in mixedFlightInit["flight"] if len(x["parts"]) == 2]
        return mixedFlightInit

    def mixAndMatchEnd(self, mixedFlightEnd, otherModesInit,otherModesInit2):
        mixedFlightEnd = miscUtility.limitResults(mixedFlightEnd, "flight")
        otherModesInit["bus"]=otherModesInit["bus"]+otherModesInit2["bus"]
        for j in range(len(mixedFlightEnd["flight"])):
            flightPart = mixedFlightEnd["flight"][j]["parts"][0]
            subParts = []
            for k in range(len(otherModesInit["bus"])):
                subPart = otherModesInit["bus"][k]["parts"][0]
                if dateTimeUtility.checkIfApplicable(subPart["arrival"], subPart["arrivalDate"],
                                                     flightPart["departure"], flightPart["departureDate"], 3):
                    subPart["waitingTime"] = dateTimeUtility.getWaitingTime(subPart["arrival"], flightPart["departure"],
                                                                            subPart["arrivalDate"],
                                                                            flightPart["departureDate"])
                    subParts.append(subPart)
            if subParts != []:
                parts = []
                newPart = {}
                newPart["subParts"] = subParts
                newPart["mode"] = "bus"
                newPart["id"] = mixedFlightEnd["flight"][j]["full"][0]["id"] + str(0)
                newPart["destination"] = subParts[0]["destination"]
                newPart["source"] = subParts[0]["source"]
                newPart["carrierName"] = subParts[0]["carrierName"]
                flightPart["id"]=mixedFlightEnd["flight"][j]["full"][0]["id"] + str(1)
                mixedFlightEnd["flight"][j]["parts"].insert(0,newPart)

        mixedFlightEnd["flight"] = [x for x in mixedFlightEnd["flight"] if len(x["parts"]) == 2]
        return mixedFlightEnd

    def flightApiCallResults(self, sourcecity, sourcestate, destinationcity, destinationstate, journeyDate, flightCounter):

        if sourcecity in FlightController.cityAndStateToStationsMap:
            source = FlightController.cityAndStateToStationsMap[sourcecity]
        elif sourcestate in FlightController.cityAndStateToStationsMap:
            source = FlightController.cityAndStateToStationsMap[sourcestate]

        if destinationcity in FlightController.cityAndStateToStationsMap:
            destination = FlightController.cityAndStateToStationsMap[destinationcity]
        elif destinationstate in FlightController.cityAndStateToStationsMap:
            destination = FlightController.cityAndStateToStationsMap[destinationstate]

        api_key = "AIzaSyAgFB2oxb44p3tgUM-baPQsT2eN_Vz1TVQ"
        url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
        headers = {'content-type': 'application/json'}
        params = {
            "request": {
                "slice": [
                    {
                        "origin": source,
                        "destination": destination,
                        "date": "2016-07-20"
                    }
                ],
                "passengers": {
                    "adultCount": 1
                },
                "solutions": 10
            }
        }

        jsonreq = json.dumps(params, encoding='utf-8')

        req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
        flight = urllib2.urlopen(req)
        response = flight.read()
        flight.close()
        onlyFlight = self.parseFlightAndReturnFare(response, flightCounter)
        return onlyFlight

    def parseFlightAndReturnFare(self,jsonData,flightCounter):
        returnedFareData = json.loads(jsonData)

        resultJsonData = {}
        resultJsonData["flight"]=[]
        partNo = 0
        if len(returnedFareData["trips"]["tripOption"])==0:
            return
        flightCounter=flightCounter
        citiesMap={}
        carrierMap = {}
        for cities in returnedFareData["trips"]["data"]["city"]:
            citiesMap[cities["code"]]=cities["name"]
        for carrier in returnedFareData["trips"]["data"]["carrier"]:
            carrierMap[carrier["code"]] = carrier["name"]
        for tripOption in returnedFareData["trips"]["tripOption"]:
            full={}
            part={}
            flightCounter=flightCounter+1

            part["price"]=tripOption["saleTotal"][3:]
            duration = tripOption["slice"][0]["duration"]
            hours = int(duration)/60
            minutes = int(duration)%60
            part["duration"]= str(hours)+":"+str(minutes)

            part["id"]= "flight"+str(flightCounter)+str(partNo)
            part["mode"]="flight"
            part["site"]="QPX"
            route = {}
            route["full"] = []
            route["parts"] = []
            subParts = []
            segmentNumber=1
            for segment in tripOption["slice"][0]["segment"]:
                legNumber = 1
                for leg in segment["leg"]:
                    subPart={}
                    subPart["flightId"]=segment["flight"]["carrier"]+"-"+segment["flight"]["number"]
                    subPart["carrierName"] = carrierMap[segment["flight"]["carrier"]]
                    duration = leg["duration"]
                    hours = int(duration) / 60
                    minutes = int(duration) % 60
                    subPart["duration"] = str(hours) + ":" + str(minutes)
                    subPart["source"] = leg["origin"]
                    subPart["destination"]= leg["destination"]
                    subPart["arrival"]=leg["arrivalTime"][11:16]
                    subPart["departure"]=leg["departureTime"][11:16]
                    subPart["mode"] = "flight"
                    subPart["id"]="flight"+str(flightCounter)+ str(segmentNumber) + str(legNumber)
                    subParts.append(subPart)
                    legNumber = legNumber+1
                segmentNumber= segmentNumber+1

            part["subParts"]=subParts
            part["source"] = citiesMap[subParts[0]["source"]]
            part["destination"] = citiesMap[subParts[int(segmentNumber - 2)]["destination"]]
            part["arrival"] = subParts[0]["arrival"]
            part["departure"] = subParts[int(segmentNumber - 2)]["departure"]
            part["carrierName"] = subParts[0]["carrierName"]
            full = part
            full["id"] = "flight" + str(flightCounter)
            route["parts"].append(part);
            route["full"].append(full)

            resultJsonData["flight"].append(route)
        return resultJsonData