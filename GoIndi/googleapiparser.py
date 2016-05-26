
import urllib
import trainConstants
import json
import models
from sets import Set

skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN'])

def parseTransitRoutes(jsontransitroute,destination, logger):

    """
    To parse breaking journey json object
    :param jsontransitroute: breaking journey data
    :param destination: destination of journey
    :return: list of all possible breaking stations
    """
    returnedData = json.loads(jsontransitroute)
    # list containing list of all breaking points
    possiblebreaklist=[]
    for route in returnedData["routes"]:
        if route:
            for leg in route["legs"]:
                counter=0
                possiblebreak = []
                for step in leg["steps"]:
                    if "transit_details" in step and ("RAIL" in step["transit_details"]["line"]["vehicle"]["type"] or "Train" in step["transit_details"]["line"]["vehicle"]["name"]):
                        routedestinationstation = str(step["transit_details"]["arrival_stop"]["name"]).upper()
                        destinationcity = getdestinationcity(routedestinationstation, logger)
                        if counter == 1 and destination in destinationcity:
                            possiblebreak.append(step["transit_details"]["departure_stop"]["name"])

                        if counter != 0 and destination not in destinationcity:
                            possiblebreak.append(step["transit_details"]["departure_stop"]["name"])
                            possiblebreak.append(step["transit_details"]["arrival_stop"]["name"])
                        counter += 1
                possiblebreaklist.append(possiblebreak)
    return possiblebreaklist


def getdestinationcity(routedestinationstation, logger):

    """
    This method is used to fetch destination from station name
    :param routedestinationstation: destination station/city
    :param logger: to log events
    :return: destination city name if mapped to routedestinationstation
    """
    try:
        city = models.getBreakingCity(routedestinationstation, logger)
        if city:
            return city
    except:
        logger.error("Error getting city for breakingstation[%s]", routedestinationstation)

    possiblecities = routedestinationstation.split()  # split by space and search on indiviual words
    for possiblecity in possiblecities:
        try:
            if possiblecity.upper() not in skipValues:
                city = models.getBreakingCity(possiblecity.upper(), logger)
                if city:
                    return city
        except:
            logger.error("Error getting city for breakingstation[%s]", possiblecity.upper())

    logger.warning("Breaking Station [%s] not mapped to any station in DB", routedestinationstation)
    return routedestinationstation # return same value if not mapped to any station


def getPossibleBreakingPlacesForTrain(source,destination, logger):

    """
    To get possible stations to break journey between source & destination stations
    :param source: source of the journey
    :param destination: destination of the journey
    :param logger: to log actions
    :return: list of breaking cities between source & destination
    """
    possiblebreakage = []
    try:
        logger.info("Getting breaking station in journey from source[%s] to destination[%s]", source, destination)
        jsontransitroute = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+ source +",IN&destination="+ destination +",IN&mode=transit&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY).read()
    except:
        logger.error("Error in getting breaking station between source[%s] and destination[%s]", source, destination)
    if not jsontransitroute:
        logger.warning("No breaking journey between source[%s] and destination[%s]", source, destination)
        return possiblebreakage
    logger.debug("Breaking journey between source[%s] and destination[%s] is [%s]", source, destination, jsontransitroute)
    possiblebreakage = parseTransitRoutes(jsontransitroute,destination, logger)
    logger.debug("Breaking journey stations between source[%s] and destination[%s] are [%s]", source, destination, possiblebreakage)
    return possiblebreakage

