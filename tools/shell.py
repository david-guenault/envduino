#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009-2011:
#    David GUENAULT, david.guenault@gmail.com 
#
# This file is part of envduino.
#
# envduino is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# envduino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with envduino.  If not, see <http://www.gnu.org/licenses/>.

import os
import cmd
import sys
import time

class Dummy:
    def add(self, o):
        pass

class EnvduinoShell(cmd.Cmd):
    prompt = "> "

    def __init__(self):
        cmd.Cmd.__init__(self)

    def emptyline(self):
        return

    def do_connect(self, line):
        '''
        Connect to an envduino module 
        Syntax: connect 
        > connect 
        '''
        line = line.strip()
        tokens = line.split(':')
        print "Connections"
        print "Connection OK"

    def do_EOF(self, line):
        return self.do_quit('')

    def do_quit(self, line):
        print "",
        return True

intro = 'Available functions:\n# connect \n# quit'

if __name__ == "__main__":
    EnvduinoShell().cmdloop(intro)
