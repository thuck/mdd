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

#Maybe include a threads approach
#(but the concurrency in the FS could be dangerous)

import conf
import logging
import ConfigParser
from optparse import OptionParser


def parse_args(arg):
    parser = OptionParser(version="%prog 0.1")
    parser.add_option("-c", "--conf", dest="conf",
                default='~/.mdd/mdd.cfg',
                help="MDD configuration file [default: %default]")
    parser.add_option("-l", "--log", dest="log",
                default='~/.mdd/mdd.log',
                help="MDD log file [default: %default]")
    parser.add_option("--log-level", dest="log_level",
                default='ERROR',
                choices=['CRITICAL', 'DEBUG', 'ERROR',
                         'FATAL', 'INFO', 'WARNING'],
                help="Log level [defaul: %default]")
    parser.add_option("-i", "--interval",
                action="store", dest="interval", default=60,
                type='int',
                help="Change the interval between each run.")
    parser.add_option("--run-once",
                action="store_true", dest="run_once", default=False,
                help="Run once.")
    parser.add_option('-s', "--section",
                action="store", dest="section",
                help="Specify the section that should be used.")
    parser.add_option('-p', "--pid-file",
                action="store", dest="pid_file",
                default='~/.mdd/mdd.pid',
                help="Specify the section that should be used.")

    (options, args) = parser.parse_args(args=arg)

    return options


class MDException(Exception):
    pass


class MagicDirectory(object):
    def __init__(self, conf_file, section):
        try:
            self.configuration = conf.Configuration(conf_file)

        except ConfigParser.MissingSectionHeaderError, err:
            logging.error(err)
            raise MDException
        self.section = section

    def run(self):
        logging.debug('Reading sections')
        sections = self.configuration.get_magic_directories()
        logging.debug('End reading sections')
        for i in sections:
            i.update_transfer_files()
            logging.debug(i.files)
