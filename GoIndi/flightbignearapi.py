__author__ = 'Hello'


import loggerUtil, flightutil, flightSkyScanner, datetime, miscUtility, TravelPlanner.startuputil
import concurrent, copy

logger = loggerUtil.getlogger("FlightBigNearApi")


class FlightBigNearAirportController:

    """
    To get flights between source and destination cities, via big airports
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass='3A', flightclass='economy', numberofadults=1):

        logger.debug("[START]-Get Results From FlightBigNearApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            source = TravelPlanner.startuputil.gettraincity(sourcecity).title()
            destination = TravelPlanner.startuputil.gettraincity(destinationcity).title()

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
            directflightnextdayfuture = executor.submit(flightSkyScanner.getApiResults, sourcebig, destinationnear,(datetime.datetime.strptime(journeydate, '%d-%m-%Y') + datetime.timedelta(days=1)).strftime('%d-%m-%Y'), "flightnearbignextday", flightclass, numberofadults)

            directflight = directflightfuture.result()
            directflight = miscUtility.limitResults(directflight, "flight", limit=20)
            directflightnextday = directflightnextdayfuture.result()
            directflightnextday = miscUtility.limitResults(directflightnextday, "flight", limit=20)
            directflight['flight'].extend(directflightnextday['flight'])

            if len(directflight["flight"]) == 0:
                logger.warning("No flight available between sourcenear [%s] and destinationnear [%s] on [%s]", sourcenear, destinationnear, journeydate)
                return directflight

            if source != sourcebig and destination != destinationnear:
                othermodessminit = othermodesinitfuture.result()
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.getmixandmatchresult(othermodessminit, othermodessmend, copy.deepcopy(directflight), logger)
            elif source != sourcebig:
                othermodessminit = othermodesinitfuture.result()
                directflight = flightutil.getmixandmatchendresult(othermodessminit, copy.deepcopy(directflight), logger)
            elif destination != destinationnear:
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.getmixandmatchinitresult(othermodessmend, copy.deepcopy(directflight), logger)
            return directflight