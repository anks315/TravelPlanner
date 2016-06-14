from neo4jrestclient.client import GraphDatabase
from entity import TrainOption, TrainStation, FareData
import time
import calendar
import TravelPlanner.trainUtil
import logging
import urllib
import json
import trainConstants
import datetime
import loggerUtil
from datetime import timedelta
from sets import Set
import copy
import dateTimeUtility
from multiprocessing import Pool, Process

def demo():
    pass

# pool = Pool(processes=5)
citytoplacesyncmap = {"Badnera": "Amravati", "Amravati" : "Badnera", "Ankleshwar" :"Bharuch", "Basin Bridge" : "Chennai",}

#DATABASE_CONNECTION= GraphDatabase("http://ec2-54-179-130-192.ap-southeast-1.compute.amazonaws.com:7474/", username="neo4j", password="ankurjain")
DATABASE_CONNECTION= GraphDatabase("http://localhost:7474/", username="neo4j", password="rkdaimpwd")

#DATABASE_CONNECTION=GraphDatabase("http://travelplanner.sb02.stations.graphenedb.com:24789/db/data/", username="TravelPlanner", password="qKmStJDRuLfqET4ZHpQu")

def testquery():
    source = 'JAIPUR'
    other = 'AMBALA'
    results = DATABASE_CONNECTION.query("""MATCH (a:TRAINSTATION {CITY : '"""+source+"""'})-[r:BPL]->(b:TRAIN) RETURN a as station ,b as train ,r as route union MATCH (c:TRAINSTATION {CITY : '"""+other+"""'})-[e:NDLS]->(d:TRAIN) RETURN c as station,d as train ,e as route""")
    print results

def gettrainsbetweenstation(sourcecity, destinationstationset, logger, journeydate, destinationcity, trainrouteid, priceclass='3A', numberofadults=1, nextday=False):

    """
    To get train between 2 stations
    :param sourcecity: source of journey
    :param destinationstationset: set of destination city's railway station codes
    :param logger: to log information
    :param journeydate: date of journey
    :param destinationcity: destination city
    :param priceclass: preferred class for journey
    :param nextday: if train for next days are reuqired
    :return: array of trains and their data
    """
    trains = []
    logger.debug("Fetching train routes between source[%s] and destination stations[%s] on [%s]", sourcecity,destinationstationset, journeydate)
    q = """MATCH (a:TRAINSTATION {CITY : '""" + sourcecity + """'})-[r:""" + '|'.join(destinationstationset) + """]->(b:TRAIN) RETURN a,b,r"""

    try:
        results = DATABASE_CONNECTION.query(q)
    except Exception as e:
        logger.error("Error getting trains between source [%s] and destination [%s], reason [%s]", sourcecity, destinationcity, e.message)
        return trains

    if len(results.elements) == 0:
        logger.warning("No Train Routes between source[%s] and destination stations[%s]", sourcecity,destinationstationset)
        return trains

    gettrains(results,journeydate,sourcecity,logger,destinationcity,priceclass,numberofadults,trains)

    routes = parseandreturnroute(trains, logger, journeydate, trainrouteid)

    if nextday:
        nextdate = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
        gettrains(results,nextdate,sourcecity,logger,destinationcity,priceclass,numberofadults,trains)
        routes.extend(parseandreturnroute(trains, logger, nextdate, trainrouteid))
        nextdate = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=2)).strftime('%d-%m-%Y')
        gettrains(results,nextdate,sourcecity,logger,destinationcity,priceclass,numberofadults,trains)
        routes.extend(parseandreturnroute(trains, logger, nextdate, trainrouteid))

    return routes

