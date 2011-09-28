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

#import shutil
import os
import os.path
import re
import fnmatch
#import ConfigParser
#import logging


class InvalidConfiguration(Exception):
    def __repr__(self):
        """The repr for the exception"""
        return "Invalid Configuration"

    def __str__(self):
        """The str for the exception"""
        return "Invalid Configuration"


class Section(object):
    def __init__(self, name, source, destination,
                       regex, unix_pattern_matching,
                       exception, if_exists_rename,
                       pre_move, pos_move, strategy, priority):
        self.name = name
        self.source = source
        self.destination = destination
        self.regex = regex
        self.unix_pattern_matching = unix_pattern_matching
        self.exception = exception
        self.if_exists_rename = if_exists_rename
        self.pre_move = pre_move
        self.pos_move = pos_move
        self.strategy = strategy
        self.priority = priority

    @property
    def source(self):
        """A getter to source"""
        return self._source

    @source.setter
    def source(self, directory):
        """A setter to source"""
        if os.path.isdir(directory):
            self._source = directory

        else:
            #TODO: Create a log for error here
            raise InvalidConfiguration

    @property
    def destination(self):
        """A getter to destination"""
        return self._destination

    @destination.setter
    def destination(self, directory):
        """A setter to destination"""
        if os.path.isdir(directory):
            self._destination = directory

        else:
            #TODO: Create a log for error here
            raise InvalidConfiguration

    @property
    def files(self):
        """A getter to files"""
        all_files = os.listdir(self.source)
        #TODO: log all this flow

        if self.regex is not None:
            regex = re.compile(self.regex)

        elif self.unix_pattern_matching is not None:
            regex = re.compile(fnmatch.translate(self.unix_pattern_matching))

        else:
            #TODO: Create a log for error here
            raise InvalidConfiguration

        #All files that must be copy or moved
        tmp_files = [file_ for file_ in all_files
                           if re.search(regex, file_)
                           if os.path.isfile(file_)]

        #Remove the exceptions
        if self.exception is not None:
            exception = re.compile(self.exception)
            tmp_files = [file_ for  file_ in tmp_files
                               if not re.search(exception, file_)]

        return [(os.path.join(self.directory, file_),
                 os.stat(os.path.join(self.directory, file_)))[-2]
                 for file_ in tmp_files]

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        try:
            return getattr(shutil, strategy)

        except AttributeError:
            #TODO: log this error
            raise InvalidConfiguration