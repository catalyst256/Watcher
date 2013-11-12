#!/usr/bin/env python
import sys
import sqlite3 as lite
from common.entities import SSID, MonitorInterface
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
    label='Watcher - Map SSIDs',
    description='Maps SSIDs from db',
    uuids=[ 'Watcher.v2.db_2_ssid' ],
    inputs=[ ( 'Watcher', MonitorInterface ) ],
    debug=False
)
def dotransform(request, response):
    
    # Setup the sqlite database connection
    watcher_db = 'Watcher/resources/databases/watcher.db'
    con = lite.connect(watcher_db)

    ssid_list = []

    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM ssid')
        while True:
            row = cur.fetchone()
            if row == None:
                break
            if row[0] not in ssid_list:
                ssid_list.append(row[0])

    for x in ssid_list:
        e = SSID(x)
        response += e
    return response