def gettrains(results, journeydate, sourcecity, logger, destinationcity, priceclass, numberofadults, trains):

    """
    To populate array of trains which have price and are running from source on journey date
    :param results: train result from db
    :param journeydate: date of journey
    :param sourcecity: source city of journey
    :param logger: to log infomation
    :param destinationcity: destination city
    :param priceclass: default price
    :param numberofadults: no. of adults taking journey
    :param trains: array of trains
    :return: trains
    """

    trainnumberset = Set()
    for i in range(len(results.elements)):
        if istrainrunningonjourneydate(results.elements[i], journeydate, sourcecity, logger) and isnonduplicatetrain(trainnumberset, results.elements[i][1]['data']['NUMBER']):
            trainoption = TrainOption()
            trainoption.trainName = results.elements[i][1]['data']['NAME']
            trainoption.trainNumber = results.elements[i][1]['data']['NUMBER']
            trainoption.destArrivalTime = results.elements[i][2]['data']['DESTINATIONARRIVALTIME']
            trainoption.srcDepartureTime = results.elements[i][2]['data']['SOURCEDEPARTURETIME']
            trainoption.srcStation = str(results.elements[i][0]['data']['CITY']).title()
            trainoption.srcStationCode = results.elements[i][0]['data']['CODE']
            trainoption.destStationCode = results.elements[i][2]['type']
            trainoption.destStation = str(destinationcity).title()
            trainoption.prices = {"1A": 0, "2A": 0, "3A": 0, "3E": 0, "FC": 0, "CC": 0, "SL": 0, "2S": 0, "GN": 0} #empty dictionary
            trainoption.price = 0
            trainoption.priceClass=priceclass
            trainoption.numadults=numberofadults

            if 'FARE_'+priceclass in results.elements[i][2]['data']:
                setdefaultpriceifnotpresent(trainoption,trainoption.price,int(results.elements[i][2]['data']['FARE_'+priceclass]),priceclass,numberofadults)

            trainoption.duration = getduration(trainoption.srcDepartureTime, results.elements[i][2]['data']['SOURCEDAYNUMBER'], trainoption.destArrivalTime, results.elements[i][2]['data']['DESTINATIONDAYNUMBER'])

            if 'FARE_3A' in results.elements[i][2]['data']:
                trainoption.prices["3A"] = int(results.elements[i][2]['data']['FARE_3A'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["3A"],"3A",numberofadults)

            if 'FARE_CC' in results.elements[i][2]['data']:
                trainoption.prices["CC"] = int(results.elements[i][2]['data']['FARE_CC'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["CC"],"CC",numberofadults)

            if 'FARE_SL' in results.elements[i][2]['data']:
                trainoption.prices["SL"] = int(results.elements[i][2]['data']['FARE_SL'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["SL"],"SL",numberofadults)

            if 'FARE_2A' in results.elements[i][2]['data']:
                trainoption.prices["2A"] = int(results.elements[i][2]['data']['FARE_2A'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["2A"],"2A",numberofadults)

            if 'FARE_3E' in results.elements[i][2]['data']:
                trainoption.prices["3E"] = int(results.elements[i][2]['data']['FARE_3E'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["3E"],"3E",numberofadults)

            if 'FARE_2S' in results.elements[i][2]['data']:
                trainoption.prices["2S"] = int(results.elements[i][2]['data']['FARE_2S'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["2S"],"2S",numberofadults)
            
            if 'FARE_FC' in results.elements[i][2]['data']:
                trainoption.prices["FC"] = int(results.elements[i][2]['data']['FARE_FC'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["FC"],"FC",numberofadults)

            if 'FARE_1A' in results.elements[i][2]['data']:
                trainoption.prices["1A"] = int(results.elements[i][2]['data']['FARE_1A'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["1A"],"1A",numberofadults)

            if 'FARE_GN' in results.elements[i][2]['data']:
                trainoption.prices["GN"] = int(results.elements[i][2]['data']['FARE_GN'])*numberofadults
                setdefaultpriceifnotpresent(trainoption,trainoption.price,trainoption.prices["GN"],"GN",numberofadults)
            trains.append(trainoption)


def setdefaultpriceifnotpresent(trainoption,currentprice,newpriceavailable,priceclass,numberofadults):
    
    """
    To set default price on train option if available. If default option is not available then set prices in order of relevance
    :param trainoption: current train option
    :param currentprice: current set price
    :param newpriceavailable: new price
    :param priceclass: price class
    """

    if currentprice == 0 and newpriceavailable != 0:
                    trainoption.price = newpriceavailable*int(numberofadults)
                    trainoption.priceClass = priceclass

def getduration(sourcedeparturetime, sourceday, destinationarrivaltime, destinationday):
    """
    to get time duration between 2 stations
    :param sourcedeparturetime: source departure time
    :param sourceday: day on which it reaches source station
    :param destinationarrivaltime: destination arrival time
    :param destinationday: day on which it reaches destination station
    :return: duration between source & destination
    """
    destinationarrivaltimesplit = destinationarrivaltime.split(':')
    destinationarrivaltimeintominutes = int(destinationarrivaltimesplit[0])*60 + int(destinationarrivaltimesplit[1])
    sourcedeparturetimesplit = sourcedeparturetime.split(':')
    sourcedeparturetimeintominutes = int(sourcedeparturetimesplit[0])*60 + int(sourcedeparturetimesplit[1])
    duration = (destinationday * 24 * 60 + destinationarrivaltimeintominutes) - (sourceday * 24 * 60 + sourcedeparturetimeintominutes)
    durationhours = duration/60
    durationminutes = duration%60
    return str(durationhours) + ':' + str(durationminutes)

def getstationcodesbycityname(cityname, logger):
    """
    To fetch all nearby or in stations in the given city
    :param cityname: city for which stations needs to be fetched
    :param logger: to logger events
    :return: list of all stations that are either in the city or nearby
    """
    logger.info("Fetching Station for City[%s]", cityname)
    start = time.time()
    q = """MATCH (a:TRAINSTATION) where a.NAME = '""" + cityname + """' OR a.NAME STARTS WITH '""" + cityname + """ ' OR a.NAME ENDS WITH ' """ + cityname + """' OR a.CITY = '""" + cityname + """' OR a.CITY STARTS WITH '""" + cityname + """ ' OR a.CITY ENDS WITH ' """ + cityname + """' return a.CODE"""
    stationcodes = []
    try:
        results = DATABASE_CONNECTION.query(q)
    except:
        logger.error("Error while fetching station codes for city[%s]", cityname)
        return stationcodes
    print("--- %s [MODELS] Stations By Code---" % (time.time() - start))
    if len(results.elements) == 0:
        logger.warning("No Station for city[%s]", cityname)
        return stationcodes
    for i in range(len(results.elements)):
        stationcodes.append(results.elements[i][0])
    logger.info("Stations for City[%s] are [%s]", cityname, stationcodes)
    return stationcodes


def addstationtotrainmapping(relationinformation):
    q = """MATCH (a:TRAINSTATION),(b:TRAIN) WHERE a.CODE = '""" + relationinformation.sourceStationCode + """' AND b.NUMBER = '""" + relationinformation.trainNumber + """' CREATE (a)-[r:""" + relationinformation.destinationStationCode
    q = q + """ {SOURCEDEPARTURETIME: '""" + relationinformation.sourceDepartureTime
    q = q + """' ,DESTINATIONARRIVALTIME:'""" + relationinformation.destinationArrivalTime
    q = q + """' ,SOURCEDAYNUMBER:""" + str(relationinformation.sourceDayNumber)
    q = q + """ ,DESTINATIONDAYNUMBER:""" + str(relationinformation.destinationDayNumber)
    q = q + """ ,FARE_1A:""" + str(relationinformation.fare_1A)
    q = q + """ ,FARE_2A:""" + str(relationinformation.fare_2A)
    q = q + """ ,FARE_3A:""" + str(relationinformation.fare_3A)
    q = q + """ ,FARE_SL:""" + str(relationinformation.fare_SL)
    q = q + """ ,FARE_2S:""" + str(relationinformation.fare_2S)
    q = q + """ ,FARE_CC:""" + str(relationinformation.fare_CC)
    q = q + """ ,FARE_FC:""" + str(relationinformation.fare_FC)
    q = q + """ ,FARE_3E:""" + str(relationinformation.fare_3E)
    q = q + """ ,FARE_GN:""" + str(relationinformation.fare_GN) + """}]->(b) RETURN r"""
    DATABASE_CONNECTION.query(q)
    pass


def addStationToRouteMapping(relationInformation):
    q = """MATCH (a:TRAINSTATION),(b:TRAIN) WHERE a.CODE = '""" + relationInformation.sourceStationCode + """' AND b.NUMBER = '""" + relationInformation.trainNumber + """' CREATE (a)-[r:""" + relationInformation.destinationStationCode
    q = q + """ {SOURCEDEPARTURETIME: '""" + relationInformation.sourceDepartureTime
    q = q + """' ,DESTINATIONARRIVALTIME:'""" + relationInformation.destinationArrivalTime
    q = q + """' ,SOURCEDAYNUMBER:""" + str(relationInformation.sourceDayNumber)
    q = q + """ ,DESTINATIONDAYNUMBER:""" + str(relationInformation.destinationDayNumber) + """}]->(b) RETURN r"""
    DATABASE_CONNECTION.query(q)
    pass


def addRunningDaysToTrain(runningdays, trainnumber):
    q = """match (a:TRAIN) where a.NUMBER = '""" + trainnumber + """' set a.SUNDAY = '""" + runningdays[
        "SUN"] + """', a.MONDAY = '""" + runningdays["MON"]
    q = q + """', a.TUESDAY = '""" + runningdays["TUE"] + """', a.WEDNESDAY = '""" + runningdays[
        "WED"] + """', a.THRUSDAY = '""" + runningdays["THU"]
    q = q + """', a.FRIDAY = '""" + runningdays["FRI"] + """', a.SATURDAY = '""" + runningdays["SAT"] + """'"""

    DATABASE_CONNECTION.query(q)
    pass


def checkroutestationexists(routestations):
    for route in routestations:
        code = str(route["code"]).upper()
        name = str(route["name"]).upper()
        q = """ MERGE (a:TRAINSTATION {CODE : '""" + code + """'}) ON CREATE SET a.NAME = '""" + name + """', a.CITY = '""" + name + """'"""
        DATABASE_CONNECTION.query(q)
    pass


def checkstationexists(stations):
    for line in stations:
        print line
        trainNumber, trainName = line.split(",", 1)
        q = """ MERGE (a:TRAIN {NUMBER : '""" + trainNumber + """'}) ON CREATE SET a.NAME = '""" + trainName + """'"""
        DATABASE_CONNECTION.query(q)
    pass


def getbreakingcity(possiblecity, logger):
    """
    To get name of the city from where we can split journey between source & destination
    :param possiblecity: possible city or station name
    :param logger: logger to log events
    :return: breaking city name
    """
    logger.info("Fetching matching city from breaking city/station[%s]", possiblecity)
    return TravelPlanner.trainUtil.getcityfromstation(possiblecity, logger)

    # q = """MATCH (a:TRAINSTATION) where a.NAME = '""" + possiblecity + """' OR a.NAME STARTS WITH '""" + possiblecity + """ ' OR a.NAME ENDS WITH ' """ + possiblecity + """' OR a.CITY = '""" + possiblecity + """' OR a.CITY STARTS WITH '""" + possiblecity + """ ' OR a.CITY ENDS WITH ' """ + possiblecity + """' return a"""
    # logger.debug("Fetch matching city query [%s]", q)
    # try:
    #     result = DATABASE_CONNECTION.query(q)
    # except:
    #     logger.error("Error while fetching breaking city for [%s]", possiblecity)
    # if len(result.elements) == 0:
    #     logger.warning("No Breaking city present for [%s]", possiblecity)
    #     return
    # return result.elements[0][0]['data']['CITY']


def getdayfromdate(journeydate, diff):

    """
    this method is used to get day of the week(uppercase) on journeydate
    :param journeydate: date of the journey
    :param diff: difference in number of days from starting point of train into reaching the station
    """
    t = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') - timedelta(days=diff)).weekday()
    return calendar.day_name[t].upper()


def istrainrunningonjourneydate(train, journeydate, sourcecity, logger):

    """
    Checks whether train runs from given station on particular date or not
    :param train: train information
    :param journeydate: date of journey
    :param sourcecity: source station
    :param logger: to logger information
    :return: true if train runs else false
    """
    sourcedaynumber = train[2]['data']['SOURCEDAYNUMBER']
    day = getdayfromdate(journeydate, sourcedaynumber - 1)
    if day == 'THURSDAY':
        day = 'THRUSDAY'
    if train[1]['data'][day] == 'N':
        logger.warning("Skipping train since it doesn't run from [%s] on [%s]", sourcecity, journeydate)
        return False
    return True


def isnonduplicatetrain(trainnumberset, trainnumber):

    """
    To check train is already loaded or not
    :param trainnumberset: set of trains already loaded
    :param trainnumber: train to be loaded
    :return: True if train is new else False
    """
    if trainnumber not in trainnumberset:
        trainnumberset.add(trainnumber)
        return True
    return False


def loadtraindata(trainstationsmap):
    """
    To load train stations on startup
    :return: Map of train stations with code as key and train station as value
    """
    q = "MATCH (n:TRAINSTATION) return n"
    try:
        trainstations = DATABASE_CONNECTION.query(q)
    except Exception as e:
        logger = loggerUtil.getLogger("loaddata", logging.WARNING)
        logger.error("Error in loading train data on startup, reason [%s]", e.message)
        return trainstationsmap

    if len(trainstations.elements) == 0:
        return trainstationsmap

    for i in range(len(trainstations.elements)):
        trainstation = TrainStation()
        trainstation.code = trainstations.elements[i][0]['data']['CODE']
        trainstation.name = trainstations.elements[i][0]['data']['NAME']
        trainstation.city = trainstations.elements[i][0]['data']['CITY']
        trainstationsmap[trainstation.code]= trainstation

    return trainstationsmap


def citytoplacesync():
    return


def getfarefortrainandpersist(trainnumber ,sourcestationcode, destinationstationcode, logger):
    """
    To get fare data and pesist in DB
    :param trainnumber: train for which fare needs to be fetched
    :param sourcestationcode: source station code
    :param destinationstationcode: destination station code
    :param logger: to log
    :return: faredata if present else nothing
    """
    print 'inside method'
    try:
        jsonresponsetrainfare = urllib.urlopen("http://api.railwayapi.com/fare/train/" + trainnumber + "/source/"+ sourcestationcode+ "/dest/"+ destinationstationcode+ "/age/20/quota/GN/doj/"+ '11-06'+ "/apikey/"+trainConstants.ERAILWAYAPI_APIKEY +"/").read()
    except:
        logger.error("Connection Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s] ",trainnumber,sourcestationcode,destinationstationcode)
        return

    faredatajson = parseandreturnfare(jsonresponsetrainfare, logger, trainnumber, sourcestationcode, destinationstationcode)

    if faredatajson:
        faredata = getfaredataentity(faredatajson)
        persistfaredata(faredata, trainnumber, sourcestationcode, destinationstationcode, logger)
        return faredata


def parseandreturnfare(jsondata, logger, trainnumber, sourcestationcode, destinationstationcode):
    """
    To get fare data from railway api and persist in DB is result is successful
    :param jsondata: fare data json
    :param logger: to log information
    :return: faredata
    """
    faredata = {}
    if not jsondata:
        return faredata
    try:
        returnedfaredata = json.loads(jsondata)
        logger.debug("Fare Data [%s] for train [%s] between source [%s] and destination [%s]", returnedfaredata, trainnumber, sourcestationcode, destinationstationcode)
        if returnedfaredata["response_code"] == 200:
            if len(returnedfaredata["fare"]) != 0:
                return returnedfaredata["fare"]
    except Exception as e:
        logger.error("Response Error Getting Fare Data for TrainNumber[%s] ,SourceStation[%s],DestinationStation[%s], reason [%s] ",trainnumber, sourcestationcode, destinationstationcode, e.message)

    return faredata

def getfaredataentity(faredatajson):

    """
    Get fare information from json
    :param faredatajson: fare data json
    :return: FareData object having all fares for train
    """
    faredata = FareData()
    for fare in faredatajson:
        if fare["code"]=="1A":
            faredata.fare_1A=fare["fare"]
        if fare["code"]=="2A":
            faredata.fare_2A=fare["fare"]
        if fare["code"]=="3A":
            faredata.fare_3A=fare["fare"]
        if fare["code"]=="SL":
            faredata.fare_SL=fare["fare"]
        if fare["code"]=="CC":
            faredata.fare_CC=fare["fare"]
        if fare["code"]=="2S":
            faredata.fare_2S=fare["fare"]
        if fare["code"]=="GN":
            faredata.fare_GN=fare["fare"]
        if fare["code"]=="FC":
            faredata.fare_FC=fare["fare"]
        if fare["code"]=="3E":
            faredata.fare_3E=fare["fare"]
    return faredata


def persistfaredata(faredata, trainnumber, sourcestationcode, destinationstationcode, logger):
    """
    Persist fare information in DB
    :param faredata: fare data object
    :param trainnumber: train number
    :param sourcestationcode: source station code
    :param destinationstationcode: destination station code
    :param logger: to log
    """
    q = """MATCH (a:TRAINSTATION {CODE : '""" + sourcestationcode + """'})-[r:""" + destinationstationcode + """]->(b:TRAIN {NUMBER: '""" + trainnumber + """'}) SET r.FARE_1A=""" + str(faredata.fare_1A)
    q = q + """ ,r.FARE_2A = """ + str(faredata.fare_2A)
    q = q + """ ,r.FARE_3A = """ + str(faredata.fare_3A)
    q = q + """ ,r.FARE_SL = """ + str(faredata.fare_SL)
    q = q + """ ,r.FARE_2S = """ + str(faredata.fare_2S)
    q = q + """ ,r.FARE_CC = """ + str(faredata.fare_CC)
    q = q + """ ,r.FARE_FC = """ + str(faredata.fare_FC)
    q = q + """ ,r.FARE_3E = """ + str(faredata.fare_3E)
    q = q + """ ,r.FARE_GN = """ + str(faredata.fare_GN)
    print q
    try:
        DATABASE_CONNECTION.query(q)
        logger.info("Fare persisted in DB for trainNumber [%s], source [%s], destination [%s]", trainnumber, sourcestationcode, destinationstationcode)
    except Exception as e:
        logger.error("Error while persisting fare information for trainNumber [%s], source [%s], destination [%s], reason [%s]", trainnumber, sourcestationcode, destinationstationcode, e.message)


def parseandreturnroute(trainroutes, logger, journeydate, trainid):
    """
    to return map of train routes in either full or by parts journey
    :param trainroutes: list of trainroutes
    :param logger: to log information
    :return: map of full and part journey of train
    """

    logger.info("Generating route map with full & parts journey")
    routes = []
    futures = []
    traincounter = -1

    for trainroute in trainroutes:
        traincounter += 1
        futures.append(TravelPlanner.trainUtil.trainfareexecutor.submit(gettrainroute, trainroute, trainid, traincounter, journeydate, logger))

    for future in futures:
        if future and future.result(timeout=5):
            routes.append(future.result())
    return routes

def gettrainroute(trainroute, trainid, traincounter, journeydate, logger):

    """
    To get train journey route
    :param trainroute: train route object having route information
    :param trainid: global train route id
    :param traincounter: train counter used for id generation
    :param journeydate: date of journey
    :return: train route if it is having fare
    """
    route = {"full": [], "parts": []}
    try:
        full = {"carrierName": trainroute.trainName, "duration": trainroute.duration, "id": trainid + str(traincounter), "mode": "train",
                "site": "IRCTC", "source": trainroute.srcStation, "destination": trainroute.destStation, "arrival": trainroute.destArrivalTime,
                "sourceStation": trainroute.srcStationCode, "destinationStation": trainroute.destStationCode,
                "arrivalDate": dateTimeUtility.calculateArrivalTimeAndDate(journeydate, trainroute.srcDepartureTime,trainroute.duration)["arrivalDate"],
                "departure": trainroute.srcDepartureTime, "departureDate": journeydate, "prices": trainroute.prices, "price": trainroute.price,
                "priceClass": trainroute.priceClass, "route": trainroute.srcStation + ",train," + trainroute.destStation, "trainNumber": trainroute.trainNumber
                }
        part = copy.deepcopy(full)
        part["id"] = full["id"] + str(1)
        part["subParts"] = []
        part["subParts"].append(copy.deepcopy(full))
        part["subParts"][0]["id"] = full["id"] + str(1) + str(1)

        # this min/max data only in full journey for filtering purpose
        full["minPrice"] = full["maxPrice"] = trainroute.price
        full["minDuration"] = full["maxDuration"] = trainroute.duration
        full["minArrival"] = full["maxArrival"] = trainroute.destArrivalTime
        full["minDeparture"] = full["maxDeparture"] = trainroute.srcDepartureTime
        route["full"].append(full)
        route["parts"].append(part)
        # check if train has fare present for source & destination, if not get it from railway api and persisit in DB
        if hasprice(route, trainroute.trainNumber, trainroute.srcStationCode, trainroute.destStationCode,trainroute.numadults, logger):
            return route
    except Exception as e:
        logger.error("Error getting route with full & parts journey between source [%s], destination [%s], reason [%s]",trainroute.srcStation, trainroute.destStation, e.message)
        return


def hasprice(route, trainnumber ,sourcestationcode, destinationstationcode,numadults, logger):
    """
    Check whether any price exists for the train or not, if not try to get from railway api. Ignore train if either no price data is present or could not get from railway api
    :param route: train route
    :return: True if price exists else False
    """

    # prices = route["full"][0]["prices"]
    trainname = route["full"][0]["carrierName"]

    if route["full"][0]["price"] == 0:
        logger.warning("re-trying fare data for train [%s] since all prices are 0", trainname)
        # Process(target=getfarefortrainandpersist, args=(trainnumber, sourcestationcode, destinationstationcode, logger)).start()
        # if not faredata:
        return False
        # else:
        #     prices["1A"] = faredata.fare_1A*numadults
        #     prices["2A"] = faredata.fare_2A*numadults
        #     prices["3A"] = faredata.fare_3A*numadults
        #     prices["3E"] = faredata.fare_3E*numadults
        #     prices["FC"] = faredata.fare_FC*numadults
        #     prices["CC"] = faredata.fare_CC*numadults
        #     prices["SL"] = faredata.fare_SL*numadults
        #     prices["2S"] = faredata.fare_2S*numadults
        #     prices["GN"] = faredata.fare_GN*numadults
        #     if prices[route["full"][0]["priceClass"]] == 0:
        #         return False
        #     route["full"][0]["price"]=prices[route["full"][0]["priceClass"]]
        #     return True

    return True


def faredataresult(faredata):
    print faredata