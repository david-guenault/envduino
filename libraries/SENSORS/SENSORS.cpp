/*
  SENSORS.cpp - Library for handling environmental sensors
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#include "SENSORS.h"

SENSORS::SENSORS()
{

}

SENSORS::~SENSORS()
{

}

void SENSORS::begin(){
  _dht.begin(DHTPIN,DHTTYPE);  
}

void SENSORS::mesure(){
  _humidity = (int)_dht.readHumidity();
  _temperature = (int)_dht.readTemperature();  
}

int SENSORS::temperature()
{
  return _temperature;
}

int SENSORS::humidity()
{
  return _humidity;
}

int SENSORS::pressure()
{
  return NAN;
}

