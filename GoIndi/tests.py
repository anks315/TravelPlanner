# from django.test import TestCase
# from multiprocessing import Pool
# import threading, time
# import dateTimeUtility
# import models
# import trainDBscript
import datetime, re
import glob, os, trainavailabilityapi
# trainDBscript.fetchnonexitingfaredata()
#models.testquery()
# Create your tests here.
# import trainapiNeo4j
# filename = "C:/Users/Ankit Kumar/Downloads/11073_routes.txt"
#
#
# #getPossibleBreakingPlacesForTrain('Jammu', 'KANPUR', )
# #trainapiNeo4j.TrainController.getRoutes(trainapiNeo4j.TrainController(), 'NEW DELHI', 'MUMBAI')
# #getPipeSeperatedStationCodes(Set(['RAILWAY', 'STATION', 'JUNCTION', 'CITY', 'CANTT']))
#
#
# def populateDB():
#     with open(filename) as data_file:
#         routedata = json.load(data_file)
#     print routedata
#     trainstations = []
#
#     for route in routedata["route"]:
#         stationinformation = {"code": route["code"], "arrivalTime": route["scharr"], "departureTime": route["schdep"],
#                              "day": route["day"], "name": route["fullname"]}
#         print stationinformation
#         trainstations.append(stationinformation)
#
#     index=0
#     # We can use a with statement to ensure threads are cleaned up promptly
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         # Start the load operations and mark each future with its URL
#         numberOfStations=len(trainstations)
#         while index < numberOfStations-1:
#             iterator=index+1
#             while iterator <= numberOfStations -1:
#                 executor.submit(trainDBscript.getTrainFare(trainstations[index]["code"],trainstations[iterator]["code"],'11057', trainstations[index],trainstations[iterator]))
#                 iterator += 1
#             index += 1
#
# populateDB()

# def getDay():
#     journeydate = '24-01-1991'
#     diff = 2
#     t = (datetime.strptime(journeydate, '%d-%m-%Y') - timedelta(days=1))
#     print t.strftime('%d-%m-%Y')
#     #day = calendar.day_name[t].upper()
#     #print day
#
# getDay()

#print dateTimeUtility.getduration('04:35', '09:12','16-02-2016','14-02-2016')
#dateTimeUtility.addduration('04:35', '24:20')
#models.getfarefortrainandpersist('12013', 'NDLS', 'ASR',loggerUtil.getLogger('tmp',logging.DEBUG))

# def readConfig():
#     H = dict(line.strip().split('=') for line in open('../configuration.properties'))
#     print H
#
# readConfig()

# def f(x):
#     print 'started'
#     time.sleep(5)
#     return x*x

# def z():
#     thread = threading.Thread(target=f(5))
#     thread.setDaemon(False)
#     thread.start()
#     time.sleep(3)
#     print 'called thread'

# def c(x):
#     print 'callback'
#     print x

# if __name__ == '__main__':
#     pool = Pool(processes=1)
#     result = pool.apply_async(f, [2], callback=c)
#     pool.close()
#     pool.join()
#     print 'done'


#dateTimeUtility.isjourneypossible('04:35', '09:12','16-02-2016','14-02-2016', 3, 12)

path = "C:/Users/Hello/Downloads/logs"
destpath = "C:/Users/Hello/Downloads/done"
def test():
    today = datetime.date.today()
    d = (today + datetime.timedelta(days=20)).strftime('%d-%m')
    print str(d)

def readmultiplefiles():
    for filename in os.listdir(path):
        if filename.endswith('.log'):
            lines = open(path + '/' +filename, 'r').read().splitlines()
            for line in lines:
                print line

def movefile():
    for filename in os.listdir(path):
        if filename.endswith('.log'):
            os.rename(path+'/'+filename, destpath+'/'+filename)

# readmultiplefiles()
def convertstringtotime():
    string = '12:35:00'
    t = datetime.datetime.strptime(string, '%H:%M:%S')
    print t.time().strftime('%H:%M')

# convertstringtotime()
#trainavailabilityapi.TrainAvailabilityController().getavailablity('12013', 'NDLS', 'ASR', '24-07-2016', 'CC')

matched = bool(re.compile("[A-Z]*[ ]?[A-Z]*[ ]?" + re.sub("[AIE]", "[AIE]", "NAMPALLY") + "[ ]?[A-Z ]*").match( "HYDERABAD DECAN NAMPALLY"))
print matched
v = 'tsivakasi'
v = re.sub('^(siva|shiva)', "(siva|shiva)", v)
print v
v = re.sub("[aie]", "[aie]", v)
print v
matched = bool(re.compile("[A-Z]*[ ]?[A-Z]*[ ]?" + v + "[ ]?[A-Z ]*").match( "sivakasi"))
print matched
n = 'nlampalli'
n = re.sub('^(GARH|GADH)|(GARH|GADH)$', '(GARH|GADH)', n)
print n
n = re.sub('(ll|l)', '(ll|l)', n)
n = re.sub('[aiye]', '[aiye]', n)
print n
