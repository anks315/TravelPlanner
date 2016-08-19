# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import flightapi, flightdirectandnearairportapi, flightfrombigairportapi, flightnearbigapi, flightbignearapi, flightutil, busapi, trainapineo4j, trainavailabilityapi
import TravelPlanner.startuputil as startup
import trie

# bus, train, flight controller to get results
traincontrollerneo = trainapineo4j.TrainController()
trainavailabilitycontroller = trainavailabilityapi.TrainAvailabilityController()
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
     context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
     return render_to_response('index.html',{},context_instance = context)


def main(request):

     return render_to_response('main.html',{},context_instance = RequestContext(request))

def mainMobile(request):

     return render_to_response('mainMobile.html',{},context_instance = RequestContext(request))

def planning(request):

     return render_to_response('planning.html',{},context_instance = RequestContext(request))

def planningMobile(request):

     return render_to_response('planningMobile.html',{},context_instance = RequestContext(request))

def traininit(request):

     startup.loadtraindata()
     return render_to_response('index.html',{},context_instance = RequestContext(request))

def cityinit(request):
    trie.initialize()
    return render_to_response('index.html',{},context_instance = RequestContext(request))

def test(request):
     prefix = request.GET['prefix']
     listtoreturn= trie.TRIE.autocomplete(str(prefix).title())
     jsoncity = {'cities':list(listtoreturn)}
     return HttpResponse(json.dumps(jsoncity), content_type='application/json')

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


def trainavailabilityapi(request):

    """
    To get availablity data for trainnumber from source to destination on journeydate for given trainclass
    :param request: hhtp request
    :return: availablity data between requested stations
    """

    source = request.GET['source']
    destination = request.GET['destination']
    journeydate = request.GET['journeyDate']
    trainclass = request.GET["trainClass"]
    quota = request.GET["quota"]
    trainnumber = request.GET['trainNumber']
    resultjsondata = trainavailabilitycontroller.getavailablity(trainnumber, source, destination, journeydate, trainclass)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')


def busapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeyDate = request.GET['journeyDate']
    numberofAdults=request.GET["adults"]
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = buscontroller.getresults(source,destination,journeyDate,numberofAdults)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

