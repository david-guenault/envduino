/*
  SEMAPHORE.cpp - Library for handling a three led semaphore
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#ifndef SEMAPHORE_H
#define SEMAPHORE_H

#include <Arduino.h>

class SEMAPHORE {
    public:
        SEMAPHORE(int red,int yellow,int green);
        ~SEMAPHORE();
        void red(int state);
        void yellow(int state);
        void green(int state);
        void leds(int redstate,int yellowstate, int greenstate);
        void alarm(int state);

    private:
        int _red;
        int _yellow;
        int _green;

        int _OK;
        int _WARNING;
        int _CRITICAL;
        int _UNKNOWN;


};

#endif
