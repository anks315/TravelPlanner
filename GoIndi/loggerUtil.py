import logging
import datetime


def getLogger(loggerKey,loggerLevel):

    logger = logging.getLogger("TravelPlanner."+loggerKey)
    today = datetime.date.today().strftime("%Y-%m-%d")
    fileHandler = logging.FileHandler('./' + today + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(thread)d %(filename)s %(funcName)s %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(loggerLevel)
    return logger
