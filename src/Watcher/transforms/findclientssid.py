#!/usr/bin/env python
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
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
    label='Watcher - Look for Probe Requests',
    description='Looks for wireless Probe Requests from clients',
    uuids=[ 'Watcher.v2.findclientprobesreqs' ],
    inputs=[ ( 'Watcher', MonitorInterface ) ],
    debug=False
)
def dotransform(request, response):

    iface = request.value
    probe_reqs = []

    try:
        pktcount = int(request.fields['Watcher.pktcount'])
    except:
        pktcount = 100

    def sniff_probes(p):
        if p.haslayer(Dot11ProbeReq):
            ssid = p[Dot11ProbeReq].info
            mac = p[Dot11].addr2
            if ssid != '':
                station = ssid, mac
                if station not in probe_reqs:
                    probe_reqs.append(station)
            else:
                pass

    sniff(iface=iface, prn=sniff_probes, count=pktcount)

    for ssid, mac in probe_reqs:
        e = SSID(ssid)
        e.cmac = mac
        e.monint = iface
        response += e
    return response
    
