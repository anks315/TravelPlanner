from _ast import mod
from argparse import _StoreTrueAction

__author__ = 'ankur'

import urllib
import json
import time
import trainConstants
import logging
from entity import StationToTrainRelation
import models
"""

For all combinations of stations :
       Fetch train between stations from railwayapi.com
        parse all those trains with src station and destination station matches the concerned stations respectively.
            for all the trains parsed get fare from railwayapi server ,
            create the relation between the srcstation node to train node with relation name as DestStation and set fare,
            timings as properties of relation



"""

filename = "C:/Users/Ankit Kumar/Downloads/tmp.txt"

logger = logging.getLogger("TravelPlanner.Train.DBSCRIPT")
fileHandler = logging.FileHandler('C:/Users/Ankit Kumar/Downloads/DBSCRIPT.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

jsonLogger = logging.getLogger("DBSCRIPTJSON")
jsonfileHandler = logging.FileHandler('C:/Users/Ankit Kumar/Downloads/DBSCRIPTJSON.log')
jsonformatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
jsonfileHandler.setFormatter(jsonformatter)
jsonLogger.addHandler(jsonfileHandler)
jsonLogger.setLevel(logging.INFO)



def parseAndReturnFare(jsonData):
    route={}
    if not jsonData:
            return route
    try:
        returnedFareData = json.loads(jsonData)
        jsonLogger.info("Fare Data *** ", returnedFareData)
        if returnedFareData["response_code"]==200:
            if len(returnedFareData["fare"])!=0:
                return returnedFareData["fare"]
    except ValueError:
            return route

    return route






def getTrainFare(sourceStation,destinationStation,journeyDate,trainNumber):
    start = time.time()
    jsonResponseTrainFare=""
    try:
        jsonResponseTrainFare = urllib.urlopen("http://api.railwayapi.com/fare/train/" + trainNumber + "/source/"+ sourceStation+ "/dest/"+ destinationStation+ "/age/20/quota/GN/doj/"+ '11-06'+ "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
    except:
        logger.error("Connection Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s] ",trainNumber,sourceStation,destinationStation)
        return
    fareData=parseAndReturnFare(jsonResponseTrainFare)
    if not fareData:
        logger.error("Response Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s] ",trainNumber,sourceStation,destinationStation)
        return
    else:
        logger.info("Fare Data Fetch Success for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s]",trainNumber,sourceStation,destinationStation)
        return fareData


def parseTrainRoute(jsonData):
    if not jsonData:
        return []
    returnedData = json.loads(jsonData)
    jsonLogger.info("Route Data[%s] *** ",returnedData)
    trainStations = []

    if returnedData["response_code"]==200:

        for route in returnedData["route"]:
                stationInformation={}
                stationInformation["code"]=route["code"]
                stationInformation["arrivalTime"]=route["scharr"]
                stationInformation["departureTime"]=route["schdep"]
                stationInformation["day"]=route["day"]
                trainStations.append(stationInformation)

    return  trainStations


def parseAndPopulateTrainRunningDates(jsonData, trainNumber):
    """


    :rtype : map of days on which train run and doesn't run
    :param jsonData:
    :param trainNumber:
    :return:
    """
    if not jsonData:
        logger.error("TrainNumber[%s] doesn't run on any day.", trainNumber)
        return[]

    returneddata = json.loads(jsonData)
    jsonLogger.info("Days Data[%s] for TrainNumber[%s] *** ",returneddata,trainNumber)
    days = {}

    if returneddata["response_code"]==200:
        trainData = returneddata["train"]
        daysData = trainData["days"]
        if daysData:
            for day in trainData["days"]:
                days[day["day-code"]]=day["runs"]

    if len(days) == 0:
        logger.error("TrainNumber[%s] doesn't run on any day.", trainNumber)
        return []

    models.addRunningDaysToTrain(days, trainNumber)



def consolidateRelationDatatoUpdate(srcStationInformation,destStationInformation,fareInformation,trainNumber):
        relation =StationToTrainRelation()
        relation.destinationArrivalTime=destStationInformation["arrivalTime"]
        relation.destinationDayNumber = destStationInformation["day"]
        relation.sourceDayNumber = srcStationInformation["day"]
        relation.sourceDepartureTime = srcStationInformation["departureTime"]
        relation.sourceStationCode=srcStationInformation["code"]
        relation.destinationStationCode=destStationInformation["code"]
        relation.trainNumber=trainNumber
        for fare in fareInformation:
            if fare["code"]=="1A":
                relation.fare_1A=fare["fare"]
            if fare["code"]=="2A":
                relation.fare_2A=fare["fare"]
            if fare["code"]=="3A":
                relation.fare_3A=fare["fare"]
            if fare["code"]=="SL":
                relation.fare_SL=fare["fare"]
            if fare["code"]=="CC":
                relation.fare_CC=fare["fare"]
            if fare["code"]=="2S":
                relation.fare_2S=fare["fare"]
            if fare["code"]=="GN":
                relation.fare_GN=fare["fare"]
            if fare["code"]=="FC":
                relation.fare_FC=fare["fare"]
            if fare["code"]=="3E":
                relation.fare_3E=fare["fare"]

        return relation



def main():
    lines = read();
    for line in lines:
        trainNumber, trainName, station =line.split(",",2)
        """ Get Route of Train"""
        jsonResponseTrainRoute=""
        try:
            jsonResponseTrainRoute = urllib.urlopen("http://api.railwayapi.com/route/train/" + trainNumber + "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
        except:
            logger.error("Connection Error Getting Train Route  for TrainNumber[%s]",trainNumber)
        parseAndPopulateTrainRunningDates(jsonResponseTrainRoute, trainNumber)
        routeStations=parseTrainRoute(jsonResponseTrainRoute)
        if len(routeStations)==0:
            logger.error("Response Error Getting Train Route  for TrainNumber[%s]",trainNumber)
        else:
            logger.info("Route Data Fetch Success for TrainNumber[%s] having train Route",trainNumber)
        index=0
        numberOfStations=len(routeStations)
        while index < numberOfStations-1:
            iterator=index+1
            while iterator <= numberOfStations -1:
                fareData = getTrainFare(routeStations[index]["code"],routeStations[iterator]["code"],'11-06-2016',trainNumber)
                if fareData:
                    finalInformationToCommit=consolidateRelationDatatoUpdate(routeStations[index],routeStations[iterator],fareData,trainNumber)
                    """call database to create relation between src station to train with relation as trainNumber """
                    try:
                        models.addStationToTrainMapping(finalInformationToCommit)
                    except:
                        logger.info("DB Error for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s]",trainNumber,routeStations[index]["code"],routeStations[iterator]["code"])

                iterator=iterator+1
            index=index+1



def read():
    f = open(filename, "r")
    print filename
    line = f.read().splitlines()
    f.close()
    return line

