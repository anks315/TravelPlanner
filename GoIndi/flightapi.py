__author__ = 'ankur'

import json
import urllib2
from django.http import HttpResponse

class FlightController:
    """Class returs all stations corresponding to a city"""

    cityAndStateToStationsMap={'Agartala':'IXA','Agra':'AGR','Ahmedabad':'AMD','Allahabad':'IXD','Amritsar':'ATQ','Aurangabad':'IXU','Bagdogra':'IXB','Bangalore':'BLR','Bhavnagar':'BHU','Bhopal':'BHO','Bhubaneswar':'BBI','Bhuj':'BHJ','Calcutta':'CCU','Kolkata':'CCU','Chandigarh':'IXC','Chennai':'MAA','Madras':'MAA','Cochin':'COK','Coimbatore':'CJB','Daman':'NMB','Dehradun':'DED','Dibrugarh':'DIB','Dimapur':'DMU','Diu':'DIU','Gauhati':'GAU','Goa':'GOI','Gwalior':'GWL','Hubli':'HBX','Hyderabad':'HYD','Imphal':'IMF','Indore':'IDR','Jaipur':'JAI','Jammu':'IXJ','Jamnagar':'JGA','Jamshedpur':'IXW','Jodhpur':'JDH','Jorhat':'JRH','Kanpur':'KNU','Khajuraho':'HJR','Kozhikode':'CCJ','calicut':'CCJ','Leh':'IXL','Lucknow':'LKO','Ludhiana':'LUH','Madurai':'IXM','Mangalore':'IXE','Mumbai':'BOM','Bombay':'BOM','Nagpur':'NAG','Nanded':'NDC','Nasik':'ISK','New Delhi':'DEL','Delhi':'DEL','Patna':'PAT','Pondicherry':'PNY','Poona':'PNQ','Pune':'PNQ','Porbandar':'PBD','Port Blair':'IXZ','Puttaparthi':'PUT','Rae Bareli':'BEK','Rajkot':'RAJ','Ranchi':'IXR','Shillong':'SHL','Silchar':'IXS','Srinagar':'SXR','Surat':'STV','Tezpur':'TEZ','Tiruchirapally':'TRZ','Tirupati':'TIR','Trivandrum':'TRV','Udaipur':'UDR','Vadodara':'BDQ','Varanasi':'VNS','Vijayawada':'VGA','Vishakhapatnam':'VTZ','Gurgaon':'DEL','Noida':'DEL','Ghaziabad':'DEL','Tripura':'IXA','Uttar Pradesh':'AGR','Gujarat':'AMD','Uttar Pradesh':'IXD','Punjab':'ATQ','Maharashtra':'IXU','Sikkim':'IXB','Karnataka':'BLR','Gujarat':'BHU','Madhya Pradesh':'BHO','Orissa':'BBI','Gujarat':'BHJ','West Bengal':'CCU','Chandigarh':'IXC','Tamil Nadu':'MAA','Kerala':'COK','Coimbatore':'CJB','Daman':'NMB','Uttar Pradesh':'DED','Assam':'DIB','Nagaland':'DMU','Daman and Diu':'DIU','Assam':'GAU','Goa':'GOI','Madhya Pradesh':'GWL','Karnataka':'HBX','Andhra Pradesh':'HYD','Manipur':'IMF','Madhya Pradesh':'IDR','Rajasthan':'JAI','Jammu & Kashmir':'IXJ','Gujarat':'JGA','Jharkhand':'IXW','Rajasthan':'JDH','Assam':'JRH','Uttar Pradesh':'KNU','Madhya Pradesh':'HJR','Kerala':'CCJ','Jammu & Kashmir':'IXL','Utter Pradesh':'LKO','Punjab':'LUH','Tamil Nadu':'IXM','Karnataka':'IXE','Maharashtra':'BOM','Maharashtra':'NDC','Maharashtra':'ISK','Delhi':'DEL','Bihar':'PAT','Maharashtra':'PNQ','Gujarat':'PBD','Andaman and Nicobar Islands':'IXZ','Andhra Pradesh':'PUT','Uttar Pradesh':'BEK','Gujarat':'RAJ','Jharkhand':'IXR','Meghalaya':'SHL','Mizoram':'IXS','J & K':'SXR','Gujrat':'STV','Assam':'TEZ','Tamil Nadu':'TRZ','Andhra Pradesh':'TIR','Kerala':'TRV','Rajasthan':'UDR','Gujarat':'BDQ','Uttar Pradesh':'VNS','Andhra Pradesh':'VGA','Andhra Pradesh':'VTZ'}

    def getResults(self, sourcecity,sourcestate, destinationcity,destinationstate, journeyDate):

        if sourcecity in FlightController.cityAndStateToStationsMap:
           source =  FlightController.cityAndStateToStationsMap[sourcecity]
        elif sourcestate in FlightController.cityAndStateToStationsMap:
           source =  FlightController.cityAndStateToStationsMap[sourcestate]

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
                        "date": "2016-05-20"
                        }
                    ],
            "passengers": {
                        "adultCount": 1
                          },
            "solutions": 5
                         }
                }

        jsonreq = json.dumps(params, encoding = 'utf-8')
        req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
        flight = urllib2.urlopen(req)
        response = flight.read()
        flight.close()
        return HttpResponse(json.dumps(self.parseFlightAndReturnFare(response)), content_type='application/json')

    def parseFlightAndReturnFare(self,jsonData):
        returnedFareData = json.loads(jsonData)

        resultJsonData = {}
        resultJsonData["flight"]=[]

        if len(returnedFareData["trips"]["tripOption"])==0:
            return
        flightCounter=0
        citiesMap={}
        carrierMap = {}
        for cities in returnedFareData["trips"]["data"]["city"]:
            citiesMap[cities["code"]]=cities["name"]
        for carrier in returnedFareData["trips"]["data"]["carrier"]:
            carrierMap[carrier["code"]] = carrier["name"]
        for tripOption in returnedFareData["trips"]["tripOption"]:
            full={}
            flightCounter=flightCounter+1
            full["carrierName"]=""
            full["price"]=tripOption["saleTotal"][3:]
            duration = tripOption["slice"][0]["duration"]
            hours = int(duration)/60
            minutes = int(duration)%60
            full["duration"]= str(hours)+":"+str(minutes)
            full["id"]= "flight"+str(flightCounter)
            full["mode"]="flight"
            full["site"]="QPX"
            route = {}
            route["full"] = []
            route["parts"] = []

            parts = {}
            segmentNumber=1
            for segment in tripOption["slice"][0]["segment"]:
                legNumber = 1
                for leg in segment["leg"]:
                    part={}
                    part["flightId"]=segment["flight"]["carrier"]+"-"+segment["flight"]["number"]
                    part["carrierName"] = carrierMap[segment["flight"]["carrier"]]
                    duration = leg["duration"]
                    hours = int(duration) / 60
                    minutes = int(duration) % 60
                    part["duration"] = str(hours) + ":" + str(minutes)
                    part["source"] = leg["origin"]
                    part["destination"]= leg["destination"]
                    part["arrival"]=leg["arrivalTime"][11:16]
                    part["departure"]=leg["departureTime"][11:16]
                    part["mode"] = "flight"
                    part["id"]="flight"+str(flightCounter)+ str(segmentNumber) + str(legNumber)
                    route["parts"].append(part)
                    legNumber = legNumber+1
                segmentNumber= segmentNumber+1

            full["source"]=citiesMap[route["parts"][0]["source"]]
            full["destination"]=citiesMap[route["parts"][int(segmentNumber-2)]["destination"]]
            full["arrival"]=route["parts"][0]["arrival"]
            full["departure"]=route["parts"][int(segmentNumber-2)]["departure"]

            route["full"].append(full)

            resultJsonData["flight"].append(route)
        return resultJsonData