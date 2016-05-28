__author__ = 'ankur'

from skyscanner import Flights

def getApiResults(source,destination):
    flights_service = Flights('ea816376821941695778768433999242')
    result = flights_service.get_result(
        country='IN',
        currency='INR',
        locale='en-US',
        originplace=source+'-sky',
        destinationplace=destination+'-sky',
        outbounddate='2016-05-28',
        adults=1).parsed
    resultJson=parseFlightAndReturnFare(result)
    return resultJson



def parseFlightAndReturnFare(apiresult):
    returnedFareData = apiresult

    resultJsonData = {}
    resultJsonData["flight"]=[]
    partNo = 0
    if len(returnedFareData["Itineraries"])==0:
        return
    flightCounter=-1

    for itinerary in returnedFareData["Itineraries"]:
            route ={}
            full={}
            part={}
            flightCounter=flightCounter+1
            route["full"]=full
            route["parts"]=[]
            route["parts"].append(part)
            part["price"]=itinerary["PricingOptions"][0]["Price"]
            part["id"]= "flight"+str(flightCounter)+str(partNo)
            part["mode"]="flight"
            part["arrival"]=returnedFareData["Legs"][flightCounter]["Arrival"]
            part["departure"]=returnedFareData["Legs"][flightCounter]["Departure"]
            duration = returnedFareData["Legs"][flightCounter]["Duration"]
            hours = int(duration)/60
            minutes = int(duration)%60
            part["duration"]= str(hours)+":"+str(minutes)
            part["subparts"]=[]
            if returnedFareData["Legs"][flightCounter]["Stops"]:
                Source =getCityNameById(returnedFareData["Legs"][flightCounter]["OriginStation"],returnedFareData["Places"])
                stopNumber=0
                for stop in returnedFareData["Legs"][flightCounter]["Stops"]:
                    subpart = {}
                    subpart["source"]=Source
                    subpart["destination"]=getCityNameById(stop,returnedFareData["Places"])
                    subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["FlightNumber"]
                    subpart["carrier"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["CarrierId"],returnedFareData["Carriers"])
                    Source=subpart["destination"]
                    part["subparts"].append(subpart)
                    stopNumber=stopNumber+1
                subpart = {}
                subpart["source"]=Source
                subpart["destination"]=getCityNameById(returnedFareData["Legs"][flightCounter]["DestinationStation"],returnedFareData["Places"])
                subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["FlightNumber"]
                subpart["carrier"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["CarrierId"],returnedFareData["Carriers"])
                part["subparts"].append(subpart)
            else:
                subpart = {}
                subpart["source"]=getCityNameById(returnedFareData["Legs"][flightCounter]["OriginStation"],returnedFareData["Places"])
                subpart["destination"]=getCityNameById(returnedFareData["Legs"][flightCounter]["DestinationStation"],returnedFareData["Places"])
                subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][0]["FlightNumber"]
                subpart["carrier"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][0]["CarrierId"],returnedFareData["Carriers"])
                part["subparts"].append(subpart)

            resultJsonData["flight"].append(route)
    return resultJsonData


def getCityNameById(stationId,stationsList):
    for station in stationsList:
        if station["Id"]==stationId:
            return station["Name"]

def getCarrierNameById(carrierId,carriersList):
    for carrier in carriersList:
        if carrier["Id"]==carrierId:
            return carrier["Name"]