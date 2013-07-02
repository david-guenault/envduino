/*
  THRESHOLDS.cpp - Library for handling a three led THRESHOLDS
  Created by David GUENAULT, JUNE 27, 2013.
  Released under the AGPL License
*/
#include "Arduino.h"
#include "EEPROM.h"  
#include "THRESHOLDS.h"


THRESHOLDS::THRESHOLDS(){
  _thresholds = {-9999,-9999,-9999,-9999,-9999,-9999};    
}

THRESHOLDS::~THRESHOLDS(){}


bool THRESHOLDS::set(char sensor,char threshold, int value)
{
  /*
  * sensor (t,h,p)
  * threshold (w,c)
  * value (int threshold value)
  */
  int p1 = -1;


  char code[] = { sensor, threshold, '\0' };
  if ( strEqual(code,const_cast<char *>("tw")) ) p1 = 0;
  if ( strEqual(code,const_cast<char *>("tc")) ) p1 = 1;
  if ( strEqual(code,const_cast<char *>("hw")) ) p1 = 2;
  if ( strEqual(code,const_cast<char *>("hc")) ) p1 = 3;
  if ( strEqual(code,const_cast<char *>("pw")) ) p1 = 4;
  if ( strEqual(code,const_cast<char *>("pc")) ) p1 = 5;



  if ( p1 >= 0 ){
    _thresholds[p1] = value;
    return true;
  }else{
    return false;
  }
}

bool THRESHOLDS::get(char sensor,int* result)
{
  int p1;

  p1 = thresholdPosition(sensor);
  if ( p1 >= 0 ){
    result[0] = _thresholds[p1];
    result[1] = _thresholds[p1+1];
    return true;
  }else{
    result[0] = -9999;
    result[1] = -9999;
    return false;
  }
}

int THRESHOLDS::check(char sensor,int value)
{
  int thr[2];
  get(sensor,thr);

  if ( thr[0] != -9999 && thr[1] != -9999){
    if (value < thr[0]){
      return 0;
    }else if (value >= thr[0] && value < thr[1]){
      return 1;
    }else if (value >= thr[1]){
      return 2;
    }else{
      return 3;
    }
  }else{
    return 3;
  }
}

bool THRESHOLDS::strEqual(char* str1, char* str2)
{
  if (strcmp(str1, str2) == 0){
    return true;
  }else{
    return false;
  }
}

bool THRESHOLDS::read(char sensor)
{
  // byte 0 is a flag saying if thresholds have been writen 
  int flag = -1;
  int position = thresholdPosition(sensor);
  /*int warning = -9999;
  int critical = -9999;*/
  if (position > 0)
  {
    flag = EEPROM.read(0);
    if (flag == 999){
      /*warning = EEPROM.read(position+1);
      critical = EEPROM.read(position+2);
      set(sensor,'w',warning);
      set(sensor,'c',critical);*/
      return true;     
    }else{
      return false;
    }
  }else{
    return true;
  }
}

void THRESHOLDS::write(char sensor,int warning,int critical)
{

}

int THRESHOLDS::thresholdPosition(char sensor){
  int p1;
  if (sensor == 't'){
    return 0;
  }else if (sensor == 'h'){
    return 2;
  }else if (sensor == 'p'){
    return 4;
  }else{
    return -1;
  }  
}