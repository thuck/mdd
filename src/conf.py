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
import section
from section import InvalidConfiguration
#import logging


class Configuration(object):

    default = {'use_safe_mode':True,
               'strategy':'move',
               'if_exists_rename':True,
               'source':None,
               'destination':None,
               'regex':None,
               'unix_pattern_matching':None,
               'exception':None,
               'pre_move':None,
               'pos_move':None,
               'priority':1}

    def __init__(self, conf_file):
        self.config = ConfigParser.SafeConfigParser(self.default)
        self.config.read(os.path.expanduser(conf_file))

    def get_magic_directories(self):
        directories = []
        #Change the default configuration.
        if self.config.has_section('default'):
            for name, value in self.config.items('default'):
                self.config.set('DEFAULT', name, value)
            self.config.remove_section('default')

        get_value = lambda section, option:(
                    self.config.has_option(section, option) and
                    self.config.get(section, option) or
                    self.config.get('DEFAULT', option)
                    )
        get_bool = lambda section, option:(
                    self.config.has_option(section, option) and
                    self.config.getboolean(section, option) or
                    self.config.getboolean('DEFAULT', option)
                    )
        get_int = lambda section, option:(
                    self.config.has_option(section, option) and
                    self.config.getint(section, option) or
                    self.config.getint('DEFAULT', option)
                    )

        for section in self.config.sections():

            name = get_value(section, 'name')
            source = get_value(section, 'source')
            destination = get_value(section, 'destination')
            regex = get_value(section, 'regex')
            unix_pattern_matching = get_value(section, 'unix_pattern_matching')
            exception = get_value(section, 'exception')
            try:
                if_exists_rename = get_bool(section, 'if_exists_rename')
            except ValueError:
                #TODO: log this error as a configuration error
                continue
            pre_move = get_value(section, 'pre_move')
            pos_move = get_value(section, 'pos_move')
            strategy = get_value(section, 'strategy')
            try:
                priority = get_int(section, 'priority')
            except ValueError:
                #TODO: log this error as a configuration error
                continue

            try:
                directories.append(
                    section.Section(
                                name, source, destination,
                                regex, unix_pattern_matching,
                                exception, if_exists_rename,
                                pre_move, pos_move, strategy, priority
                              )
                        )
            except InvalidConfiguration:
                #Nothing todo with the exception, maybe a log, but not sure
                #Indeed where should the log be, in the place where the exception
                #is raised on where is captured? I think it should be in the
                #place that catch(check the past f catch) so here.
                continue

        return directories