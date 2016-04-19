__author__ = 'ankur'

import json

def parseFlightAndReturnFare(jsonData):
    returnedFareData = json.loads(jsonData)

    resultJsonData = {}
    resultJsonData["flight"]=[]

    if len(returnedFareData["trips"]["tripOption"])==0:
        return
    flightCounter=0
    for tripOption in returnedFareData["trips"]["tripOption"]:
        full={}
        flightCounter=flightCounter+1
        full["carrierName"]=tripOption["slice"][0]["segment"][0]["flight"]["carrier"]
        full["price"]=tripOption["saleTotal"]
        full["duration"]=tripOption["slice"][0]["duration"]
        full["id"]= "flight"+str(flightCounter)
        full["mode"]="flight"
        full["site"]="QPX"
        full["source"]=returnedFareData["trips"]["data"]["city"][1]["name"]
        full["destination"]=returnedFareData["trips"]["data"]["city"][0]["name"]
        full["arrival"]=tripOption["slice"][0]["segment"][0]["leg"][0]["arrivalTime"]
        full["departure"]=tripOption["slice"][0]["segment"][0]["leg"][0]["departureTime"]
        route={}
        route["full"]=[]
        route["parts"]=[]
        route["full"].append(full)
        parts=full
        parts["id"]="flight"+str(flightCounter)+str(1)
        route["parts"].append(parts)
        resultJsonData["flight"].append(route)
    return resultJsonData