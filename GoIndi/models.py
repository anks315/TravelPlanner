
from neo4jrestclient.client import GraphDatabase
import logging
from entity import TrainOption,StationToTrainRelation
import time

def demo():
   pass


DATABASE_CONNECTION = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="rkdaimpwd")

def getTrainsBetweenStation(srcStationCode,destinationStationCode,journeyDate):
    start = time.time()
    q = """MATCH (a:TrainStation)-[r:""" + destinationStationCode + """]->(b:Train) WHERE a.CODE='""" +srcStationCode + """' RETURN a,b,r"""
    results =DATABASE_CONNECTION.query(q)
    trainOption = TrainOption()
    trainOption.trainName = results.elements[0][1]['data']['name']
    trainOption.destArrivalTime=results.elements[0][2]['data']['arrival_time']
    trainOption.srcDepartureTime=results.elements[0][2]['data']['departure_time']
    trainOption.srcStation=results.elements[0][0]['data']['name']
    trainOption.fare=results.elements[0][2]['data']['fare']
    print("--- %s [MODELS] Train Between Stations---" % (time.time() - start))
    return trainOption



def getStationCodesByName(stationName):
    start =time.time()
    q = """MATCH (a:TrainStation) WHERE  a.NAME='""" + stationName + """' return a.CODE"""
    results = DATABASE_CONNECTION.query(q)
    stationcodes=[]
    print("--- %s [MODELS] Stations By Code---" % (time.time() - start))
    stationcodes.append(results.elements[0][0])
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


def addRunningDaysToTrain(runningDays, trainNumber):
    q = """match (a:TRAIN) where a.NUMBER = '""" + trainNumber + """' set a.SUNDAY = '""" + runningDays["SUN"] + """', a.MONDAY = '""" + runningDays["MON"]
    q=q+"""', a.TUESDAY = '""" + runningDays["TUE"] + """', a.WEDNESDAY = '""" + runningDays["WED"] + """', a.THRUSDAY = '""" + runningDays["THU"]
    q=q+"""', a.FRIDAY = '""" + runningDays["FRI"] + """', a.SATURDAY = '""" + runningDays["SAT"] + """'"""

    results = DATABASE_CONNECTION.query(q)
    print results
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
        trainNumber, trainName =line.split(",",1)
        q = """ MERGE (a:TRAIN {NUMBER : '""" + trainNumber + """'}) ON CREATE SET a.NAME = '""" + trainName + """'"""
        DATABASE_CONNECTION.query(q)
    pass


