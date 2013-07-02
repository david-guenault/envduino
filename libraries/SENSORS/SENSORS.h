/*
  SENSORS.cpp - Library for handling a three led SENSORS
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#ifndef SENSORS_H
#define SENSORS_H
#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif
#include "DHT.h"

#ifndef DHTPIN
    #define DHTPIN 28        // sensor data pin 
#endif
#ifndef DHTTYPE
    #define DHTTYPE DHT22    // DHT 22  (AM2302)
#endif

class SENSORS {
    public:
        SENSORS();
        ~SENSORS();
        void begin();
        void mesure();
        int temperature();
        int humidity();
        int pressure();
    private:
        DHT _dht;
        int _temperature;
        int _humidity;
        int _pressure;
};

#endif
