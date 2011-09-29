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

from optparse import OptionParser
import daemon
import daemon.pidlockfile as pid
import sys
from core import MagicDirectory
import time

RUN = True

def parse_args():
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="conf", default='~/.config/mdd/conf'
                  help="MDD configuration file, default: [~/.config/mdd/conf]")
    parser.add_option("-i", "--interval",
                  action="store", dest="interval", default=60,
                  type='int',
                  help="Change the interval between each run.")
    parser.add_option("--no-daemon",
                  action="store_true", dest="no_daemon", default=False,
                  help="Don't detach from console.")
    parser.add_option('-s', "--section",
                  action="store", dest="section",
                  help="Specify the section that should be used.")
    parser.add_option("-v", "--version",
                  action="store_true", dest="version", default=False,
                  help="Print the current version.")


    (options, args) = parser.parse_args()

    return options

if __name__ == '__main__':
    options = parse_args()

    if options.version:
        print '0.1'
        sys.exit(0)
        
    #TODO: create the pid control
        
    magic_directory = MagicDirectory(options.conf, options.section)

    if options.no_daemon:
        magic_directory.run()
    else:
        with daemon.DaemonContext():
            while RUN:
                magic_directory.run()
                time.sleep(options.interval)