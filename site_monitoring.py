#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
import json
import time
from monitor.monitor import Monitor
from kafka import KafkaProducer
from argparse import ArgumentParser


def main():
    # Ensure Python version
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    # Get arguments from execution
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", required=True,
                        help="Target website to monitor")
    parser.add_argument("-c", "--config", required=True,
                        help="Path to config file")
    parser.add_argument("-i", "--interval", required=False, default=1,
                        help="Time interval in seconds to polling data")
    args = parser.parse_args()

    # Read configuration file
    with open(args.config) as fh:
        config_file = json.load(fh)

    kafka_config = config_file.get("kafka", {})

    # Initialise kafka producer
    producer = KafkaProducer(
        bootstrap_servers=kafka_config["kafka_url"],
        security_protocol="SSL",
        ssl_cafile=kafka_config['ssl_ca_file'],
        ssl_certfile=kafka_config['ssl_access_certificate_file'],
        ssl_keyfile=kafka_config['ssl_access_key_file'],
    )

    while True:
        monitor = Monitor(args.target)
        monitor.fetch()

        # Format monitoring data into JSON
        message = json.dumps(monitor.__dict__, indent=4)
        print("Sending: ", format(message))
        producer.send("monitoring", message.encode("utf-8"))

        # Force sending of all messages
        producer.flush()

        zzz = float(args.interval)
        print("sleeping for {} seconds Zzz...".format(zzz))
        time.sleep(zzz)


if __name__ == '__main__':
    main()
