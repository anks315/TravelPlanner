__author__ = 'Hello'

#
# <root>
#  <doc>
#      <field1 name="blah">some value1</field1>
#      <field2 name="asdfasd">some vlaue2</field2>
#  </doc>
#
# </root>


# root = ET.Element("root")
# doc = ET.SubElement(root, "doc")
#
# ET.SubElement(doc, "field1", name="blah").text = "some value1"
# ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
#
# tree = ET.ElementTree(root)
# tree.write("filename.xml")

import requests, datetime
import xml.etree.ElementTree as ET
from cStringIO import StringIO

url = "http://affapi.mantistechnologies.com/Service.asmx?WSDL"
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor


travelYaariCityMap = {}
def createauthenticationrequest():

    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
    <Authenticate xmlns="http://tempuri.org/">
        <LoginID>%s</LoginID>
        <Password>%s</Password>
        <UserType>%s</UserType>
        <LoginCode>%s</LoginCode>
    </Authenticate>
    </soap12:Body>
    </soap12:Envelope>""" %("eazzer", "mantis123", "S", "9542")

    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)

    print response.content

# createauthenticationrequest()


def getcities():

    body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetAllCities xmlns="http://tempuri.org/">
      <Authentication>
        <UserID>%s</UserID>
        <UserType>%s</UserType>
        <Key>%s</Key>
      </Authentication>
    </GetAllCities>
  </soap12:Body>
</soap12:Envelope>""" % (6898, "S", "76383b34503afb0508f8364787c55800")

    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    searchTree = ET.parse(StringIO(response.content))

    for elem in searchTree.iter(tag='{http://tempuri.org/}City'):
        travelYaariCityMap[elem.find('{http://tempuri.org/}CityName').text] = elem.find('{http://tempuri.org/}CityID').text


# getcities()

date = datetime.datetime.strptime("26/09/2016", '%d/%m/%Y').strftime('%Y-%m-%d')
print date

def getroutes(journeyDateStr,source,destination):
    journeyDate = datetime.datetime.strptime(journeyDateStr, '%d-%m-%Y').strftime('%Y-%m-%d')
    sourceCode = travelYaariCityMap[str(source).lower()]
    destinationCode = travelYaariCityMap[str(destination).lower()]
    body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetRoutes2 xmlns="http://tempuri.org/">
      <Authentication>
        <UserID>%s</UserID>
        <UserType>%s</UserType>
        <Key>%s</Key>
      </Authentication>
      <SearchRequest>
        <FromCityId>%s</FromCityId>
        <ToCityId>%s</ToCityId>
        <JourneyDate>%s</JourneyDate>
        <NoOfSeats>%s</NoOfSeats>
        <SearchId>%s</SearchId>
      </SearchRequest>
    </GetRoutes2>
  </soap12:Body>
</soap12:Envelope>"""% (6898, "S", "76383b34503afb0508f8364787c55800", sourceCode, destinationCode, journeyDate, 1, 0)
    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    searchTree = ET.parse(StringIO(response.content))
    jsondata={"apiAvailableBuses" : []}
    for elem in searchTree.iter(tag='{http://tempuri.org/}clsRoute2'):
        detail = {}
        detail['routeScheduleId']  = elem.find('{http://tempuri.org/}RouteScheduleId').text
        detail['arrivalTime'] = elem.find('{http://tempuri.org/}ArrTime').text.split('T')[1]
        detail['departureTime'] = elem.find('{http://tempuri.org/}DepTime').text.split('T')[1]
        detail['operatorName'] = elem.find('{http://tempuri.org/}CompanyName').text
        detail['busType'] = elem.find('{http://tempuri.org/}BusTypeName').text
        detail['fare'] = elem.find('{http://tempuri.org/}Fare').text
        detail['availableSeats'] = elem.find('{http://tempuri.org/}AvailableSeats').text
        detail['vendor'] = "travelyaari"
        jsondata["apiAvailableBuses"].append(detail)

    return jsondata

# getroutes()



def getpickups():

    body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetPickups xmlns="http://tempuri.org/">
      <Authentication>
        <UserID>%s</UserID>
        <UserType>%s</UserType>
        <Key>%s</Key>
      </Authentication>
      <RouteScheduleId>%s</RouteScheduleId>
    </GetPickups>
  </soap12:Body>
</soap12:Envelope>"""%(6898, "S", "76383b34503afb0508f8364787c55800", 552261119)
    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    print response.content

