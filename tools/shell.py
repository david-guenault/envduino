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

import os
import cmd
import sys
import time
import serial
import io

class EnvduinoShell(cmd.Cmd):
    prompt = "> "
    ser = None;

    def __init__(self):
        cmd.Cmd.__init__(self)

    def emptyline(self):
        return

    def do_connect(self, line):
        '''
        Connect to an envduino module 
        Syntax: connect /dev/ttyXXX baudrate
        > connect /dev/ttyACM0 9600
        '''
        line = line.strip()
        try:
            (dev,baudrate) = line.split(" ")

            # check if user is allowed to read/write serial port
            myGroups = os.getgroups()
            devGroup = os.stat(dev).st_gid

            if not devGroup in myGroups:
                print "You are not in the groups of %s. Please add your user to group %s" % (dev,devGroup)
                return

            print "Connecting to %s with a baudrate of %s" % (dev,baudrate)
            self.ser = serial.Serial(dev,int(baudrate),timeout=1)
            self.ser.readline()
            print "Connection OK"
        except:        
            print "Unable to connect to serial port"

    def do_connectionState(self,line):
        '''
        Check if we are connected to an envduino module
        Syntax: connectionState
        > connectionState
        '''

        if not self.ser:
            print "Not connected to an envduino module"
            return

        if self.ser.isOpen():
            print "Connected to an envduino module"
        else:
            print "Not connected to an envduino module"

        return

    def do_setDebug(self,line):
        '''
        Set envduino debug mode on/off
        Syntax: setDebug [on|off]
        > setDebug on
        '''
        debug = "E"
        if line == "on":
            debug = "1"
        elif line == "off":
            debug = "0"
        else:
            print "Invalid debug mode"

        if not debug == "E":
            if self.ser.isOpen() and self.ser.writable():
                self.ser.write("d;%s" % (debug)) 
            else:
                print "Unable to set debug mode (either because not connected or port not writable"

        return


    def do_ping(self,line=""):
        '''
        Check if envduino module is answering requests
        Syntax: ping
        > ping
        '''

        if not self.ser:
            print "Not connected"
            return

        if self.ser.isOpen() and self.ser.writable():

            self.ser.write("t;t;w;20")
            time.sleep(2)
            while self.ser.inWaiting() != 0:
                print self.ser.read(1)            

        else:
            print "Unable to ping envduino"


    def do_setThreshold(self,line):
        '''
        Set a sensor threshold 
        Syntax: setThreshold sensor type value
            sensor should be on of temperature, humidity, pressure
            type should be on of warning, critical
            value should be an integer
        > setThreshold temperature warning 25
        '''
        (sensor,type,value) = line.split(" ")
        if not sensor in ("temperature","humidity","pressure"):
            print "Invalid sensor"
            return

        if not type in ("warning","critical"):
            print "Invalid threshold type"
            return

        if not value.isDigit():
            print "Invalid threshold value"
            return



    def do_disconnect(self,line=""):
        '''
        Disconnect from an envduino module 
        Syntax: disconnect
        > disconnect
        '''
        try:
            self.ser.close()
            print "Serial connection closed"
        except:
            print "Unable to close serial port"       

    def do_quit(self,line=""):
        '''
        Quit envduino shell
        Syntax: quit
        > quit
        '''
        if self.ser:
            if self.ser.isOpen():
                self.do_disconnect()
        return True

    def do_exit(self,line=""):
        '''
        Quit envduino shell
        Syntax: exit
        > exit
        '''
        return self.do_quit()



intro = """\
------------------------------------------------\n
Welcome to Envduino Shell\n
(c) David GUENAULT\n
david.guenault@gmail.com\n
Released under GNU Affero General Public License\n
http://www.gnu.org/licenses\n
------------------------------------------------\n
"""

if __name__ == "__main__":

    if sys.version_info < (2, 6):
        sys.stderr.write("""\
            ===================================================
            FATAL: envduino shell require Python >= 2.6 to work
            ===================================================
        """)
        sys.exit(2)
    else:
        EnvduinoShell().cmdloop(intro)
