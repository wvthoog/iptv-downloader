# Script to scan UPD addresses to find the media streams
# Please read the manual (run the script with -h parameter)
#
# author: Yuri Ponomarev
# Github: https://github.com/ponwork/

import datetime
import ipaddress
import json
import os
import select
import subprocess
import socket

# Variables
ip_ranges = ['224.0.250.0/24', '224.0.251.0/24', '224.0.252.0/24']
udp_timeout = 5
info_timeout = 10
channels_list = []
unnamed_channels_list = []


def get_ffprobe(address, port):
    """ To get the json data from ip:port """
    # Run the ffprobe with given IP and PORT with a given timeout to execute
    try:

        # Capture the output from ffprobe
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_programs', f'udp://@{address}:{port}'],
            capture_output=True, text=True, timeout=info_timeout)

        # Convert the STDOUT to JSON
        json_string = json.loads(str(result.stdout))

    except:
        print(f'[*] No data found for {address}:{port}')
        return 0

    # Parse the JSON "PROGRAMS" section
    for program in json_string['programs']:

        # Parse the JSON "STEAMS" section
        for stream in program['streams']:

            # Check the stream via index data
            try:

                stream['index'] != ''

                # Check the stream's channel name
                try:

                    if program['tags']['service_name'] != '':
                        return program['tags']['service_name']
                    else:
                        print(f'[!] No channel name found for {address}:{port}')
                        return 1

                except:
                    print(f'[!] No channel name found for {address}:{port}')
                    return 1

            except:

                print(f'[!] No stream found for {address}:{port}')
                return 0


def create_file():
    """ Prepare the resulting playlist file """

    # define the current directory
    currentPath = os.path.dirname(os.path.realpath(__file__))

    # Define the playlist file name
    playlistFileName = f'scan_results_range_kpn_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.m3u'
    playlistFile = os.path.join(currentPath, playlistFileName)

    # Open the playlist file and add the first line (header)
    with open(playlistFile, 'w') as file:
        file.write(f'#EXTM3U\n')

    return playlistFileName, playlistFile


def playlist_add(ip, port, name):
    """ Add the given IP and port to the playlist file"""

    # Define the full name/path to the playlist file
    global playlistFile

    # Define the given list
    global channels_list

    # Check the name variable
    if type(name) is int:
        channel_string = f'#EXTINF:2,Channel: {ip}:{port}\n'
    else:
        channel_string = f'#EXTINF:2,{name}\n'

    # Open the file
    with open(playlistFile, 'a') as file:
        # Add the channel name line
        file.write(channel_string)

        # Add the channel address
        file.write(f'udp://@{ip}:{port}\n')

    print(f'[!] Channel added to the playlist. {ip}:{port} >>> {name}')

    return 0


def ip_scanner(ip_ranges):
    def run_ffprobe(ip, portnr):
        print(f'[*] Scanning IP: {ip} on port: {portnr}')
        sock = socket_creator('0.0.0.0', str(ip), portnr)
        result = channel_checker(sock)
        if result == 0:

            print(f'[*] Found opened port {portnr} for {str(ip)}')

            # Get the data of the possible stream
            info = get_ffprobe(ip, portnr)

            if info == 0:  # No metadata found for the stream
                pass

            elif info == 1:  # Stream captured but without channel name
                playlist_add(ip, portnr, info)

            else:  # Stream captured with the channel name
                playlist_add(ip, portnr, info)

    """ Scan the given lists of IPs and ports """
    print('IP Ranges: ', ip_ranges)

    for range in ip_ranges:
        ip_range = ipaddress.IPv4Network(range).hosts()
        for ip_address in ip_range:
            ip_address = str(ip_address).split(".")
            third_octet = int(ip_address[2])
            fourth_octet = int(ip_address[3])
            if third_octet == 250:
                port_range = 6000
                custom_port = 2 * fourth_octet
                portnr = str(port_range + custom_port)
                ip_joined = '.'.join(ip_address)
                run_ffprobe(ip_joined, portnr)
            elif third_octet == 251:
                port_range = 7000
                custom_port = 2 * fourth_octet
                portnr = str(port_range + custom_port)
                ip_joined = '.'.join(ip_address)
                run_ffprobe(ip_joined, portnr)
            elif third_octet == 252:
                port_range = 8000
                custom_port = 2 * fourth_octet
                portnr = str(port_range + custom_port)
                ip_joined = '.'.join(ip_address)
                run_ffprobe(ip_joined, portnr)

    print(f'[*] Scanning for {ip_ranges} completed!')


def channel_checker(sock):
    """ Function to check the given UDP socket """
    ready = select.select([sock], [], [], udp_timeout)
    if ready[0]:
        sock.close()
        return 0
    else:
        return 1


def socket_creator(nic, address, port):
    """ Creates a sockets for a given ports """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the port that we know will receive multicast data
    sock.bind((nic, int(port)))

    # Tell the kernel that we are a multicast socket
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

    # Tell the kernel that we want to add ourselves to a multicast group
    # The address for the multicast group is the third param
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(address) + socket.inet_aton(nic))

    return sock

if __name__ == "__main__":
    playlistFileName, playlistFile = create_file()

    ip_scanner(ip_ranges)

