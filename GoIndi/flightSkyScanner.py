__author__ = 'ankur'

from skyscanner import Flights
import dateTimeUtility

def getApiResults(sourcecity,destinationcity,journeyDate,id):
    cityAndStateToStationsMap = {'Agartala': 'IXA', 'Agra': 'AGR', 'Ahmedabad': 'AMD', 'Allahabad': 'IXD',
                                 'Amritsar': 'ATQ', 'Aurangabad': 'IXU', 'Bagdogra': 'IXB', 'Bangalore': 'BLR',
                                 'Bhavnagar': 'BHU', 'Bhopal': 'BHO', 'Bhubaneswar': 'BBI', 'Bhuj': 'BHJ',
                                 'Calcutta': 'CCU', 'Kolkata': 'CCU', 'Chandigarh': 'IXC', 'Chennai': 'MAA',
                                 'Madras': 'MAA', 'Cochin': 'COK', 'Coimbatore': 'CJB', 'Daman': 'NMB',
                                 'Dehradun': 'DED', 'Dibrugarh': 'DIB', 'Dimapur': 'DMU', 'Diu': 'DIU',
                                 'Gauhati': 'GAU', 'Goa': 'GOI', 'Gwalior': 'GWL', 'Hubli': 'HBX', 'Hyderabad': 'HYD',
                                 'Imphal': 'IMF', 'Indore': 'IDR', 'Jaipur': 'JAI', 'Jammu': 'IXJ', 'Jamnagar': 'JGA',
                                 'Jamshedpur': 'IXW', 'Jodhpur': 'JDH', 'Jorhat': 'JRH', 'Kanpur': 'KNU',
                                 'Khajuraho': 'HJR', 'Kozhikode': 'CCJ', 'calicut': 'CCJ', 'Leh': 'IXL',
                                 'Lucknow': 'LKO', 'Ludhiana': 'LUH', 'Madurai': 'IXM', 'Mangalore': 'IXE',
                                 'Mumbai': 'BOM', 'Bombay': 'BOM', 'Nagpur': 'NAG', 'Nanded': 'NDC', 'Nasik': 'ISK',
                                 'New Delhi': 'DEL', 'Delhi': 'DEL', 'Patna': 'PAT', 'Pondicherry': 'PNY',
                                 'Poona': 'PNQ', 'Pune': 'PNQ', 'Porbandar': 'PBD', 'Port Blair': 'IXZ',
                                 'PuttasubParthi': 'PUT', 'Rae Bareli': 'BEK', 'Rajkot': 'RAJ', 'Ranchi': 'IXR',
                                 'Shillong': 'SHL', 'Silchar': 'IXS', 'Srinagar': 'SXR', 'Surat': 'STV',
                                 'Tezpur': 'TEZ', 'Tiruchirapally': 'TRZ', 'Tirupati': 'TIR', 'Trivandrum': 'TRV',
                                 'Udaipur': 'UDR', 'Vadodara': 'BDQ', 'Varanasi': 'VNS', 'Vijayawada': 'VGA',
                                 'Vishakhapatnam': 'VTZ', 'Gurgaon': 'DEL', 'Noida': 'DEL', 'Ghaziabad': 'DEL',
                                 'Tripura': 'IXA', 'Uttar Pradesh': 'AGR', 'Gujarat': 'AMD', 'Uttar Pradesh': 'IXD',
                                 'Punjab': 'ATQ', 'Maharashtra': 'IXU', 'Sikkim': 'IXB', 'Karnataka': 'BLR',
                                 'Gujarat': 'BHU', 'Madhya Pradesh': 'BHO', 'Orissa': 'BBI', 'Gujarat': 'BHJ',
                                 'West Bengal': 'CCU', 'Chandigarh': 'IXC', 'Tamil Nadu': 'MAA', 'Kerala': 'COK',
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
                                 'Uttar Pradesh': 'VNS', 'Andhra Pradesh': 'VGA', 'Andhra Pradesh': 'VTZ'}
    nearestBigAirportMap = {'Jammu': 'Delhi', 'Mangalore': 'Bangalore', 'Delhi': 'Delhi'}

    source = cityAndStateToStationsMap[sourcecity]


    destination = cityAndStateToStationsMap[destinationcity]
    year = journeyDate.split("-")[2]
    month = journeyDate.split("-")[1]
    day = journeyDate.split("-")[0]
    flights_service = Flights('ea816376821941695778768433999242')
    result = flights_service.poll_session(flights_service.create_session( country='IN',
        currency='INR',
        locale='en-US',
        originplace=source+'-sky',
        destinationplace=destination+'-sky',
        outbounddate=str(year)+'-'+str(month)+'-'+str(day),
        adults=1), initial_delay = 5, delay = 3, tries = 20).parsed

    resultJson=parseFlightAndReturnFare(result,id, sourcecity, destinationcity,journeyDate)
    return resultJson



