
import urllib
import trainConstants
import json
import models
from sets import Set
import calendar
import time
import concurrent.futures

skipValues = Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT', 'JN', 'ROAD'])


def parsetransitroutes(jsontransitroute, destination, logger):

    """
    To parse breaking journey json object
    :param jsontransitroute: breaking journey data
    :param destination: destination of journey
    :return: list of all possible breaking stations list
    """
    returneddata = json.loads(jsontransitroute)
    # list containing list of all breaking points
    possiblebreaklist = []
    for route in returneddata["routes"]:
        if route:
            for leg in route["legs"]:
                counter=0
                possiblebreak = []
                for step in leg["steps"]:
                    if "transit_details" in step and ("RAIL" in step["transit_details"]["line"]["vehicle"]["type"] or "Train" in step["transit_details"]["line"]["vehicle"]["name"]):
                        routedestinationstation = str(step["transit_details"]["arrival_stop"]["name"]).upper()
                        destinationcity = getcityfromstation(routedestinationstation, logger)
                        if counter == 1 and destination in destinationcity:
                            addtopossiblebreaklist(possiblebreak, getcityfromstation(str(step["transit_details"]["departure_stop"]["name"]).upper(), logger), logger)

                        if counter != 0 and destination not in destinationcity:
                            addtopossiblebreaklist(possiblebreak, getcityfromstation(str(step["transit_details"]["departure_stop"]["name"]).upper(), logger), logger)
                            addtopossiblebreaklist(possiblebreak, destinationcity, logger)
                        counter += 1
                possiblebreaklist.append(possiblebreak)
    return possiblebreaklist


def addtopossiblebreaklist(possiblebreak, breakingcityname, logger):
    """
    To add breaking city name in possiblebreak city list
    :param possiblebreak: list of possible breaking city
    :param breakingcityname: breaking city name
    """
    if breakingcityname not in possiblebreak:
        logger.info("Adding breaking city [%s] to possible breaking city list", breakingcityname)
        possiblebreak.append(breakingcityname)


def getcityfromstation(routedestinationstation, logger):
    """
    This method is used to fetch destination from station name
    :param routedestinationstation: destination station/city
    :param logger: to log events
    :return: destination city name if mapped to routedestinationstation
    """
    try:
        city = models.getbreakingcity(routedestinationstation, logger)
        if city:
            return city
    except Exception as e:
        logger.error("Error getting city for breakingstation[%s], reason [%s]", routedestinationstation, e.message)

    possiblecities = routedestinationstation.split()  # split by space and search on indiviual words
    for possiblecity in possiblecities:
        possiblecity = possiblecity.upper()
        try:
            if possiblecity not in skipValues:
                city = models.getbreakingcity(possiblecity, logger)
                if city:
                    return city
        except Exception as e:
            logger.error("Error getting city for breakingstation[%s], reason [%s]", possiblecity, e.message)

    logger.warning("Breaking Station [%s] not mapped to any city", routedestinationstation)
    return routedestinationstation # return same value if not mapped to any station


def getpossiblebreakingplacesfortrain(source,destination, logger, journeydate, executor):

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
    for epoch in epochs:
        logger.debug("Getting breaking station in journey from source[%s] to destination[%s]", source, destination)
        futures.append(executor.submit(getbreakingcities, source, destination, epoch, logger))
    for future in futures:
        if future:
            possiblebreakage.extend(future.result())
            logger.info("Breaking journey stations between source[%s] and destination[%s] are [%s]", source, destination, possiblebreakage)
        else:
            logger.warning("No breaking station between source[%s] and destination[%s]", source, destination)
    return possiblebreakage


def getbreakingcities(source, destination, epoch, logger):
    jsontransitroute = ''
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ source +",IN&destination="+ destination +",IN&mode=transit&transit_mode=train&departure_time=" + str(epoch) +"&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY
    try:
        jsontransitroute = urllib.urlopen(url).read()
    except Exception as e:
        logger.error("Error in getting breaking station between source[%s] and destination[%s], reason [%s]", source, destination, e.message)
        return jsontransitroute

    return parsetransitroutes(jsontransitroute,destination, logger)
