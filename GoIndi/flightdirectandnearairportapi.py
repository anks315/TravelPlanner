__author__ = 'Hello'


import loggerUtil, logging, flightutil, flightSkyScanner, datetime
import miscUtility
import concurrent, copy
import TravelPlanner

logger = loggerUtil.getlogger("FlightDirectAndNearAirportApi")


class FlightDirectAndNearAirportController:

    """
    To get flightes between source and destination cities, via nearest airports
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass='3A', flightclass='economy', numberofadults=1):

        logger.debug("[START]-Get Results From FlightDirectAndNearAirportApi for Source:[%s] to Destination:[%s] on JourneyDate:[%s] ", sourcecity, destinationcity, journeydate)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            source = TravelPlanner.trainUtil.gettraincity(sourcecity).title()
            destination = TravelPlanner.trainUtil.gettraincity(destinationcity).title()

            airports = flightutil.getnearestairports(source, destination)
            sourcenear = airports.sourceairports.near
            destinationnear = airports.destinationairports.near

            if sourcenear == destinationnear:
                logger.warning("Nearest airports to source [%s] and destination [%s] are same [%s]. Hence no flight journey possible", source, destination, sourcenear)
                return {"flight": []}
            # elif source == sourcenear and destination == destinationnear:
            #     logger.warning("Nearest airports sourceNearest [%s] and destinationNearest [%s] are same as given cities source [%s] and destination [%s]", airports.sourceairports.near, airports.destinationairports.near, source, destination)
            #     return {"flight": []}

            logger.debug("Fetching direct flights possible between sourcenear [%s] and destinationnear [%s] on [%s]", sourcenear, destinationnear, journeydate)

            if source != sourcenear:
                othermodesinitfuture = executor.submit(flightutil.getothermodes, sourcecity, sourcenear, journeydate, logger, trainclass, numberofadults)
                directflightnextdayfuture = executor.submit(flightSkyScanner.getApiResults, sourcenear, destinationnear, (datetime.datetime.strptime(journeydate, '%d-%m-%Y') + datetime.timedelta(days=1)).strftime('%d-%m-%Y'), "flightnearnext", flightclass, numberofadults)
            if destination != destinationnear:
                othermodesendfuture = executor.submit(flightutil.getothermodes, destinationnear, destinationcity, journeydate, logger, trainclass, numberofadults)

            directflightfuture = executor.submit(flightSkyScanner.getApiResults, sourcenear, destinationnear, journeydate, "flightnear", flightclass, numberofadults)
            directflight = directflightfuture.result()
            directflight = miscUtility.limitResults(directflight, "flight", limit=10)

            if len(directflight["flight"]) == 0:
                logger.warning("No flight available between sourcenear [%s] and destinationnear [%s] on [%s]", sourcenear, destinationnear, journeydate)
                return directflight

            if source != sourcenear and destination != destinationnear:
                othermodessminit = othermodesinitfuture.result()
                othermodessmend = othermodesendfuture.result()
                directflightnextday = directflightnextdayfuture.result()
                directflightnextday = miscUtility.limitResults(directflightnextday, "flight", limit=10)
                directflight['flight'].extend(directflightnextday['flight'])
                directflight = flightutil.getmixandmatchresult(othermodessminit, othermodessmend, copy.deepcopy(directflight), logger)
            elif source != sourcenear:
                othermodessminit = othermodesinitfuture.result()
                directflightnextday = directflightnextdayfuture.result()
                directflightnextday = miscUtility.limitResults(directflightnextday, "flight", limit=10)
                directflight['flight'].extend(directflightnextday['flight'])
                directflight = flightutil.getmixandmatchendresult(othermodessminit, copy.deepcopy(directflight), logger)
            elif destination != destinationnear:
                othermodessmend = othermodesendfuture.result()
                directflight = flightutil.getmixandmatchinitresult(othermodessmend, copy.deepcopy(directflight), logger)

            return directflight