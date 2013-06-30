/*
  SEMAPHORE.cpp - Library for handling a three led semaphore
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/

#include "SEMAPHORE.h"

SEMAPHORE semaphore(22,24,26);

void setup()
{
}

void loop()
{
  semaphore.green(1);
  delay(1000);
  semaphore.yellow(1);
  delay(1000);
  semaphore.red(1);
  delay(1000);
  semaphore.red(0);
  delay(1000);
  semaphore.yellow(0);
  delay(1000);
  semaphore.green(0);
  delay(1000);
}
