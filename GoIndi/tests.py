# from django.test import TestCase

# Create your tests here.

from sets import Set
import trainapiNeo4j


#getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR', )
trainapiNeo4j.TrainController.getRoutes(trainapiNeo4j.TrainController(), 'NEW DELHI', 'MUMBAI')
#getPipeSeperatedStationCodes(Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT']))