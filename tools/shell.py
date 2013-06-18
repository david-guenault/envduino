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
from serial import Serial
import io
from multiprocessing import Process, Queue, TimeoutError

class EnhancedSerial(Serial):
    def __init__(self, *args, **kwargs):
        #ensure that a reasonable timeout is set
        timeout = kwargs.get('timeout',0.1)
        if timeout < 0.01: timeout = 0.1
        kwargs['timeout'] = timeout
        Serial.__init__(self, *args, **kwargs)
        self.buf = ''
        
    def readline(self, maxsize=None, timeout=1):
        """maxsize is ignored, timeout in seconds is the max time that is way for a complete line"""
        tries = 0
        while 1:
            self.buf += self.read(512)
            pos = self.buf.find('\n')
            if pos >= 0:
                line, self.buf = self.buf[:pos+1], self.buf[pos+1:]
                return line
            tries += 1
            if tries * self.timeout > timeout:
                break
        line, self.buf = self.buf, ''
        return line

    def readlines(self, sizehint=None, timeout=1):
        """read all lines that are available. abort after timout
        when no more data arrives."""
        lines = []
        while 1:
            line = self.readline(timeout=timeout)
            if line:
                lines.append(line)
            if not line or line[-1:] != '\n':
                break
        return lines

class EnvduinoShell(cmd.Cmd):
    prompt = "> "
    ser = None;

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.do_connect("/dev/ttyACM0 9600")
        self.do_connectionState()

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
            self.ser = EnhancedSerial(dev,int(baudrate),timeout=2)
            print "Connection OK"
        except:        
            print "Unable to connect to serial port"

    def do_connectionState(self,line=""):
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

    def do_debug(self,line):
        '''
        Set envduino debug mode on/off
        Syntax: debug [on|off]
        > debug on
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
                self.ser.write("d;%s\n" % (debug)) 
                print ''.join(self.ser.readlines())                
            else:
                print "Unable to set debug mode (either because not connected or port not writable"

        return

    def do_raw(self,line=""):
        '''
        Send raw commands to envduino
        Syntax: raw data
        > raw t;t;w;20
        '''
        if self.ser.isOpen() and self.ser.writable():
            self.ser.write("%s\n" % (line)) 
            print ''.join(self.ser.readlines())                            
        else:
            print "Unable to send command to envduino"


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
            self.ser.write("p\n")
            print ''.join(self.ser.readlines())
        else:
            print "Unable to ping envduino"


    def do_threshold(self,line):
        '''
        Set a sensor threshold 
        Syntax: threshold sensor type value
            sensor should be on of temperature, humidity, pressure
            type should be on of warning, critical
            value should be an integer
        > threshold temperature warning 25
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
