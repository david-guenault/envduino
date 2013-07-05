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

class EnduinoSimpleSerial():

    buffer = ""
    debug = False

    def __init__(self,port="/dev/ttyACM1",baudrate=9600,timeout=1):

        self.port = def_port
        self.baudrate = def_baudrate

        self.connect()

    def log(self,message):
        if self.debug:
            sys.stdout.write(message)
            sys.stdout.flush

    def connect(self):
        try:
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


    def read(self,sensor="temperature"):
        self.buffer = ""

        if sensor in ("temperature","humidity","pressure"):
            if sensor == "temperature":
                s = "t"
            if sensor == "humidity":
                s = "h"
            if sensor == "pressure":
                s = "p"

            self.serial.write("m;%s\n" % s)
            exit = False
            while not exit:
                exit = self.poll()

            return self.buffer


    def poll(self):
        readc = self.serial.read(3)
        self.buffer += readc
        if len(self.buffer) > 0:
            if 'EOC' in self.buffer:
                return True
        else:
            return False



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
