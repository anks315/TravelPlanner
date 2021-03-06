
def limitResults(results, type, limit=40):

    """
    To limit no. of result in a list
    :param results:
    :param type: type of records
    :param limit: no. of records to be retained
    :return: list after removing records
    """

    if len(results[type]) > limit:
        results[type] = results[type][0:limit]

    return results


def sortOnWaitingTime(x, y):
    if greaterThan(x["waitingTime"],y["waitingTime"]):
        return 1
    elif x["waitingTime"] == y["waitingTime"]:
        return 0
    else:
        return -1


def sortonsubjourneytime(x, y):

    """
    To sort list of subparts on basis of subJourneyTime (subpart journey + waiting time)
    :param x:
    :param y:
    :return:
    """

    if greaterThan(x["subJourneyTime"],y["subJourneyTime"]):
        return 1
    elif x["subJourneyTime"] == y["subJourneyTime"]:
        return 0
    else:
        return -1


def greaterThan(t1,t2):
    """
    return True if t1 is greater than t2
    :param t1: time in HH:MM format
    :param t2: time in HH:MM format
    :return: True/False
    """
    t1Hr = int(t1.split(":")[0])
    t1Min = int(t1.split(":")[1])
    t2Hr = int(t2.split(":")[0])
    t2Min = int(t2.split(":")[1])
    if t1Hr>t2Hr:
        return True
    elif t1Hr==t2Hr:
        if t1Min>t2Min:
            return True
        else:
            return False
    else:
        return False