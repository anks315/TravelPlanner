__author__ = 'Ankit Kumar'

import GoIndi.models
from sets import Set

trainmapping = {}
citytostationcodesmap = {}

def loadtraindata():

    """
    To load all train station on startup and create city to station map cache
    """
    trainmapping = GoIndi.models.loadtraindata()

    for code, trainstation in trainmapping.items():
        if trainstation.city in citytostationcodesmap:
            citytostationcodesmap[trainstation.city].add(code)
        else:
            citytostationcodesmap[trainstation.city] = Set([code])


def getcityfromstation(possiblecityname, logger):

    """
    To get city from possible city
    :param possiblecityname: possible city name
    :param logger: logger
    :return: city name in DB corresponding to possiblecity
    """
    for trainstation in trainmapping.values():
        stationname = str(trainstation.name)
        cityname = str(trainstation.city)
        if stationname == possiblecityname or stationname.startswith(possiblecityname+ " ") or stationname.endswith(" "+possiblecityname) or \
                        cityname == possiblecityname or cityname.startswith(possiblecityname+ " ") or cityname.endswith(" "+possiblecityname):
            return trainstation.city
        else:
            logger.warning("No Breaking city present for [%s]", possiblecityname)
            return str()

