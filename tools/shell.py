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

import readline
import os
import cmd
import sys
import time
import io
import multiprocessing
from multiprocessing import Process, Queue

# default serial port values
def_port="/dev/ttyACM1"
def_baudrate="9600"

try:
    from serial import Serial
except:
    print "You need the pySerial module. Install it before using envduino shell"
    sys.exit(2)

class EnvduinoSerial(Process):

    running = True
    count = 0
    serial=None
    debug=False
    buffer=""

    def __init__(self,port="/dev/ttyACM1",baudrate=9600,timeout=1,command=None,result=None):
        multiprocessing.Process.__init__(self)

        self.port = def_port
        self.baudrate = def_baudrate
        self.qcommand = command 
        self.qresult = result

        self.connect()

    def connect(self):
        try:
            self.log("Opening serial port")
            self.serial = Serial()
            self.serial.baudrate = self.baudrate
            self.serial.port = self.port
            self.serial.timeout = 2
            self.serial.open()
            if not self.serial.isOpen():
                self.log("Unable to connect to serial port",force = True)
            else:
                self.log("Connection to serial port OK",force = True)
            self.eoc()
        except:
            self.log("Unable to connect to serial port",force = True)
            self.eoc()


    def log(self,message,force=False):
        if self.debug or force:
            self.qresult.put(message)

    def eoc(self):
        self.qresult.put("EOC")

    def run(self):
        while True:
            # always check serial available before anything
            if not self.serial.isOpen():
                self.log("Not connected to envduino module")
                self.eoc()
            else:
                # if a command appear in queue process command and bypass reading
                if not self.qcommand.empty():
                    c = self.qcommand.get()
                    self.log("Command : %s" % (c))
                    if c[0:5] == "debug":
                        if c[6:] == "on":
                            self.debug = True
                            self.serial.write("d;1\n")                                
                        elif c[6:] == "off":
                            self.debug = False
                            self.serial.write("d;0\n")
                    elif c == "close":
                        self.log("Closing port")
                        if self.serial.isOpen():
                            self.serial.close()
                        self.log("serial port closed",force=True)
                        self.eoc()
                    elif c == "open":
                        self.log("Openning port")
                        self.serial.open()
                        if self.serial.isOpen():
                            self.log("serial port opened",force=True)
                        else:
                            self.log("Failed opening serial port",force=True)
                        eoc()
                    else:
                        self.log("Writing command %s" % (c))
                        if c[-1:] != '\n':
                            c += '\n'
                        self.serial.write(c)
                        self.poll()

                else:
                    self.poll()

    def poll(self):
        # read serial buffer until getting a new line and put result in queue
        # buffer += self.serial.read(1)

        readc = self.serial.read(3)
        self.buffer += readc
        if len(self.buffer) > 0:
            if 'EOC' in self.buffer:
                # end of communication
                self.qresult.put(self.buffer)
                self.buffer=""                                
        else:
            pass


