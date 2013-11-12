#!/usr/bin/env python
import os, sys
import sqlite3 as lite
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from canari.maltego.utils import debug
from canari.maltego.message import UIMessage
from common.entities import SSID, MonitorInterface
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
    'dotransform',
    'onterminate'
]

@superuser
@configure(
    label='Watcher - Sniff Wireless Stuff',
    description='Looks for wireless traffic',
    uuids=[ 'Watcher.v2.findclientprobesreqs' ],
    inputs=[ ( 'Watcher', MonitorInterface ) ],
    debug=True
)
def dotransform(request, response):

    iface = request.value
    
    ap_list = []
    c_list = []

    # Setup the sqlite database connection
    watcher_db = 'Watcher/resources/databases/watcher.db'
    con = lite.connect(watcher_db)

    # Look for probe requests and write them to the sqlite table
    def sniff_probes(p):
        if p.haslayer(Dot11ProbeReq):
            ssid = p[Dot11ProbeReq].info
            mac = p[Dot11].addr2
            if ssid != '':
                station = ssid, mac, iface
                if station not in c_list:
                    with con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO ssid VALUES(?, ?, ?)", station)
                        c_list.append(station)
                else:
                    pass
            else:       
                pass

        if p.haslayer(Dot11Beacon):
            ssid = p[Dot11Elt].info
            bssid = p[Dot11].addr3
            channel = int(ord(p[Dot11Elt:3].info))
            capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
            rssi = (ord(p.notdecoded[-4:-3])-256)

            if re.search("privacy", capability): 
                enc = 'Y'
            else:
                enc = 'N'

            entity = ssid, bssid, channel, enc, iface
            if entity not in ap_list:
                with con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO aplist VALUES(?, ?, ?, ?, ?)", entity)
                    ap_list.append(entity)
            else:
                pass

    sniff(iface=iface, prn=sniff_probes)

    return response + UIMessage('Scan iteration complete')

def onterminate():
    debug('Caught signal....exiting..')
    exit(0)