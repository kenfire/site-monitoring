#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.
import json
import datetime
import pytest
import warnings
from monitor.monitor import Monitor
from unittest import mock, TestCase
from urllib.error import HTTPError
# This method will be used by the mock to replace requests.get


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, elapsed, text):
            self.status_code = status_code
            self.elapsed = elapsed
            self.text = text

    url = args[0]
    one_sec_in_day = 1 / 24 / 60 / 60

    if url == 'http://up.com':
        return MockResponse(200, datetime.timedelta(one_sec_in_day), "html text")
    elif url == 'http://exceotion.com':
        raise Exception


class TestMonitor(TestCase):
    monitor = Monitor()

    def setUp(self):
        self.url = "https://duckduckgo.com"
        self.http_status = 200
        self.response_time = 0.100604
        self.page_content = "content"
        self.date_time = 1592379760.808488

        self.sample = '''
        {{
            "url": "{}",
            "http_status": {},
            "response_time": {},
            "page_content": "{}",
            "date_time": {}
        }}
        '''.format(self.url, self.http_status, self.response_time, self.page_content, self.date_time)

    def test_equal(self):
        m1 = Monitor(self.url, self.http_status,
                     self.response_time, self.page_content, self.date_time)
        m2 = Monitor(self.url + "diff", self.http_status,
                     self.response_time, self.page_content, self.date_time)
        self.assertNotEqual(m1, m2)
        self.assertEqual(m1, m1)
        print(m1 == 1)
        self.assertNotEqual(m1, 1)

    def test_to_string(self):
        expected = "<class 'monitor.monitor.Monitor'>: {'url': 'https://duckduckgo.com', 'http_status': 200, 'response_time': 0.100604, 'page_content': 'content', 'date_time': 1592379760.808488}"
        actual = str(Monitor(self.url, self.http_status,
                             self.response_time, self.page_content, self.date_time))

        self.assertEqual(expected, actual)

    def test_class_representation(self):
        expected = "Monitor()"
        actual = repr(Monitor())
        self.assertEqual(expected, actual)

    def test_decode_json(self):
        expected = Monitor(self.url, self.http_status,
                           self.response_time, self.page_content, self.date_time)
        actual = self.monitor.decode_json(json.loads(self.sample))

        print("actual -", actual)
        print("expected", expected)
        self.assertEqual(expected, actual)

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):
        # Assert requests.get calls
        url = 'http://up.com'
        expected = Monitor(url, 200, 1, "html text", 1592379760.808488)
        actual = Monitor(url)
        actual.fetch()
        actual.date_time = 1592379760.808488  # setting of date_time is not part of the

        self.assertEqual(expected, actual)

        url = 'http://exceotion.com'
        expected = Monitor(url, None, None, None)

        actual = Monitor(url)
        actual.fetch()

        self.assertEqual(expected, actual)
