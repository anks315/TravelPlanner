
__author__ = 'ankur'

import requests
from requests.auth import HTTPDigestAuth
import dateTimeUtility
import loggerUtil, models
import TravelPlanner.startuputil

logger = loggerUtil.getlogger("BusApi")


class BusController:
    """Class returns all stations corresponding to a city"""

    def getresults(self, source, destination, journeydate, numberofadults=1):

        response = {"bus": []}
        try:
            source = TravelPlanner.startuputil.getbuscity(source)
            destination = TravelPlanner.startuputil.getbuscity(destination)
            logger.debug("[START]-Get Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeydate)
            jdlist = journeydate.split("-")
            newformatjourneydate = jdlist[2]+"-"+jdlist[1]+"-"+jdlist[0]
            url = "http://agent.etravelsmart.com/etsAPI/api/getAvailableBuses?sourceCity="+source+"&destinationCity="+destination+"&doj="+newformatjourneydate
            req = requests.get(url, auth=HTTPDigestAuth('eazzer', 'E@ZZer1713'), timeout=20)
            response = self.parseresultandreturnfare(req.json(),source,destination,journeydate,newformatjourneydate,numberofadults)
        except Exception as e:
            logger.error("Error Getting Data For Source[%s] and Destination[%s],JourneyDate:[%s], reason [%s]",source,destination,journeydate, e.message)
            return response
        logger.debug("[END]-Get Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeydate)
        return response

    def parseresultandreturnfare(self, jsondata, source, destination, journeydate, newformatjourneydate, numberofadults=1):
            resultjsondata= {"bus": []}
            try:
                counter = 1
                if jsondata["apiAvailableBuses"]:
                    for option in jsondata["apiAvailableBuses"]:
                        route = {"full": [], "parts": []}
                        part = {"carrierName": option["operatorName"]}
                        pricelist = option["fare"].split(',')
                        prices = ''
                        for price in pricelist:
                            prices = prices + str(int(price.split('.')[0])*int(numberofadults))+','
                        part["busType"]=option["busType"]
                        part["price"]=prices
                        part["mode"]="bus"
                        arrival = option["arrivalTime"]
                        departure = option["departureTime"]
                        arrarr = arrival.split(' ')
                        arrtimearr = arrarr[0].split(':')
                        if arrarr[1]=="PM" and arrtimearr[0]!="12":
                            arrhr=int(arrtimearr[0])+12
                        else:
                            arrhr = arrtimearr[0]
                        arrmin = arrtimearr[1]

                        deparr = departure.split(' ')
                        deptimearr = deparr[0].split(':')
                        if deparr[1] == "PM" and deptimearr[0]!="12":
                            dephr = int(deptimearr[0]) + 12
                        else:
                            dephr = deptimearr[0]
                        depmin = deptimearr[1]
                        if int(arrhr)<int(dephr):
                            durhr = 24 + (int(arrhr)-int(dephr))
                        else:
                            durhr = int(arrhr)-int(dephr)
                        durmin = int(arrmin)-int(depmin)
                        if durmin<0:
                            durmin = 60 + int(durmin)
                            durhr = int(durhr) - 1
                        part["duration"] = str(durhr)+":"+str(durmin)
                        part["source"] = source
                        part["destination"] = destination
                        part["arrival"] = str(arrhr)+':'+str(arrmin)
                        part["departure"] = str(dephr)+':'+str(depmin)
                        part["availableSeats"] = option["availableSeats"]
                        part["id"] = "bus"+str(counter)+str("1")
                        part["inventoryType"] = option["inventoryType"]
                        part["routeScheduleId"]= option["routeScheduleId"]
                        part["departureDate"] = journeydate
                        part["departureDay"] = models.getdayabbrevationfromdatestr(journeydate)
                        part["arrivalDate"] = dateTimeUtility.calculatearrivaltimeanddate(journeydate, part["departure"], part["duration"])["arrivalDate"]
                        part["arrivalDay"] = models.getdayabbrevationfromdatestr(part["arrivalDate"])
                        part["bookingLink"] = "http://www.etravelsmart.com/bus/seat-book.htm?source="+source+"&destination="+destination+"&jdate="+newformatjourneydate+"&routeid="+option["routeScheduleId"]+"&apiType="+str(option["inventoryType"])+"&userId=eazzer&txnId=000111"
                        route["parts"].append(part)
                        full = part
                        full["id"] = "bus"+str(counter)

                        route["full"].append(full)

                        resultjsondata["bus"].append(route)
                else:
                    logger.debug("Empty Results From BusApi for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeydate)
            except:
                logger.info("Parsing Error for Source:[%s] and Destination:[%s],JourneyDate:[%s]",source,destination,journeydate)

            return resultjsondata