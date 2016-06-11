
__author__ = 'ankur'

import json
import urllib2
import requests
from requests.auth import HTTPDigestAuth
from django.http import HttpResponse
import dateTimeUtility
import loggerUtil
import logging
import TravelPlanner.trainUtil

logger = loggerUtil.getLogger("BusApi",logging.DEBUG)


class BusController:
    """Class returns all stations corresponding to a city"""


    def getResults(self, source, destination, journeyDate):
        response = {"bus": []}
        try:
            source = TravelPlanner.trainUtil.getbuscity(source)
            destination = TravelPlanner.trainUtil.getbuscity(destination)
            logger.debug("[START]-Get Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeyDate)
            jdList = journeyDate.split("-")
            newFormatJourneyDate = jdList[2]+"-"+jdList[1]+"-"+jdList[0]
            url = "http://agent.etravelsmart.com/etsAPI/api/getAvailableBuses?sourceCity="+source+"&destinationCity="+destination+"&doj="+newFormatJourneyDate
            req = requests.get(url, auth=HTTPDigestAuth('eazzer', 'E@ZZer1713'), timeout=20)
            response = self.parseResultAndReturnFare(req.json(),source,destination,journeyDate,newFormatJourneyDate)
        except:
            logger.info("Error Getting Data For Source[%s] and Destination[%s],JourneyDate:[%s]",source,destination,journeyDate)
        logger.debug("[END]-Get Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeyDate)
        return response

    def parseResultAndReturnFare(self, jsonData, source, destination,journeyDate,newFormatJourneyDate):
            resultjsondata= {"bus": []}
            try:
                counter = 1
                if jsonData["apiAvailableBuses"]:
                    for option in jsonData["apiAvailableBuses"]:
                        route = {}
                        route["full"] = []
                        route["parts"] = []
                        part = {}
                        part["carrierName"] = option["operatorName"]
                        priceList = option["fare"].split(',')
                        prices = ''
                        for price in priceList:
                            prices = prices + str(price.split('.')[0])+','
                        part["busType"]=option["busType"]
                        part["price"]=prices
                        part["mode"]="bus"
                        arrival = option["arrivalTime"]
                        departure = option["departureTime"]
                        arrArr = arrival.split(' ')
                        arrTimeArr = arrArr[0].split(':')
                        if arrArr[1]=="PM" and arrTimeArr[0]!="12":
                            arrHr=int(arrTimeArr[0])+12
                        else:
                            arrHr = arrTimeArr[0]
                        arrMin = arrTimeArr[1]

                        depArr = departure.split(' ')
                        depTimeArr = depArr[0].split(':')
                        if depArr[1] == "PM" and depTimeArr[0]!="12":
                            depHr = int(depTimeArr[0]) + 12
                        else:
                            depHr = depTimeArr[0]
                        depMin = depTimeArr[1]
                        if int(arrHr)<int(depHr):
                            durHr = 24 + (int(arrHr)-int(depHr))
                        else:
                            durHr = int(arrHr)-int(depHr)
                        durMin = int(arrMin)-int(depMin)
                        if durMin<0:
                            durMin = 60 + int(durMin)
                            durHr = int(durHr) - 1
                        part["duration"] = str(durHr)+":"+str(durMin)
                        part["source"] = source
                        part["destination"] = destination
                        part["arrival"] = str(arrHr)+':'+str(arrMin)
                        part["departure"] = str(depHr)+':'+str(depMin)
                        part["availableSeats"] = option["availableSeats"]
                        part["id"] = "bus"+str(counter)+str("1")
                        part["inventoryType"] = option["inventoryType"]
                        part["routeScheduleId"]= option["routeScheduleId"]
                        part["departureDate"]=journeyDate
                        part["arrivalDate"]=dateTimeUtility.calculateArrivalTimeAndDate(journeyDate,part["departure"],part["duration"])["arrivalDate"]
                        part["bookingLink"]= "http://www.etravelsmart.com/bus/seat-book.htm?source="+source+"&destination="+destination+"&jdate="+newFormatJourneyDate+"&routeid="+option["routeScheduleId"]+"&apiType="+option["routeScheduleId"]+"&userId=eazzer&txnId=000111"
                        route["parts"].append(part)
                        full=part
                        full["id"]="bus"+str(counter)

                        route["full"].append(full)

                        resultjsondata["bus"].append(route)
                else:
                    logger.debug("Empty Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeyDate)
            except:
                logger.info("Parsing Error for Source:[%s] and Destination:[%s],JourneyDate:[%s]",source,destination,journeyDate)

            return resultjsondata