# getpickups()


def holdseats():
    imp = Import('http://www.w3.org/XML/1998/namespace',
                 location='http://localhost:8000/static/XMLSchema.xsd')
    imp.filter.add('http://tempuri.org/')
    client = Client(url, doctor=ImportDoctor(imp))
    print client
    authentication = client.factory.create('clsAuthenticateRequest')
    authentication.UserID = 6898
    authentication.UserType = "S"
    authentication.Key = "76383b34503afb0508f8364787c55800"
    contactInfo = client.factory.create('clsContactInformation')
    contactInfo.CustomerName="Shekhar"
    contactInfo.Email = "ab@xyz.com"
    contactInfo.Phone = "99877778"
    contactInfo.Mobile = "09999988988"
    arrayOfPassenger = client.factory.create('ArrayOfPassenger')
    passenger = client.factory.create('Passenger')
    passenger.Name = 'shekhar'
    passenger.Age = '25'
    passenger.Gender = 'M'
    passenger.SeatNo = 'S5'
    passenger.Fare = '200'
    passenger.SeatType = 'ac'
    passenger.IsAcSeat = '1'
    arrayOfPassenger.Passenger.append(passenger)
    result = client.service.HoldSeatsForSchedule(authentication,123,'',123,contactInfo,arrayOfPassenger)
    print result.content



def getArrangement(routeScheduleId, journeyDateStr):
    journeyDate = datetime.datetime.strptime(journeyDateStr, '%Y-%m-%d').strftime('%Y-%m-%d')
    body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
     <GetArrangement xmlns="http://tempuri.org/">
      <Authentication>
        <UserID>%s</UserID>
        <UserType>%s</UserType>
        <Key>%s</Key>
      </Authentication>
      <RouteScheduleId>%s</RouteScheduleId>
      <JourneyDate>%s</JourneyDate>
    </GetArrangement>
  </soap12:Body>
</soap12:Envelope>""" % (6898, "S", "76383b34503afb0508f8364787c55800", routeScheduleId, journeyDate)

    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    searchTree = ET.parse(StringIO(response.content))

    seatInfo = {}
    root = searchTree.getroot()
    seatInfo["maxRows"] = searchTree.findall('.//{http://tempuri.org/}MaxRows')[0].text
    seatInfo["maxColumns"] = searchTree.findall('.//{http://tempuri.org/}MaxColumns')[0].text
    seatList=[]
    for elem in searchTree.iter(tag='{http://tempuri.org/}clsSeat'):
        details = {}
        details['Row'] = elem.find('{http://tempuri.org/}Row').text
        details['Col'] = elem.find('{http://tempuri.org/}Col').text
        details['Height'] = elem.find('{http://tempuri.org/}Height').text
        details['SeatNo'] = elem.find('{http://tempuri.org/}SeatNo').text
        details['Gender'] = elem.find('{http://tempuri.org/}Gender').text
        details['IsSleeper'] = elem.find('{http://tempuri.org/}IsSleeper').text
        details['IsAvailable'] = elem.find('{http://tempuri.org/}IsAvailable').text
        details['Fare'] = elem.find('{http://tempuri.org/}Fare').text
        details['IsAisle'] = elem.find('{http://tempuri.org/}IsAisle').text

        seatList.append(details)
    seatInfo["seatList"] = seatList
    return seatInfo

