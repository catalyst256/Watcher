#!/usr/bin/env python
from common.entities import SSID, WirelessClient
from canari.maltego.message import Field, UIMessage
from canari.framework import configure #, superuser

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


#@superuser
@configure(
    label='Watcher - Map SSID to Phone',
    description='Maps an SSID to a wireless client',
    uuids=[ 'Watcher.v2.ssid_2_wirelessclient' ],
    inputs=[ ( 'Watcher', SSID ) ],
    debug=False
)
def dotransform(request, response):

    try:
        mac = request.fields['Watcher.cmac']
    except:
        return response + UIMessage('Sorry no associated MAC address')

    e = WirelessClient(mac)
    response += e
    return response
