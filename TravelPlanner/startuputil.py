__author__ = 'Ankit Kumar'

import GoIndi.models
from sets import Set
import concurrent.futures, re

trainmapping = {}
trainstationsmap = {}
citytostationcodesmap = {}
citytobusmap = {"HISSAR":"HISAR", "EDLABAD" : "ADILABAD", "AJAYMERU" : "AJMER", "ALLYGURH" : "ALIGARH", "PRAYAG" : "ALLAHABAD","ALAPPUZHA":"ALLEPPEY","ALWAYE" : "ALUVA", "NEW DELHI":"DELHI", "BENGALURU":"BANGALORE", "BHAGYANAGARAM":"HYDERABAD", "BEKAL" : "BEKAL(BEKAL FORT)", "BELAGAVI":"BELGAUM", "BALLARI":"BELLARY","VIJAYAPURA":"BIJAPUR", "USALAPUR" : "BILASPUR","MADRAS":"CHENNAI", "CALCUTTA":"KOLKATA", "CUDDAPAH": "KADAPA", "KARUVUR":"KARUR","QUILON":"KOLLAM", "MACHELIPATNAM": "MACHILIPATNAM", "MAYAVARAM":"MAYILADUTHURAI","GAUTAM BUDHA NAGAR":"NOIDA","NOWGONG":"NAGAON","BOMBAY":"MUMBAI","NAVI MUMBAI" : "MUMBAI", "GURUGRAM":"GURGAON","GAUHATI":"GUWAHATI","HOSAPETE":"HOSPET","HUBBALLI":"HUBLI","JUBBULPORE":"JABALPUR","JULLUNDER":"JALANDHAR","COCANADA":"KAKINADA","CONJEEVARAM":"KANCHIPURAM","CANNANORE":"KANNUR","CAWNPORE":"KANPUR","CAPE COMORIN":"KANYAKUMARI","INDUR":"NIZAMABAD","PUDUCHERRY": "PONDICHERRY","POONA":"PUNE","RAJAMAHENDRAVARAMU":"RAJAHMUNDRY","RAJAMUNDRY":"RAJAHMUNDRY","PALAI":"PALA","RUPNAGAR":"ROPAR","SAS NAGAR":"MOHALI","SAUGOR":"SAGAR","VIRATNAGARI":"SHAHDOL","SHIVAMOGGA":"SHIMOGA","SIVASAGAR":"SIBSAGAR","SURYAPUR":"SURAT","TELLICHERRY":"THALASSERY","THANA":"THANE","TIRUCHIRAPALLI" : "TIRUCHIRAPALLY","TRICHINOPOLY": "TIRUCHIRAPALLY","TINNEVELLY":"TIRUNELVELI","TRINOMALEE":"TIRUVANNAMALAI","MANGALURU":"MANGALORE","TUMAKURU":"TUMKUR","AVANTIKA":"UJJAIN","BULSAR":"VALSAD","BHELSA":"VIDISHA","VIRUDUPATTI":"VIRUDHUNAGAR","KARNAVATI":"AHMEDABAD","SHERTALLAI" : "CHERTHALA"}
citytotrainmap = {"HISSAR":"HISAR", "EDLABAD" : "ADILABAD", "AJAYMERU" : "AJMER", "ALLYGURH" : "ALIGARH", "PRAYAG" : "ALLAHABAD","ALAPPUZHA":"ALLEPPEY","ALWAYE" : "ALUVA", "DELHI":"NEW DELHI", "BAIKUNTHPUR": "BAIKUNTHPUR ROAD", "BAGWADA" : "BAGWADA (HALT)", "BAITARANI" : "BAITARANI ROAD", "BALPUR" : "BALPUR HALT", "BENGALURU":"BANGALORE", "BARCHI" : "BARCHI ROAD","BARDHANA" : "BARDHANA HALT", "BARGARH" : "BARGARH ROAD", "BARSHI" : "BARSI TOWN", "BHAGYANAGARAM":"HYDERABAD", "BEKAL" : "BEKAL FORT", "BELAGAVI":"BELGAUM", "BALLARI":"BELLARY", "BELTHARA":"BELTHARA ROAD", "BERHAMPORE":"BERHAMPORE CRT", "BHABUA" : "BHABUA ROAD","BHADRACHALAM":"BHADRACHALAM ROAD", "BHANDARA":"BHANDARA ROAD","BHATISUDA":"BHATISUDA(HALT)", "BHAVNAGAR":"BHAVNAGAR TERMINUS","BHILAI":"BHILAI PWR HS", "BHIVPURI":"BHIVPURI ROAD", "BHIWANDI":"BHIWANDI ROAD","VIJAYAPURA":"BIJAPUR","BINDKI":"BINDKI ROAD", "CHACHAURA-BINAGANJ":"CHACHAURA BNGJ","CHAMPANER":"CHAMPANER ROAD", "CHANDAULI":"CHANDAULI MJHWR", "CHANDIA":"CHANDIA ROAD", "CHANDRAKONA":"CHANDRAKONA ROAD","CHAUTH KA BARWARA":"CHAUTH KA BRWRA","MADRAS":"CHENNAI","CHIKNI":"CHIKNI ROAD", "CALCUTTA":"KOLKATA", "KADAPA":"CUDDAPAH", "ELAGANDLA":"KARIMNAGAR", "KARUVUR":"KARUR","QUILON":"KOLLAM", "CALICUT":"KOZHIKODE", "MACHILIPATNAM":"MACHELIPATNAM", "MANGALURU":"MANGALORE","MAYAVARAM":"MAYILADUTURAI", "MAYILADUTHURAI":"MAYILADUTURAI","MYSURU":"MYSORE","NOWGONG":"NAGAON","NASHIK":"NASIK","BOMBAY":"MUMBAI", "NAVI MUMBAI" : "MUMBAI", "GURUGRAM":"GURGAON","GAUHATI":"GUWAHATI","HOSAPETE":"HOSPET","CHIKMAGALUR":"CHIKKAMAGALUR","HUBBALLI":"HUBLI","JUBBULPORE":"JABALPUR","JULLUNDER":"JALANDHAR","COCANADA":"KAKINADA","CONJEEVARAM":"KANCHIPURAM","CANNANORE":"KANNUR","CAWNPORE":"KANPUR","CAPE COMORIN":"KANYAKUMARI","INDUR":"NIZAMABAD","PALGHAT":"PALAKKAD","PONDICHERRY":"PUDUCHERRY","POONA":"PUNE","RAJAMAHENDRAVARAMU":"RAJAMUNDRY", "RAJAHMUNDRY":"RAJAMUNDRY","PALAI":"PALA","ROPAR":"RUPNAGAR","MOHALI":"SAHIBZADA ASNGR","SAS NAGAR":"SAHIBZADA ASNGR","SAGAR":"SAUGOR","VIRATNAGARI":"SHAHDOL","SHIVAMOGGA":"SHIMOGA","SIVASAGAR":"SIBSAGAR TOWN","SIBSAGAR":"SIBSAGAR TOWN","SHIMLA":"SIMLA","SURYAPUR":"SURAT","TELLICHERRY":"THALASSERY","THANA":"THANE","TANJORE":"THANJAVUR","TRICHUR":"THRISSUR","TRICHINOPOLY": "TIRUCHCHIRAPPALLI", "TIRUCHIRAPALLI":"TIRUCHCHIRAPPALLI","TINNEVELLY":"TIRUNELVELI","TRINOMALEE":"TIRUVANNAMALAI","THIRUVANANTHAPURAM":"TRIVANDRUM","TUMAKURU":"TUMKUR","THOOTHUKUDI":"TUTICORIN", "OOTACAMUND":"UDAGAMANDALAM","AVANTIKA":"UJJAIN","BARODA":"VADODARA","BULSAR":"VALSAD","BANARAS":"VARANASI","BHELSA":"VIDISHA","VIRUDUPATTI":"VIRUDUNAGAR","VIRUDHUNAGAR":"VIRUDUNAGAR","ORUGALLU":"WARANGAL","CAMBAY":"KHAMBHAT","COCHIN":"KOCHI","KARNAVATI":"AHMEDABAD","CHERTHALA":"SHERTALAI","SHERTALLAI":"SHERTALAI", "VISAKHAPATNAM":"VISHAKHAPATNAM"}

