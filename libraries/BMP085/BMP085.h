/*
  SENSORS.cpp - Library for handling env SENSORS
  Created by David GUENAULT, AUG 11, 2013.
  Based on sparkfun sample code
  Released under the AGPL License
*/
#ifndef BMP085_H
    #define BMP085_H  
    #if (ARDUINO >= 100)
        #include "Arduino.h"
    #else
        #include "WProgram.h"
    #endif
    #include "Wire.h"
    
    #ifndef BMP085_ADDRESS
        #define BMP085_ADDRESS 0x77  // I2C address of BMP085
    #endif
    #ifndef BMP085_OSS
        #define BMP085_OSS 0
    #endif
    #ifndef BMP085_PRESSURE_SEA_LEVEL
        #define BMP085_PRESSURE_SEA_LEVEL 102100
    #endif


class BMP085 {
  public:
    BMP085();
    ~BMP085();  
    short getTemperature();
    long getPressure();
    void calibration();

  private:
    // Calibration values
    int ac1;
    int ac2; 
    int ac3; 
    unsigned int ac4;
    unsigned int ac5;
    unsigned int ac6;
    int b1; 
    int b2;
    int mb;
    int mc;
    int md;

    // b5 is calculated in bmp085GetTemperature(...), this variable is also used in bmp085GetPressure(...)
    // so ...Temperature(...) must be called before ...Pressure(...).
    long b5; 

    short temperature;
    long pressure;

    // Use these for altitude conversions
    float p0;     // Pressure at sea level (Pa)
    float altitude;

    unsigned char OSS;

    char read(unsigned char address);  
    int readInt(unsigned char address);
    unsigned int readUT();
    unsigned long readUP();
};
#endif
