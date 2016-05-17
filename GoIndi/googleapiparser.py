
import urllib
import trainConstants
import json


def getPossibleBreakingPlacesForTrain(source,destination):
    jsonTransitRoute = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=Jammu,IN&destination=Kanpur,IN&mode=transit&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY).read()
    possibleBreakage = parseTransitRoutes(jsonTransitRoute,destination)
    return possibleBreakage



def parseTransitRoutes(jsonTransitRoute,destination):
    returnedData = json.loads(jsonTransitRoute)
    possibleBreakList=[]
    for leg in returnedData["legs"]:
        stepNumber=0
        possibleBreak=[]
        for step in leg["steps"]:
            if step["transit_details"]["line"]["vehicle"]["type"]=="Rail":
                if stepNumber==1 and destination not in step["transit_details"]["arrival_stop"]:
                    possibleBreak.append(step["transit_details"]["departure_stop"])
                else:
                    if stepNumber!=0 and destination not in step["transit_details"]["arrival_stop"]:
                        possibleBreak.append(step["transit_details"]["arrival_stop"])
                        possibleBreak.append(step["transit_details"]["departure_stop"])

                stepNumber=stepNumber+1
        possibleBreakList.append(possibleBreak)