__author__ = 'Hello'
import loggerUtil, logging

logger = loggerUtil.getlogger("FlightDirectApi", loggerlevel=logging.WARNING)


class FlightDirectController:

    """
    To get only direct flighte between source and destination cities
    """

    def getresults(self, sourcecity, destinationcity, journeydate, trainclass, flightclass, numberofadults):
        pass