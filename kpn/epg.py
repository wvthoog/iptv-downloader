import json

import requests
from http import cookiejar
from .constants import CONST_BASE_HEADERS, CONST_LOGIN_CREDENTIALS

# Variables
deviceId = CONST_LOGIN_CREDENTIALS['credentialsStdAuth']['deviceRegistrationData']['deviceId']
channelId = ''
responses = []
cookies = {}
epgLive = []
vodChannels = []
vodPrograms = []

# URL's
base_url = 'https://api.prd.tv.kpn.com/101/1.2.0/A/nld/pctv/kpn'
login_url = base_url + '/USER/SESSIONS/'
live_url = base_url + '/TRAY/SEARCH/PROGRAM?from=0&to=999&filter_airingTime=now&dfilter_channels=subscription&filter_isAdult=false&filter_includeRegionalChannels=true&filter_channelIds=18,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,36,37,38,39,40,41,45,46,47,49,50,51,52,53,57,60,64,65,67,68,69,70,71,72,103,106,109,112,126,149,166,175,176,190,191,205,221,222,223,224,225,241,251,253,257,260,278,2100,2581,2586,2671,2694,2696,2698,3400&orderBy=extendedMetadata.extendedIds.orderId&sortOrder=asc'
vod_url = base_url + '/TRAY/EPG?filter_day={}&filter_channelIds=18,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,36,37,38,39,40,41,45,46,47,49,50,51,52,53,57,60,64,65,67,68,69,70,71,72,103,106,109,112,126,149,166,175,176,190,191,205,221,222,223,224,225,241,251,253,257,260,278,2100,2581,2586,2671,2694,2696,2698,3400&extendedChannelMetadata=true'
token_url = base_url + '/USER/DSHTOKEN?deviceId=' + deviceId
mpd_url = base_url + '/CONTENT/VIDEOURL/LIVE/' + channelId + '/20?deviceId=' + deviceId + '&profile=G03'

# Login and store cookies
session = requests.session()
login = session.post(url=login_url, headers=CONST_BASE_HEADERS, json=CONST_LOGIN_CREDENTIALS)
login = login.json()
cookies = session.cookies.get_dict()

#print('Cookies:', cookies)

# for key, value in cookies.items():
#     if key == 'avs6_cookie':
#         print(f'avs6_cookie: {value}')
#     if key == 'sessionId':
#         print(f'sessionId: {value}')
#     if key == 'up':
#         print(f'up: {value}')

# print(response)

# Get current live programs
def get_live_channels():
    live_channels = requests.get(url=live_url, headers=CONST_BASE_HEADERS, cookies=cookies)

    for item in live_channels.json()['resultObj']['containers']:
        epgLive.append([item['channel'].get('channelId'), item['channel'].get('channelName'),
                        item['metadata'].get('title'),
                        item['metadata'].get('airingEndTime')])
        # currentlyLive[item['channel'].get('channelId')] = {}
        # currentlyLive[item['channel'].get('channelId')]['channelName'] = item['channel'].get('channelName')
        # currentlyLive[item['channel'].get('channelId')]['title'] = item['metadata'].get('title')

    return epgLive

def search_vod(action, url=vod_url ,channel=0, day=0, program=0):
    day = str(day)
    #vod_request = requests.get(url=url.format(day), headers=CONST_BASE_HEADERS, cookies=cookies)

    def vod_search(inUrl):
        outUrl = requests.get(url=inUrl, headers=CONST_BASE_HEADERS, cookies=cookies)
        return outUrl


    # with open('vod_data2.json', 'w') as outfile:
    #     for item in vod_programs.json()['resultObj']['containers']:
    #         print(item)
    #         json.dump(item, outfile)

    if action == 'get_channels':
        channelsUrl = vod_search(url.format(day))
        for channels in channelsUrl.json()['resultObj']['containers']:
            #print([channels['metadata'].get('channelId'), channels['metadata'].get('channelName')])
            #vodChannels.append([channels.get('id'), channels['metadata'].get('channelName')])
            vodChannels.append(channels['metadata'].get('channelName'))
        return vodChannels

    elif action == 'get_programs':
        programsUrl = vod_search(url.format(day))
        for programs in programsUrl.json()['resultObj']['containers'][channel]['containers']:
            #print(programs['metadata'].get('title'))
            vodPrograms.append(programs['metadata'].get('title'))
        return vodPrograms

    elif action == 'get_program':
        detailUrl = vod_search(url.format(day))
        #print(url.format(day), day, channel, program)
        vodProgram = detailUrl.json()['resultObj']['containers'][channel]['containers'][program]['actions'][0].get('uri')
        #vodProgramdetail = vod_request.json()['resultObj']['containers'][channel]['containers'][program].get('actions')
        # with open('vod_program_detail1.json', 'w') as outfile:
        #     for item in vod_request.json()['resultObj']['containers'][channel]['containers']:
        #         print(item)
        #         json.dump(item, outfile)
        #print(vodProgram) # /CONTENT/DETAIL/PROGRAM/891146286 - werkt
        return vodProgram

    elif action == 'get_program_videourl':
        userdataUrl = vod_search(url)
        #print(url)
        vodProgramuserdata = userdataUrl.json()['resultObj']['containers'][0]['actions'][1].get('uri')
        #print(vodProgramuserdata)
        vodProgamassets = vod_search(base_url + vodProgramuserdata)
        vidId = vodProgamassets.json()['resultObj']['containers'][0].get('id')
        assetId = ''
        for assets in vodProgamassets.json()['resultObj']['containers'][0]['entitlement']['assets']:
            if assets.get('videoType') == 'SD_DASH_WV' and assets.get('programType') == 'CUTV' and assets.get('rights') == 'watch':
                assetId = assets.get('assetId')
        #print(vidId, assetId)
        # https://api.prd.tv.kpn.com/101/1.2.0/A/nld/pctv/kpn/CONTENT/VIDEOURL/PROGRAM/891345750/860562590?deviceId=c4db3b93a4c462db3e705dc1849f41060107a6a9ee1570caf630362f5d42560b&profile=G03
        vodProgramvideourl = f'{base_url}/CONTENT/VIDEOURL/PROGRAM/{vidId}/{assetId}?deviceId={deviceId}&profile=G03'
        #print(vodProgramvideourl)
        return vodProgramvideourl


def search_series():
    print('bla')


# # Get token
def get_token():
    token_request = requests.get(url=token_url, headers=CONST_BASE_HEADERS, cookies=cookies)
    tokenValue = token_request.json()['resultObj']['token']
    print(tokenValue)


# Get mpd and drm url
def get_mpd_drm_url(url):
    # print(url)
    get_mpd = requests.get(url=url, headers=CONST_BASE_HEADERS, cookies=cookies)
    get_mpd = get_mpd.json()
    print(get_mpd)
    try:
        mpd_src = get_mpd['resultObj']['src']['sources'].get('src')
        mpd_drm = get_mpd['resultObj']['src']['sources']['contentProtection']['widevine'].get('licenseAcquisitionURL')
    except KeyError:
        print('MPD and/or DRM url not found')
    # print('MPD: ', mpd_src, 'DRM: ', mpd_drm)
    return mpd_src, mpd_drm

