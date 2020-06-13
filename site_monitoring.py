#!/usr/bin/env python3

# Copyright 2020, Kenzo Hosomi
#
# This file is under the GNU General Public License Version 3.0.
# See the file `LICENSE` for details.

import sys
from monitor import monitor


def main():
    if sys.version_info < (3, 0):
        print('Please use python 3 to run this program')

    _monitor = monitor.Monitor('https://duckduckgo.com')
    _monitor.fetch()


if __name__ == '__main__':
    main()
