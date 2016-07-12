from GoIndi import models

__author__ = 'ankur'

from skyscannerEazzer import Flights
import dateTimeUtility
import logging
import loggerUtil


logger = loggerUtil.getlogger("FlighSkyScanner", logging.DEBUG)

def getApiResults(sourcecity,destinationcity,journeydate,id,flightClass='Economy',numberOfAdults=1):
    cityandstatetostationsmap = {'Jaisalmer':'JSA','Rajahmundry':'RJA','Rajamundry':'RJA','Pantnagar':'PGH','Pathankot':'IXP','Kullu':'KUU','Agartala': 'IXA', 'Agra': 'AGR', 'Ahmedabad': 'AMD', 'Allahabad': 'IXD',
                                 'Amritsar': 'ATQ', 'Aurangabad': 'IXU', 'Bagdogra': 'IXB', 'Bangalore': 'BLR',
                                 'Bhavnagar': 'BHU', 'Bhopal': 'BHO', 'Bhubaneswar': 'BBI', 'Bhuj': 'BHJ',
                                 'Calcutta': 'CCU', 'Kolkata': 'CCU', 'Chandigarh': 'IXC', 'Chennai': 'MAA',
                                 'Madras': 'MAA', 'Cochin': 'COK', 'Coimbatore': 'CJB', 'Daman': 'NMB',
                                 'Dehradun': 'DED', 'Dibrugarh': 'DIB', 'Dimapur': 'DMU', 'Diu': 'DIU',
                                 'Guwahati': 'GAU', 'Goa': 'GOI', 'Gwalior': 'GWL', 'Hubli': 'HBX', 'Hyderabad': 'HYD',
                                 'Imphal': 'IMF', 'Indore': 'IDR', 'Jaipur': 'JAI', 'Jammu': 'IXJ', 'Jamnagar': 'JGA',
                                 'Jamshedpur': 'IXW', 'Jodhpur': 'JDH', 'Jorhat': 'JRH', 'Kanpur': 'KNU',
                                 'Khajuraho': 'HJR', 'Kozhikode': 'CCJ', 'calicut': 'CCJ', 'Leh': 'IXL',
                                 'Lucknow': 'LKO', 'Ludhiana': 'LUH', 'Madurai': 'IXM', 'Mangalore': 'IXE',
                                 'Mumbai': 'BOM', 'Bombay': 'BOM', 'Nagpur': 'NAG', 'Nanded': 'NDC', 'Nasik': 'ISK',
                                 'New Delhi': 'DEL', 'Patna': 'PAT', 'Pondicherry': 'PNY',
                                 'Poona': 'PNQ', 'Pune': 'PNQ', 'Porbandar': 'PBD', 'Port Blair': 'IXZ',
                                 'PuttasubParthi': 'PUT', 'Rae Bareli': 'BEK', 'Rajkot': 'RAJ', 'Ranchi': 'IXR',
                                 'Shillong': 'SHL', 'Silchar': 'IXS', 'Srinagar': 'SXR', 'Surat': 'STV',
                                 'Tezpur': 'TEZ', 'Tiruchirapally': 'TRZ', 'Tirupati': 'TIR', 'Trivandrum': 'TRV',
                                 'Udaipur': 'UDR', 'Vadodara': 'BDQ', 'Varanasi': 'VNS', 'Vijayawada': 'VGA',
                                 'Vishakhapatnam': 'VTZ', 'Gurgaon': 'DEL', 'Noida': 'DEL', 'Ghaziabad': 'DEL',
                                 'Tripura': 'IXA', 'Uttar Pradesh': 'AGR', 'Gujarat': 'AMD', 'Uttar Pradesh': 'IXD',
                                 'Punjab': 'ATQ', 'Maharashtra': 'IXU', 'Sikkim': 'IXB', 'Karnataka': 'BLR',
                                 'Gujarat': 'BHU', 'Madhya Pradesh': 'BHO', 'Orissa': 'BBI', 'Gujarat': 'BHJ',
                                 'West Bengal': 'CCU', 'Chandigarh': 'IXC', 'Tamil Nadu': 'MAA', 'Kochi': 'COK',
                                 'Coimbatore': 'CJB', 'Daman': 'NMB', 'Uttar Pradesh': 'DED', 'Assam': 'DIB',
                                 'Nagaland': 'DMU', 'Daman and Diu': 'DIU', 'Assam': 'GAU', 'Goa': 'GOI',
                                 'Madhya Pradesh': 'GWL', 'Karnataka': 'HBX', 'Andhra Pradesh': 'HYD', 'Manipur': 'IMF',
                                 'Madhya Pradesh': 'IDR', 'Rajasthan': 'JAI', 'Jammu & Kashmir': 'IXJ',
                                 'Gujarat': 'JGA', 'Jharkhand': 'IXW', 'Rajasthan': 'JDH', 'Assam': 'JRH',
                                 'Uttar Pradesh': 'KNU', 'Madhya Pradesh': 'HJR', 'Kerala': 'CCJ',
                                 'Jammu & Kashmir': 'IXL', 'Utter Pradesh': 'LKO', 'Punjab': 'LUH', 'Tamil Nadu': 'IXM',
                                 'Karnataka': 'IXE', 'Maharashtra': 'BOM', 'Maharashtra': 'NDC', 'Maharashtra': 'ISK',
                                 'Delhi': 'DEL', 'Bihar': 'PAT', 'Maharashtra': 'PNQ', 'Gujarat': 'PBD',
                                 'Andaman and Nicobar Islands': 'IXZ', 'Andhra Pradesh': 'PUT', 'Uttar Pradesh': 'BEK',
                                 'Gujarat': 'RAJ', 'Jharkhand': 'IXR', 'Meghalaya': 'SHL', 'Mizoram': 'IXS',
                                 'J & K': 'SXR', 'Gujrat': 'STV', 'Assam': 'TEZ', 'Tamil Nadu': 'TRZ',
                                 'Andhra Pradesh': 'TIR', 'Kerala': 'TRV', 'Rajasthan': 'UDR', 'Gujarat': 'BDQ',
                                 'Uttar Pradesh': 'VNS', 'Andhra Pradesh': 'VGA', 'Andhra Pradesh': 'VTZ','Shimla':'SLV',
                                 'Keshod' : 'IXK', 'Jabalpur' : 'JLR'}

    resultjson = {"flight": []}
    try:
        source = cityandstatetostationsmap[sourcecity]
        destination = cityandstatetostationsmap[destinationcity]
        logger.info("[START]-Get Results From SkyScanner for Source:[%s]-[%s] and Destination:[%s]-[%s],JourneyDate:[%s] ",sourcecity,source,destinationcity,destination,journeydate)
        year = journeydate.split("-")[2]
        month = journeydate.split("-")[1]
        day = journeydate.split("-")[0]
        flights_service = Flights('ea816376821941695778768433999242')
        logger.debug("Polling Session for Source:[%s] and Destination:[%s],JourneyDate:[%s]",source,destination,journeydate)
        retries=3
        while retries!=0:
            result = flights_service.poll_session(flights_service.create_session( country='IN',
                currency='INR',
                locale='en-US',
                originplace=source+'-sky',
                destinationplace=destination+'-sky',
                outbounddate=str(year)+'-'+str(month)+'-'+str(day),
                adults=int(numberOfAdults),cabinclass=flightClass,groupPricing=True), initial_delay = 1, delay = 1, tries = 100).parsed
            if result:
                resultjson = parseflightandreturnfare(result, id, sourcecity, destinationcity, journeydate)
                break
            logger.debug("Retrying... Empty Response From SkyScanner for Source:[%s] and Destination:[%s],journeyDate:[%s]",source,destination,journeydate)
            retries=retries-1
    except Exception as e:
        logger.error("Exception while fetching flights from [%s] to destination [%s] on [%s]", sourcecity, destinationcity, journeydate)
        pass

    logger.info("[END]-Get Results From SkyScanner for Source:[%s]-[%s] and Destination:[%s]-[%s],JourneyDate:[%s] ",sourcecity,source,destinationcity,destination,journeydate)

    return resultjson


