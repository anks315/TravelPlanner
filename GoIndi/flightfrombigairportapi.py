__author__ = 'Hello'


import loggerUtil, logging, flightutil, flightSkyScanner
import miscUtility
import concurrent
import TravelPlanner

logger = loggerUtil.getlogger("FlightFromBigAirportApi", loggerlevel=logging.WARNING)


class FlightFromBigAirportController:

    """
    To get flights between source and destination cities, via big airports
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass='3A', flightclass='economy', numberofadults=1):

        logger.debug("[START]-Get Results From FlightFromBigAirportApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()

            airports = flightutil.getnearestairports(source, destination)
            sourcenear = airports.sourceairports.near
            sourcebig = airports.sourceairports.big
            destinationnear = airports.destinationairports.near
            destinationbig = airports.destinationairports.big

            if sourcenear == destinationnear:
                logger.warning("Nearest airports to source [%s] and destination [%s] are same [%s]. Hence no flight journey possible", source, destination, sourcenear)
                return {"flight": []}
            elif sourcebig == destinationbig:
                logger.warning("Big airports to source [%s] and destination [%s] are same [%s]. Hence no flight journey possible", source, destination, sourcebig)
                return {"flight": []}
            elif source == sourcebig and destination == destinationbig:
                logger.warning("Big airports sourcebig [%s] and destinationbig [%s] are same as given cities source [%s] and destination [%s]", sourcebig, destinationbig, source, destination)
                return {"flight": []}
            elif sourcebig == sourcenear:
                logger.warning("source nearest [%s] & big airport [%s] are same", sourcenear, sourcebig)
                return {"flight": []}
            elif destinationbig == destinationnear:
                logger.warning("destination nearest [%s] & big airport [%s] are same", destinationnear, destinationbig)
                return {"flight": []}

            logger.debug("Fetching direct flights possible between sourcebig [%s] and destinationbig [%s] on [%s]", sourcenear, destinationnear, journeydate)

            if source != sourcebig:
                othermodesinitfuture = executor.submit(flightutil.getothermodes, sourcecity, sourcebig, journeydate, logger, trainclass,numberofadults)
            if destination != destinationbig:
                othermodesendfuture = executor.submit(flightutil.getothermodes, destinationbig, destinationcity, journeydate, logger, trainclass,numberofadults)

            directflightfuture = executor.submit(flightSkyScanner.getApiResults, sourcebig, destinationbig, journeydate, "flightbig", flightclass, numberofadults)
            directflight = directflightfuture.result()
            if len(directflight["flight"]) == 0:
                logger.warning("No flight available between sourcenear [%s] and destinationnear [%s] on [%s]", sourcenear, destinationnear, journeydate)
                return directflight
            directflight = miscUtility.limitResults(directflight, "flight")

            if source != sourcebig and destination != destinationbig:
                othermodessminit = othermodesinitfuture.result()
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.mixandmatch(directflight, othermodessminit, othermodessmend, logger)
            elif source != sourcebig:
                othermodessminit = othermodesinitfuture.result()
                directflight = flightutil.mixandmatchend(directflight, othermodessminit, logger)
            elif destination != destinationbig:
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.mixandmatchinit(directflight, othermodessmend, logger)

            return directflight