#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
}


class Monitor(object):
    def __init__(self, url=None, http_status=None, response_time=None, page_content=None):
        self.url = url
        self.http_status = http_status
        self.response_time = response_time
        self.page_content = page_content

    def __repr__(self):
        return 'Monitor()'

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def decode_json(self, dct):
        return Monitor(dct["url"], dct["http_status"], dct["response_time"], dct["page_content"])

    def fetch(self):
        try:
            print('Processing... ', self.url)
            response = requests.get(self.url, headers=headers)

        except Exception as e:
            print('Exception occured while fetching data')
            print(str(e))

        finally:
            self.http_status = response.status_code
            self.response_time = response.elapsed.total_seconds()
            self.page_content = response.text
