__author__ = 'ankur'

import urllib
import json
import trainConstants
import logging
from entity import StationToTrainRelation
import models, datetime, os
import concurrent.futures
"""

For all combinations of stations :
       Fetch train between stations from railwayapi.com
        parse all those trains with src station and destination station matches the concerned stations respectively.
            for all the trains parsed get fare from railwayapi server ,
            create the relation between the srcstation node to train node with relation name as DestStation and set fare,
            timings as properties of relation



"""

filename = "C:/Users/Ankit Kumar/Downloads/tmp.txt"
logfilename = "C:/Users/Hello/Downloads/DBSCRIPT_2016-05-18.log"
logfiledir = "C:/Users/Hello/Downloads/logs"
destdir = "C:/Users/Hello/Downloads/done"

today = datetime.date.today().strftime("%Y-%m-%d")

logger = logging.getLogger("TravelPlanner.Train.DBSCRIPT")
fileHandler = logging.FileHandler('C:\Users\Hello\Downloads\DBSCRIPT_' + today +'.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

jsonLogger = logging.getLogger("DBSCRIPTJSON")
jsonfileHandler = logging.FileHandler('C:\Users\Hello\Downloads\DBSCRIPTJSON_'+today+'.log')
jsonformatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
jsonfileHandler.setFormatter(jsonformatter)
jsonLogger.addHandler(jsonfileHandler)
jsonLogger.setLevel(logging.INFO)


def parseandreturnfare(jsonData):
    route = {}
    if not jsonData:
        return route
    try:
        returnedFareData = json.loads(jsonData)
        jsonLogger.info("Fare Data *** [%s]", returnedFareData)
        if returnedFareData["response_code"] == 200:
            if len(returnedFareData["fare"]) != 0:
                return returnedFareData["fare"]
    except ValueError:
        return route

    return route


def gettrainfare(sourcestation,destinationstation,trainnumber,srcstationinformation,deststationinformation, runningdate):

    try:
        jsonresponsetrainfare = urllib.urlopen("http://api.railwayapi.com/fare/train/" + trainnumber + "/source/"+ sourcestation+ "/dest/"+ destinationstation+ "/age/20/quota/GN/doj/"+ getfuturedate(runningdate, int(srcstationinformation["day"]))+ "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
    except:
        logger.error("Connection Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s] ",trainnumber,sourcestation,destinationstation)
        return
    faredata = parseandreturnfare(jsonresponsetrainfare)
    if not faredata:
        logger.error("Response Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s] ",trainnumber,sourcestation,destinationstation)
        logger.debug("Adding route relation without fare for TrainNumber[%s]", trainnumber)
        routeinformationtocommit = consolidateroutedatatoupdate(srcstationinformation,deststationinformation,trainnumber)
        try:
            models.addstationtoroutemapping(routeinformationtocommit)
        except:
            logger.error("DB Error for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s]. Failed to commit route information",trainnumber,sourcestation,destinationstation)
        return
    else:
        logger.debug("Fare Data Fetch Success for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s]",trainnumber,sourcestation,destinationstation)
    finalinformationtocommit = consolidaterelationdatatoupdate(srcstationinformation,deststationinformation,faredata,trainnumber)
    """call database to create relation between src station to train with relation as trainNumber """
    try:
        models.addstationtoroutemapping(finalinformationtocommit)
        models.addstationtofaremapping(finalinformationtocommit)
    except:
        logger.error("DB Error for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s]. Failed to commit fare information",trainnumber,sourcestation,destinationstation)



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
                stationInformation["name"]=route["fullname"]
                trainStations.append(stationInformation)

    return  trainStations


def parseTrainRouteAsMap(jsonData):
    if not jsonData:
        return []
    returnedData = json.loads(jsonData)
    jsonLogger.info("Route Data[%s] *** ",returnedData)
    trainStations = {}

    if returnedData["response_code"]==200:

        for route in returnedData["route"]:
                stationInformation= {"code": route["code"], "arrivalTime": route["scharr"],
                                     "departureTime": route["schdep"], "day": route["day"], "name": route["fullname"]}
                trainStations[route["code"]] = stationInformation

    return  trainStations


def parseAndPopulateTrainRunningDates(jsonData, trainNumber):
    """
    To populate train node with running days information
    :rtype : map of days on which train run and doesn't run
    :param jsonData: train data having running days information
    :param trainNumber: train number
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


def getnextrunningdate(jsondata):

    """
    To get next running date of train after one week
    :param jsondata: train data
    :return: next runnig date of train after one week from today
    """

    returneddata = json.loads(jsondata)
    days = {}

    if returneddata["response_code"]==200:
        trainData = returneddata["train"]
        daysData = trainData["days"]
        if daysData:
            for day in trainData["days"]:
                days[day["day-code"]]=day["runs"]

    today = datetime.date.today()
    nextweekday = (today + datetime.timedelta(days=7))

    for i in range(len(days)):
        runningdate = (nextweekday + datetime.timedelta(days=i))
        if models.istrainrunningonjourneydate(days, runningdate):
            return runningdate

    return nextweekday


def consolidaterelationdatatoupdate(srcStationInformation,destStationInformation,fareInformation,trainNumber):
        relation = consolidateroutedatatoupdate(srcStationInformation, destStationInformation, trainNumber)
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


def consolidateroutedatatoupdate (srcStationInformation, destStationInformation, trainNumber):

    relation = StationToTrainRelation
    relation.destinationArrivalTime=destStationInformation["arrivalTime"]
    relation.destinationDayNumber = destStationInformation["day"]
    relation.sourceDayNumber = srcStationInformation["day"]
    relation.sourceDepartureTime = srcStationInformation["departureTime"]
    relation.sourceStationCode=srcStationInformation["code"]
    relation.destinationStationCode=destStationInformation["code"]
    relation.trainNumber=trainNumber

    return relation




def main():
    lines = read();
    for line in lines:
        trainnumber, trainname =line.split(",",1)
        """ Get Route of Train"""
        logger.info("Fetching data for TrainNumber[%s]",trainnumber)
        jsonresponsetrainroute=""
        try:
            jsonresponsetrainroute = urllib.urlopen("http://api.railwayapi.com/route/train/" + trainnumber + "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
        except:
            logger.error("Connection Error Getting Train Route  for TrainNumber[%s]",trainnumber)
        parseAndPopulateTrainRunningDates(jsonresponsetrainroute, trainnumber)
        routeStations=parseTrainRoute(jsonresponsetrainroute)
        runningdate = getnextrunningdate(jsonresponsetrainroute)
        if len(routeStations)==0:
            logger.error("Response Error Getting Train Route  for TrainNumber[%s]",trainnumber)
        else:
            logger.info("Route Data Fetch Success for TrainNumber[%s], No of Routes[%s].",trainnumber, len(routeStations))
        models.checkroutestationexists(routeStations)
        index=0
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # Start the load operations and mark each future with its URL
            numberOfStations=len(routeStations)
            while index < numberOfStations-1:
                iterator=index+1
                while iterator <= numberOfStations -1:
                    executor.submit(gettrainfare(routeStations[index]["code"],routeStations[iterator]["code"],trainnumber, routeStations[index],routeStations[iterator]), runningdate)
                    iterator += 1
                index += 1


def read():
    f = open(filename, "r")
    print filename
    line = f.read().splitlines()
    f.close()
    return line


def readfromlogfile(filename):
    f = open(filename)
    print filename
    lines = f.read().splitlines()
    f.close()
    return lines


def fetchnonexitingfaredata():
    # We can use a with statement to ensure threads are cleaned up promptly
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
    trainnumbermap = {}
    for filename in os.listdir(logfiledir):
        if filename.endswith('.log'):
            lines = readfromlogfile(logfiledir+'/'+filename)
            for line in lines:
                if 'Error Getting Fare Data for TrainNumber' in line:
                    i = str(line).find('[')
                    if i < 0:
                        continue
                    else:
                        line = line[i:]
                        j = line.find(']')
                        if j < 0:
                            continue
                        else:
                            trainnumber = line[1:j]
                            line = line[j:]
                            k = line.find('[')
                            if k < 0:
                                continue
                            else:
                                line = line[k:]
                                l = line.find(']')
                                if l < 0:
                                    continue
                                else:
                                    source = line[1:l]
                                    line = line[l:]
                                    m = line.find('[')
                                    if m < 0:
                                        continue
                                    else:
                                        line = line[m:]
                                        n = line.find(']')
                                        if n < 0:
                                            continue
                                        else:
                                            destination = line[1:n]
                                            """ Get Route of Train"""
                                            logger.debug("Fetching data for TrainNumber[%s]",trainnumber)
                                            if trainnumber in trainnumbermap.keys():
                                                routestations = trainnumbermap[trainnumber]
                                            else:
                                                try:
                                                    jsonresponsetrainroute = urllib.urlopen("http://api.railwayapi.com/route/train/" + trainnumber + "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
                                                except:
                                                    logger.error("Connection Error Getting Train Route  for TrainNumber[%s]",trainnumber)
                                                    continue
                                                routestations = parseTrainRouteAsMap(jsonresponsetrainroute)
                                                trainnumbermap[trainnumber] = routestations
                                                runningdate = getnextrunningdate(jsonresponsetrainroute)
                                            if len(routestations)==0:
                                                logger.error("Response Error Getting Train Route  for TrainNumber[%s]",trainnumber)
                                            else:
                                                logger.debug("Route Data Fetch Success for TrainNumber[%s], No of Routes[%s].",trainnumber, len(routestations))
                                            # Start the load operations and mark each future with its URL
                                            if source in routestations.keys() and destination in routestations.keys():
                                                executor.submit(gettrainfare(source,destination,trainnumber, routestations[source],routestations[destination], runningdate))
            os.rename(logfiledir+'/'+filename, destdir+'/'+filename)


def getfuturedate(runningdate, futuredays):

    """
    Get future date after adding no. of days
    :param runningdate next running date from source station of train
    :param futuredays: no. of days in future
    :return: running date in future after futuredays from runningdate
    """
    d = (runningdate + datetime.timedelta(days=(futuredays-1))).strftime('%d-%m')
    return str(d)