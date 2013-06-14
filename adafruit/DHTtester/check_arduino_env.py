#!/usr/bin/env python

import time, sys, getopt, sys, os

try:
  import pynagios
  from pynagios import * 
except:
  print "You need the pynagios module ... "
  sys.exit(2)

try:
  import serial
except:
  print "You need the pySerial module ... "
  sys.exit(2)

def usage():
  print "arduisensor [-s sensorname -d serialport -w warning threshold -c critical threshold] | -h"
  print " -s sensor name (curently humidity or temperature)"
  print " -d serial port where arduino board is connected (/dev/ttyACM1)"
  print " -w warning threshold (in percentage for humidity or celsius degre for temperature)"
  print " -c critical threshold (in percentage for humidity or celsius degre for temperature)"
  print " -h display usage"

def parseOptions():
  opts = { 
    "sensor" : None,
    "port" : None,
    "warning" : None,
    "critical" : None
  }

  try:
    opts, args = getopt.getopt(sys.argv[1:], "s:d:w:c:h", [])
  except getopt.GetoptError, err:
      print str(err)
      usage()
      sys.exit(pynagios.UNKNOWN)

  if opts.count() == 0:
    usage()
    sys.exit(pynagios.UNKNOWN)

  for o, a in opts:
    if o == "-s":
      opts["sensor"] = a
    elif o == "-d":
      opts["port"] = a
    elif o == "-c":
      opts["critical"] = a
    elif o == "-w":
      opts["warning"] = a
    elif o == "-h":
      usage()
      sys.exit(pynagios.UNKNOWN)
    else:
      print "unhandled option %s" % (o)
      sys.exit(pynagios.UNKNOWN)

  if sensor

  if sensor not in ("temperature","humidity"):
    print "Unknow sensor %s" % (sensor)
    sys.exit(pynagios.UNKNOWN)

  if warning == None or critical == None:
    print "You must provide thresholds for temperature or humidity"
    sys.exit(pynagios.UNKNOWN)

  if port == None :
    print "Invalid device"
    sys.exit(pynagios.UNKNOWN)

  return {
    "port" : port,
    "sensor" : sensor,
    "warning" : warning,
    "critical" : critical
  }

def getserial(path):
  try:
    ser = serial.Serial(path,9600)
    test = ser.readline()
    return ser
  except:
    print "There was an error connecting to serial port"
    sys.exit(pynagios.UNKNOWN)

def read(ser):
  data = ser.readline()
  p = data.split(';')
  if p[0] != "data":
    data = ser.readline()
    p = data.split(';')
  p[2] = p[2].rstrip() 
  humidity, = p[1]
  temperature = p[2] 
  return { "humidity" : humidity, "temperature":temperature }
 
if __name__ == "__main__":
  opts = parseOptions()
  ser = getserial(opts["port"])
  data = read(ser)

  print data
  
