import kpn.constants
from kpn import epg
from datetime import datetime, date, timedelta
from urllib.parse import urlparse
from widevine_keys.getPSSH import get_pssh
from widevine_keys.l3 import WV_Function
from simple_term_menu import TerminalMenu
from XstreamDL.XstreamDL_CLI import xstream

# Variables
channelName = ''
programName = ''
selectedDate = ''

def entry_menu():
    modes = ['Live', 'VOD', 'Movies', 'Series', 'Sports']

    terminal_menu = TerminalMenu(modes, title='Select category')
    menu_entry_index = terminal_menu.show()

    if modes[menu_entry_index] == 'Live':
        currentlyLive = epg.get_live_channels()
        live_menu(currentlyLive)
    elif modes[menu_entry_index] == 'VOD':
        vod_menu('get_channels')
    elif modes[menu_entry_index] == 'Movies':
        print('Movies is not implemented yet')
    elif modes[menu_entry_index] == 'Series':
        print('Series is not implemented yet')
    elif modes[menu_entry_index] == 'Sports':
        print('Sports is not implemented yet')


def live_menu(currentlyLive):
    headers = ("Channel", "Title")

    # print(currentlyLive)
    max_length_column1 = max(len(val[1]) for val in currentlyLive)

    if max_length_column1 < len(headers[0]):
        max_length_column1 = len(headers[0])

    column_separator = "  "
    title = "  " + f"{{:{max_length_column1}s}}".format(headers[0]) + column_separator + headers[1]
    channel_info = [
        (chanInfo[0], chanInfo[3]) for chanInfo in currentlyLive
    ]
    # print(channel_info)
    menu_entries = [
        f"{{col1:{max_length_column1}s}}{{sep}}{{col2}}".format(col1=val[1], sep=column_separator, col2=val[2])
        for val in currentlyLive
    ]

    terminal_menu = TerminalMenu(menu_entries, title=title)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {'  '.join(menu_entries[menu_entry_index].split())} at index {channel_info[menu_entry_index][0]}!")

    mpd_url = epg.base_url + '/CONTENT/VIDEOURL/LIVE/' + str(channel_info[menu_entry_index][0]) + '/20?deviceId=' + epg.deviceId + '&profile=G03'
    # print(epg.get_mpd_drm_url(mpd_url))
    mpd, drm = epg.get_mpd_drm_url(mpd_url)
    key = widevine(mpd, drm)
    xstream_download(mpd, key, mode='live', endtime=channel_info[menu_entry_index][1])


def vod_menu(action, day=0, channel=0, program=0):
    if action == 'get_channels':
        #print(epg.search_vod('get_channels'))
        menu_entries = epg.search_vod('get_channels')
        title = 'Channels'
        terminal_menu = TerminalMenu(menu_entries, title=title)
        menu_entry_index = terminal_menu.show()
        #print(f"You have selected {menu_entries[menu_entry_index]} at index {menu_entry_index}!")
        global channelName
        channelName = menu_entries[menu_entry_index]
        vod_menu('select_day', channel=menu_entry_index)

    elif action == 'select_day':
        channel = channel
        past7days = []

        today = date.today()
        for dates in range(7 + 1):
            day = today - timedelta(days=dates)
            iso = day.isoformat()
            #print(f'{dates} days ago: {iso}')
            past7days.append(iso)

        title = 'Date'
        terminal_menu = TerminalMenu(past7days, title=title)
        menu_entry_index = terminal_menu.show()
        #print(f"You have selected {past7days[menu_entry_index]} at index {menu_entry_index}!")
        global selectedDate
        selectedDate = past7days[menu_entry_index]
        vod_menu('get_programs', day=menu_entry_index, channel=channel)

    elif action == 'get_programs':
        day, channel = day, channel
        menu_entries = epg.search_vod('get_programs', channel=channel)
        title = 'Programs'
        terminal_menu = TerminalMenu(menu_entries, title=title)
        menu_entry_index = terminal_menu.show()
        #print(f"You have selected {menu_entries[menu_entry_index]} at index {menu_entry_index}!")
        global programName
        programName = menu_entries[menu_entry_index]
        vod_menu('get_program_details', day=day, channel=channel, program=menu_entry_index)

    elif action == 'get_program_details':
        day, channel, program = -abs(day), channel, program
        #print(day, channel, program)
        program_url = epg.search_vod('get_program', channel=channel, day=day, program=program)
        ## print(detail_url, channel, program) = /CONTENT/DETAIL/PROGRAM/891231243 9 4
        video_url = epg.search_vod('get_program_videourl', url=epg.base_url + program_url)
        #print(video_url)
        mpd, drm = epg.get_mpd_drm_url(video_url)
        #print(mpd, drm)
        fileName = f'{channelName.replace(" ","_")}-{programName.replace(" ", "_")}-{selectedDate}'
        print(fileName)
        key = widevine(mpd, drm)
        xstream_download(mpd, key, mode='vod', name=fileName)



def widevine(mpd_url, drm_url):
    pssh = get_pssh(mpd_url)
    params = urlparse(drm_url).query

    # print(f'{chr(10)}PSSH obtained.\n{pssh}')

    correct, keys = WV_Function(pssh, drm_url, params=params)

    for key in keys:
        print(f'KID:KEY found: {key}')
    return key


def xstream_download(mpd_url, key, mode='', endtime=0, name=''):
    args = xstream.main()

    args.URI = [mpd_url]
    args.key = key
    args.merge = True
    args.merge_files = []
    #args.headers = kpn.constants.CONST_BASE_HEADERS
    args.name = name
    #args.log_level = 'DEBUG'

    if mode == 'live':
        duration = str(timedelta(seconds=((endtime / 1000 + 5 * 60) - round(datetime.now().timestamp()))))
        #print(duration)

        args.best_quality = True
        args.live = True
        args.live_duration = duration

    if mode == 'vod':
        #args.resolution = '720'
        args.best_quality = True

    '''
    --name NAME           specific stream base name
    --save-dir SAVE_DIR   set save dir for Stream
    --headers HEADERS     read headers from headers.json, you can also use
    --log-level {DEBUG,INFO,WARNING,ERROR}

    '''

    print(args)

    xstream.command_handler(args)
    xstream.daemon = xstream.Daemon(args)
    xstream.daemon.daemon()

if __name__ == "__main__":
    entry_menu()
