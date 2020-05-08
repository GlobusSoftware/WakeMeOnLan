#!/usr/bin/env python3
#
# Based on wol.py from https://github.com/bentasker/Wake-On-Lan-Python
# There were a few changes that have been made because it seems to me that it is better
#
# Copyright (C) Larchenkov Mike
#

import socket
import struct
import os
import sys
import configparser
import re


class WOL:
    """Wake On Lan Communication Class"""
    C_default_config = 'wol.ini'

    @staticmethod
    def wake(host_name, config_path=''):
        """ Switches on remote computers using WOL. """

        host_name = host_name.lower()
        # Find config file
        config_path = config_path.strip()
        if len(config_path) <= 0:
            config_path = WOL.C_default_config

        # Load configuration
        configs = WOL.load_config(config_path)
        if configs is None:
            print('Configuration file not found...')
            return -1
        if 'General' not in configs:
            print('Invalid configuration: No key "General"')
            return -2
        if 'broadcast' not in configs['General']:
            print('Invalid configuration: No option "General.broadcast"')
            return -3
        if 'Devices' not in configs:
            print('Invalid configuration: No key "Devices"')
            return -4
        if host_name not in configs['Devices']:
            msg_tmplate = 'Invalid configuration: No option "{key}"'
            print(msg_tmplate.format(key=host_name))
            return -5

        broadcast = configs['General']['broadcast']
        mac_address = configs['Devices'][host_name]

        # Check mac address format
        found = re.fullmatch(
            '^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([\s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([\s][a-f0-9]{2}){5}))$',
            mac_address)
        # We must found 1 match , or the MAC is invalid
        if found:
            # If the match is found, remove mac separator [:-\s]
            macaddress = mac_address.replace(mac_address[2], '')
        else:
            print('Incorrect MAC address format')
            return -6

        # Pad the synchronization stream.
        data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
        send_data = b''

        # Split up the hex values and pack.
        for i in range(0, len(data), 2):
            send_data = b''.join([send_data,
                                  struct.pack('B', int(data[i: i + 2], 16))])

        # Broadcast it to the LAN.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (broadcast, 7))

        print('Magic packet was sent successfully!')
        print('Host: ' + host_name)
        print('Broadcast: ' + broadcast)
        print('mac address: ' + configs['Devices'][host_name])

        return True

    @staticmethod
    def load_config(config_path=''):
        """ Read in the Configuration file to get CDN specific settings
        """
        configs = {}

        # Check config file
        config_path = config_path.strip()
        if not os.path.isfile(config_path):
            return None

        # Load configuration
        ccp = configparser.ConfigParser()
        ccp.read(config_path)
        sections = ccp.sections()

        for section in sections:
            options = ccp.options(section)

            sectkey = section
            configs[sectkey] = {}

            for option in options:
                configs[sectkey][option] = ccp.get(section, option)

        return configs


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Not enought actual parametres...')
        exit()
    if len(sys.argv) >= 3:
        WOL.wake(sys.argv[1], sys.argv[2])
    else:
        WOL.wake(sys.argv[1])
