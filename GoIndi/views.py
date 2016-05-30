# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext,loader,Context
import logging
import datetime
import urllib2
import json
from django.core.context_processors import csrf
import trainapi
import flightapi

import busapi

import models
import trainapiNeo4j
import trainDBscript
from googleapiparser import getPossibleBreakingPlacesForTrain
from flightSkyScanner import getApiResults


trainController = trainapi.TrainController()
trainControllerneo = trainapiNeo4j.TrainController()
flightController = flightapi.FlightController()


busController = busapi.BusController()

def home(request):
     #getPossibleBreakingPlacesForTrain('x',"Kanpur")
     #models.isCityExist("ADRA")
     #getApiResults()
     return render_to_response('eazzer.html',{},context_instance = RequestContext(request))

def main(request):

     return render_to_response('main.html',{},context_instance = RequestContext(request))

def test(request):

     return render_to_response('index.html',{},context_instance = RequestContext(request))
def flightapi(request):
    sourcecity = request.GET['sourcecity']
    sourcestate = request.GET['sourcestate']
    destinationcity = request.GET['destinationcity']
    destinationstate = request.GET['destinationstate']
    journeyDate = request.GET['journeyDate']
    # request.session['source']=source
    # request.session['destination']=destination
    resultJsonData = flightController.getResults(sourcecity,sourcestate, destinationcity,destinationstate, journeyDate)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

def trainapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeyDate = request.GET['journeyDate']
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = trainControllerneo.getRoutes(source,destination,journeyDate)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

def busapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeyDate = request.GET['journeyDate']
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = busController.getResults(source,destination,journeyDate)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

