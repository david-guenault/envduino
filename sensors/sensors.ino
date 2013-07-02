#include <Arduino.h>
#include <DHT.h>
#include <SENSORS.h>

SENSORS sensors;

void setup(){
  sensors.begin();
  Serial.begin(9600);  
}

void loop(){
  int temperature;
  int humidity;
  char buffer[255];

  sensors.mesure();

  temperature = sensors.temperature();
  humidity = sensors.humidity();  

  sprintf(buffer,"temperature:%i | humidity:%i",temperature,humidity);
  
  Serial.println(buffer);
  
  delay(2000);
}
