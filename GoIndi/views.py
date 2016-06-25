# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext,loader,Context
import json
import trainapi
import flightapi, flightdirectapi
import distanceutil
import busapi
import trainapiNeo4j

traincontroller = trainapi.TrainController()
traincontrollerneo = trainapiNeo4j.TrainController()
flightcontroller = flightapi.FlightController()
flightdirectcontroller = flightdirectapi.FlightDirectController()
buscontroller = busapi.BusController()


def home(request):
     #getPossibleBreakingPlacesForTrain('x',"Kanpur")
     #models.isCityExist("ADRA")
     #getApiResults()
     print(distanceutil.findnearestbigairport(32.7218,74.8577))
     return render_to_response('eazzer.html',{},context_instance = RequestContext(request))


def main(request):

     return render_to_response('main.html',{},context_instance = RequestContext(request))


def test(request):

     return render_to_response('index.html',{},context_instance = RequestContext(request))


def flightapi(request):

    sourcecity = request.GET['sourcecity']
    #sourcestate = request.GET['sourcestate']
    destinationcity = request.GET['destinationcity']
    #destinationstate = request.GET['destinationstate']
    journeydate = request.GET['journeyDate']
    trainclass = request.GET["trainClass"]
    flightclass = request.GET["flightClass"]
    numberofadults = request.GET["adults"]
    # request.session['source']=source
    # request.session['destination']=destination
    resultjsondata = flightcontroller.getresults(sourcecity, destinationcity, journeydate, trainclass, flightclass,
                                                 numberofadults)
    return HttpResponse(json.dumps(resultjsondata), content_type='application/json')


def flightdirectapi(request):

    """
    To fetch only direct flight between source & destination
    :param request: Http request from gui
    :return: http response having direct flight data
    """
    sourcecity = request.GET['sourcecity']
    destinationcity = request.GET['destinationcity']
    journeydate = request.GET['journeyDate']
    flightclass = request.GET["flightClass"]
    numberofadults = request.GET["adults"]
    resultjsondata = flightdirectcontroller.getresults(sourcecity, destinationcity, journeydate, flightclass, numberofadults)
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
    resultJsonData = buscontroller.getResults(source,destination,journeyDate,numberofAdults)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

