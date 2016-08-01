__author__ = 'Ankit Kumar'

from GoIndi.entity import BreakingStations
import sets
from GoIndi import constants, loggerUtil, models
import TravelPlanner.startuputil

logger = loggerUtil.getlogger("BreakingCityUtil")


def getlistoftwobreakingcityset(breakingcitieslist):
    """
    To get list of those breaking cities which have 2 breaking stations
    :param breakingcitieslist: list of all possible breaking city list
    :return: list of those 2 breaking cities list
    """
    breakingcitylist = []
    for breakingcities in breakingcitieslist:
        if len(breakingcities) == 2:
            brkstations = BreakingStations()
            brkstations.first = breakingcities[0]
            brkstations.second = breakingcities[1]
            addtobreakingcitylist(brkstations, breakingcitylist)
    return breakingcitylist


def addtobreakingcitylist(breakingstations, breakingcitylist):
    """
    Add breaking stations to breakingcitylist only if already not exists
    :param breakingstations: list of breaking stations with 2 breaking cities
    """

    if len(breakingcitylist) == 0:
        breakingcitylist.append(breakingstations)

    else:
        for brkstations in breakingcitylist:
            if brkstations.first == breakingstations.first and brkstations.second == breakingstations.second:
                return
        breakingcitylist.append(breakingstations)


def getbreakingcityset(breakingcitieslist):

    """
    To get set of all breaking cities
    :param breakingcitieslist: list of breaking city sets
    :return: breaking city sets
    """
    breakingcityset = sets.Set()

    """
    this method is used to get relevant breaking cities from all the breaking cities list.
    First prefernece is given to list having only one element then so on
    :param breakingcitieslist: list of breaking cities
    :return: breaking city set
    """
    for breakingcities in breakingcitieslist:
        breakingcities = sets.Set(breakingcities)
        if len(breakingcities) == 1:
            breakingcityset.add(breakingcities.pop())
        else:
            for breakingcity in breakingcities:
                if breakingcity.upper() in constants.bigcities:
                    breakingcityset.add(breakingcity)
    return breakingcityset


def getstationsbycityname(cityname):

    """
    This method is used to get stations corrsponding to city given
    :param cityname: name of city for which all railway station are to be found
    :return: station for cityname
    """
    if cityname in TravelPlanner.startuputil.citytostationcodesmap:
        return TravelPlanner.startuputil.citytostationcodesmap[cityname]
    else:
        stationlist = models.getstationcodesbycityname(cityname, logger)
        if stationlist:
            logger.info("Added city [%s] in citytostationcodesmap with [%s] stations", cityname, stationlist)
            TravelPlanner.startuputil.citytostationcodesmap[cityname] = stationlist
        return stationlist
