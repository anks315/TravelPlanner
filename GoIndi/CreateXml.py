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

url = "http://affapi.mantistechnologies.com/Service.asmx?WSDL"


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
    </soap12:Envelope>""" %("eazzer", "Shekhar123@", "S", "9542")

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

    open("C:/Users/Ankit Kumar/Downloads/file.xml", "w").write(response.content)

# getcities()

date = datetime.datetime.strptime("26/09/2016", '%d/%m/%Y').strftime('%Y-%m-%d')
print date

def getroutes():

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
</soap12:Envelope>"""% (6898, "S", "76383b34503afb0508f8364787c55800", 2551, 2592, date, 1, 0)
    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    print response.content

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


def holdseats6():
    body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <HoldSeats6 xmlns="http://tempuri.org/">
      <Authentication>
        <UserID>%s</UserID>
        <UserType>%s</UserType>
        <Key>%s</Key>
      </Authentication>
      <RouteScheduleId>%s</RouteScheduleId>
      <JourneyDate>%s</JourneyDate>
      <PickUpID>%s</PickUpID>
      <ContactInformation>
        <CustomerName>%s</CustomerName>
        <Email>%s</Email>
        <Phone>%s</Phone>
        <Mobile>%s</Mobile>
      </ContactInformation>
      <Passengers>
        <Passenger>
          <Name>%s</Name>
          <Age>%s</Age>
          <Gender>%s</Gender>
          <SeatNo>%s</SeatNo>
          <Fare>%s</Fare>
          <SeatType>%s</SeatType>
          <IsAcSeat>%s</IsAcSeat>
        </Passenger>
      </Passengers>
      <Remarks>%s</Remarks>
      <BookingPaymentModeID>%s</BookingPaymentModeID>
      <TicketCollectionID>%s</TicketCollectionID>
      <PartyID>%s</PartyID>
      <BankID>%s</BankID>
      <GatewayUsed>%s</GatewayUsed>
      <OldPNR>%s</OldPNR>
      <Comments>%s</Comments>
      <TransactionID>%s</TransactionID>
      <Address>%s</Address>
      <CityID>%s</CityID>
      <AreaID>%s</AreaID>
      <PincodeID>%s</PincodeID>
      <OrderID>%s</OrderID>
      <IsReturnJourney>%s</IsReturnJourney>
      <Discount>%s</Discount>
      <DiscountPer>%s</DiscountPer>
      <DiscountReason>%s</DiscountReason>
      <DeliveryCharge>%s</DeliveryCharge>
      <PGName>%s</PGName>
      <ProviderDiscount>%s</ProviderDiscount>
      <PgMethod>%s</PgMethod>
      <PgProvider>%s</PgProvider>
      <InsuranceFees>%s</InsuranceFees>
      <InsuranceAgentComm>%s</InsuranceAgentComm>
      <InsuranceCommKey>%s</InsuranceCommKey>
    </HoldSeats6>
  </soap12:Body>
</soap12:Envelope>"""%(6898, "S", "76383b34503afb0508f8364787c55800", 552261119, date, 19361568, "RD", "rishabhdaim1991@gmail.com",8800640514,8800640514, "RD", 25, "Male", 24, 227, "", "true",
                       "", 0,0,0,0,"","","", "","",2551,"","",0, "false",0.0, 0.0,"",0.0,"", 0.0,"", 0.0,0.0, 0.0, "")
    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)
    print response.content


holdseats6()