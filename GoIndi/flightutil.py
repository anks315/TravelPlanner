__author__ = 'Hello'

import urllib2, json, datetime, copy
import distanceutil, trainapineo4j, busapi, dateTimeUtility, minMaxUtil, miscUtility, models, TravelPlanner.startuputil
from entity import Airports, NearestAirports, FlightRequest
import threading

# map of airport code and their corresponding cities. City names should either be same as that present in trainDB or their mapping should be TravelPlanner.trainUtil.citytotrainmap
stationtocitymap = {'JLR':'Jabalpur', 'JSA':'Jaisalmer','RJA':'Rajahmundry','PGH':'Pantnagar','IXP':'Pathankot','KUU':'Kullu','SLV':'Shimla','IXA':'Agartala','AGR':'Agra','AMD':'Ahmedabad','IXD':'Allahabad','ATQ':'Amritsar','IXU':'Aurangabad','IXB':'Bagdogra','BLR':'Bangalore','BHU':'Bhavnagar','BHO':'Bhopal','BBI':'Bhubaneswar','BHJ':'Bhuj','CCU':'Kolkata','IXC':'Chandigarh','MAA':'Chennai','COK':'Cochin','CJB':'Coimbatore','NMB':'Daman','DED':'Dehradun','DIB':'Dibrugarh','DMU':'Dimapur','DIU':'Diu','GAU':'Guwahati','GOI':'Goa','GWL':'Gwalior','HBX':'Hubli','HYD':'Hyderabad','IMF':'Imphal','IDR':'Indore','JAI':'Jaipur','IXJ':'Jammu','JGA':'Jamnagar','IXW':'Jamshedpur','JDH':'Jodhpur','JRH':'Jorhat','KNU':'Kanpur','HJR':'Khajuraho','CCJ':'Kozhikode','IXL':'Leh','LKO':'Lucknow','LUH':'Ludhiana','IXM':'Madurai','IXE':'Mangalore','BOM':'Mumbai','NAG':'Nagpur','NDC':'Nanded','ISK':'Nasik','DEL':'New Delhi','PAT':'Patna','PNY':'Pondicherry','PNQ':'Pune','PBD':'Porbandar','IXZ':'Port Blair','PUT':'PuttasubParthi','BEK':'Rae Bareli','RAJ':'Rajkot','IXR':'Ranchi','SHL':'Shillong','IXS':'Silchar','SXR':'Srinagar','STV':'Surat','TEZ':'Tezpur','TRZ':'Tiruchirapally','TIR':'Tirupati','TRV':'Trivandrum','UDR':'Udaipur','BDQ':'Vadodara','VNS':'Varanasi','VGA':'Vijayawada','VTZ': 'Vishakhapatnam', 'IXK': 'Keshod'}
nearestairportsmap = {}
lock = threading.RLock()


