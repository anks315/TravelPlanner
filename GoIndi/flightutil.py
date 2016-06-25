__author__ = 'Hello'

import urllib2, json
import distanceutil
from entity import Airports, NearestAirports
import threading

# map of airport code and their corresponding cities
stationtocitymap = {'JSA':'Jaisalmer','RJA':'Rajahmundry','PGH':'Pantnagar','IXP':'Pathankot','KUU':'Kullu','SLV':'Shimla','IXA':'Agartala','AGR':'Agra','AMD':'Ahmedabad','IXD':'Allahabad','ATQ':'Amritsar','IXU':'Aurangabad','IXB':'Bagdogra','BLR':'Bangalore','BHU':'Bhavnagar','BHO':'Bhopal','BBI':'Bhubaneswar','BHJ':'Bhuj','CCU':'Kolkata','IXC':'Chandigarh','MAA':'Chennai','COK':'Cochin','CJB':'Coimbatore','NMB':'Daman','DED':'Dehradun','DIB':'Dibrugarh','DMU':'Dimapur','DIU':'Diu','GAU':'Gauhati','GOI':'Goa','GWL':'Gwalior','HBX':'Hubli','HYD':'Hyderabad','IMF':'Imphal','IDR':'Indore','JAI':'Jaipur','IXJ':'Jammu','JGA':'Jamnagar','IXW':'Jamshedpur','JDH':'Jodhpur','JRH':'Jorhat','KNU':'Kanpur','HJR':'Khajuraho','CCJ':'Kozhikode','IXL':'Leh','LKO':'Lucknow','LUH':'Ludhiana','IXM':'Madurai','IXE':'Mangalore','BOM':'Mumbai','NAG':'Nagpur','NDC':'Nanded','ISK':'Nasik','DEL':'New Delhi','PAT':'Patna','PNY':'Pondicherry','PNQ':'Poona','PNQ':'Pune','PBD':'Porbandar','IXZ':'Port Blair','PUT':'PuttasubParthi','BEK':'Rae Bareli','RAJ':'Rajkot','IXR':'Ranchi','SHL':'Shillong','IXS':'Silchar','SXR':'Srinagar','STV':'Surat','TEZ':'Tezpur','TRZ':'Tiruchirapally','TIR':'Tirupati','TRV':'Trivandrum','UDR':'Udaipur','BDQ':'Vadodara','VNS':'Varanasi','VGA':'Vijayawada','VTZ': 'Vishakhapatnam'}
nearestairportsmap = {}
lock = threading.RLock()


def getnearestairports(source, destination):

    """
    To get entity of nearest airports for given source & destination
    :param source: source of journey
    :param destination: destination of journey
    :return: collection of nearest airports
    """

    airports = Airports()
    sourceairports = getnearestairportfrommap(source)
    if not sourceairports:
        # get nearest airport and nearest big airport to our source city
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + source
        url = url.replace(' ', '%20')
        response = urllib2.urlopen(url)
        sourcelatlong = json.loads(response.read())
        response.close()
        sourcelat = sourcelatlong["results"][0]["geometry"]["location"]["lat"]
        sourcelong = sourcelatlong["results"][0]["geometry"]["location"]["lng"]
        sourceairport = stationtocitymap[distanceutil.findnearestairport(sourcelat,sourcelong)]
        bigsourceairport = stationtocitymap[distanceutil.findnearestbigairport(sourcelat,sourcelong)]
        sourceairports = NearestAirports()
        sourceairports.near = sourceairport
        sourceairports.big = bigsourceairport
        with lock:
            nearestairportsmap[source] = sourceairports

    destinationairports = getnearestairportfrommap(destination)
    if not destinationairports:
        # get nearest airport and nearest big airport to our destination city
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + destination
        url = url.replace(' ', '%20')
        response2 = urllib2.urlopen(url)
        destlatlong = json.loads(response2.read())
        destlat = destlatlong["results"][0]["geometry"]["location"]["lat"]
        destlong = destlatlong["results"][0]["geometry"]["location"]["lng"]
        destairport = stationtocitymap[distanceutil.findnearestairport(destlat, destlong)]
        bigdestinationairport = stationtocitymap[distanceutil.findnearestbigairport(destlat, destlong)]
        destinationairports = NearestAirports()
        destinationairports.near = destairport
        destinationairports.big = bigdestinationairport
        with lock:
            nearestairportsmap[destination] = destinationairports

    airports.sourceairports = sourceairports
    airports.destinationairports = destinationairports

    return airports


def getnearestairportfrommap(city):
    """
    Get nearest airports to given city from map
    :param city: city for which nearest airports are to calculated
    :return:
    """

    lock.acquire()
    try:
        if city in nearestairportsmap.keys():
            return nearestairportsmap[city]
        else:
            return
    finally:
        # Always called, even if exception is raised in try block
        lock.release()