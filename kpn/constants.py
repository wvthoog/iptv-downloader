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

# Google Analytics Cookies _ga _gid _gat
CONST_COOKIES = {
    '_ga': 'GA1.2.973420811.1651405387',
    '_gid': 'GA1.2.1274582633.1651405387',
    '_gat': '1',
    'sessionId': 'ed14b435-d794-cee2-1196-75f30af9107e',
}

CONST_LOGIN_CREDENTIALS = {
    'credentialsStdAuth': {
        'username': '20000003832416',
        'password': '1149',
        'remember': 'Y',
        'deviceRegistrationData': {
            'deviceId': '014dc8ec5c997942bef19c0aec00fbba9ff1d7d29f12ee34ebed2ad2a918b2f2',
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