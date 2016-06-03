
from neo4jrestclient.client import GraphDatabase
import logging
from entity import TrainOption
import time
from datetime import datetime, timedelta
import calendar


def demo():
    pass


DATABASE_CONNECTION= GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="ankurjain")

#DATABASE_CONNECTION=GraphDatabase("http://travelplanner.sb02.stations.graphenedb.com:24789/db/data/", username="TravelPlanner", password="qKmStJDRuLfqET4ZHpQu")


def getTrainsBetweenStation(sourcecity, destinationStationSet, logger, journeydate, destinationcity):
    """
    :param sourcecity: source of the journey
    :param destinationStationSet: destination cities station set
    :param logger: to log information
    :return: all possible routes along with fare between source and destination stations
    """

    logger.debug("Fetching train routes between source[%s] and destination stations[%s] on [%s]", sourcecity,
                 destinationStationSet, journeydate)
    q = """MATCH (a:TRAINSTATION {CITY : '""" + sourcecity + """'})-[r:""" + '|'.join(
        destinationStationSet) + """]->(b:TRAIN) RETURN a,b,r"""
    results = DATABASE_CONNECTION.query(q)
    trains = []

    if len(results.elements) == 0:
        logger.warning("No Train Routes between source[%s] and destination stations[%s]", sourcecity,
                       destinationStationSet)
        return trains

    for i in range(len(results.elements)):
        if istrainrunningonjourneydate(results.elements[i], journeydate, sourcecity, logger):
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
            trainoption.duration =  getDuration(trainoption.srcDepartureTime, results.elements[i][2]['data']['SOURCEDAYNUMBER'], trainoption.destArrivalTime, results.elements[i][2]['data']['DESTINATIONDAYNUMBER'])
            if 'FARE_1A' in results.elements[i][2]['data']:
                trainoption.prices["1A"] = int(results.elements[i][2]['data']['FARE_1A'])
            if 'FARE_2A' in results.elements[i][2]['data']:
                trainoption.prices["2A"] = int(results.elements[i][2]['data']['FARE_2A'])
            if 'FARE_3A' in results.elements[i][2]['data']:
                trainoption.prices["3A"] = int(results.elements[i][2]['data']['FARE_3A'])
                if trainoption.prices["3A"] != 0:
                    trainoption.price = trainoption.prices["3A"]
                    trainoption.priceClass = "3A"
            if 'FARE_3E' in results.elements[i][2]['data']:
                trainoption.prices["3E"] = int(results.elements[i][2]['data']['FARE_3E'])
            if 'FARE_FC' in results.elements[i][2]['data']:
                trainoption.prices["FC"] = int(results.elements[i][2]['data']['FARE_FC'])
            if 'FARE_CC' in results.elements[i][2]['data']:
                trainoption.prices["CC"] = int(results.elements[i][2]['data']['FARE_CC'])
                if trainoption.prices["3A"] == 0 and trainoption.prices["CC"] != 0:
                    trainoption.price = trainoption.prices["CC"]
                    trainoption.priceClass = "CC"
            if 'FARE_SL' in results.elements[i][2]['data']:
                trainoption.prices["SL"] = int(results.elements[i][2]['data']['FARE_SL'])
                if trainoption.prices["3A"] == 0 and trainoption.prices["CC"] == 0 and trainoption.prices["SL"] != 0:
                    trainoption.price = trainoption.prices["SL"]
                    trainoption.priceClass = "SL"
            if 'FARE_2S' in results.elements[i][2]['data']:
                trainoption.prices["2S"] = int(results.elements[i][2]['data']['FARE_2S'])
            if 'FARE_GN' in results.elements[i][2]['data']:
                trainoption.prices["GN"] = int(results.elements[i][2]['data']['FARE_GN'])
            trains.append(trainoption)
    return trains


def getDuration(sourceDepartureTime, sourceDay, destinationArrivalTime, destinationDay):
    """
    to get time duration between 2 stations
    :param sourceDepartureTime: source departure time
    :param sourceDay: day on which it reaches source station
    :param destinationArrivalTime: destination arrival time
    :param destinationDay: day on which it reaches destination station
    :return: duration between source & destination
    """
    destinationArrivalTimeSplit = destinationArrivalTime.split(':')
    destinationArrivalTimeIntoMinutes=int(destinationArrivalTimeSplit[0])*60 + int(destinationArrivalTimeSplit[1])
    sourceDepartureTimeSplit = sourceDepartureTime.split(':')
    sourceDepartureTimeIntoMinutes = int(sourceDepartureTimeSplit[0])*60 + int(sourceDepartureTimeSplit[1])
    duration = (destinationDay * 24 * 60 + destinationArrivalTimeIntoMinutes) - (sourceDay * 24 * 60 + sourceDepartureTimeIntoMinutes)
    durationHours=duration/60
    durationMinutes=duration%60
    return str(durationHours) + ':' + str(durationMinutes)

