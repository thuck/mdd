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
    def __init__(self, option, value, error):
        Exception.__init__(self)
        self.option = option
        self.value = value
        self.error = error

    def __repr__(self):
        """The repr for the exception"""
        return "Option:%s Value:%s Error:%s" % (self.option, self.value,
                                                             self.error)

    def __str__(self):
        """The str for the exception"""
        return "Option:%s Value:%s" % (self.option, self.value, self.error)


class Section(object):
    def __init__(self, name, source, destination,
                       regex, unix_pattern_matching,
                       exception, force,
                       pre_move, pos_move, strategy, priority):
        self.name = name
        self.source = source
        self.destination = destination
        self.regex = regex
        self.unix_pattern_matching = unix_pattern_matching
        self.exception = exception
        self.force = force
        self.pre_move = pre_move
        self.pos_move = pos_move
        self.strategy = strategy
        self.priority = priority
        self.files = []

    @property
    def source(self):
        """A getter to source"""
        return self._source

    @source.setter
    def source(self, directory):
        """A setter to source"""
        if not os.path.isdir(directory):
            raise InvalidConfiguration('source', directory, 'is not a directory')

        elif not os.access(directory, os.R_OK):
            raise InvalidConfiguration('source', directory, 'permission denied')

        elif directory is None:
            raise InvalidConfiguration('source', directory, 'empty parameter')

        self._source = directory

    @property
    def destination(self):
        """A getter to destination"""
        return self._destination

    @destination.setter
    def destination(self, directory):
        """A setter to destination"""
        if not os.path.isdir(directory):
            raise InvalidConfiguration('source', directory, 'is not a directory')

        elif not os.access(directory, os.W_OK):
            raise InvalidConfiguration('source', directory, 'permission denied')

        elif directory is None:
            raise InvalidConfiguration('source', directory, 'empty parameter')

        self._destination = directory

    def update_transfer_files(self):
        """A getter to files"""
        all_files = os.listdir(self.source)
        #TODO: log all this flow

        if self.regex is not None:
            regex = re.compile(self.regex)

        elif self.unix_pattern_matching is not None:
            regex = re.compile(fnmatch.translate(self.unix_pattern_matching))

        else:
            raise InvalidConfiguration('pattern matching', None,
                                       'empty parameter')

        #All files that must be copy or moved, directories included
        tmp_files = [file_ for file_ in all_files if re.search(regex, file_)]

        #Remove the exceptions
        if self.exception is not None:
            exception = re.compile(self.exception)
            tmp_files = [file_ for  file_ in tmp_files
                               if not re.search(exception, file_)]
        #TODO: log all files that doesn't have permission to be moved/copied (Warning)
        #[(os.path.join(self.source, file_),
        #  os.stat(os.path.join(self.source, file_)))[-2]
        #  for file_ in tmp_files
        #  if not os.access(os.path.join(self.source, file_), os.R_OK)]

        #This will return a list with a tuple that contain a pair FILE,MODIFIED_TIME
        #This will be used to check if it's safe or note to copy a file (torrents should be a problem)
        self.files = [(os.path.join(self.source, file_),
                 os.path.getmtime(os.path.join(self.source, file_)))
                 for file_ in tmp_files
                 if os.access(os.path.join(self.source, file_), os.R_OK)]

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        if strategy in ('move', 'copy'):
            self._strategy = strategy

        else:
            #TODO: log this error
            raise InvalidConfiguration('strategy',
                                        strategy,
                                        'not a valid strategy')

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        try:
            self._priority = int(priority)

        except ValueError:
            raise InvalidConfiguration('priority',
                                        priority,
                                        'not a valid priority')
