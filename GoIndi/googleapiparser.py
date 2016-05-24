
import urllib
import trainConstants
import json
from sets import Set


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
                if stepNumber == 1 and destination in str(step["transit_details"]["arrival_stop"]["name"]).upper():
                    possibleBreakList.append(step["transit_details"]["departure_stop"]["name"])

                if stepNumber != 0 and destination not in str(step["transit_details"]["arrival_stop"]["name"]).upper():
                    possibleBreakList.append(step["transit_details"]["departure_stop"]["name"])
                    possibleBreakList.append(step["transit_details"]["arrival_stop"]["name"])
                stepNumber += 1
    return possibleBreakList



def getPossibleBreakingPlacesForTrain(source,destination, logger):

    """
    To get possible stations to break journey between source & destination stations
    :param source: source of the journey
    :param destination: destination of the journey
    :param logger: to log actions
    :return: list of breaking cities between source & destination
    """
    possibleBreakage = []
    try:
        logger.info("Getting breaking station in journey from source[%s] to destination[%s]", source, destination)
        jsonTransitRoute = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+ source +",IN&destination="+ destination +",IN&mode=transit&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY).read()
    except:
        logger.error("Error in getting breaking station between source[%s] and destination[%s]", source, destination)
    if not jsonTransitRoute:
        logger.warning("No breaking journey between source[%s] and destination[%s]", source, destination)
        return possibleBreakage
    logger.debug("Breaking journey between source[%s] and destination[%s] is [%s]", source, destination, jsonTransitRoute)
    possibleBreakage = parseTransitRoutes(jsonTransitRoute,destination)
    logger.debug("Breaking journey stations between source[%s] and destination[%s] are [%s]", source, destination, possibleBreakage)
    return possibleBreakage


def removeDuplicates(breakingStations):
    stations = breakingStations.split()
    set = Set(stations)
