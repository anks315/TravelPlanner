import logging
import datetime


def getlogger(loggerkey, loggerlevel = logging.DEBUG):

    logger = logging.getLogger("TravelPlanner."+loggerkey)
    today = datetime.date.today().strftime("%Y-%m-%d")
    filehandler = logging.FileHandler('./' + today + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(thread)d %(filename)s %(funcName)s %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.setLevel(loggerlevel)
    return logger
