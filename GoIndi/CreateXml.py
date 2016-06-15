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

import xml.etree.cElementTree as ET
import requests
from suds.client import Client

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
    </soap12:Envelope>""" %("test", "test456", "S", "9542")

    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)

    print response.content

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
</soap12:Envelope>""" % (50, "S", "c0c7c76d30bd3dcaefc96f40275bdc0a")

    headers = {"POST" : "/Service.asmx HTTP/1.1",
               "Host": "affapi.mantistechnologies.com",
            "Content-Type": "application/soap+xml; charset=utf-8",
               "Content-Length" : len(body)}

    print body
    print headers

    response = requests.post(url,data=body, headers=headers)

    open("C:/Users/Hello/Downloads/file.xml", "w").write(response.content)

getcities()