def getStationCodesByCityName(cityName, logger):
    """
    To fetch all nearby or in stations in the given city
    :param cityName: city for which stations needs to be fetched
    :param logger: to logger events
    :return: list of all stations that are either in the city or nearby
    """
    logger.info("Fetching Station for City[%s]", cityName)
    start = time.time()
    q = """MATCH (a:TRAINSTATION) where a.NAME = '""" + cityName + """' OR a.NAME STARTS WITH '""" + cityName + """ ' OR a.NAME ENDS WITH ' """ + cityName + """' OR a.CITY = '""" + cityName + """' OR a.CITY STARTS WITH '""" + cityName + """ ' OR a.CITY ENDS WITH ' """ + cityName + """' return a.CODE"""
    stationcodes = []
    try:
        results = DATABASE_CONNECTION.query(q)
    except:
        logger.error("Error while fetching station codes for city[%s]", cityName)
        return stationcodes
    print("--- %s [MODELS] Stations By Code---" % (time.time() - start))
    if len(results.elements) == 0:
        logger.warning("No Station for city[%s]", cityName)
        return stationcodes
    for i in range(len(results.elements)):
        stationcodes.append(results.elements[i][0])
    logger.info("Stations for City[%s] are [%s]", cityName, stationcodes)
    return stationcodes


def addStationToTrainMapping(relationInformation):
    q = """MATCH (a:TRAINSTATION),(b:TRAIN) WHERE a.CODE = '""" + relationInformation.sourceStationCode + """' AND b.NUMBER = '""" + relationInformation.trainNumber + """' CREATE (a)-[r:""" + relationInformation.destinationStationCode
    q = q + """ {SOURCEDEPARTURETIME: '""" + relationInformation.sourceDepartureTime
    q = q + """' ,DESTINATIONARRIVALTIME:'""" + relationInformation.destinationArrivalTime
    q = q + """' ,SOURCEDAYNUMBER:""" + str(relationInformation.sourceDayNumber)
    q = q + """ ,DESTINATIONDAYNUMBER:""" + str(relationInformation.destinationDayNumber)
    q = q + """ ,FARE_1A:""" + str(relationInformation.fare_1A)
    q = q + """ ,FARE_2A:""" + str(relationInformation.fare_2A)
    q = q + """ ,FARE_3A:""" + str(relationInformation.fare_3A)
    q = q + """ ,FARE_SL:""" + str(relationInformation.fare_SL)
    q = q + """ ,FARE_2S:""" + str(relationInformation.fare_2S)
    q = q + """ ,FARE_CC:""" + str(relationInformation.fare_CC)
    q = q + """ ,FARE_FC:""" + str(relationInformation.fare_FC)
    q = q + """ ,FARE_3E:""" + str(relationInformation.fare_3E)
    q = q + """ ,FARE_GN:""" + str(relationInformation.fare_GN) + """}]->(b) RETURN r"""
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
        trainNumber, trainName = line.split(",", 1)
        q = """ MERGE (a:TRAIN {NUMBER : '""" + trainNumber + """'}) ON CREATE SET a.NAME = '""" + trainName + """'"""
        DATABASE_CONNECTION.query(q)
    pass


def getBreakingCity(possiblecity, logger):
    """
    To get name of the city from where we can split journey between source & destination
    :param possiblecity: possible city or station name
    :param logger: logger to log events
    :return: breaking city name
    """
    logger.info("Fetching matching city from breaking city/station[%s]", possiblecity)
    q = """MATCH (a:TRAINSTATION) where a.NAME = '""" + possiblecity + """' OR a.NAME STARTS WITH '""" + possiblecity + """ ' OR a.NAME ENDS WITH ' """ + possiblecity + """' OR a.CITY = '""" + possiblecity + """' OR a.CITY STARTS WITH '""" + possiblecity + """ ' OR a.CITY ENDS WITH ' """ + possiblecity + """' return a"""
    logger.debug("Fetch matching city query [%s]", q)
    try:
        result = DATABASE_CONNECTION.query(q)
    except:
        logger.error("Error while fetching breaking city for [%s]", possiblecity)
    if len(result.elements) == 0:
        logger.warning("No Breaking city present for [%s]", possiblecity)
        return
    return result.elements[0][0]['data']['CITY']


def getDayFromDate(journeydate, diff):

    """
    this method is used to get day of the week(uppercase) on journeydate
    :param journeydate: date of the journey
    :param diff: difference in number of days from starting point of train into reaching the station
    """
    t = (datetime.strptime(journeydate, '%d-%m-%Y') - timedelta(days=diff)).weekday()
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
    day = getDayFromDate(journeydate, sourcedaynumber - 1)
    if day == 'THURSDAY':
        day = 'THRUSDAY'
    if train[1]['data'][day] == 'N':
        logger.warning("Skipping train since it doesn't run from [%s] on [%s]", sourcecity, journeydate)
        return False
    return True
