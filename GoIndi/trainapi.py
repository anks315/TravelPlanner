__author__ = 'ankur'


import hmac
import json
import trainConstants
import urllib
import concurrent.futures
import time
import  logging



trainNumberstoDurationMap ={}

def parseTrainBetweenStationsAndReturnTrainNumber(jsonData):
    returnedData = json.loads(jsonData)
    trainNumbers = []
    global trainNumberstoDurationMap
    for train in returnedData["train"]  :
            trainNumbers.append(train["number"])
            trainNumberstoDurationMap[train["number"]]={}
            trainNumberstoDurationMap[train["number"]]["departure"]=train["src_departure_time"]
            trainNumberstoDurationMap[train["number"]]["arrival"]=train["dest_arrival_time"]
            trainNumberstoDurationMap[train["number"]]["duration"]=train["travel_time"]
            trainNumberstoDurationMap[train["number"]]["srcStation"]=train["from"]["code"]
            trainNumberstoDurationMap[train["number"]]["destStation"]=train["to"]["code"]

    return  trainNumbers


def parseAndReturnFare(jsonData,trainCounter):
    route={}
    try:

        returnedFareData = json.loads(jsonData)


        if len(returnedFareData["fare"])!=0:
            full={}
            full["carrierName"]=returnedFareData["train"]["name"]
            full["price"]=returnedFareData["fare"][0]["fare"]
            full["duration"]=trainNumberstoDurationMap[returnedFareData["train"]["number"]]["duration"]
            full["id"]= "train"+str(trainCounter)
            full["mode"]="train"
            full["site"]="IRCTC"
            full["source"]=""
            full["destination"]=""
            full["arrival"]=trainNumberstoDurationMap[returnedFareData["train"]["number"]]["arrival"]
            full["departure"]=trainNumberstoDurationMap[returnedFareData["train"]["number"]]["departure"]
            route["full"]=[]
            route["parts"]=[]
            route["full"].append(full)
            parts=full
            parts["id"]="train"+str(trainCounter)+str(1)
            route["parts"].append(parts)
    except ValueError:
        return route
    return route


class PlaceToStationCodesCache:
    """Class returs all stations corresponding to a city"""

    cityToStationsMap={}


    def parseStationNameToStationCodes(self,jsonData):
        returnedData = json.loads(jsonData)
        stationList=[]
        if returnedData["response_code"]==200:
            for station in returnedData["stations"]:
                stationList.append(station["code"])

        return  stationList

    def getStationsByCode(self,stationName):
        if stationName in PlaceToStationCodesCache.cityToStationsMap:
            return PlaceToStationCodesCache.cityToStationsMap[stationName]
        else:
            jsonResponseNameToCode = urllib.urlopen("http://api.railwayapi.com/name_to_code/station/"+ stationName + "/apikey/" + trainConstants.ERAILWAYAPI_APIKEY + "/").read()
            stationList = self.parseStationNameToStationCodes(jsonResponseNameToCode)
            if stationList:
                PlaceToStationCodesCache.cityToStationsMap[stationName]=stationList
            return stationList


class TrainController:
    """Entry point to get all routes with train as the major mode of transport"""
    placetoStationCodesCache = PlaceToStationCodesCache()

    def getTrainBetweenStations(self,sourceStation,destinationStation,journeyDate):
        jsonResponseTrainBetweenStations = urllib.urlopen("http://api.railwayapi.com/between/source/"+ sourceStation + "/dest/" + destinationStation+ "/date/" + '05-05' +"/apikey/"+ trainConstants.ERAILWAYAPI_APIKEY +"/").read()
        availableTrainNumbers = parseTrainBetweenStationsAndReturnTrainNumber(jsonResponseTrainBetweenStations)
        return availableTrainNumbers


    def getTrainFare(self,sourceStation,destinationStation,journeyDate,trainNumber,trainCounter):
        start = time.time()
        jsonResponseTrainFare = urllib.urlopen("http://api.railwayapi.com/fare/train/" + trainNumber + "/source/"+ sourceStation+ "/dest/"+ destinationStation+ "/age/18/quota/GN/doj/"+ '05-05'+ "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
        fareData=parseAndReturnFare(jsonResponseTrainFare,trainCounter)
        print("--- %s api---" % (time.time() - start))
        if not fareData:
            return
        else:
            return fareData



    def findTrainsBetweenStations(self,sourceStationList,destinationStationList,journeyDate):
        resultJsonData = {}
        resultJsonData["train"]=[]
        availableTrainNumbers=set([])
        futures =[]
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            hack=0

            for sourceStation in sourceStationList:
                if hack==0:
                    for destinationStation in destinationStationList:
                        hack=1
                        futures.append(executor.submit(self.getTrainBetweenStations,sourceStation,destinationStation,journeyDate))
                        #availableTrainNumbersList = self.getTrainBetweenStations(sourceStation,destinationStation,journeyDate)
                        #availableTrainNumbers = availableTrainNumbers.union(availableTrainNumbersList)

        trainCounter=0
        for future in futures:
            availableTrainNumbers = availableTrainNumbers.union(future.result())

        farefutures=[]
        print("--- %s seconds kjbnkj---" % (time.time() - start_time))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for trainNumber in availableTrainNumbers:
                trainCounter=trainCounter+1
                if trainCounter<10:
                    farefutures.append(executor.submit(self.getTrainFare,trainNumberstoDurationMap[trainNumber]["srcStation"],trainNumberstoDurationMap[trainNumber]["destStation"],journeyDate,trainNumber,trainCounter))

        for future in farefutures:
            fareData = future.result()
            if not fareData:
                pass
            else:
                resultJsonData["train"].append(future.result())
        print("--- %s seconds ---" % (time.time() - start_time))
        logging.error(time.time() - start_time)
        return resultJsonData


    def getRoutes(self,source,destination,dateOfJourney):

        sourceStations = self.placetoStationCodesCache.getStationsByCode(source)
        destinationStations = self.placetoStationCodesCache.getStationsByCode(destination)
        if not sourceStations or not destinationStations:
            return
        else:
            return self.findTrainsBetweenStations(sourceStations,destinationStations,dateOfJourney)





def getdummyRoute(source,destination):
    route={}
    part ={}
    part["carrierName"]="Duronto Express"
    part["price"]="700"
    part["duration"]=610
    part["id"]= "train0"
    part["mode"]="train"
    part["site"]="IRCTC"
    part["source"]=source
    part["destination"]=destination
    part["arrival"]="18:10"
    part["departure"]="6:00"
    route["full"]={}
    route["parts"]=[]
    route["parts"].append(part)
    return route