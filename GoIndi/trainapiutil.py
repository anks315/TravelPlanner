__author__ = 'Ankit Kumar'

import copy, datetime
from GoIndi import dateTimeUtility, models, loggerUtil, miscUtility, minMaxUtil
from datetime import timedelta


logger = loggerUtil.getlogger("TrainApiUtil")


def getnextdaybusresults(buscontroller, sourcecity, destination, journeydate, numberofadults):
    """
    To fetch bus data for today, tomorrow and day after tomorrow between source and destination
    :param buscontroller: controller of bus api
    :param sourcecity: source city
    :param destination: destination of bus journey
    :param journeydate: date of journey
    :param numberofadults: no. of people travelling
    :return: bus data
    """
    breakingstationtodestinationbusjson = buscontroller.getresults(sourcecity, destination, journeydate, numberofadults)
    nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
    breakingstationtodestinationbusjson["bus"].extend(buscontroller.getresults(sourcecity, destination, nextday, numberofadults)["bus"])
    nextday = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + timedelta(days=2)).strftime('%d-%m-%Y')
    breakingstationtodestinationbusjson["bus"].extend(buscontroller.getresults(sourcecity, destination, nextday, numberofadults)["bus"])
    return breakingstationtodestinationbusjson


def combinedata(sourcetobreakingstationjson, breakingtodestinationjson):

    """
    To combine data from 2 parts into one
    :param sourcetobreakingstationjson: journey data from source to breaking city
    :param breakingtodestinationjson: journey data from breaking city to destination
    :return: combined data
    """
    resultjsondata = {"train": []}
    for route1 in sourcetobreakingstationjson["train"]:
        for route2 in breakingtodestinationjson["train"]:
            if dateTimeUtility.isjourneypossible(route1["parts"][0]["arrival"], route2["parts"][0]["departure"], route1["parts"][0]["arrivalDate"], route2["parts"][0]["departureDate"]):
                combinedjson = convertspartstofulljson(route1, route2)
                resultjsondata["train"].append(combinedjson)
    return resultjsondata


def combinemultipletraindata(sourcetofirstbreakingstationjson, firsttosecondbreakingstationjson, secondbreakingstationtodestinationjson):

    """
    To combine data from 3 train journey parts into one
    :param sourcetofirstbreakingstationjson: journey data from source to first breaking city
    :param firsttosecondbreakingstationjson: journey data from first breaking station to second one
    :param secondbreakingstationtodestinationjson: journey data from second breaking city to destination
    :return: combined data from 3 independent journeys
    """
    resultjsondata = {"train": []}
    for route1 in sourcetofirstbreakingstationjson["train"]:
        for route2 in firsttosecondbreakingstationjson["train"]:
            if dateTimeUtility.isjourneypossible(route1["parts"][0]["arrival"], route2["parts"][0]["departure"], route1["parts"][0]["arrivalDate"], route2["parts"][0]["departureDate"]):
                for route3 in secondbreakingstationtodestinationjson["train"]:
                    if dateTimeUtility.isjourneypossible(route2["parts"][0]["arrival"], route3["parts"][0]["departure"], route2["parts"][0]["arrivalDate"], route3["parts"][0]["departureDate"]):
                        combinedjson = convertmultipleparttofulljourney(route1, route2, route3)
                        resultjsondata["train"].append(combinedjson)
    return resultjsondata


