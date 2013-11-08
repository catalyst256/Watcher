#!/usr/bin/env python
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from canari.maltego.utils import progress
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
    'dotransform'
]

@superuser
@configure(
    label='Look for Probe Requests',
    description='Looks for wireless Probe Requests from clients',
    uuids=[ 'Watcher.v2.findclientprobesreqs' ],
    inputs=[ ( 'Watcher', MonitorInterface ) ],
    debug=True
)
def dotransform(request, response):

    iface = request.value
    probe_reqs = []

    def sniff_probes(p):
        if p.haslayer(Dot11ProbeReq):
            ssid = p[Dot11ProbeReq].info
            mac = p[Dot11].addr2
            raw = str(p[RadioTap].notdecoded).replace('\t', '\00')
            raw2 = map(ord, raw)
            rssi = int(raw2[6]) - 256
            if ssid != '':
                station = ssid, mac, rssi
                if station not in probe_reqs:
                    probe_reqs.append(station)
            else:
                pass

    sniff(iface=iface, prn=sniff_probes)

    print probe_reqs



    