def getnearestairports(source, destination):

    """
    To get entity of nearest airports for given source & destination
    :param source: source of journey
    :param destination: destination of journey
    :return: collection of nearest airports
    """

    airports = Airports()
    sourceairports = getnearestairportfrommap(source)
    if not sourceairports:
        # get nearest airport and nearest big airport to our source city
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + source
        url = url.replace(' ', '%20')
        response = urllib2.urlopen(url)
        sourcelatlong = json.loads(response.read())
        response.close()
        sourcelat = sourcelatlong["results"][0]["geometry"]["location"]["lat"]
        sourcelong = sourcelatlong["results"][0]["geometry"]["location"]["lng"]
        sourceairport = TravelPlanner.startuputil.gettraincity(stationtocitymap[distanceutil.findnearestairport(sourcelat,sourcelong)]).title()
        bigsourceairport = TravelPlanner.startuputil.gettraincity(stationtocitymap[distanceutil.findnearestbigairport(sourcelat,sourcelong)]).title()
        sourceairports = NearestAirports()
        sourceairports.near = sourceairport
        sourceairports.big = bigsourceairport
        with lock:
            nearestairportsmap[source] = sourceairports

    destinationairports = getnearestairportfrommap(destination)
    if not destinationairports:
        # get nearest airport and nearest big airport to our destination city
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination
        url = url.replace(' ', '%20')
        response2 = urllib2.urlopen(url)
        destlatlong = json.loads(response2.read())
        destlat = destlatlong["results"][0]["geometry"]["location"]["lat"]
        destlong = destlatlong["results"][0]["geometry"]["location"]["lng"]
        destairport = TravelPlanner.startuputil.gettraincity(stationtocitymap[distanceutil.findnearestairport(destlat, destlong)]).title()
        bigdestinationairport = TravelPlanner.startuputil.gettraincity(stationtocitymap[distanceutil.findnearestbigairport(destlat, destlong)]).title()
        destinationairports = NearestAirports()
        destinationairports.near = destairport
        destinationairports.big = bigdestinationairport
        with lock:
            nearestairportsmap[destination] = destinationairports

    airports.sourceairports = sourceairports
    airports.destinationairports = destinationairports

    return airports


def getnearestairportfrommap(city):
    """
    Get nearest airports to given city from map
    :param city: city for which nearest airports are to calculated
    :return:
    """

    lock.acquire()
    try:
        if city in nearestairportsmap.keys():
            return nearestairportsmap[city]
        else:
            return
    finally:
        # Always called, even if exception is raised in try block
        lock.release()


