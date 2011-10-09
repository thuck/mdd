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

import ConfigParser
import section as sec
from section import InvalidConfiguration
import logging


class Configuration(object):

    default = {'strategy': 'move',
               'force': True,
               'source': None,
               'destination': None,
               'regex': None,
               'unix_pattern_matching': None,
               'exception': None,
               'pre_move': None,
               'pos_move': None,
               'priority': 1}

    def __init__(self, conf_file):
        self.config = ConfigParser.SafeConfigParser(self.default)
        self.config.read(conf_file)

    def _get_value(self, section, option):
        return (self.config.has_option(section, option) and
                self.config.get(section, option) or
                self.config.get('DEFAULT', option))

    def get_magic_directories(self, section_conf):
        sections = []
        #Change the default configuration.
        if self.config.has_section('default'):
            for name, value in self.config.items('default'):
                self.config.set('DEFAULT', name, value)
            self.config.remove_section('default')

        logging.debug('Reading sections')
        for section in self.config.sections():
            name = section
            logging.debug('Reading section %s' % (name))
            if section_conf is not None and section != section_conf:
                logging.debug('Aborting section %s' % (name))
                continue
            source = self._get_value(section, 'source')
            destination = self._get_value(section, 'destination')
            regex = self._get_value(section, 'regex')
            upm = self._get_value(section, 'unix_pattern_matching')
            exception = self._get_value(section, 'exception')
            force = self._get_value(section, 'force')
            pre_move = self._get_value(section, 'pre_move')
            pos_move = self._get_value(section, 'pos_move')
            strategy = self._get_value(section, 'strategy')
            priority = self._get_value(section, 'priority')

            try:
                sections.append(
                    sec.Section(
                                name, source, destination,
                                regex, upm,
                                exception, force,
                                pre_move, pos_move, strategy, priority
                              )
                        )
            except InvalidConfiguration, error:
                logging.error(error)
                continue
            logging.debug('End reading section %s' % (name))
        logging.debug('End reading sections')

        return sections
