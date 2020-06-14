#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
import json
from monitor import monitor
from kafka import KafkaConsumer


def main():
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    consumer = KafkaConsumer(
        "monitoring",
        auto_offset_reset="earliest",
        bootstrap_servers="kafka-site-monitoring-kenzo-134a.aivencloud.com:16845",
        client_id="demo-client-1",
        group_id="demo-group",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
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

    # Commit offsets so we won't get the same messages again

    consumer.commit()


if __name__ == '__main__':
    main()
