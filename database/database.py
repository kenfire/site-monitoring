#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from monitor.monitor import Monitor


class Database():
    def __init__(self, uri):
        '''
        Monitoring data structure

        Handle the formating and fetching of the website monitoring data

        Parameters
        ----------
        uri : `str`
            URI to connect to thw database.
        '''
        self.db_conn = psycopg2.connect(uri)
        self.cursor = self.db_conn.cursor(cursor_factory=RealDictCursor)

    def init_table(self):
        '''
        Initialise table
        '''
        # self.cursor.execute('DROP TABLE  monitoring;')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS monitoring (
            id serial PRIMARY KEY,
            url varchar,
            http_status int ,
            response_time float,
            page_content varchar,
            date_time timestamp
        );''')
        self.db_conn.commit()

    def store(self, monitored_site):
        '''
        Insert monitoring data

        Raises
        ------
        TypeError
            argument should be of time Monitor

        '''
        if not isinstance(monitored_site, Monitor):
            raise TypeError(
                "argument `monitored_site` must be of type Monitor"
            )
        self.cursor.execute('''INSERT INTO monitoring(url, http_status, response_time, page_content) VALUES (%s, %s,%s, %s)''',
                            (monitored_site.url, monitored_site.http_status, monitored_site.response_time, monitored_site.page_content))

        self.db_conn.commit()

    def print_all(self):
        '''
        Print all the data stored in the database
        '''
        self.cursor.execute("SELECT * FROM monitoring;")
        print(self.cursor.fetchall())

    def stop(self):
        '''
        Closes database connection
        '''
        self.cursor.close()
        self.db_conn.close()
