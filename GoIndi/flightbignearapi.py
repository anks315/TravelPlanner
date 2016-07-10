__author__ = 'Hello'


import loggerUtil, logging, flightutil, flightSkyScanner, datetime
import miscUtility
import concurrent
import TravelPlanner

logger = loggerUtil.getlogger("FlightBigNearApi", loggerlevel=logging.WARNING)


class FlightBigNearAirportController:

    """
    To get flights between source and destination cities, via big airports
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass='3A', flightclass='economy', numberofadults=1):

        logger.debug("[START]-Get Results From FlightBigNearApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()

            airports = flightutil.getnearestairports(source, destination)
            sourcenear = airports.sourceairports.near
            sourcebig = airports.sourceairports.big
            destinationnear = airports.destinationairports.near

            if sourcenear == destinationnear:
                logger.warning("Nearest airports to source [%s] and destination [%s] are same [%s]. Hence no flight journey possible", source, destination, sourcenear)
                return {"flight": []}
            elif source == sourcebig:
                logger.warning("Source city [%s] is same as source big airport [%s]", source, sourcebig)
                return {"flight": []}
            elif sourcenear == sourcebig:
                logger.warning("Big and nearest airports [%s] of source [%s] are same", sourcebig, sourcecity)
                return {"flight": []}
            elif sourcebig == destination:
                logger.warning("Source Big airport [%s] is same as destination [%s]", sourcebig, destination)
                return {"flight": []}

            logger.debug("Fetching direct flights possible between sourcebig [%s] and destinationnear [%s] on [%s]", sourcebig, destinationnear, journeydate)

            if source != sourcebig:
                othermodesinitfuture = executor.submit(flightutil.getothermodes, sourcecity, sourcebig, journeydate, logger, trainclass,numberofadults)
            if destination != destinationnear:
                othermodesendfuture = executor.submit(flightutil.getothermodes, destinationnear, destinationcity, journeydate, logger, trainclass,numberofadults)

            directflightfuture = executor.submit(flightSkyScanner.getApiResults, sourcebig, destinationnear, journeydate, "flightnearbig", flightclass, numberofadults)
            # conflict in id generation and should only be used if source != sourcebig
            directflightNextDayfuture = executor.submit(flightSkyScanner.getApiResults, sourcebig, destinationnear,(datetime.datetime.strptime(journeydate, '%d-%m-%Y') + datetime.timedelta(days=1)).strftime('%d-%m-%Y'), "flightnearbig", flightclass, numberofadults)

            directflight = directflightfuture.result()
            directflightNextDay = directflightNextDayfuture.result()
            directflight['flight'].extend(directflightNextDay['flight'])

            if len(directflight["flight"]) == 0:
                logger.warning("No flight available between sourcenear [%s] and destinationnear [%s] on [%s]", sourcenear, destinationnear, journeydate)
                return directflight
            directflight = miscUtility.limitResults(directflight, "flight")

            if source != sourcebig and destination != destinationnear:
                othermodessminit = othermodesinitfuture.result()
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.mixandmatch(directflight, othermodessminit, othermodessmend, logger)
            elif source != sourcebig:
                othermodessminit = othermodesinitfuture.result()
                directflight = flightutil.mixandmatchend(directflight, othermodessminit, logger)
            elif destination != destinationnear:
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.mixandmatchinit(directflight, othermodessmend, logger)

            return directflight