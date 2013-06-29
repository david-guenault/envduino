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