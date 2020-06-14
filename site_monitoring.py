#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
from monitor import monitor
from kafka import KafkaProducer
import json


def main():
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    _monitor = monitor.Monitor('https://duckduckgo.com')
    _monitor.fetch()

    producer = KafkaProducer(
        bootstrap_servers="kafka-site-monitoring-kenzo-134a.aivencloud.com:16845",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
    )

    message = json.dumps(_monitor.__dict__, indent=4)
    print("Sending: ", format(message))
    producer.send("monitoring", message.encode("utf-8"))

    # Force sending of all messages

    producer.flush()


if __name__ == '__main__':
    main()
