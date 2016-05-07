__author__ = 'ankur'

import json
import urllib2
import requests
from requests.auth import HTTPDigestAuth
from django.http import HttpResponse

class BusController:
    """Class returns all stations corresponding to a city"""


    def getResults(self, source, destination, journeyDate):
        jdList = journeyDate.split("-")
        journeyDate = jdList[2]+"-"+jdList[1]+"-"+jdList[0]
        url = "http://agent.etravelsmart.com/etsAPI/api/getAvailableBuses?sourceCity="+source+"&destinationCity="+destination+"&doj="+journeyDate
        req = requests.get(url, auth=HTTPDigestAuth('eazzer', 'E@ZZer1713'))
        response = self.parseResultAndReturnFare(req.json(),source,destination)
        return response

    def parseResultAndReturnFare(self, jsonData, source, destination):
            resultJsonData={}
            resultJsonData["bus"]=[]
            counter = 1
            for option in jsonData["apiAvailableBuses"]:
                route = {}
                route["full"] = []
                route["parts"] = []
                part = {}
                part["carrierName"] = option["operatorName"]
                part["busType"]=option["busType"]
                part["price"]=option["fare"]
                part["mode"]="bus"
                arrival = option["arrivalTime"]
                departure = option["departureTime"]
                arrArr = arrival.split(' ')
                arrTimeArr = arrArr[0].split(':')
                if arrArr[1]=="PM" and arrTimeArr[0]!="12":
                    arrHr=int(arrTimeArr[0])+12
                else:
                    arrHr = arrTimeArr[0]
                arrMin = arrTimeArr[1]

                depArr = departure.split(' ')
                depTimeArr = depArr[0].split(':')
                if depArr[1] == "PM" and depTimeArr[0]!="12":
                    depHr = int(depTimeArr[0]) + 12
                else:
                    depHr = depTimeArr[0]
                depMin = depTimeArr[1]
                if int(arrHr)<int(depHr):
                    durHr = 24 + (int(arrHr)-int(depHr))
                else:
                    durHr = int(arrHr)-int(depHr)
                durMin = int(arrMin)-int(depMin)
                if durMin<0:
                    durMin = 60 + int(durMin)
                    durHr = int(durHr) - 1
                part["duration"] = str(durHr)+":"+str(durMin)
                part["source"] = source
                part["destination"] = destination
                part["arrival"] = option["arrivalTime"]
                part["departure"] = option["departureTime"]
                part["availableSeats"] = option["availableSeats"]
                part["id"] = "bus"+str(counter)+str("1")
                route["parts"].append(part)
                full=part
                full["id"]="bus"+str(counter)
                full["site"]="travelyaari"

                route["full"].append(full)

                resultJsonData["bus"].append(route)

            return resultJsonData