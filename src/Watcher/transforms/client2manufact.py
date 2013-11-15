#!/usr/bin/env python
import urllib2, os, time
from common.entities import WirelessClient, Vendor
from canari.maltego.message import UIMessage
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
    label='Watcher - MAC Address Lookup',
    description='Tries to work out the vendor from the MAC address',
    uuids=[ 'Watcher.v2.client_2_manufacturer' ],
    inputs=[ ( 'Watcher', WirelessClient ) ],
    debug=True
)
def dotransform(request, response):

    mac_addr = request.value[:-9].upper()
    f_name = '/root/localTransforms/Watcher/src/Watcher/resources/external/maclist.txt'
    mac_list = []
    f_age = time.time() - 604800

    def download_list():
        maclist = urllib2.urlopen('http://anonsvn.wireshark.org/wireshark/trunk/manuf')
        output = open(f_name, 'w')
        output.write(maclist.read())
        output.close()

    try:
        if os.path.isfile(f_name) == False:
            download_list()
    except:
        return response + UIMessage('Sorry unable to download file, check internet connection')
    else:
        st = os.stat(f_name)
        mtime = st.st_mtime
        if mtime < f_age:
            download_list()
        else:
            pass

    f = open(f_name, 'r')
    for line in f:
        if mac_addr in line:
            x = ','.join(line.split()).split(',')
            mac_list.append(x)

    for m in mac_list:
        e = Vendor(m[1])
        response += e
    return response