def parseFlightAndReturnFare(apiresult,id,source,destination,journeyDate):
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
            full["id"]=str(id)+str(flightCounter)
            part={}
            flightCounter=flightCounter+1
            route["full"]=[]
            route["full"].append(full)
            route["parts"]=[]
            route["parts"].append(part)
            part["price"]=itinerary["PricingOptions"][0]["Price"]
            full["price"]=itinerary["PricingOptions"][0]["Price"]
            full["minPrice"]=itinerary["PricingOptions"][0]["Price"]
            full["maxPrice"]=itinerary["PricingOptions"][0]["Price"]
            part["id"]= str(id)+str(flightCounter)+str(partNo)
            part["mode"]="flight"
            part["source"] = source
            part["destination"] = destination
            part["arrival"]=(returnedFareData["Legs"][flightCounter]["Arrival"]).split("T")[1]
            part["departureDate"]=journeyDate
            full["minArrival"]=(returnedFareData["Legs"][flightCounter]["Arrival"]).split("T")[1]
            full["maxArrival"]=(returnedFareData["Legs"][flightCounter]["Arrival"]).split("T")[1]
            part["departure"]=returnedFareData["Legs"][flightCounter]["Departure"].split("T")[1]
            full["minDeparture"]=returnedFareData["Legs"][flightCounter]["Departure"].split("T")[1]
            full["maxDeparture"]=returnedFareData["Legs"][flightCounter]["Departure"].split("T")[1]
            duration = returnedFareData["Legs"][flightCounter]["Duration"]
            hours = int(duration)/60
            minutes = int(duration)%60
            part["duration"]= str(hours)+":"+str(minutes)
            part["arrivalDate"] = dateTimeUtility.calculateArrivalTimeAndDate(journeyDate, part["departure"],part["duration"])["arrivalDate"]
            full["minDuration"]=str(hours)+":"+str(minutes)
            full["maxDuration"]=str(hours)+":"+str(minutes)
            part["bookingOptions"] = itinerary["PricingOptions"]
            for option in part["bookingOptions"]:
                option["Agents"]=getAgentNameById(option["Agents"][0],returnedFareData["Agents"])
            part["subParts"]=[]
            if returnedFareData["Legs"][flightCounter]["Stops"]:
                Source =getCityNameById(returnedFareData["Legs"][flightCounter]["OriginStation"],returnedFareData["Places"])
                stopNumber=0
                for stop in returnedFareData["Legs"][flightCounter]["Stops"]:
                    subpart = {}
                    subpart["source"]=Source
                    subpart["destination"]=getCityNameById(stop,returnedFareData["Places"])
                    subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["FlightNumber"]
                    subpart["carrierName"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["CarrierId"],returnedFareData["Carriers"])
                    Source=subpart["destination"]
                    part["subParts"].append(subpart)
                    stopNumber=stopNumber+1
                subpart = {}
                subpart["source"]=Source
                subpart["destination"]=getCityNameById(returnedFareData["Legs"][flightCounter]["DestinationStation"],returnedFareData["Places"])
                subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["FlightNumber"]
                subpart["carrierName"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][stopNumber]["CarrierId"],returnedFareData["Carriers"])
                part["subParts"].append(subpart)
            else:
                subpart = {}
                subpart["source"]=getCityNameById(returnedFareData["Legs"][flightCounter]["OriginStation"],returnedFareData["Places"])
                subpart["destination"]=getCityNameById(returnedFareData["Legs"][flightCounter]["DestinationStation"],returnedFareData["Places"])
                subpart["flightNumber"]=returnedFareData["Legs"][flightCounter]["FlightNumbers"][0]["FlightNumber"]
                subpart["carrierName"]=getCarrierNameById(returnedFareData["Legs"][flightCounter]["FlightNumbers"][0]["CarrierId"],returnedFareData["Carriers"])
                part["subParts"].append(subpart)

            resultJsonData["flight"].append(route)
    return resultJsonData


def getCityNameById(stationId,stationsList):
    for station in stationsList:
        if station["Id"]==stationId:
            return station["Name"]

def getCarrierNameById(carrierId,carriersList):
    for carrier in carriersList:
        if carrier["Id"]==carrierId:
            return carrier["ImageUrl"]

def getAgentNameById(agentId,agentsList):
    for agent in agentsList:
        if agent["Id"]==agentId:
            return agent["ImageUrl"]