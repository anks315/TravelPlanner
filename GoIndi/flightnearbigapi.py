__author__ = 'Hello'


import loggerUtil, logging, flightutil, flightSkyScanner
import miscUtility
import concurrent, copy
import TravelPlanner

logger = loggerUtil.getlogger("FlightNearBigApi", loggerlevel=logging.WARNING)


class FlightNearBigAirportController:

    """
    To get flights between source and destination cities, via big airports
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass='3A', flightclass='economy', numberofadults=1):

        logger.debug("[START]-Get Results From FlightNearBigApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()

            airports = flightutil.getnearestairports(source, destination)
            sourcenear = airports.sourceairports.near
            destinationnear = airports.destinationairports.near
            destinationbig = airports.destinationairports.big

            if sourcenear == destinationnear:
                logger.warning("Nearest airports to source [%s] and destination [%s] are same [%s]. Hence no flight journey possible", source, destination, sourcenear)
                return {"flight": []}
            elif destination == destinationbig:
                logger.warning("Destination city [%s] is same as destination big airport [%s]", destination, destinationbig)
                return {"flight": []}
            elif destinationnear == destinationbig:
                logger.warning("Big and nearest airports [%s] of destination [%s] are same", destinationbig, destination)
                return {"flight": []}
            elif destinationbig == source:
                logger.warning("Destination Big airport [%s] is same as source [%s]", destinationbig, source)
                return {"flight": []}

            logger.debug("Fetching direct flights possible between sourcebig [%s] and destinationbig [%s] on [%s]", sourcenear, destinationnear, journeydate)

            if source != sourcenear:
                othermodesinitfuture = executor.submit(flightutil.getothermodes, sourcecity, sourcenear, journeydate, logger, trainclass,numberofadults)
            if destination != destinationbig:
                othermodesendfuture = executor.submit(flightutil.getothermodes, destinationbig, destinationcity, journeydate, logger, trainclass,numberofadults)

            directflightfuture = executor.submit(flightSkyScanner.getApiResults, sourcenear, destinationbig, journeydate, "flightnearbig", flightclass, numberofadults)
            directflight = directflightfuture.result()

            if len(directflight["flight"]) == 0:
                logger.warning("No flight available between sourcenear [%s] and destinationbig [%s] on [%s]", sourcenear, destinationbig, journeydate)
                return directflight
            directflight = miscUtility.limitResults(directflight, "flight")

            if source != sourcenear and destination != destinationbig:
                othermodessminit = othermodesinitfuture.result()
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.getmixandmatchresult(othermodessminit, othermodessmend, copy.deepcopy(directflight), logger)
            elif source != sourcenear:
                othermodessminit = othermodesinitfuture.result()
                directflight = flightutil.getmixandmatchendresult(othermodessminit, copy.deepcopy(directflight),logger)
            elif destination != destinationbig:
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.getmixandmatchinitresult(othermodessmend, copy.deepcopy(directflight), logger)

            return directflight