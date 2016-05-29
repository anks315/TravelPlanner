import datetime
def getDateArray(date):
    dateDic = {};
    dateDic["day"] = date.split("-")[0]
    dateDic["month"] = date.split("-")[1]
    dateDic["year"] = date.split("-")[2]
    return dateDic

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
    depHr = depTime.split(":")[0]
    depMin = depTime.split(":")[1]
    durationHr = duration.split(":")[0]
    durationMin = duration.split(":")[1]

    arrMin = (depMin+durationMin)%60
    hrCarry = (depMin+durationMin)//60
    arrHr = (depHr+durationHr+hrCarry)%24
    dayCarry = (depHr+durationHr+hrCarry)//24
    if dayCarry>0:
        newDay = theday + datetime.timedelta(days=dayCarry)
        arrivalDate = theday.strftime('%d-%m-%Y')
    result = {}
    result["arrivalTime"]=str(arrHr)+":"+str(arrMin)
    result["arrivalDate"]=arrivalDate

def checkIfApplicable(arrivalTime,arrivalDate,depTime,depDate,bufferHrs):
    dateDic = getDateArray(arrivalDate)
    arrivalDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    dateDic = getDateArray(depDate)
    depDay = datetime.date(dateDic["year"], dateDic["month"], dateDic["day"])
    depHr = depTime.split(":")[0]
    depMin = depTime.split(":")[1]
    arrHr = arrivalTime.split(":")[0]
    finalArrHr = (arrHr + bufferHrs) % 24
    arrDayCarry = (arrHr + bufferHrs) // 24
    arrMin = arrivalTime.split(":")[1]
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
