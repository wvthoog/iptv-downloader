CONST_BASE_DOMAIN = ''
CONST_BASE_DOMAIN_MOD = False
CONST_BASE_IP = ''

CONST_URLS = {
    'api': 'https://api.tv.kpn.com/101/1.2.0/A/nld/pctv/kpn',
    'base': 'https://tv.kpn.com',
    'image': 'https://images.tv.kpn.com'
}

CONST_BASE_HEADERS = {
    'AVSSite': 'http://www.itvonline.nl',
    'Accept': '*/*',
    'Accept-Language': 'en-NL,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://tv.kpn.com',
    'Referer': 'https://tv.kpn.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
    'X-Xsrf-Token': 'null',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

# CHANGE THESE SETTINGS (username, password, deviceid)
CONST_LOGIN_CREDENTIALS = {
    'credentialsStdAuth': {
        'username': '200000123456789',
        'password': '1234',
        'remember': 'Y',
        'deviceRegistrationData': {
            'deviceId': 'jkfsa82989asdf0asdf0asjko20380asd82931kadfhakshfkhds8',
            'accountDeviceIdType': 'DEVICEID',
            'deviceType': 'PCTV',
            'vendor': 'Chrome',
            'model': '102.0.5005.61',
            'deviceFirmVersion': 'Linux',
            'appVersion': 'unknown',
        },
    },
}

CONST_FIRST_BOOT = {
    'erotica': True,
    'minimal': True,
    'regional': True,
    'home': True
}

CONST_HAS = {
    'dutiptv': True,
    'library': False,
    'live': True,
    'onlinesearch': False,
    'profiles': False,
    'proxy': True,
    'replay': True,
    'search': True,
    'startfrombeginning': True,
    'upnext': False,
}

CONST_IMAGES = {
    'still': {
        'large': '',
        'small': '',
        'replace': '[format]'
    },
    'poster': {
        'large': '',
        'small': '',
        'replace': '[format]'
    },
    'replay': {
        'large': '',
        'small': '',
        'replace': '[format]'
    },
    'vod': {
        'large': '',
        'small': '',
        'replace': '[format]'
    },
}

CONST_LIBRARY = {}

CONST_MOD_CACHE = {}

CONST_WATCHLIST = {}

CONST_WATCHLIST_CAPABILITY = {}