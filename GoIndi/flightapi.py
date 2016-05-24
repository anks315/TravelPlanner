__author__ = 'ankur'
import busapi
import json
import urllib2
from django.http import HttpResponse

class FlightController:
    """Class returns all stations corresponding to a city"""

    cityAndStateToStationsMap={'Agartala':'IXA','Agra':'AGR','Ahmedabad':'AMD','Allahabad':'IXD','Amritsar':'ATQ','Aurangabad':'IXU','Bagdogra':'IXB','Bangalore':'BLR','Bhavnagar':'BHU','Bhopal':'BHO','Bhubaneswar':'BBI','Bhuj':'BHJ','Calcutta':'CCU','Kolkata':'CCU','Chandigarh':'IXC','Chennai':'MAA','Madras':'MAA','Cochin':'COK','Coimbatore':'CJB','Daman':'NMB','Dehradun':'DED','Dibrugarh':'DIB','Dimapur':'DMU','Diu':'DIU','Gauhati':'GAU','Goa':'GOI','Gwalior':'GWL','Hubli':'HBX','Hyderabad':'HYD','Imphal':'IMF','Indore':'IDR','Jaipur':'JAI','Jammu':'IXJ','Jamnagar':'JGA','Jamshedpur':'IXW','Jodhpur':'JDH','Jorhat':'JRH','Kanpur':'KNU','Khajuraho':'HJR','Kozhikode':'CCJ','calicut':'CCJ','Leh':'IXL','Lucknow':'LKO','Ludhiana':'LUH','Madurai':'IXM','Mangalore':'IXE','Mumbai':'BOM','Bombay':'BOM','Nagpur':'NAG','Nanded':'NDC','Nasik':'ISK','New Delhi':'DEL','Delhi':'DEL','Patna':'PAT','Pondicherry':'PNY','Poona':'PNQ','Pune':'PNQ','Porbandar':'PBD','Port Blair':'IXZ','PuttasubParthi':'PUT','Rae Bareli':'BEK','Rajkot':'RAJ','Ranchi':'IXR','Shillong':'SHL','Silchar':'IXS','Srinagar':'SXR','Surat':'STV','Tezpur':'TEZ','Tiruchirapally':'TRZ','Tirupati':'TIR','Trivandrum':'TRV','Udaipur':'UDR','Vadodara':'BDQ','Varanasi':'VNS','Vijayawada':'VGA','Vishakhapatnam':'VTZ','Gurgaon':'DEL','Noida':'DEL','Ghaziabad':'DEL','Tripura':'IXA','Uttar Pradesh':'AGR','Gujarat':'AMD','Uttar Pradesh':'IXD','Punjab':'ATQ','Maharashtra':'IXU','Sikkim':'IXB','Karnataka':'BLR','Gujarat':'BHU','Madhya Pradesh':'BHO','Orissa':'BBI','Gujarat':'BHJ','West Bengal':'CCU','Chandigarh':'IXC','Tamil Nadu':'MAA','Kerala':'COK','Coimbatore':'CJB','Daman':'NMB','Uttar Pradesh':'DED','Assam':'DIB','Nagaland':'DMU','Daman and Diu':'DIU','Assam':'GAU','Goa':'GOI','Madhya Pradesh':'GWL','Karnataka':'HBX','Andhra Pradesh':'HYD','Manipur':'IMF','Madhya Pradesh':'IDR','Rajasthan':'JAI','Jammu & Kashmir':'IXJ','Gujarat':'JGA','Jharkhand':'IXW','Rajasthan':'JDH','Assam':'JRH','Uttar Pradesh':'KNU','Madhya Pradesh':'HJR','Kerala':'CCJ','Jammu & Kashmir':'IXL','Utter Pradesh':'LKO','Punjab':'LUH','Tamil Nadu':'IXM','Karnataka':'IXE','Maharashtra':'BOM','Maharashtra':'NDC','Maharashtra':'ISK','Delhi':'DEL','Bihar':'PAT','Maharashtra':'PNQ','Gujarat':'PBD','Andaman and Nicobar Islands':'IXZ','Andhra Pradesh':'PUT','Uttar Pradesh':'BEK','Gujarat':'RAJ','Jharkhand':'IXR','Meghalaya':'SHL','Mizoram':'IXS','J & K':'SXR','Gujrat':'STV','Assam':'TEZ','Tamil Nadu':'TRZ','Andhra Pradesh':'TIR','Kerala':'TRV','Rajasthan':'UDR','Gujarat':'BDQ','Uttar Pradesh':'VNS','Andhra Pradesh':'VGA','Andhra Pradesh':'VTZ'}
    nearestBigAirportMap={'Jammu':'Delhi','Mangalore':'Bangalore','Delhi':'Delhi'}
    def getResults(self, sourcecity,sourcestate, destinationcity,destinationstate, journeyDate):
        flightCounter = 0
        onlyFlight = self.flightApiCallResults(sourcecity,sourcestate, destinationcity,destinationstate, journeyDate, flightCounter)
        flightCounter = len(onlyFlight["flight"])
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
        if((bigSource!=bigDestination)and(bigSource!='empty')and(bigDestination!='empty')):
            mixedFlight = self.flightApiCallResults(bigSource,bigSource, bigDestination,bigDestination, journeyDate, flightCounter)
            flightCounter = flightCounter + len(mixedFlight["flight"])
            mixedFlightEnd = self.flightApiCallResults(bigSource,bigSource, destinationcity,destinationstate, journeyDate, flightCounter)
            flightCounter = flightCounter + len(mixedFlightEnd["flight"])
            mixedFlightInit = self.flightApiCallResults(sourcecity, sourcestate, bigDestination, bigDestination, journeyDate,flightCounter)
            if(sourcecity!=bigSource):
                otherModesInit = self.getOtherModes(sourcecity,bigSource,journeyDate)
                mixedFlightEnd = self.mixAndMatchEnd(mixedFlightEnd, otherModesInit)
            if(destinationcity!=bigDestination):
                otherModesEnd = self.getOtherModes(bigDestination,destinationcity,journeyDate)
                mixedFlightInit = self.mixAndMatchInit(mixedFlightInit, otherModesEnd)
            if((sourcecity!=bigSource) and (destinationcity!=bigDestination)):
                mixedFlight = self.mixAndMatch(mixedFlight,otherModesInit,otherModesEnd)


            finalList["flight"]=onlyFlight["flight"]+mixedFlight["flight"]+mixedFlightInit["flight"]+mixedFlightEnd["flight"]
        else:
            finalList["flight"] = onlyFlight["flight"]
        return finalList

    def getOtherModes(self, source,destination, journeyDate):
        busController = busapi.BusController()
        resultJsonData = busController.getResults(source, destination, journeyDate)
        return resultJsonData

    def mixAndMatch(self, mixedFlight,otherModesInit,otherModesEnd):
        return mixedFlight

    def mixAndMatchInit(self, mixedFlightInit, otherModesEnd):

        for j in range(len(mixedFlightInit["flight"])):
            subParts = []
            for k in range(len(otherModesEnd["bus"])):
                subPart = otherModesEnd["bus"][k]["parts"][0]
                subParts.append(subPart)
            newPart = {}
            newPart["subParts"]=subParts
            newPart["mode"]="bus"
            newPart["id"]=mixedFlightInit["flight"][j]["full"][0]["id"]+str(1)
            newPart["duration"] = subParts[0]["duration"]
            newPart["destination"] = subParts[0]["destination"]
            newPart["arrival"] = subParts[0]["arrival"]
            newPart["departure"] = subParts[0]["departure"]
            newPart["source"] = subParts[0]["source"]
            newPart["carrierName"] = subParts[0]["carrierName"]
            mixedFlightInit["flight"][j]["parts"].append(newPart)
        return mixedFlightInit

    def mixAndMatchEnd(self, mixedFlightEnd, otherModesInit):
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