/*
  thresholds.ino - test program for THRESHOLDS library
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#include <EEPROM.h>
#include <SEMAPHORE.h>
#include <THRESHOLDS.h>

#define RED 22;
#define YELLOW 24;
#define GREEN 26;

SEMAPHORE semaphore(22,24,26);
THRESHOLDS thresholds;

void setup()
{
  boolean tc;
  boolean tw;
  
  Serial.begin(9600);
  
  tw = thresholds.set('t','w',20);
  tc = thresholds.set('t','c',25);
  
}

void loop()
{
  int t[2]; 
  int result;
  thresholds.set('t','w',20);
  thresholds.set('t','c',25);  
  
  result = thresholds.check('t',19);
  semaphore.alarm(result);
  delay(1000);

  result = thresholds.check('t',21);
  semaphore.alarm(result);  
  delay(1000);

  result = thresholds.check('t',26);
  semaphore.alarm(result);  
  delay(1000);

}
