__author__ = 'Hello'


import loggerUtil, logging, flightutil, flightSkyScanner
import miscUtility
import concurrent
import TravelPlanner

logger = loggerUtil.getlogger("FlightDirectApi")


class FlightDirectController:

    """
    To get only direct flighte between source and destination cities
    """

    def getresults(self, sourcecity, destinationcity, journeydate, flightclass, numberofadults):

        logger.debug("[START]-Get Results From FlightDirectApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:

            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()

            airports = flightutil.getnearestairports(source, destination)
            sourcenear = airports.sourceairports.near
            destinationnear = airports.destinationairports.near

            if source != sourcenear and destination != destinationnear:
                logger.warning("No direct flight possible between source [%s] and destination [%s]", source, destination)
                return {"flight": []}
            else:
                logger.debug("Fetching direct possible flights between source [%s] and destination [%s] on [%s]", source, destination, journeydate)
                onlyflightfuture = executor.submit(flightSkyScanner.getApiResults, source, destination, journeydate, "flightdirect", flightclass, numberofadults)
                onlyflight = onlyflightfuture.result()
                onlyflight = miscUtility.limitResults(onlyflight, "flight")
                return onlyflight