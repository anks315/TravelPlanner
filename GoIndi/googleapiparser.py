
import urllib
import trainConstants
import json
import models
from sets import Set
import calendar
import time
import concurrent.futures

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
                possiblebreak = Set()
                for step in leg["steps"]:
                    if "transit_details" in step and ("RAIL" in step["transit_details"]["line"]["vehicle"]["type"] or "Train" in step["transit_details"]["line"]["vehicle"]["name"]):
                        routedestinationstation = str(step["transit_details"]["arrival_stop"]["name"]).upper()
                        destinationcity = getcityfromstation(routedestinationstation, logger)
                        if counter == 1 and destination in destinationcity:
                            possiblebreak.add(getcityfromstation(step["transit_details"]["departure_stop"]["name"].upper(), logger))

                        if counter != 0 and destination not in destinationcity:
                            possiblebreak.add(getcityfromstation(step["transit_details"]["departure_stop"]["name"].upper(), logger))
                            possiblebreak.add(destinationcity)
                        counter += 1
                possiblebreaklist.append(possiblebreak)
    return possiblebreaklist


def getcityfromstation(routedestinationstation, logger):

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
    except Exception as e:
        logger.error("Error getting city for breakingstation[%s], reason [%s]", routedestinationstation, e.message)

    possiblecities = routedestinationstation.split()  # split by space and search on indiviual words
    for possiblecity in possiblecities:
        possiblecity = possiblecity.upper()
        try:
            if possiblecity not in skipValues:
                city = models.getBreakingCity(possiblecity, logger)
                if city:
                    return city
        except Exception as e:
            logger.error("Error getting city for breakingstation[%s], reason [%s]", possiblecity, e.message)

    logger.warning("Breaking Station [%s] not mapped to any city", routedestinationstation)
    return routedestinationstation # return same value if not mapped to any station


def getPossibleBreakingPlacesForTrain(source,destination, logger, journeydate):

    """
    To get possible stations to break journey between source & destination stations
    :param source: source of the journey
    :param destination: destination of the journey
    :param logger: to log actions
    :param journeydate date of journey
    :return: list of breaking cities between source & destination
    """

    epochjourneytime = calendar.timegm(time.strptime(journeydate, '%d-%m-%Y'))
    epochtime = int(time.time())
    epochs = [epochtime, epochjourneytime]
    futures = []
    possiblebreakage = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for epoch in epochs:
            logger.info("Getting breaking station in journey from source[%s] to destination[%s]", source, destination)
            futures.append(executor.submit(getBreakingCities, source, destination, epoch, logger))
    for future in futures:
        if future:
            possiblebreakage.extend(future.result())
            logger.debug("Breaking journey stations between source[%s] and destination[%s] are [%s]", source, destination, possiblebreakage)
        else:
            logger.warning("No breaking station between source[%s] and destination[%s]", source, destination)
    return possiblebreakage


def getBreakingCities(source, destination, epoch, logger):
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ source +",IN&destination="+ destination +",IN&mode=transit&transit_mode=train&departure_time=" + str(epoch) +"&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY
    try:
        jsontransitroute = urllib.urlopen(url).read()
    except Exception as e:
        logger.error("Error in getting breaking station between source[%s] and destination[%s], reson [%s]", source, destination, e.message)

    return parseTransitRoutes(jsontransitroute,destination, logger)
