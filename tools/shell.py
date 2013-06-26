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

    def __init__(self,port="/dev/ttyACM1",baudrate=9600,timeout=1,command=None,result=None):
        multiprocessing.Process.__init__(self)  
        self.port = port
        self.baudrate = baudrate
        self.qcommand = command 
        self.qresult = result

    def log(self,message):
        if message[-1:] == "\n":
            message=messge[:-1]
        self.qresult.put(message)

    def debug(self,message):
        message = message.strip()
        if self.debug == True:
            self.log("[DEBUG] %s" % (message))


    def run(self):
        buffer=""
        try:
            self.debug("Opening serial port")
            self.serial = Serial()
            self.serial.baudrate = self.baudrate
            self.serial.port = self.port
            self.serial.timeout = 2
            self.serial.open()
            if not self.serial.isOpen():
                self.log("Unable to connect to serial port")
            else:
                self.log("Connection to serial port OK")
        except:
            self.log("Unable to connect to serial port")


        while True:
            if not self.serial:
                self.debug("No serial next try in 2 seconds")
                time.sleep(2)
                self.connect()
                pass
            else:
                # always check serial available before anything
                if not self.serial.isOpen():
                    pass
                    # self.debug("Lost serial connection trying to open again")
                    # self.serial.open()
                else:
                    # if a command appear in queue process command and bypass reading
                    if not self.qcommand.empty():
                        c = self.qcommand.get()
                        self.debug("Command : %s" % (c))

                        if c[0:5] == "debug":
                            if c[6:] == "on":
                                self.debug = True
                                self.serial.write("d;1\n")                                
                            elif c[6:] == "off":
                                self.debug = False
                                self.serial.write("d;0\n")
                        elif c == "close":
                            self.debug("Closing port")
                            if self.serial.isOpen():
                                self.serial.close()
                            print "serial port closed"
                        elif c == "open":
                            self.debug("Openning port")
                            self.serial.open()
                        else:
                            self.debug("Writing command %s" % (c))
                            if c[-1:] != '\n':
                                c += '\n'
                            self.serial.write(c)
                    else:
                        # read serial buffer until getting a new line and put result in queue
                        # buffer += self.serial.read(1)
                        buffer += self.serial.readline()
                        if len(buffer) > 0:
                            if buffer[-1:] == '\n':
                                buffer=buffer[:-1]
                                self.qresult.put(buffer)
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
        return

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

        # make sure to not connect twice ...
        try:
            self.serial.terminate()
        except:
            pass

        line = line.strip()

        if line == "":
            # no parameter used so first try to reuse existing the try to use default
            if self.port != "" and self.baudrate > 0:
                port = self.port
                baudrate = self.baudrate
                print "Using last defined port and baudrate (%s,%s)" % (port, baudrate)
            else:
                port = "/dev/ttyACM1"
                baudrate = 9600
                print "Using default port and baudrate (%s,%s)" % (port, baudrate)
        else:
            # parameters provided
            try:
                (port,baudrate) = line.split(" ")
                baudrate = int(baudrate)
                print "Using provided port and baudrate (%s,%s)" % (port, baudrate)                
            except:
                print("Invalid port and baudrate")
                self.port = ""
                self.baudrate = 0
                return

        # check if port exist
        if not self.check_port(port):
            self.port = ""
            self.baudrate = 0
            return

        # only on posix os, check current user can read/write on serial port
        if not self.check_right(port):
            self.port = ""
            self.baudrate = 0
            return

        # finally try to make connection
        try:
            self.serial = EnvduinoSerial(port = port, baudrate = baudrate, timeout = 2, command = self.qcommand, result = self.qresult)
            self.serial.daemon = True
            self.serial.start()
            self.do_debug("off")
            self.port = port
            self.baudrate = baudrate
        except:        
            self.port = ""
            self.baudrate = 0
            print "Unable to connect to serial port"


    def do_reset(self,line=""):
        '''
        reset envduino module connection
        Syntax: reset
        > reset
        '''
        try:
            self.serial.terminate()
            self.do_connect()
        except:
            pass

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
            print "Invalid debug mode"
            return

        self.do_raw("d;%s\n" % (mode))

    def do_raw(self,line=""):
        '''
        Send raw commands to envduino
        Syntax: raw data
        > raw t;t;w;20
        '''
        if not self.serial:
            print "Not connected"
            return

        if line != "":
            self.qcommand.put(line)

    def postcmd(stop,line):
        line = ""
        data = []
        print line
        print stop
        # while not line=="EOF":
        #     try:
        #         line = self.qresult.get()
        #         sys.stdout.write(line+"\n")
        #         sys.stdout.flush()
        #     except:
        #         pass

        # print '\n'.join(data)

    def do_temperature(self,line=""):
        '''
        request temperature metric
        Syntax: temperature
        > temperature
        '''
        self.do_raw("m;t")

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
                print "Invalid command"

        except:
            print("invalid led setting")
            pass

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
                print("invalid threshold definition")
                return

            if not sensor in ("temperature","humidity","pressure"):
                print "Invalid sensor"
                return
            else:
                if sensor == "temperature":
                    sensor = "t"
                elif sensor == "humidity":
                    sensor = "h"
                elif sensor == "pressure":
                    sensor = "p"

            if not type in ("warning","critical"):
                print "Invalid threshold type"
                return
            else:
                if type == "warning":
                    type = "w"
                elif type == "critical":
                    type = "c"

            if not value.isdigit():
                print "Invalid threshold value"
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
        self.do_raw("close")

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