def convertspartstofulljson(part_1, part_2):
    """
    This method is used to combine train journey data from part_1 and part_2 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    try:
        duration = dateTimeUtility.gettotalduration(part_2["full"][0]["arrival"],part_1["full"][0]["departure"],part_2["full"][0]["arrivalDate"],part_1["full"][0]["departureDate"])
        waitingTime = dateTimeUtility.getWaitingTime(part_1["full"][0]["arrival"],part_2["full"][0]["departure"],part_1["full"][0]["arrivalDate"],part_2["full"][0]["departureDate"])
        price = part_1["full"][0]["price"] + part_2["full"][0]["price"]
        part = {"carrierName": "Train","duration": duration, "id": part_1["full"][0]["id"] + "_" +part_2["full"][0]["id"] + str(1), "mode": "train", "site": "IRCTC", "source": part_1["full"][0]["source"],
                "destination": part_2["full"][0]["destination"], "arrival": part_2["full"][0]["arrival"], "departure": part_1["full"][0]["departure"], "departureDate": part_1["full"][0]["departureDate"],
                "arrivalDate": part_2["full"][0]["arrivalDate"], "route" : part_1["full"][0]["source"] + ",train," + part_2["full"][0]["source"] + ",train," + part_2["full"][0]["destination"],
                "prices": {"1A": part_1["full"][0]["prices"]["1A"] + part_2["full"][0]["prices"]["1A"],
                           "2A": part_1["full"][0]["prices"]["2A"] + part_2["full"][0]["prices"]["2A"],
                           "3A": part_1["full"][0]["prices"]["3A"] + part_2["full"][0]["prices"]["3A"],
                           "3E": part_1["full"][0]["prices"]["3E"] + part_2["full"][0]["prices"]["3E"],
                           "FC": part_1["full"][0]["prices"]["FC"] + part_2["full"][0]["prices"]["FC"],
                           "CC": part_1["full"][0]["prices"]["CC"] + part_2["full"][0]["prices"]["CC"],
                           "SL": part_1["full"][0]["prices"]["SL"] + part_2["full"][0]["prices"]["SL"],
                           "2S": part_1["full"][0]["prices"]["2S"] + part_2["full"][0]["prices"]["2S"],
                           "GN": part_1["full"][0]["prices"]["GN"] + part_2["full"][0]["prices"]["GN"]},
                "price": price, "priceClass": part_1["full"][0]["priceClass"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"] = part["id"] + str(1)
        part["subParts"][0]["waitingTime"] = waitingTime
        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(2)
        route["parts"].append(part)
        route["full"] = []
        full = {"id": part_1["full"][0]["id"]+ "_" +part_2["full"][0]["id"], "minPrice": price, "maxPrice": price, "minDuration": duration, "maxDuration": duration, "minArrival": part_2["full"][0]["arrival"],"maxArrival": part_2["full"][0]["arrival"],
                "minDeparture": part_1["full"][0]["departure"], "maxDeparture": part_1["full"][0]["departure"], "route": part["route"], "duration": duration, "price": price, "destination": part["destination"], "source": part["arrival"],
                "departureDate": part["departureDate"], "departureDay": models.getdayabbrevationfromdatestr(part["departureDate"], 0), "arrivalDate": part["arrivalDate"], "arrivalDay" : models.getdayabbrevationfromdatestr(part["arrivalDate"], 0),
                "departure": part["departure"], "arrival": part["arrival"]}

        route["full"].append(full)
    except Exception as e:
        logger.error("Error while combining data for Train[%s] and Train[%s], reason [%s]", part_1["full"]["id"], part_2["full"]["id"], e.message)

    return route


def convertmultipleparttofulljourney(part_1, part_2, part_3):
    """
    This method is used to combine train journey data from part_1, part_2 and part_3 into a single entity
    :param part_1: part 1 of journey
    :param part_2: part 2 of journey
    :param part_3: part 3 of the journey
    :return: combined journey data
    """

    route = {"full": {}, "parts": []}
    try:
        duration = dateTimeUtility.gettotalduration(part_3["full"][0]["arrival"],part_1["full"][0]["departure"],part_3["full"][0]["arrivalDate"],part_1["full"][0]["departureDate"])
        price = part_1["full"][0]["price"] + part_2["full"][0]["price"] + part_3["full"][0]["price"]
        waitingTime1 = dateTimeUtility.getWaitingTime(part_1["full"][0]["arrival"], part_2["full"][0]["departure"],
                                                     part_1["full"][0]["arrivalDate"],
                                                     part_2["full"][0]["departureDate"])
        waitingTime2 = dateTimeUtility.getWaitingTime(part_2["full"][0]["arrival"], part_3["full"][0]["departure"],
                                                      part_2["full"][0]["arrivalDate"],
                                                      part_3["full"][0]["departureDate"])
        part = {"carrierName": "Train","duration": duration, "id": part_1["full"][0]["id"] + "_" + part_2["full"][0]["id"] + part_3["full"][0]["id"] + str(1), "mode": "train", "site": "IRCTC", "source": part_1["full"][0]["source"],
                "destination": part_3["full"][0]["destination"], "arrival": part_3["full"][0]["arrival"], "departure": part_1["full"][0]["departure"], "departureDate": part_1["full"][0]["departureDate"],
                "arrivalDate": part_3["full"][0]["arrivalDate"], "route" : part_1["full"][0]["source"] + ",train," + part_2["full"][0]["source"] + ",train," + part_2["full"][0]["destination"] + ",train," + part_3["full"][0]["destination"],
                "prices": {"1A": part_1["full"][0]["prices"]["1A"] + part_2["full"][0]["prices"]["1A"] + part_3["full"][0]["prices"]["1A"],
                           "2A": part_1["full"][0]["prices"]["2A"] + part_2["full"][0]["prices"]["2A"] + part_3["full"][0]["prices"]["2A"],
                           "3A": part_1["full"][0]["prices"]["3A"] + part_2["full"][0]["prices"]["3A"] + part_3["full"][0]["prices"]["3A"],
                           "3E": part_1["full"][0]["prices"]["3E"] + part_2["full"][0]["prices"]["3E"] + part_3["full"][0]["prices"]["3E"],
                           "FC": part_1["full"][0]["prices"]["FC"] + part_2["full"][0]["prices"]["FC"] + part_3["full"][0]["prices"]["FC"],
                           "CC": part_1["full"][0]["prices"]["CC"] + part_2["full"][0]["prices"]["CC"] + part_3["full"][0]["prices"]["CC"],
                           "SL": part_1["full"][0]["prices"]["SL"] + part_2["full"][0]["prices"]["SL"] + part_3["full"][0]["prices"]["SL"],
                           "2S": part_1["full"][0]["prices"]["2S"] + part_2["full"][0]["prices"]["2S"] + part_3["full"][0]["prices"]["2S"],
                           "GN": part_1["full"][0]["prices"]["GN"] + part_2["full"][0]["prices"]["GN"] + part_3["full"][0]["prices"]["GN"]},
                "price": price, "priceClass": part_1["full"][0]["priceClass"], "subParts": []}
        part["subParts"].append(copy.deepcopy(part_1["parts"][0]["subParts"][0]))
        part["subParts"][0]["id"] = part["id"] + str(1)
        part["subParts"][0]["waitingTime"] = waitingTime1

        part["subParts"].append(copy.deepcopy(part_2["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(2)
        part["subParts"][1]["waitingTime"] = waitingTime2

        part["subParts"].append(copy.deepcopy(part_3["parts"][0]["subParts"][0]))
        part["subParts"][1]["id"] = part["id"] + str(3)

        route["parts"].append(part)
        route["full"] = []
        full = {"id": part_1["full"][0]["id"] + "_" + part_2["full"][0]["id"] + "_" + part_3["full"][0]["id"], "minPrice": price, "maxPrice": price, "minDuration": duration, "maxDuration": duration, "minArrival": part_3["full"][0]["arrival"],"maxArrival": part_3["full"][0]["arrival"],
                "minDeparture": part_1["full"][0]["departure"], "maxDeparture": part_1["full"][0]["departure"], "route": part["route"], "duration": duration, "price": price, "destination": part["destination"], "source": part["arrival"],
                "departureDate": part["departureDate"], "departureDay": models.getdayabbrevationfromdatestr(part["departureDate"], 0), "arrivalDate": part["arrivalDate"], "arrivalDay" : models.getdayabbrevationfromdatestr(part["arrivalDate"], 0),
                "departure": part["departure"], "arrival": part["arrival"]}

        route["full"].append(full)
    except Exception as e:
        logger.error("Error while combining data for Train[%s] and Train[%s], reason [%s]", part_1["full"]["id"], part_2["full"]["id"], e.message)

    return route


def combinebusandtraininit(sourcetobreakingbusjson, breakingtodestinationtrainjson):

    """
    To combine bus and train data. bus data is inserted before train journey.
    :param sourcetobreakingbusjson: bus data from source to breaking staion
    :param breakingtodestinationtrainjson: train data from breaking to destination
    :return: combined data (Source - Bus - Breaking City - Train - Destination)
    """

    combinedjson = {"train": []}

    for j in range(len(breakingtodestinationtrainjson["train"])):
        trainpart = breakingtodestinationtrainjson["train"][j]["parts"][0]
        subparts = []
        for k in range(len(sourcetobreakingbusjson["bus"])):
            subpart = sourcetobreakingbusjson["bus"][k]["parts"][0]
            if dateTimeUtility.isjourneypossible(subpart["arrival"], trainpart["departure"], subpart["arrivalDate"], trainpart["departureDate"], 2, 24):
                subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], trainpart["departure"],subpart["arrivalDate"],trainpart["departureDate"])
                subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(trainpart["departure"], subpart["departure"], trainpart["departureDate"], subpart["departureDate"])
                subparts.append(copy.deepcopy(subpart))

        if len(subparts) > 5:
            subparts.sort(miscUtility.sortonsubjourneytime)
            subparts = subparts[0:5]

        if subparts:
            minmax = minMaxUtil.getMinMaxValues(subparts)
            newpart = {"subParts": subparts, "mode": "bus","id": breakingtodestinationtrainjson["train"][j]["full"][0]["id"] + str(0), "destination": subparts[0]["destination"],
                       "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
            breakingtodestinationtrainjson["train"][j]["parts"].insert(0, newpart)
            breakingtodestinationtrainjson["train"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",train," + breakingtodestinationtrainjson["train"][j]["full"][0]["destination"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["price"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
            breakingtodestinationtrainjson["train"][j]["full"][0]["minPrice"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
            breakingtodestinationtrainjson["train"][j]["full"][0]["maxPrice"] = int(breakingtodestinationtrainjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
            breakingtodestinationtrainjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
            breakingtodestinationtrainjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
            breakingtodestinationtrainjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(breakingtodestinationtrainjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
            breakingtodestinationtrainjson["train"][j]["full"][0]["minDeparture"] = minmax["minDep"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["source"] = newpart["source"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["departure"] = subparts[0]["departure"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["departureDate"] = subparts[0]["departureDate"]
            breakingtodestinationtrainjson["train"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(subparts[0]["departureDate"], 0)
            breakingtodestinationtrainjson["train"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(breakingtodestinationtrainjson["train"][j]["full"][0]["arrivalDate"], 0)

    combinedjson["train"] = [x for x in breakingtodestinationtrainjson["train"] if len(x["parts"]) == 2]
    return combinedjson


def combinebusandtrainend(sourcetobreakingtrainjson, breakingtodestinationbusjson):

    """
    To combine train and bus data. Bus data is inserted after train journey.
    :param sourcetobreakingtrainjson: train data from source to breaking station
    :param breakingtodestinationbusjson: bus data from breaking to destination
    :return: combined data (Source - Train - Breaking City - Bus - Destination)
    """
    combinedjson = {"train": []}

    for j in range(len(sourcetobreakingtrainjson["train"])):
        trainpart = sourcetobreakingtrainjson["train"][j]["parts"][0]
        subparts = []
        for k in range(len(breakingtodestinationbusjson["bus"])):
            subpart = breakingtodestinationbusjson["bus"][k]["parts"][0]
            if dateTimeUtility.isjourneypossible(trainpart["arrival"], subpart["departure"], trainpart["arrivalDate"], subpart["departureDate"], 2, 10):
                subpart["waitingTime"] = dateTimeUtility.getWaitingTime(trainpart["arrival"], subpart["departure"],trainpart["arrivalDate"],subpart["departureDate"])
                subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], trainpart["arrival"], subpart["arrivalDate"], trainpart["arrivalDate"])
                subparts.append(copy.deepcopy(subpart))

        if len(subparts) > 5:
            subparts.sort(miscUtility.sortonsubjourneytime)
            subparts = subparts[0:5]

        if subparts:
            minmax = minMaxUtil.getMinMaxValues(subparts)
            newpart = {"subParts": subparts, "mode": "bus", "id": sourcetobreakingtrainjson["train"][j]["full"][0]["id"] + str(2), "destination": subparts[0]["destination"],
                       "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
            sourcetobreakingtrainjson["train"][j]["parts"].append(newpart)
            sourcetobreakingtrainjson["train"][j]["full"][0]["route"] = sourcetobreakingtrainjson["train"][j]["full"][0]["source"] + ",train," + newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["price"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
            sourcetobreakingtrainjson["train"][j]["full"][0]["minPrice"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
            sourcetobreakingtrainjson["train"][j]["full"][0]["maxPrice"] = int(sourcetobreakingtrainjson["train"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
            sourcetobreakingtrainjson["train"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
            sourcetobreakingtrainjson["train"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["minDuration"], minmax["minDuration"])
            sourcetobreakingtrainjson["train"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(sourcetobreakingtrainjson["train"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
            sourcetobreakingtrainjson["train"][j]["full"][0]["minArrival"] = minmax["minArr"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["destination"] = subparts[0]["destination"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
            sourcetobreakingtrainjson["train"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
            sourcetobreakingtrainjson["train"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(sourcetobreakingtrainjson["train"][j]["full"][0]["departureDate"], 0)

    combinedjson["train"] = [x for x in sourcetobreakingtrainjson["train"] if len(x["parts"]) == 2]
    return combinedjson