# train thread pools
trainexecutor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
googleplacesexecutor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
trainfareexecutor = concurrent.futures.ThreadPoolExecutor(max_workers=100)


def loadtraindata():

    """
    To load all train station on startup and create city to station map cache
    """
    print "hiiiiiiiiiii"
    global trainmapping
    trainmapping = GoIndi.models.loadtraindata()

    for code, trainstation in trainmapping.items():
        trainstationsmap[code] = trainstation
        if trainstation.city in citytostationcodesmap:
            citytostationcodesmap[trainstation.city].add(code)
        else:
            citytostationcodesmap[trainstation.city] = Set([code])


# needs to be optimized
def getcityfromstation(possiblecityname, logger):

    """
    To get city from possible city
    :param possiblecityname: possible city name
    :param logger: logger
    :return: city name in DB corresponding to possiblecity
    """
    citynamepattern = possiblecityname
    citynamepattern = re.sub('^(SIVA|SHIVA)', '(SIVA|SHIVA)', citynamepattern)
    citynamepattern = re.sub('^(GARH|GADH)|(GARH|GADH)$', '(GARH|GADH)', citynamepattern)
    citynamepattern = re.sub('(LL|L)', '(LL|L)', citynamepattern)
    pattern = re.compile("[A-Z]*[ ]?[A-Z]*[ ]?" + re.sub('[AIEY]', '[AIEY]', citynamepattern) + "[ ]?")
    logger.debug("Pattern converted from cityname [%s] is pattern [%s]", possiblecityname, str(pattern))

    for trainstation in trainstationsmap.values():
        stationname = str(trainstation.name)
        cityname = str(trainstation.city)
        if bool(pattern.match(stationname)) or bool(pattern.match(cityname)):
            return trainstation.city

    logger.info("No Breaking city present for [%s]", possiblecityname)
    return str()


def getbuscity(cityname):
    """
    To map incoming city name to one present in bus data
    :param cityname: incoming city name
    :return: mapped bus city name present in cache or return cityname as it is present no mapping is there
    """
    if cityname.upper() in citytobusmap.keys():
        return citytobusmap[cityname.upper()].title()
    return cityname.title()


def gettraincity(cityname):
    """
    To map incoming city name to one present in train db data
    :param cityname: incoming city name
    :return: mapped train db city name present in cache or return cityname as it is present no mapping is there
    """
    if cityname.upper() in citytotrainmap.keys():
        return citytotrainmap[cityname.upper()]
    return cityname