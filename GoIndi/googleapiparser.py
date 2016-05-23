
import urllib
import trainConstants
import json


def parseTransitRoutes(jsonTransitRoute,destination):
    returnedData = json.loads(jsonTransitRoute)
    possibleBreakList=[]
    for leg in returnedData["routes"][0]["legs"]:
        stepNumber=0
        possibleBreak=[]
        for step in leg["steps"]:
            if "transit_details" in step and  "RAIL" in step["transit_details"]["line"]["vehicle"]["type"]:
                if stepNumber==1 and destination in step["transit_details"]["arrival_stop"]["name"]:
                    possibleBreak.append(step["transit_details"]["departure_stop"]["name"])

                if stepNumber!=0 and destination not in step["transit_details"]["arrival_stop"]["name"]:
                    possibleBreak.append(step["transit_details"]["arrival_stop"]["name"])
                    possibleBreak.append(step["transit_details"]["departure_stop"]["name"])

                stepNumber=stepNumber+1
        possibleBreakList.append(possibleBreak)
    return possibleBreakList



def getPossibleBreakingPlacesForTrain(source,destination):
    jsonTransitRoute = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=Jammu,IN&destination=Kanpur,IN&mode=transit&alternatives=true&key="+ trainConstants.GOOGLE_API_KEY).read()
    possibleBreakage = parseTransitRoutes(jsonTransitRoute,destination)
    return possibleBreakage



