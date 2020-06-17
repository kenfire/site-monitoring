#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
import json
import psycopg2
from monitor import monitor
from kafka import KafkaConsumer
from psycopg2.extras import RealDictCursor
from argparse import ArgumentParser
from database.database import Database


def main():
    # Ensure Python version
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    # Get arguments from execution
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", required=True,
                        help="Path to config file")
    parser.add_argument("-i", "--interval", required=False, default=1,
                        help="Time interval in seconds to polling data")
    args = parser.parse_args()

    # Read configuration file
    with open(args.config) as fh:
        config_file = json.load(fh)

    uri = config_file.get("database", {})["uri"]
    db = Database(uri)
    db.init_table()

    kafka_config = config_file.get("kafka", {})
    # Initialise kafka consumer
    consumer = KafkaConsumer(
        "monitoring",
        auto_offset_reset="earliest",
        bootstrap_servers=kafka_config["kafka_url"],
        client_id="demo-client-1",
        group_id="demo-group",
        security_protocol="SSL",
        ssl_cafile=kafka_config['ssl_ca_file'],
        ssl_certfile=kafka_config['ssl_access_certificate_file'],
        ssl_keyfile=kafka_config['ssl_access_key_file'],
        api_version=(0, 10)
    )

    # Call poll twice. First call will just assign partitions for our
    # consumer without actually returning anything
    for _ in range(2):
        raw_msgs = consumer.poll(timeout_ms=1000)
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                data = json.loads(msg.value.decode('utf-8'))
                print("data", data, "\n\n")
                monitored_site = monitor.Monitor().decode_json(data)

                print("Received: ", json.dumps(
                    monitored_site.__dict__, indent=4)
                )

                db.store(monitored_site)
                # Check if the data is correctory added
                db.print_all()

    # Commit offsets so we won't get the same messages again
    consumer.commit()

    # Close communication with the database
    db.stop()


if __name__ == '__main__':
    main()
