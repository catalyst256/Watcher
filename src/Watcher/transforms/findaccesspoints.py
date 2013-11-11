#!/usr/bin/env python
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import os, sys, time, thread
from common.entities import AccessPoint, MonitorInterface
from canari.framework import configure, superuser

__author__ = 'catalyst256'
__copyright__ = 'Copyright 2013, Watcher Project'
__credits__ = 'This transform is based off the airoscapy code which can be found here: http://www.thesprawl.org/projects/airoscapy/'

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
    label='Watcher - Find Access Points',
    description='Look for Wireless Beacon Frames (APs)',
    uuids=[ 'Watcher.v2.find_access_points' ],
    inputs=[ ( 'Watcher', MonitorInterface ) ],
    debug=True
)
def dotransform(request, response):

    iface = request.value
    ap = []
    
    try:
        count = int(request.fields['Watcher.pktcount'])
    except:
        count = 100

    def sniff_ap(p):

        if p.haslayer(Dot11Beacon):# or p.haslayer(Dot11ProbeResp):
            ssid = p[Dot11Elt].info
            bssid      = p[Dot11].addr3    
            channel    = int(ord(p[Dot11Elt:3].info))
            capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
            rssi = (ord(p.notdecoded[-4:-3])-256)
        
            if re.search("privacy", capability): 
                enc = 'Y'
            else:
                enc = 'N'

            entity = ssid, bssid, channel, enc
            if entity not in ap:
                ap.append(entity)

    def channel_hopper():
        loop_count = 0
        while loop_count != 100:
            channel = random.randrange(1,15)
            cmd = 'iw dev %s set channel %d' % (iface, channel)
            os.system(cmd)
            time.sleep(1)
            loop_count += 1

    # Create a channel hopping thread for the duration of the packet capture
    thread.start_new_thread(channel_hopper, ())

    sniff(iface=iface, prn=sniff_ap, count=count)

    for ssid, bssid, channel, enc in ap:
        e = AccessPoint(ssid)
        e.apbssid = bssid
        e.apchannel = channel
        e.apencryption = enc
        e.apmoninterface = iface
        response += e
    return response
