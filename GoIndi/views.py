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
from flightapi import parseFlightAndReturnFare

trainController = trainapi.TrainController()
def home(request):
     return render_to_response('eazzer.html',{},context_instance = RequestContext(request))

def main(request):
     return render_to_response('main.html',{},context_instance = RequestContext(request))

def test(request):
     return render_to_response('index.html',{},context_instance = RequestContext(request))

def trainapi(request):
    source = request.GET['source']
    destination = request.GET['destination']
    journeyDate = request.GET['journeyDate']
    #request.session['source']=source
    #request.session['destination']=destination
    resultJsonData = trainController.getRoutes(source,destination,journeyDate)
    return HttpResponse(json.dumps(resultJsonData), content_type='application/json')

def flightapi(request):
    api_key = "AIzaSyAgFB2oxb44p3tgUM-baPQsT2eN_Vz1TVQ"
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}
    params = {
        "request": {
        "slice": [
                    {
                    "origin": "DEL",
                    "destination": "BLR",
                    "date": "2016-04-20"
                    }
                ],
        "passengers": {
                    "adultCount": 1
                      },
        "solutions": 5
                     }
            }

    jsonreq = json.dumps(params, encoding = 'utf-8')
    req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
    flight = urllib2.urlopen(req)
    response = flight.read()
    flight.close()
    return HttpResponse(json.dumps(parseFlightAndReturnFare(response)), content_type='application/json')
