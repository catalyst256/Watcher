#!/usr/bin/env python
import os
import sqlite3 as lite
from common.entities import Database, MonitorInterface
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
    label='Watcher - Delete data from database',
    description='Deletes data from existing Watcher database',
    uuids=[ 'Watcher.v2.delete_db_data' ],
    inputs=[ ( 'Watcher', Database ) ],
    debug=True
)
def dotransform(request, response):

    watcher_db = 'Watcher/resources/databases/watcher.db'

    try:
        if os.path.isfile(watcher_db) == True:
            pass
    except:
        return response + UIMessage('Database doesnt exist, please run Watcher - Create Database transform')

    con = lite.connect(watcher_db)

    with con:
        cur = con.cursor()
        cur.execute('DELETE FROM ssid')
        cur.execute('DELETE FROM aplist')

    return response + UIMessage('Data deleted...!!!')
