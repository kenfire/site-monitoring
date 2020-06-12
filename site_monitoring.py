#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
import requests


def main():
    if sys.version_info < (3, 0):
        print("Please use python 3 to run this program")

    fetch("https://duckduckgo.com")


def fetch(url):
    page_content = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache'
    }

    try:
        print('Processing... ', url)
        response = requests.get(url, headers=headers)

    except Exception as e:
        print('Exception occured while fetching data')
        print(str(e))

    finally:
        http_status = response.status_code
        response_time = response.elapsed.total_seconds()
        page_content = response.text

        print('Status: {', http_status, '}', 'Response time ', response_time)
        print(response_time)
        print(page_content.strip())
        return page_content


if __name__ == "__main__":
    main()
