/*
  THRESHOLDS.cpp - Library for handling envduino thresholds
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#ifndef THRESHOLDS_H
#define THRESHOLDS_H

#include <Arduino.h>
#include <EEPROM.h>  

class THRESHOLDS {
    public:
        THRESHOLDS();
        ~THRESHOLDS();
        
        void pins(int red, int yellow, int green);

        bool set(char sensor,char threshold, int value);

        bool get(char sensor,int* result);

        bool read(char sensor);

        void write(char sensor, int warning, int critical);

        int check(char sensor,int value);

        bool strEqual(char* str1, char* str2);
        
        int thresholdPosition(char sensor);

    private:
      /*
      * 0 => temperature warning threshold
      * 1 => temperature criticial threshold
      * 2 => humidity warning threshold
      * 3 => humidity critical threshold
      * 4 => pressure warning threshold
      * 4 => pressure critical threshold
      */
      int _thresholds[6];




};

#endif
