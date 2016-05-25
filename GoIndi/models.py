
from neo4jrestclient.client import GraphDatabase
import logging
from entity import TrainOption,StationToTrainRelation
import time

def demo():
   pass


DATABASE_CONNECTION = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="rkdaimpwd")

def getTrainsBetweenStation(sourceCity,destinationStationSet):

    """
    :param sourceCity: source of the journey
    :param destinationStationSet: destination cities station set
    :param journeyDate: date of journey
    :return: all possible routes along with fare between source and destination stations
    """



    start = time.time()
    q = """MATCH (a:TRAINSTATION {CITY : '""" + sourceCity + """'})-[r:""" + '|'.join(destinationStationSet) + """]->(b:TRAIN) RETURN a,b,r"""
    results =DATABASE_CONNECTION.query(q)
    trainOption = TrainOption()
    trainOption.trainName = results.elements[0][1]['data']['name']
    trainOption.destArrivalTime=results.elements[0][2]['data']['arrival_time']
    trainOption.srcDepartureTime=results.elements[0][2]['data']['departure_time']
    trainOption.srcStation=results.elements[0][0]['data']['name']
    trainOption.fare=results.elements[0][2]['data']['fare']
    print("--- %s [MODELS] Train Between Stations---" % (time.time() - start))
    return trainOption



def getStationCodesByCityName(cityName, logger):

    """
    To fetch all nearby or in stations in the given city
    :param cityName: city for which stations needs to be fetched
    :param logger: to logger events
    :return: list of all stations that are either in the city or nearby
    """
    logger.info("Fetching Station for City[%s]", cityName)
    start =time.time()
    q = """MATCH (a:TRAINSTATION) WHERE  a.CITY='""" + cityName + """' return a.CODE"""
    try:
        results = DATABASE_CONNECTION.query(q)
    except:
        logger.error("Error while fetching station codes for city[%s]", cityName)
        return
    stationcodes=[]
    print("--- %s [MODELS] Stations By Code---" % (time.time() - start))
    if len(results.elements) == 0 :
        logger.warning("No Station for city[%s]", cityName)
        return
    for i in range(len(results.elements)):
        stationcodes.append(results.elements[i][0])
    logger.info("Stations for City[%s] are [%s]", cityName, stationcodes)
    return stationcodes

def addStationToTrainMapping(relationInformation):
    q ="""MATCH (a:TRAINSTATION),(b:TRAIN) WHERE a.CODE = '""" + relationInformation.sourceStationCode + """' AND b.NUMBER = '"""+ relationInformation.trainNumber + """' CREATE (a)-[r:""" + relationInformation.destinationStationCode
    q=q+""" {SOURCEDEPARTURETIME: '"""+relationInformation.sourceDepartureTime
    q=q+"""' ,DESTINATIONARRIVALTIME:'"""+relationInformation.destinationArrivalTime
    q=q+"""' ,SOURCEDAYNUMBER:"""+str(relationInformation.sourceDayNumber)
    q=q+""" ,DESTINATIONDAYNUMBER:"""+str(relationInformation.destinationDayNumber)
    q=q+""" ,FARE_1A:"""+str(relationInformation.fare_1A)
    q=q+""" ,FARE_2A:"""+str(relationInformation.fare_2A)
    q=q+""" ,FARE_3A:"""+str(relationInformation.fare_3A)
    q=q+""" ,FARE_SL:"""+str(relationInformation.fare_SL)
    q=q+""" ,FARE_2S:"""+str(relationInformation.fare_2S)
    q=q+""" ,FARE_CC:"""+str(relationInformation.fare_CC)
    q=q+""" ,FARE_FC:"""+str(relationInformation.fare_FC)
    q=q+""" ,FARE_3E:"""+str(relationInformation.fare_3E)
    q=q+""" ,FARE_GN:"""+str(relationInformation.fare_GN) + """}]->(b) RETURN r"""
    DATABASE_CONNECTION.query(q)
    pass


def addStationToRouteMapping(relationInformation):
    q ="""MATCH (a:TRAINSTATION),(b:TRAIN) WHERE a.CODE = '""" + relationInformation.sourceStationCode + """' AND b.NUMBER = '"""+ relationInformation.trainNumber + """' CREATE (a)-[r:""" + relationInformation.destinationStationCode
    q=q+""" {SOURCEDEPARTURETIME: '"""+relationInformation.sourceDepartureTime
    q=q+"""' ,DESTINATIONARRIVALTIME:'"""+relationInformation.destinationArrivalTime
    q=q+"""' ,SOURCEDAYNUMBER:"""+str(relationInformation.sourceDayNumber)
    q=q+""" ,DESTINATIONDAYNUMBER:"""+str(relationInformation.destinationDayNumber) + """}]->(b) RETURN r"""
    DATABASE_CONNECTION.query(q)
    pass


def addRunningDaysToTrain(runningDays, trainNumber):
    q = """match (a:TRAIN) where a.NUMBER = '""" + trainNumber + """' set a.SUNDAY = '""" + runningDays["SUN"] + """', a.MONDAY = '""" + runningDays["MON"]
    q=q+"""', a.TUESDAY = '""" + runningDays["TUE"] + """', a.WEDNESDAY = '""" + runningDays["WED"] + """', a.THRUSDAY = '""" + runningDays["THU"]
    q=q+"""', a.FRIDAY = '""" + runningDays["FRI"] + """', a.SATURDAY = '""" + runningDays["SAT"] + """'"""

    results = DATABASE_CONNECTION.query(q)
    pass


def checkRouteStationExists(routeStations):
    for route in routeStations:
        code = str(route["code"]).upper()
        name = str(route["name"]).upper()
        q = """ MERGE (a:TRAINSTATION {CODE : '""" + code + """'}) ON CREATE SET a.NAME = '""" + name + """', a.CITY = '""" + name + """'"""
        DATABASE_CONNECTION.query(q)
    pass


def checkStationExists(stations):
    for line in stations:
        print line
        trainNumber, trainName =line.split(",",1)
        q = """ MERGE (a:TRAIN {NUMBER : '""" + trainNumber + """'}) ON CREATE SET a.NAME = '""" + trainName + """'"""
        DATABASE_CONNECTION.query(q)
    pass


def getBreakingCity(possibleCity, logger):

    """
    To get name of the city from where we can split journey between source & destination
    :param possibleCity: possible city or station name
    :param logger: logger to log events
    :return: breaking city name
    """
    logger.info("Fetching matching city from breaking city/station[%s]", possibleCity)
    start = time.time()
    q = """MATCH (a:TRAINSTATION) where a.NAME = '""" + possibleCity + """' OR a.NAME STARTS WITH '""" + possibleCity + """ ' OR a.NAME ENDS WITH ' """ + possibleCity + """' OR a.CITY = '""" + possibleCity + """' OR a.CITY STARTS WITH '""" + possibleCity + """ ' OR a.CITY ENDS WITH ' """ + possibleCity + """' return a"""
    logger.debug("Fetch matching city query [%s]", q)
    try:
        result = DATABASE_CONNECTION.query(q)
    except:
        logger.error("Error while fetching breaking city for [%s]", possibleCity)
    if len(result.elements) == 0:
        logger.warning("No Breaking city present for [%s]", possibleCity)
        return
    return result.elements[0][0]['data']['CITY']
