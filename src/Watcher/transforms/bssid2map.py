#!/usr/bin/env python
import requests, re
from common.entities import AccessPoint
from canari.maltego.entities import Image
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
    label='Watcher - BSSID to Google Map',
    description='Uses Wigle.net to try and get Map of BSSID location',
    uuids=[ 'Watcher.v2.bssid_2_googlemap' ],
    inputs=[ ( 'Watcher', AccessPoint ) ],
    debug=True
)
def dotransform(request, response):
    
    bssid = request.fields['Watcher.bssid']

    username = 'catalyst25'
    password = 'Hwyaa370'
    
    
    w_login = 'https://wigle.net/gps/gps/main/login'
    w_query = 'https://wigle.net/gps/gps/main/confirmlocquery/'
    gurl_base = 'http://maps.googleapis.com/maps/api/streetview?size=800x800&sensor=false&location='

    map_details = []
    
    def Wigle_Loc(username, password, bssid):
    # Create a session with requests to enable the use of auth cookies
        agent = requests.Session()
    
    # Login to Wigle.net using the specified creds
        agent.post(w_login, data={'credential_0': username, 'credential_1': password, 'destination': '/gps/gps/main'})
    
    # Submit query against the MAC address of the AP (confirmlocquery, netid)
        response = agent.post(url=w_query, data={'netid': bssid,'Query': 'Query'})
    # Pull the latitude and longitude from the raw response
        for s in re.finditer(r'maplat=(\S*)&maplon=(\S*)&map', response.text):
            lat = s.group(1)
            lng = s.group(2)
            gurl = gurl_base + str(lat) + ',' + str(lng)
            mapping = str(lat), str(lng), gurl, bssid, ltime
            if mapping not in map_details:
                map_details.append(mapping)
    
    Wigle_Loc(username, password, bssid)
    
    for x in map_details:
        cords = x[0], x[1]
        e = Image(cords)
        e.url = x[2]
        response += e
    return response