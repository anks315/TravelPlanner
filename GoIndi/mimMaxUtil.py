import dateTimeUtility


def getMinMaxValues(subParts):
    price = subParts[0]["price"]
    if subParts[0]["mode"] == "bus":
        price = price.split(",")[0]
    minPrice = price*1
    maxPrice = price*1
    minDuration = dateTimeUtility.addDurations(subParts[0]["duration"],subParts[0]["waitingTime"])
    maxDuration = dateTimeUtility.addDurations(subParts[0]["duration"],subParts[0]["waitingTime"])
    minDep = subParts[0]["departure"]
    maxDep = subParts[0]["departure"]
    minArr = subParts[0]["arrival"]
    maxArr = subParts[0]["arrival"]
    for t in range(len(subParts)):
        price = subParts[t]["price"]*1
        if subParts[t]["mode"] == "bus":
            price = price.split(",")[0]
        if price < minPrice:
            minPrice = price
        if price > maxPrice:
            maxPrice = price
        duration =  dateTimeUtility.addDurations(subParts[t]["duration"],subParts[t]["waitingTime"])
        if dateTimeUtility.compareTime(duration,minDuration)==-1:
            minDuration = duration
        if dateTimeUtility.compareTime(duration, maxDuration) == 1:
            maxDuration = duration
        dep = subParts[t]["departure"]
        if dateTimeUtility.compareTime(dep, minDep) == -1:
            minDep = dep
        if dateTimeUtility.compareTime(dep, maxDep) == 1:
            maxDep = dep
        arr = subParts[t]["arrival"]
        if dateTimeUtility.compareTime(arr, minArr) == -1:
            minArr = arr
        if dateTimeUtility.compareTime(dep, maxArr) == 1:
            maxArr = arr

    result = {}

    result["minPrice"] =minPrice
    result["maxPrice"] =maxPrice
    result["minDuration"] =minDuration
    result["maxDuration"] =maxDuration
    result["minDep"] =minDep
    result["maxDep"] =maxDep
    result["minArr"] =minArr
    result["maxArr"] =maxArr
    return result