# from django.test import TestCase

# Create your tests here.
import dateTimeUtility
import calendar
from datetime import datetime, timedelta
import time
import models
import loggerUtil
import logging
from sets import Set
#import trainapiNeo4j
# import json
# import trainDBscript
# import concurrent.futures
# filename = "C:/Users/Ankit Kumar/Downloads/11073_routes.txt"
#
#
# #getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR', )
# #trainapiNeo4j.TrainController.getRoutes(trainapiNeo4j.TrainController(), 'NEW DELHI', 'MUMBAI')
# #getPipeSeperatedStationCodes(Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT']))
#
#
# def populateDB():
#     with open(filename) as data_file:
#         routedata = json.load(data_file)
#     print routedata
#     trainstations = []
#
#     for route in routedata["route"]:
#         stationinformation = {"code": route["code"], "arrivalTime": route["scharr"], "departureTime": route["schdep"],
#                              "day": route["day"], "name": route["fullname"]}
#         print stationinformation
#         trainstations.append(stationinformation)
#
#     index=0
#     # We can use a with statement to ensure threads are cleaned up promptly
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         # Start the load operations and mark each future with its URL
#         numberOfStations=len(trainstations)
#         while index < numberOfStations-1:
#             iterator=index+1
#             while iterator <= numberOfStations -1:
#                 executor.submit(trainDBscript.getTrainFare(trainstations[index]["code"],trainstations[iterator]["code"],'11057', trainstations[index],trainstations[iterator]))
#                 iterator += 1
#             index += 1
#
# populateDB()

# def getDay():
#     journeydate = '24-01-1991'
#     diff = 2
#     t = (datetime.strptime(journeydate, '%d-%m-%Y') - timedelta(days=1))
#     print t.strftime('%d-%m-%Y')
#     #day = calendar.day_name[t].upper()
#     #print day
#
# getDay()

#print dateTimeUtility.getduration('04:35', '09:12','16-02-2016','14-02-2016')
#dateTimeUtility.addduration('04:35', '24:20')
models.getfarefortrainandpersist('12013', 'NDLS', 'ASR',loggerUtil.getLogger('tmp',logging.DEBUG))