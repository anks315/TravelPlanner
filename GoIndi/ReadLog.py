__author__ = 'Hello'


filename = "C:/Users/Hello/Downloads/sortedTrainList.log"
# filename1 = "C:/Users/Ankit Kumar/Downloads/test1.txt"
# filename2 = "C:/Users/Ankit Kumar/Downloads/test2.txt"
#
# def read():
#     f = open(filename, "r")
#     print filename
#     line = f.read().splitlines()
#     models.checkStationExists(line)
#
#
# read()

def readLog():
    f = open(filename, 'r')
    print filename
    line = f.read().splitlines()
    print line

readLog()