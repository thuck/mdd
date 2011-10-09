#!/usr/bin/env python

"""Magic Directory Daemon

Copyright (C) 2011 Denis 'Thuck' Doria
<denisdoria@gmail.com>
"""

# -------------------------------------------------------------------------
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# -------------------------------------------------------------------------

import sys
import os
import os.path
import time
import signal
import logging
import daemon
import daemon.pidlockfile as pid
from daemon.pidlockfile import PIDFileParseError
from core import MagicDirectory
from core import MDException
from core import parse_args


def refresh_conf(signal, stack):
    global REFRESH_CONF
    REFRESH_CONF = True


def stop_daemon(signal, stack):
    global RUN
    RUN = False


if __name__ == '__main__':
    options = parse_args(sys.argv[1:])
    exit_ = 0

    log_file = os.path.expanduser(options.log)
    pid_path = os.path.expanduser(options.pid_file)
    conf_file = os.path.expanduser(options.conf)

    try:
        pid_number = pid.read_pid_from_pidfile(pid_path)

    except PIDFileParseError:
        print "Pid file doesn't contain a valid pid, solve this and try again"
        exit(1)

    if pid_number is not None:
        print "MDD is running already: %s" % (pid_number)
        exit(1)

    with daemon.DaemonContext():
        RUN = True
        REFRESH_CONF = True
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    filename=log_file,
                    level=getattr(logging, options.log_level))

        logging.info('Starting MDD')
        signal.signal(signal.SIGTERM, stop_daemon)
        signal.signal(signal.SIGUSR1, refresh_conf)
        signal.signal(signal.SIGUSR2, refresh_conf)

        pid.write_pid_to_pidfile(pid_path)

        while RUN:
            logging.debug('Starting MD')

            try:
                if REFRESH_CONF is True:
                    REFRESH_CONF = False
                    logging.debug('Reading configuration file')
                    magic_directory = MagicDirectory(conf_file, options.section)

                magic_directory.run()

            except MDException:
                exit_ = 1
                logging.debug('Stopping MD')
                break

            logging.debug('Stopping MD')

            if options.run_once is True:
                break

            time.sleep(options.interval)

    pid.remove_existing_pidfile(pid_path)
    logging.info('Stopping MDD')

    exit(exit_)
