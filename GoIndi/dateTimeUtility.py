import datetime
from dateutil import relativedelta


def getDateArray(date):

    datedic = {"day": int(date.split("-")[0]), "month": int(date.split("-")[1]), "year": int(date.split("-")[2])};
    return datedic

def getPreviousDate(date):
    dateDic = getDateArray(date)
    theday = datetime.date(dateDic["year"],dateDic["month"],dateDic["day"])
    prevday = theday - datetime.timedelta(days=1)
    return prevday.strftime('%d-%m-%Y')

def getNextDate(date):
    dateDic = getDateArray(date)
    theday = datetime.date(dateDic["year"],dateDic["month"],dateDic["day"])
    prevday = theday + datetime.timedelta(days=1)
    return prevday.strftime('%d-%m-%Y')

def calculateArrivalTimeAndDate(depDate,depTime,duration):
    arrivalDate = depDate
    dateDic = getDateArray(depDate)
    theday = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    depHr = int(depTime.split(":")[0])
    depMin = int(depTime.split(":")[1])
    durationHr = int(duration.split(":")[0])
    durationMin = int(duration.split(":")[1])

    arrMin = (depMin+durationMin)%60
    hrCarry = (depMin+durationMin)//60
    arrHr = (depHr+durationHr+hrCarry)%24
    dayCarry = (depHr+durationHr+hrCarry)//24
    if dayCarry>0:
        newDay = theday + datetime.timedelta(days=dayCarry)
        arrivalDate = newDay.strftime('%d-%m-%Y')
    result = {"arrivalTime": str(arrHr) + ":" + str(arrMin), "arrivalDate": arrivalDate}
    return result

def getWaitingTime(arrival,departure,arrivalDate,departureDate):
    dateDic = getDateArray(arrivalDate)
    arrivalDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    dateDic = getDateArray(departureDate)
    depDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    arrHr = int(arrival.split(":")[0])
    arrMin = int(arrival.split(":")[1])
    depHr = int(departure.split(":")[0])
    depMin = int(departure.split(":")[1])
    if depMin>arrMin:
        durMin = depMin-arrMin
        hrCarry = 0
    else:
        durMin = 60-(arrMin-depMin)
        hrCarry=-1

    if depDay > arrivalDay:
        depHr = depHr + 24
    durHr = (depHr - arrHr) + hrCarry
    return str(durHr)+":"+str(durMin)



def checkIfApplicable(arrivalTime,arrivalDate,depTime,depDate,minbufferhrs):
    dateDic = getDateArray(arrivalDate)
    arrivalDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    dateDic = getDateArray(depDate)
    depDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    depHr = int(depTime.split(":")[0])
    depMin = int(depTime.split(":")[1])
    arrHr = int(arrivalTime.split(":")[0])
    finalArrHr = (arrHr + minbufferhrs) % 24
    arrDayCarry = (arrHr + minbufferhrs) // 24
    arrMin = int(arrivalTime.split(":")[1])
    if arrDayCarry>0:
        arrivalDay = arrivalDay + datetime.timedelta(days=arrDayCarry)
    if depDay > arrivalDay:
        return 1
    elif depDay == arrivalDay :
        if finalArrHr<depHr:
            return 1
        elif finalArrHr == depHr:
            if arrMin<depMin:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0

def addDurations(dur1,dur2):

    """
    To add two time durations
    :param dur1: first time duration
    :param dur2: second time duration
    :return: sum of durations
    """

    dur1Hr = int(dur1.split(":")[0])
    dur1Min = int(dur1.split(":")[1])
    dur2Hr = int(dur2.split(":")[0])
    dur2Min = int(dur2.split(":")[1])
    resMin = (dur1Min + dur2Min)%60
    carry = (dur1Min + dur2Min)//60
    resHr = dur1Hr + dur2Hr + carry
    return str(resHr)+":"+str(resMin)

def compareTime(dur1,dur2):
    dur1Hr = int(dur1.split(":")[0])
    dur1Min = int(dur1.split(":")[1])
    dur2Hr = int(dur2.split(":")[0])
    dur2Min = int(dur2.split(":")[1])
    if dur1Hr>dur2Hr:
        return 1
    elif dur1Hr == dur2Hr:
        if dur1Min>dur2Min:
            return 1
        elif dur1Min<dur2Min:
            return -1
        else:
            return 0
    else:
        return -1

def gettotalduration(arrivaltime, departuretime, arrivaldate, departuredate):

    """
    To calculate duration of journey from departure to arrival
    :param arrivaltime: arrival time at destination station
    :param departuretime: departure from source station station
    :param arrivaldate: date on arrival
    :param departuredate: date on departure
    :return: duration of journey
    """

    arrivaltime = datetime.datetime.strptime(arrivaldate + ", " + arrivaltime, '%d-%m-%Y, %H:%M')
    departuretime = datetime.datetime.strptime(departuredate + ", " + departuretime, '%d-%m-%Y, %H:%M')
    diff = relativedelta.relativedelta(arrivaltime, departuretime)
    return str(diff.days * 24 + diff.hours) + ":" + str(diff.minutes)


def gettimedifference(arrivaltime, departuretime, arrivaldate, departuredate):

    """
    To calculate waiting time between 2 trains
    :param arrivaltime: arrival time on station
    :param departuretime: departure time from station
    :param arrivaldate: arrival date on station
    :param departuredate: departure date from station
    :return: time difference between departure and arrival
    """
    arrivaltime = datetime.datetime.strptime(arrivaldate + ", " + arrivaltime, '%d-%m-%Y, %H:%M')
    departuretime = datetime.datetime.strptime(departuredate + ", " + departuretime, '%d-%m-%Y, %H:%M')
    diff = relativedelta.relativedelta(departuretime, arrivaltime)
    return str(diff.days * 24 + diff.hours) + ":" + str(diff.minutes)


def isjourneypossible(arrivaltime, departuretime, arrivaldate, departuredate, minbuffer, maxbuffer):

    """
    To check whether combine journey is feasible or not. For feasible journey total difference between arrival & departure must be within min & max buffer
    :param arrivaltime: arrival at breaking station
    :param departuretime: departure from breaking station
    :param arrivaldate: arrival date on breaking station
    :param departuredate: departure date from breaking station
    :param minbuffer: min time differnece between 2 parts of journey
    :param maxbuffer: max time difference between 2 parts of journey
    :return: True if journey if feasible else False
    """

    timediff = gettimedifference(arrivaltime, departuretime, arrivaldate, departuredate)
    hourdiff = int(timediff.split(':', 1)[0])
    if minbuffer <= hourdiff <= maxbuffer:
        return True
    else:
        return False


def convertflighttime(time):
    """
    Convert flight arrival/departure time to '%H:%M' format
    :param time: flight arrival/departure time
    :return: converted time
    """

    time = str(time)
    if len(time.split(':')) == 3 :
        return datetime.datetime.strptime(time, '%H:%M:%S').time().strftime('%H:%M')
    return time