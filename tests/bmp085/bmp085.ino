#include <Arduino.h>
#include <Wire.h>
#include <DHT.h>
#include <BMP085.h>
#include <SENSORS.h>
// sensor parameters
#define BMP085_OSS 0
#define BMP085_ADDRESS 0x77
#define BMP085_PRESSURE_SEA_LEVEL 102100

long pressure;
SENSORS sensors;

void setup(){
  Serial.begin(9600);  
  sensors.begin();
  pressure = 0;
}

void loop(){
  sensors.mesure();  
  pressure = sensors.pressure();
  Serial.println(pressure);
  delay(2000);
}