def getothermodes(source, destination, journeydate, logger, trainclass='3A', numberofadults=1):

    """
    To get train or bus frim source city to flight source city
    :param source: source of journey
    :param destination: destination of journey
    :param journeydate: date of journey
    :param logger: to log
    :param trainclass: class of train journey preferred by user
    :param numberofadults: no. of people travelling
    :return: other journey modes, train if exists else bus
    """

    resultjsondata = { "train" : [], "bus" : []}
    traincontrollerneo = trainapineo4j.TrainController()
    nextdate = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    nexttonextdate = (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + datetime.timedelta(days=2)).strftime('%d-%m-%Y')

    logger.debug("[START] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
    trainjsondata = traincontrollerneo.getroutes(source, destination, journeydate, priceclass=trainclass, numberofadults=numberofadults, nextday=True)["train"]
    if not trainjsondata:
        logger.warning("No Data From Train,Retrieving From Bus for Source[%s] and Destination[%s],journeyDate[%s]",source,destination,journeydate)
    buscontroller = busapi.BusController()
    busjsondata = buscontroller.getresults(source, destination, nexttonextdate, numberofadults)
    busjsondata["bus"].extend(buscontroller.getresults(source, destination, journeydate, numberofadults)["bus"])
    busjsondata["bus"].extend(buscontroller.getresults(source, destination, nextdate, numberofadults)["bus"])
    busjsondata = busjsondata["bus"]
    if not busjsondata:
        logger.warning("No Data From Bus for Source[%s] and Destination[%s],journeyDate[%s]",source, destination, journeydate)

    logger.debug("[END] Calling TrainApi From Flight Api for Source:[%s] and Destination[%s],journeyDate[%s]",source, destination, journeydate)
    resultjsondata["train"] = trainjsondata
    resultjsondata["bus"] = busjsondata
    return resultjsondata


def mixandmatch(directflight, othermodesinit, othermodesend, logger):

        logger.debug("[START] Flight mix & match")
        directflight = miscUtility.limitResults(directflight, "flight")

        for j in range(len(directflight["flight"])):
            flightpart = directflight["flight"][j]["parts"][0]
            subparts = []
            for k in range(len(othermodesinit)):
                subpart = othermodesinit[k]["parts"][0]
                if dateTimeUtility.isjourneypossible(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["arrivalDate"], flightpart["departureDate"], 3, 24):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"],flightpart["departure"],subpart["arrivalDate"],flightpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["departure"], flightpart["departureDate"], subpart["departureDate"])
                    subparts.append(copy.deepcopy(subpart))
            subparts.sort(miscUtility.sortonsubjourneytime)
            if len(subparts) > 5:
                subparts = subparts[0:5]
            continuefurther = 0;

            if subparts:
                continuefurther = 1
                minmax1 = minMaxUtil.getMinMaxValues(subparts)
                price1 = int(minMaxUtil.getprice(subparts[0]))
                subJourneyTime1 = subparts[0]["subJourneyTime"]
                waitingtime1 = subparts[0]["waitingTime"]
                departuredate1 = subparts[0]["departureDate"]
                departure1 = subparts[0]["departure"]
                source = subparts[0]["source"]
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": directflight["flight"][j]["full"][0]["id"] + str(0),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                flightpart["id"] = directflight["flight"][j]["full"][0]["id"] + str(1)
                directflight["flight"][j]["parts"].insert(0, newpart)
                directflight["flight"][j]["full"][0]["route"] = newpart["source"] + ","+newpart["mode"]+"," + newpart["destination"] + ",flight," + flightpart["destination"]

            subparts = []
            for k in range(len(othermodesend)):
                subpart = othermodesend[k]["parts"][0]
                if dateTimeUtility.isjourneypossible(dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["departure"], flightpart["arrivalDate"], subpart["departureDate"], 3, 24):
                    subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightpart["arrival"], subpart["departure"],flightpart["arrivalDate"],subpart["departureDate"])
                    subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["arrivalDate"], flightpart["arrivalDate"])
                    subparts.append(copy.deepcopy(subpart))
            subparts.sort(miscUtility.sortonsubjourneytime)
            if len(subparts) > 5:
                subparts = subparts[0:5]

            if subparts and continuefurther==1:
                minmax2 = minMaxUtil.getMinMaxValues(subparts)
                price2 = int(minMaxUtil.getprice(subparts[0]))
                destination = subparts[0]["destination"]
                subJourneyTime2 = subparts[0]["subJourneyTime"]
                newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": directflight["flight"][j]["full"][0]["id"] + str(2),
                           "destination": subparts[0]["destination"], "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
                directflight["flight"][j]["parts"].append(newpart)
                directflight["flight"][j]["full"][0]["route"] = directflight["flight"][j]["full"][0]["route"] + ","+subparts[0]["mode"]+"," + newpart["destination"]
                directflight["flight"][j]["full"][0]["price"] = int(directflight["flight"][j]["full"][0]["price"]) + price1 + price2
                directflight["flight"][j]["full"][0]["minPrice"] = int(directflight["flight"][j]["full"][0]["minPrice"]) + int(minmax1["minPrice"]) + int(minmax2["minPrice"])
                directflight["flight"][j]["full"][0]["maxPrice"] = int(directflight["flight"][j]["full"][0]["maxPrice"]) + int(minmax1["maxPrice"]) + int(minmax2["maxPrice"])
                directflight["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(directflight["flight"][j]["full"][0]["duration"], subJourneyTime1),subJourneyTime2)
                directflight["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(directflight["flight"][j]["full"][0]["minDuration"], minmax1["minDuration"]),minmax2["minDuration"])
                directflight["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(dateTimeUtility.addDurations(directflight["flight"][j]["full"][0]["maxDuration"], minmax1["maxDuration"]),minmax2["maxDuration"])
                directflight["flight"][j]["full"][0]["minDeparture"] = minmax1["minDep"]
                directflight["flight"][j]["full"][0]["maxDeparture"] = minmax1["maxDep"]
                directflight["flight"][j]["full"][0]["minArrival"] = minmax2["minArr"]
                directflight["flight"][j]["full"][0]["maxArrival"] = minmax2["maxArr"]
                directflight["flight"][j]["full"][0]["destination"] = destination
                directflight["flight"][j]["full"][0]["source"] = source
                directflight["flight"][j]["full"][0]["waitingTime"] = dateTimeUtility.addDurations(waitingtime1, subparts[0]["waitingTime"])
                directflight["flight"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
                directflight["flight"][j]["full"][0]["departure"] = departure1
                directflight["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
                directflight["flight"][j]["full"][0]["departureDate"] = departuredate1
                directflight["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
                directflight["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(departuredate1, 0)

        directflight["flight"] = [x for x in directflight["flight"] if len(x["parts"]) == 3]
        logger.debug("[END] flight mix & match")
        return directflight


def mixandmatchinit(mixedflightinit, othermodesend, logger):

    """
    Join flight journey with other modes, with flight being first part of combined journey
    :param mixedflightinit: flight part of journey
    :param othermodesend: other mode of journey
    :param otherModesEnd2: other mode of journey2
    :return: combined journey flight followed by other mode
    """
    logger.debug("[START] flight + othermodesend")
    mixedflightinit = miscUtility.limitResults(mixedflightinit,"flight")

    for j in range(len(mixedflightinit["flight"])):
        flightpart = mixedflightinit["flight"][j]["parts"][0]
        subparts = []
        for k in range(len(othermodesend)):
            subpart = othermodesend[k]["parts"][0]
            if dateTimeUtility.isjourneypossible(dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["departure"], flightpart["arrivalDate"], subpart["departureDate"],3, 24):
                subpart["waitingTime"] = dateTimeUtility.getWaitingTime(flightpart["arrival"],subpart["departure"],flightpart["arrivalDate"],subpart["departureDate"])
                subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["arrival"]), subpart["arrivalDate"], flightpart["arrivalDate"])
                subparts.append(copy.deepcopy(subpart))
        subparts.sort(miscUtility.sortonsubjourneytime)
        if len(subparts) > 5:
            subparts = subparts[0:5]

        if subparts:
            minmax = minMaxUtil.getMinMaxValues(subparts)
            newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflightinit["flight"][j]["full"][0]["id"] + str(1),
                       "destination": subparts[0]["destination"], "source": subparts[0]["source"], "carrierName": subparts[0]["carrierName"]}
            mixedflightinit["flight"][j]["parts"].append(newpart)
            mixedflightinit["flight"][j]["full"][0]["route"]=flightpart["source"]+",flight,"+flightpart["destination"]+","+subparts[0]["mode"]+","+newpart["destination"]
            mixedflightinit["flight"][j]["full"][0]["price"] = int(mixedflightinit["flight"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
            mixedflightinit["flight"][j]["full"][0]["minPrice"] = int(mixedflightinit["flight"][j]["full"][0]["minPrice"]) + int(minmax["minPrice"])
            mixedflightinit["flight"][j]["full"][0]["maxPrice"] = int(mixedflightinit["flight"][j]["full"][0]["maxPrice"]) + int(minmax["maxPrice"])
            mixedflightinit["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedflightinit["flight"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
            mixedflightinit["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedflightinit["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
            mixedflightinit["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedflightinit["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
            mixedflightinit["flight"][j]["full"][0]["minArrival"] = minmax["minArr"]
            mixedflightinit["flight"][j]["full"][0]["maxArrival"] = minmax["maxArr"]
            mixedflightinit["flight"][j]["full"][0]["destination"] = subparts[0]["destination"]
            mixedflightinit["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
            mixedflightinit["flight"][j]["full"][0]["arrival"] = subparts[0]["arrival"]
            mixedflightinit["flight"][j]["full"][0]["arrivalDate"] = subparts[0]["arrivalDate"]
            mixedflightinit["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(subparts[0]["arrivalDate"], 0)
            mixedflightinit["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(flightpart["departureDate"], 0)

    mixedflightinit["flight"] = [x for x in mixedflightinit["flight"] if len(x["parts"]) == 2]
    logger.debug("[FlightApi.mixAndMatchInit]-[END]")
    return mixedflightinit


def mixandmatchend(mixedflightend, othermodesinit, logger):

    """
    Join flight with other modes, with flight in the end
    :param mixedflightend: flight part of journey
    :param othermodesinit: other mode of journey
    :param otherModesInit2: other mode of jounrey2
    :return: combined journey with flight after other mode of total journey
    """
    logger.debug("[START]")
    mixedflightend = miscUtility.limitResults(mixedflightend, "flight")
    for j in range(len(mixedflightend["flight"])):
        flightpart = mixedflightend["flight"][j]["parts"][0]
        subparts = []
        for k in range(len(othermodesinit)):
            subpart = othermodesinit[k]["parts"][0]
            if dateTimeUtility.isjourneypossible(subpart["arrival"], dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["arrivalDate"], flightpart["departureDate"], 3, 24):
                subpart["waitingTime"] = dateTimeUtility.getWaitingTime(subpart["arrival"], flightpart["departure"],subpart["arrivalDate"],flightpart["departureDate"])
                subpart["subJourneyTime"] = dateTimeUtility.gettotalduration(dateTimeUtility.convertflighttime(flightpart["departure"]), subpart["departure"], flightpart["departureDate"], subpart["departureDate"])
                subparts.append(copy.deepcopy(subpart))
        subparts.sort(miscUtility.sortonsubjourneytime)
        if len(subparts) > 5:
            subparts = subparts[0:5]

        if subparts:
            minmax = minMaxUtil.getMinMaxValues(subparts)
            newpart = {"subParts": subparts, "mode": subparts[0]["mode"],"id": mixedflightend["flight"][j]["full"][0]["id"] + str(0), "destination": subparts[0]["destination"],
                       "source": subparts[0]["source"],"carrierName": subparts[0]["carrierName"]}
            flightpart["id"]=mixedflightend["flight"][j]["full"][0]["id"] + str(1)
            mixedflightend["flight"][j]["parts"].insert(0,newpart)
            mixedflightend["flight"][j]["full"][0]["route"] = newpart["source"] + ","+subparts[0]["mode"]+"," + newpart["destination"] + ",flight," + flightpart["destination"]
            mixedflightend["flight"][j]["full"][0]["price"] = int(mixedflightend["flight"][j]["full"][0]["price"]) + int(minMaxUtil.getprice(subparts[0]))
            mixedflightend["flight"][j]["full"][0]["minPrice"] = int(mixedflightend["flight"][j]["full"][0]["minPrice"]) +  int(minmax["minPrice"])
            mixedflightend["flight"][j]["full"][0]["maxPrice"] = int(mixedflightend["flight"][j]["full"][0]["maxPrice"] ) + int(minmax["maxPrice"])
            mixedflightend["flight"][j]["full"][0]["duration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["duration"], subparts[0]["subJourneyTime"])
            mixedflightend["flight"][j]["full"][0]["minDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["minDuration"], minmax["minDuration"])
            mixedflightend["flight"][j]["full"][0]["maxDuration"] = dateTimeUtility.addDurations(mixedflightend["flight"][j]["full"][0]["maxDuration"], minmax["maxDuration"])
            mixedflightend["flight"][j]["full"][0]["minDeparture"] = minmax["minDep"]
            mixedflightend["flight"][j]["full"][0]["maxDeparture"] = minmax["maxDep"]
            mixedflightend["flight"][j]["full"][0]["source"] = subparts[0]["source"]
            mixedflightend["flight"][j]["full"][0]["waitingTime"] = subparts[0]["waitingTime"]
            mixedflightend["flight"][j]["full"][0]["departure"] = subparts[0]["departure"]
            mixedflightend["flight"][j]["full"][0]["departureDate"] = subparts[0]["departureDate"]
            mixedflightend["flight"][j]["full"][0]["departureDay"] = models.getdayabbrevationfromdatestr(subparts[0]["departureDate"], 0)
            mixedflightend["flight"][j]["full"][0]["arrivalDay"] = models.getdayabbrevationfromdatestr(flightpart["arrivalDate"], 0)

    mixedflightend["flight"] = [x for x in mixedflightend["flight"] if len(x["parts"]) == 2]
    logger.debug("[END]")
    return mixedflightend


def getflightrequestparams(request):
    """
    To get flight request parameters from Http request
    :param request: http request
    :return: FlightRequest
    """

    flightrequest = FlightRequest()

    flightrequest.sourcecity = request.GET['sourcecity']
    flightrequest.destinationcity = request.GET['destinationcity']
    flightrequest.journeydate = request.GET['journeyDate']
    flightrequest.trainclass = request.GET["trainClass"]
    flightrequest.flightclass = request.GET["flightClass"]
    flightrequest.numberofadults = request.GET["adults"]

    return flightrequest


def getmixandmatchresult(othermodessminit, othermodessmend, directflight, logger):

    """
    To get result flights from matching flight journey with other modes at both end and start of journey
    :param othermodessminit: other modes in the beginning of journey
    :param othermodessmend: other modes in the end of journey
    :param directflight: deep copy of direct flight
    :param logger: to log events
    :return: final combined result of flights and other modes
    """

    resultflight = { "flight" : [] }
    if len(othermodessminit["train"]) > 0 and len(othermodessmend["train"]) > 0:
        resultflight["flight"].extend(mixandmatch(copy.deepcopy(directflight), othermodessminit["train"], othermodessmend["train"], logger)["flight"])
    if len(othermodessminit["train"]) > 0 and len(othermodessmend["bus"]) > 0:
        resultflight["flight"].extend(mixandmatch(copy.deepcopy(directflight), othermodessminit["train"], othermodessmend["bus"], logger)["flight"])
    if len(othermodessminit["bus"]) > 0 and len(othermodessmend["bus"]) > 0:
        resultflight["flight"].extend(mixandmatch(copy.deepcopy(directflight), othermodessminit["bus"], othermodessmend["bus"], logger)["flight"])
    if len(othermodessminit["bus"]) > 0 and len(othermodessmend["train"]) > 0:
        resultflight["flight"].extend(mixandmatch(copy.deepcopy(directflight), othermodessminit["bus"], othermodessmend["train"], logger)["flight"])
    return resultflight


def getmixandmatchendresult(othermodessminit, directflight, logger):

    """
    To get result flights from matching flight journey with other modes at start of journey
    :param othermodessminit: other modes in the beginning of journey
    :param directflight: deep copy of direct flight
    :param logger: to log events
    :return: final combined result of flights and other modes
    """

    resultflight = { "flight" : [] }
    if len(othermodessminit["train"]) > 0:
        resultflight["flight"].extend(mixandmatchend(copy.deepcopy(directflight), othermodessminit["train"], logger)["flight"])
    if len(othermodessminit["bus"]) > 0:
        resultflight["flight"].extend(mixandmatchend(copy.deepcopy(directflight), othermodessminit["bus"], logger)["flight"])
    return resultflight


def getmixandmatchinitresult(othermodessmend, directflight, logger):

    """
    To get result flights from matching flight journey with other modes at end of journey
    :param othermodessmend: other modes in the end of journey
    :param directflight: deep copy of direct flight
    :param logger: to log events
    :return: final combined result of flights and other modes
    """

    resultflight = { "flight" : [] }
    if len(othermodessmend["train"]) > 0:
        resultflight["flight"].extend(mixandmatchinit(copy.deepcopy(directflight), othermodessmend["train"], logger)["flight"])
    if len(othermodessmend["bus"]) > 0:
        resultflight["flight"].extend(mixandmatchinit(copy.deepcopy(directflight), othermodessmend["bus"], logger)["flight"])
    return resultflight