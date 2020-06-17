#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.
import requests
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
}


class Monitor(object):
    def __init__(self, url=None, http_status=None, response_time=None, page_content=None, date_time=None):
        '''
        Monitoring data structure

        Handle the formating and fetching of the website monitoring data

        Parameters
        ----------
        url : `str`, optional
            URL of the website to monitor.
        http_status : `int`, optional
            HTTP status returned after the HTTP GET query.
        response_time : `float`, optional
            Response time to the query.
        page_content : `str`, optional
            Content of the page.
        date_time : `float. optional
            timestamp of the HTTP query
        '''
        self.url = url
        self.http_status = http_status
        self.response_time = response_time
        self.page_content = page_content
        self.date_time = date_time

    def __repr__(self):
        return 'Monitor()'

    def __str__(self):
        print("tostring", str(self.__class__) + ": " + str(self.__dict__))
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, Monitor):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.url == other.url and
                self.http_status == other.http_status and
                self.response_time == other.response_time and
                self.page_content == other.page_content and
                self.date_time == other.date_time
                )

    def decode_json(self, json):
        '''
        Parse JSON string

        Parameters
        ----------
        json : `dict`
            JSON object for Monitor

        Returns
        -------
        Monitor
            new Monitor object

        '''
        return Monitor(json["url"], json["http_status"], json["response_time"], json["page_content"], json["date_time"])

    def fetch(self):
        '''
        Fetch monitoring data from a website
        Sends an HTTP Get request to the specified URL and set the monitoring data.
        '''
        try:
            print('Processing... ', self.url)
            response = requests.get(self.url, headers=headers)
            self.http_status = response.status_code
            self.response_time = response.elapsed.total_seconds()
            self.page_content = response.text
            self.date_time = datetime.timestamp(datetime.now())

        except Exception as e:
            print('Exception occured while fetching data')
            print(str(e))