def parseflightandreturnfare(apiresult, id, source, destination, journeydate):
    logger.info("Parsing SkyScanner Final Result for Source:[%s] and Destination:[%s],JourneyDate:[%s] ",source,destination,journeydate)
    returnedfaredata = apiresult
    resultjsondata = {"flight": []}
    partno = 0
    if len(returnedfaredata["Itineraries"])==0:
        logger.warn("Skyscanner responded no Data for Source:[%s] and Destination:[%s],JourneyDate:[%s]",source,destination,journeydate)
        return resultjsondata
    flightcounter=-1

    for itinerary in returnedfaredata["Itineraries"]:
        route = {}
        full= {"id": str(id) + str(flightcounter)}
        part={}
        flightcounter += 1
        route["full"]=[]
        route["full"].append(full)
        route["parts"]=[]
        route["parts"].append(part)
        part["price"]=int(itinerary["PricingOptions"][0]["Price"])
        full["price"]=int(itinerary["PricingOptions"][0]["Price"])
        full["minPrice"]=int(itinerary["PricingOptions"][0]["Price"])
        full["maxPrice"]=int(itinerary["PricingOptions"][0]["Price"])
        part["id"]= str(id)+str(flightcounter)+str(partno)
        part["mode"]="flight"
        part["source"] = source
        part["destination"] = destination
        part["arrival"]=(returnedfaredata["Legs"][flightcounter]["Arrival"]).split("T")[1]
        full["arrival"] = part["arrival"]
        part["departureDate"]=journeydate
        part["departureDay"] = models.getdayabbrevationfromdatestr(journeydate, 0)
        full["minArrival"]=(returnedfaredata["Legs"][flightcounter]["Arrival"]).split("T")[1]
        full["maxArrival"]=(returnedfaredata["Legs"][flightcounter]["Arrival"]).split("T")[1]
        part["departure"]=returnedfaredata["Legs"][flightcounter]["Departure"].split("T")[1]
        full["departure"]=part["departure"]
        full["minDeparture"]=returnedfaredata["Legs"][flightcounter]["Departure"].split("T")[1]
        full["maxDeparture"]=returnedfaredata["Legs"][flightcounter]["Departure"].split("T")[1]
        duration = returnedfaredata["Legs"][flightcounter]["Duration"]
        hours = int(duration)/60
        minutes = int(duration)%60
        part["duration"]= str(hours)+":"+str(minutes)
        part["arrivalDate"] = dateTimeUtility.calculatearrivaltimeanddate(journeydate, part["departure"],part["duration"])["arrivalDate"]
        part["arrivalDay"] = models.getdayabbrevationfromdatestr(part["arrivalDate"], 0)
        full["duration"]=str(hours)+":"+str(minutes)
        full["minDuration"]=str(hours)+":"+str(minutes)
        full["maxDuration"]=str(hours)+":"+str(minutes)
        full["departureDate"] = journeydate
        full["departureDay"] = models.getdayabbrevationfromdatestr(journeydate, 0)
        full["arrivalDate"] = part["arrivalDate"]
        full["arrivalDay"] = models.getdayabbrevationfromdatestr(full["arrivalDate"], 0)
        full["route"]=part["source"]+",flight,"+part["destination"]
        part["bookingOptions"] = itinerary["PricingOptions"]
        for option in part["bookingOptions"]:
            #option["Price"]=option["Price"]*int(numberOfAdults)
            option["AgentsImg"] = getAgentImgById(option["Agents"][0], returnedfaredata["Agents"])
            option["Agents"]=getAgentNameById(option["Agents"][0],returnedfaredata["Agents"])

        part["subParts"]=[]
        if returnedfaredata["Legs"][flightcounter]["Stops"]:
            Source =getCityNameById(returnedfaredata["Legs"][flightcounter]["OriginStation"],returnedfaredata["Places"])
            stopNumber=0
            for stop in returnedfaredata["Legs"][flightcounter]["Stops"]:
                subpart = {"source": Source, "destination": getCityNameById(stop, returnedfaredata["Places"]),
                           "flightNumber": returnedfaredata["Legs"][flightcounter]["FlightNumbers"][stopNumber][
                               "FlightNumber"], "carrierName": getCarrierNameById(
                        returnedfaredata["Legs"][flightcounter]["FlightNumbers"][stopNumber]["CarrierId"],
                        returnedfaredata["Carriers"])}
                Source=subpart["destination"]
                part["subParts"].append(subpart)
                stopNumber += 1
            subpart = {"source": Source,
                       "destination": getCityNameById(returnedfaredata["Legs"][flightcounter]["DestinationStation"],
                                                      returnedfaredata["Places"]),
                       "flightNumber": returnedfaredata["Legs"][flightcounter]["FlightNumbers"][stopNumber][
                           "FlightNumber"], "carrierName": getCarrierNameById(
                    returnedfaredata["Legs"][flightcounter]["FlightNumbers"][stopNumber]["CarrierId"],
                    returnedfaredata["Carriers"])}
            part["subParts"].append(subpart)
        else:
            subpart = {"source": getCityNameById(returnedfaredata["Legs"][flightcounter]["OriginStation"],
                                                 returnedfaredata["Places"]),
                       "destination": getCityNameById(returnedfaredata["Legs"][flightcounter]["DestinationStation"],
                                                      returnedfaredata["Places"]),
                       "flightNumber": returnedfaredata["Legs"][flightcounter]["FlightNumbers"][0]["FlightNumber"],
                       "carrierName": getCarrierNameById(
                           returnedfaredata["Legs"][flightcounter]["FlightNumbers"][0]["CarrierId"],
                           returnedfaredata["Carriers"])}
            part["subParts"].append(subpart)

        resultjsondata["flight"].append(route)

    return resultjsondata


def getCityNameById(stationId,stationsList):
    for station in stationsList:
        if station["Id"]==stationId:
            return station["Name"]

def getCarrierNameById(carrierId,carriersList):

    for carrier in carriersList:
        if carrier["Id"]==carrierId:
            carrierName = carrier["Name"].split('.')
            carrierFinalName = carrierName[0].replace(" ","_")
            return "/static/images/" + carrierFinalName + ".png"


def getAgentNameById(agentId,agentsList):

    for i in range(len(agentsList)):
        agent = agentsList[i]
        if agent["Id"]==agentId:

                return agent["Name"]

def getAgentImgById(agentId,agentsList):

    for i in range(len(agentsList)):
        agent = agentsList[i]
        if agent["Id"]==agentId:
                agentName = agent["Name"].split('.')
                agentFinalName = agentName[0].replace(" ","_")
                return "/static/images/" + agentFinalName + ".png"
