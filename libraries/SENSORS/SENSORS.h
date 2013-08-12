/*
  SENSORS.cpp - Library for handling env SENSORS
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#if ARDUINO >= 100
    #include "Arduino.h"
#else
    #include "WProgram.h"
#endif
#include "DHT.h"
#include "BMP085.h"

class SENSORS {
    public:
        SENSORS();
        ~SENSORS();
        void begin();
        void mesure();
        int temperature();
        int humidity();
        long pressure();
    private:
        DHT _dht;
        BMP085 _bmp085;
        int _temperature;
        int _humidity;
        long _pressure;
};

