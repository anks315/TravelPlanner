__author__ = 'Hello'

import trainConstants, loggerUtil
import urllib, json

logger = loggerUtil.getlogger("TrainAvailabilityApi")

class TrainAvailabilityController:

    """
    To get availability of train between source & destination station on journey date
    """

    def getavailablity(self, trainnumber, sourcestation, destinationstation, journeydate, trainclass, quota='GN'):

        """
        To get availability of train between source & destination station on given date
        :param trainnumber: number of the train for which we need to check availability
        :param sourcestation: source station of the journey
        :param destinationstation: destination station of the journey
        :param journeydate: date of journey in DD-MM-YYYY format
        :param trainclass: class of train
        :param quota: quota of train seat
        :return: json response containing no. of available seats
        """

        try:
            url = "http://api.railwayapi.com/check_seat/train/"+trainnumber+"/source/"+sourcestation+"/dest/"+destinationstation+"/date/"+journeydate+"/class/"+trainclass+"/quota/" +quota +"/apikey/" + trainConstants.ERAILWAYAPI_APIKEY +"/"
            print url
            jsonresponse = urllib.urlopen(url).read()
        except Exception as e:
            logger.error("Error in fetching availability data for train[%s] from source [%s] to destination [%s] on [%s] for class [%s], reason [%s]", trainnumber, sourcestation, destinationstation, journeydate, trainclass, e.message)
        print jsonresponse
        availabledatajson = self.parseavailabilityresponse(jsonresponse, trainnumber, sourcestation, destinationstation, journeydate)
        print availabledatajson
        return availabledatajson

    def parseavailabilityresponse(self, jsonresponse, trainnumber, sourcestation, destinationstation, journeydate):

        """
        To parse and fetch availablity data from json object
        :param jsonresponse: json response for check availablity call
        :param trainnumber: number of the train for which we need to check availability
        :param sourcestation: source station of the journey
        :param destinationstation: destination station of the journey
        :param journeydate: date of journey in DD-MM-YYYY format
        :return: json object having availability data
        """

        resultjson = {"availability": []}
        try:
            availablitydata = json.loads(jsonresponse)
        except Exception as e:
            logger.error("Error in parsing availability data for train[%s] from source [%s] to destination [%s] on [%s], reason [%s]", trainnumber, sourcestation, destinationstation, journeydate, e.message)
            return resultjson

        if availablitydata['response_code'] != 200 or len(availablitydata['availability']) == 0:
            logger.warning("No availability data present for train[%s] from source [%s] to destination [%s] on [%s], reason [%s]", trainnumber, sourcestation, destinationstation, journeydate, availablitydata['error'])
            return resultjson
        print availablitydata

        for availability in availablitydata['availability']:
            availabledata = {'date': availability['date'], 'status': availability['status']}
            resultjson['availability'].append(availabledata)

        return resultjson