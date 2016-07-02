# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import trainapi
import flightapi, flightdirectandnearairportapi, flightfrombigairportapi, flightnearbigapi, flightbignearapi
import distanceutil, flightutil
import busapi
import trainapiNeo4j
import TravelPlanner.trainUtil as startup

# bus, train, flight controller to get results
traincontroller = trainapi.TrainController()
traincontrollerneo = trainapiNeo4j.TrainController()
flightcontroller = flightapi.FlightController()
buscontroller = busapi.BusController()
flightdirectandnearcontroller = flightdirectandnearairportapi.FlightDirectAndNearAirportController()
flightbigcontroller = flightfrombigairportapi.FlightFromBigAirportController()
flightnearbigcontroller = flightnearbigapi.FlightNearBigAirportController()
flightbignearcontroller = flightbignearapi.FlightBigNearAirportController()


def home(request):
     #getPossibleBreakingPlacesForTrain('x',"Kanpur")
     #models.isCityExist("ADRA")
     #getApiResults()
     #print(distanceutil.findnearestbigairport(32.7218,74.8577))
     return render_to_response('index.html',{},context_instance = RequestContext(request))


def main(request):

     return render_to_response('main.html',{},context_instance = RequestContext(request))

def traininit(request):

     startup.loadtraindata()
     return render_to_response('index.html',{},context_instance = RequestContext(request))


def test(request):

     return render_to_response('index.html',{},context_instance = RequestContext(request))


def flightapi(request):

    # #sourcestate = request.GET['sourcestate']
    # #destinationstate = request.GET['destinationstate']
    flightrequest = flightutil.getflightrequestparams(request)
    resultjsondata = flightcontroller.getresults(flightrequest.sourcecity, flightrequest.destinationcity, flightrequest.journeydate, flightrequest.trainclass, flightrequest.flightclass, flightrequest.numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')


def flightdirectandnearapi(request):
    """
    To fetch flight journey between source & destination via nearest airports
    :param request: http request
    :return: flight journey between source & destination
    """
    flightrequest = flightutil.getflightrequestparams(request)
    resultjsondata = flightdirectandnearcontroller.getresults(flightrequest.sourcecity, flightrequest.destinationcity, flightrequest.journeydate, flightrequest.trainclass, flightrequest.flightclass, flightrequest.numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')

def flightnearbigapi(request):
    """
    To fetch flight journey between source & destination via biggest airport near destination and nearest airport of source
    :param request: http request
    :return: flight journey between source & destination
    """
    flightrequest = flightutil.getflightrequestparams(request)
    resultjsondata = flightnearbigcontroller.getresults(flightrequest.sourcecity, flightrequest.destinationcity, flightrequest.journeydate, flightrequest.trainclass, flightrequest.flightclass, flightrequest.numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')


def flightbignearapi(request):
    """
    To fetch flight journey between source & destination via biggest airport near source and nearest airport of destination
    :param request: http request
    :return: flight journey between source & destination
    """
    flightrequest = flightutil.getflightrequestparams(request)
    resultjsondata = flightbignearcontroller.getresults(flightrequest.sourcecity, flightrequest.destinationcity, flightrequest.journeydate, flightrequest.trainclass, flightrequest.flightclass, flightrequest.numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')


def flightbigapi(request):
    """
    To fetch flight journey between source & destination via nearest airports
    :param request: http request
    :return: flight journey between source & destination
    """
    flightrequest = flightutil.getflightrequestparams(request)
    resultjsondata = flightbigcontroller.getresults(flightrequest.sourcecity, flightrequest.destinationcity, flightrequest.journeydate, flightrequest.trainclass, flightrequest.flightclass, flightrequest.numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')

def trainapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeydate = request.GET['journeyDate']
    trainclass = request.GET["trainClass"]
    numberofadults = request.GET["adults"]
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = traincontrollerneo.getroutes(source,destination,journeydate,0,trainclass,int(numberofadults))
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

def busapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeyDate = request.GET['journeyDate']
    numberofAdults=request.GET["adults"]
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = buscontroller.getresults(source,destination,journeyDate,numberofAdults)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

