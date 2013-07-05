#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013:
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

from envduino_serial import *

def_port="/dev/ttyACM1"
def_baudrate="9600"

if __name__ == "__main__":
    if sys.version_info < (2, 6):
        sys.stderr.write("""\
            ===================================================
            FATAL: envduino shell require Python >= 2.6 to work
            ===================================================
        """)
        sys.exit(2)
    else:
        evd = EnduinoSimpleSerial()
        print evd.read("temperature")


