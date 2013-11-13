#!/usr/bin/env python
from common.entities import AccessPoint, SSID
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
    label='Watcher - AP to SSID',
    description='Convert AP to SSID entity',
    uuids=[ 'Watcher.v2.ap_2_ssid' ],
    inputs=[ ( 'Watcher', AccessPoint ) ],
    debug=True
)
def dotransform(request, response):
    
    ssid = request.value

    e = SSID(ssid)
    response += e
    return response