class EnvduinoShell(cmd.Cmd):
    prompt = "> "
    connect = False
    serial = None 
    port = ""
    baudrate = 0
    debug = False

    def __init__(self):
        print "Starting shell..."
        cmd.Cmd.__init__(self)
        self.qcommand = Queue()
        self.qresult = Queue()


    def emptyline(self):
        pass

    def check_port(self,port):
        '''
            check port exist
        '''

        if not os.access(port, os.R_OK):
            print ("device %s does not exist." % (port))
            return False
        else:
            return True

    def check_right(self,port):
        '''
        check if we have right on this device ...
        '''

        if os.name == "posix":
            myGroups = os.getgroups()
            devGroup = os.stat(port).st_gid

            if not devGroup in myGroups:
                print "You are not in the groups of %s. Please add your user to group %s" % (port,devGroup)
                return False
            else:
                return True
        else:
            return True

    def do_connect(self, line=""):
        '''
        Connect to an envduino module 
        Syntax: connect /dev/ttyXXX baudrate
        > connect /dev/ttyACM0 9600
        '''

        port = ""
        baudrate = 0

        line = line.strip()

        if line == "":
            # no parameter used so first try to reuse existing the try to use default
            if self.port != "" and self.baudrate > 0:
                port = self.port
                baudrate = self.baudrate
                self.qresult.put("Using last defined port and baudrate (%s,%s)" % (port, baudrate))
            else:
                port = def_port
                baudrate = def_baudrate
                self.qresult.put("Using default port and baudrate (%s,%s)" % (port, baudrate))
        else:
            # parameters provided
            try:
                (port,baudrate) = line.split(" ")
                baudrate = int(baudrate)
                self.qresult.put("Using provided port and baudrate (%s,%s)" % (port, baudrate))
            except:
                self.qresult.put("Invalid port and baudrate")
                self.port = ""
                self.baudrate = 0
                self.eoc()
                return

        # check if port exist
        if not self.check_port(port):
            self.port = ""
            self.baudrate = 0
            self.eoc()
            return

        # only on posix os, check current user can read/write on serial port
        if not self.check_right(port):
            self.port = ""
            self.baudrate = 0
            self.eoc()
            return

        # finally try to make connection
        try:
            self.serial = EnvduinoSerial(port = port, baudrate = baudrate, timeout = 2, command = self.qcommand, result = self.qresult)
            self.serial.daemon = True
            self.serial.start()
            self.port = port
            self.baudrate = baudrate
        except:        
            self.port = ""
            self.baudrate = 0
            self.log("Unable to connect to serial port")

        self.poll()

    def log(self,message,force=False):
        if self.debug or force:
            self.qresult.put(message)
    
    def eoc(self):
        self.qresult.put("EOC")

    def do_reset(self,line=""):
        '''
        reset envduino module connection
        Syntax: reset
        > reset
        '''
        self.log("Not implemented",force=True)
        self.eoc()

    def do_debug(self,line):
        '''
        Set envduino debug mode on/off
        Syntax: debug [on|off]
        > debug on
        '''
        if line == "on":
            mode = "1"
        elif line == "off":
            mode = "0"
        else:
            self.qresult.put("Invalid debug mode",force=True)
            self.eoc()            
            return

        self.do_raw("d;%s\n" % (mode))

    def do_raw(self,line=""):
        '''
        Send raw commands to envduino
        Syntax: raw data
        > raw t;t;w;20
        '''
        if not self.serial:
            self.qresult.put("Not connected")
            self.eoc()
            return
        self.qcommand.put(line)
        self.poll()


    def poll(self):
        timeout = 5
        exit = False
        t1 = time.time()  
        while not exit:
            try:
                data = self.qresult.get(timeout=timeout)
                sys.stdout.write(data.replace("EOC",""))
                if not data.replace("EOC","")[-1:] == "\n":
                    sys.stdout.write("\n")
                sys.stdout.flush()     
                if "EOC" in data:
                    exit=True
            except:
                exit = True
                print "Timeout after %d seconds waiting for data in queue" % timeout        

    def do_temperature(self,line=""):
        '''
        request temperature metric
        Syntax: temperature
        > temperature
        '''
        self.do_raw("m;t")

    def do_humidity(self,line=""):
        '''
        request humidity metric
        Syntax: humidity
        > humidity
        '''
        self.do_raw("m;h")

    def do_ping(self,line=""):
        '''
        Check if envduino module is answering requests
        Syntax: ping
        > ping
        '''
        self.do_raw("p")

    def do_led(self,line):
        '''
        Play with envduino leds
        Syntax: led name state
        > led red on
        > led red off
        '''

        try:
            (led,state) = line.split(" ")
            p = []
            s = ""
            if led == "red":
                p = ["r"]
            if led == "green":
                p = ["g"]
            if led == "yellow":
                p = ["y"]
            if led == "all":
                p = ["r","g","y"]

            if state == "on":
                s = "1"
            if state == "off":
                s = "0"

            if p != "" and s != "":
                for lc in p:
                    self.do_raw("l;%s;%s\n" % (lc,s))
            else:
                self.qresult.put("Invalid command")
                self.eoc()
        except:
            self.qresult.put("invalid led setting")
            self.eoc()

    def do_threshold(self,line):
        '''
        Set a sensor threshold 
        Syntax: threshold sensor type value
            sensor should be on of temperature, humidity, pressure
            type should be on of warning, critical
            value should be an integer
        > threshold temperature warning 25
        '''
        if line == "":
            self.do_raw("r\n");
        else:
            try:
                (sensor,type,value) = line.split(" ")
            except:
                self.qresult.put("invalid threshold definition")
                self.eoc()
                return

            if not sensor in ("temperature","humidity","pressure"):
                self.qresult.put("Invalid sensor")
                self.eoc()
                return
            else:
                if sensor == "temperature":
                    sensor = "t"
                elif sensor == "humidity":
                    sensor = "h"
                elif sensor == "pressure":
                    sensor = "p"

            if not type in ("warning","critical"):
                self.qresult.put("Invalid threshold type")
                self.eoc()
                return
            else:
                if type == "warning":
                    type = "w"
                elif type == "critical":
                    type = "c"

            if not value.isdigit():
                self.qresult.put("Invalid threshold value")
                self.eoc()
                return
            else:
                value = int(value)

            self.do_raw("t;%s;%s;%d" % (sensor,type,value))

    def do_close(self,line=""):
        '''
        Disconnect from an envduino module 
        Syntax: close
        > close
        '''
        self.log("Not implemented",force=True)
        self.eoc()

    def do_quit(self,line=""):
        '''
        Quit envduino shell
        Syntax: quit
        > quit
        '''
        # if self.ser:
        #     if self.ser.isOpen():
        #         self.do_disconnect()
        print "Exiting"
        sys.exit(0)
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
