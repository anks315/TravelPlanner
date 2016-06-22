import dateTimeUtility


def getMinMaxValues(subparts):

    """
    To calculate min/max value for price, duration, departure and arrival time
    :param subparts: all possible sub parts of bus
    :return: min/max values for price. duration, departure and arrival time for bus journey
    """

    price = subparts[0]["price"]
    if subparts[0]["mode"] == "bus":
        price = price.split(",")[0]
    minPrice = price*1
    maxPrice = price*1
    minDuration = dateTimeUtility.addDurations(subparts[0]["duration"],subparts[0]["waitingTime"])
    maxDuration = dateTimeUtility.addDurations(subparts[0]["duration"],subparts[0]["waitingTime"])
    minDep = subparts[0]["departure"]
    maxDep = subparts[0]["departure"]
    minArr = subparts[0]["arrival"]
    maxArr = subparts[0]["arrival"]
    for t in range(len(subparts)):
        price = subparts[t]["price"]*1
        if subparts[t]["mode"] == "bus":
            price = price.split(",")[0]
        if price < minPrice:
            minPrice = price
        if price > maxPrice:
            maxPrice = price
        duration =  dateTimeUtility.addDurations(subparts[t]["duration"],subparts[t]["waitingTime"])
        if dateTimeUtility.compareTime(duration,minDuration)==-1:
            minDuration = duration
        if dateTimeUtility.compareTime(duration, maxDuration) == 1:
            maxDuration = duration
        dep = subparts[t]["departure"]
        if dateTimeUtility.compareTime(dep, minDep) == -1:
            minDep = dep
        if dateTimeUtility.compareTime(dep, maxDep) == 1:
            maxDep = dep
        arr = subparts[t]["arrival"]
        if dateTimeUtility.compareTime(arr, minArr) == -1:
            minArr = arr
        if dateTimeUtility.compareTime(dep, maxArr) == 1:
            maxArr = arr

    result = {"minPrice": minPrice, "maxPrice": maxPrice, "minDuration": minDuration, "maxDuration": maxDuration,
              "minDep": minDep, "maxDep": maxDep, "minArr": minArr, "maxArr": maxArr}

    return result


def getprice(subpart):

    """
    To get price of subpart
    :param subpart: subpart of journey, either train or bus
    :return: price of subpart
    """
    if subpart["mode"] == "bus":
        return subpart["price"].split(",")[0]
    return subpart["price"]