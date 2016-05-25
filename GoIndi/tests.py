# from django.test import TestCase

# Create your tests here.

from sets import Set
import trainapiNeo4j


#getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR', )
trainapiNeo4j.TrainController.findTrainsBetweenStations(trainapiNeo4j.TrainController(), 'NEW DELHI', Set(['BCT', 'CSTM', 'UMB', 'BTI']))
#getPipeSeperatedStationCodes(Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT']))