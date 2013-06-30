/*
  SEMAPHORE.cpp - Library for handling a three led semaphore
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#include "Arduino.h"
#include "SEMAPHORE.h"

SEMAPHORE::SEMAPHORE(int red,int yellow, int green)
{
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);  
  pinMode(green,OUTPUT);
  _red = red;
  _yellow = yellow;
  _green = green;

  _OK = 0;
  _WARNING = 1;
  _CRITICAL = 2;
  _UNKNOWN = 3;

}

SEMAPHORE::~SEMAPHORE(){}

void SEMAPHORE::red(int state)
{
  digitalWrite(_red, state);
}

void SEMAPHORE::yellow(int state)
{
  digitalWrite(_yellow, state);
}

void SEMAPHORE::green(int state)
{
  digitalWrite(_green, state);
}

void SEMAPHORE::leds(int redstate,int yellowstate, int greenstate)
{
 digitalWrite(_red, redstate);
 digitalWrite(_yellow, yellowstate);
 digitalWrite(_green, greenstate); 
}

void SEMAPHORE::alarm(int state)
{
  switch (state) {
    case 0:
      leds(0,0,1);
      break;
    case 1:
      leds(0,1,0);
      break;
    case 2:
      leds(1,0,0);
      break;
    case 3:
      leds(1,1,1);
    default:
      leds(0,0,0);
      break;
  }
}