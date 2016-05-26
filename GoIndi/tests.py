# from django.test import TestCase

# Create your tests here.

from sets import Set
#import trainapiNeo4j
import json
import trainDBscript
import concurrent.futures
filename = "C:/Users/Ankit Kumar/Downloads/11073_routes.txt"


#getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR', )
#trainapiNeo4j.TrainController.getRoutes(trainapiNeo4j.TrainController(), 'NEW DELHI', 'MUMBAI')
#getPipeSeperatedStationCodes(Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT']))


def populateDB():
    with open(filename) as data_file:
        routedata = json.load(data_file)
    print routedata
    trainStations = []

    for route in routedata["route"]:
        stationInformation={}
        stationInformation["code"]=route["code"]
        stationInformation["arrivalTime"]=route["scharr"]
        stationInformation["departureTime"]=route["schdep"]
        stationInformation["day"]=route["day"]
        stationInformation["name"]=route["fullname"]
        print stationInformation
        trainStations.append(stationInformation)

    index=0
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        numberOfStations=len(trainStations)
        while index < numberOfStations-1:
            iterator=index+1
            while iterator <= numberOfStations -1:
                executor.submit(trainDBscript.getTrainFare(trainStations[index]["code"],trainStations[iterator]["code"],'11072', trainStations[index],trainStations[iterator]))
                iterator += 1
            index += 1

populateDB()