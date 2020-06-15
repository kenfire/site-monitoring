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


def main():
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    parser = ArgumentParser()
    parser.add_argument("-c", "--config", required=True,
                        help="Path to config file")
    args = parser.parse_args()

    with open(args.config) as fh:
        config_file = json.load(fh)

    uri = config_file.get("database", {})["uri"]
    db_conn = psycopg2.connect(uri)
    c = db_conn.cursor(cursor_factory=RealDictCursor)
    c.execute('''CREATE TABLE IF NOT EXISTS monitoring (
        id serial PRIMARY KEY, 
        url varchar,
        http_status int ,
        response_time float,
        page_content varchar
    );''')

    kafka_config = config_file.get("kafka", {})
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
                monitored_site = monitor.Monitor().decode_json(data)

                print("Received: ", json.dumps(
                    monitored_site.__dict__, indent=4)
                )

                # Execute a command: this creates a new table

                c.execute("INSERT INTO monitoring(url, http_status, response_time, page_content) VALUES (%s, %s,%s, %s)",
                          (monitored_site.url, monitored_site.http_status,
                           monitored_site.response_time, monitored_site.page_content)
                          )

                c.execute("SELECT * FROM monitoring;")
                print(c.fetchone())

                db_conn.commit()

    # Commit offsets so we won't get the same messages again

    consumer.commit()

    # Close communication with the database
    c.close()
    db_conn.close()


if __name__ == '__main__':
    main()
