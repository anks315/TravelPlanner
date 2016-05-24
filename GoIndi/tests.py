# from django.test import TestCase

# Create your tests here.

import urllib
import trainConstants
import json
from sets import Set
import models

def parseTransitRoutes(jsonTransitRoute,destination):

    """
    To parse breaking journey json object
    :param jsonTransitRoute: breaking journey data
    :param destination: destination of journey
    :return: list of all possible breaking stations
    """
    returnedData = json.loads(jsonTransitRoute)
    possibleBreakList=[]
    for leg in returnedData["routes"][0]["legs"]:
        stepNumber=0
        for step in leg["steps"]:
            if "transit_details" in step and "RAIL" in step["transit_details"]["line"]["vehicle"]["type"]:
                if stepNumber==1 and destination in str(step["transit_details"]["arrival_stop"]["name"]).upper():
                    possibleBreakList.append(step["transit_details"]["departure_stop"]["name"])

                if stepNumber!=0 and destination not in str(step["transit_details"]["arrival_stop"]["name"]).upper():
                    possibleBreakList.append(step["transit_details"]["departure_stop"]["name"])
                    possibleBreakList.append(step["transit_details"]["arrival_stop"]["name"])

                stepNumber=stepNumber+1
    return possibleBreakList



def getPossibleBreakingPlacesForTrain(source,destination):

    """
    To get possible stations to break journey between source & destination stations
    :param source: source of the journey
    :param destination: destination of the journey
    :param logger: to log actions
    :return: list of breaking cities between source & destination
    """
    possibleBreakage = []
    try:
        url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ source +",IN&destination="+ destination +",IN&mode=transit&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY
        jsonTransitRoute = urllib.urlopen(url).read()
    except:
        ""
    if not jsonTransitRoute:
        return possibleBreakage

    possibleBreakage = parseTransitRoutes(jsonTransitRoute,destination)
    print possibleBreakage
    print possibleBreakage[0]
    return removeDuplicates(possibleBreakage[0])

def removeDuplicates(breakingStations):
    print breakingStations
    mySet = Set
    print mySet
    return mySet


#getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR')
models.getBreakingCity('BORIVALI')