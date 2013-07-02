#include <Arduino.h>
#include <EEPROM.h>
#include <DHT.h>
#include <SEMAPHORE.h>
#include <THRESHOLDS.h>
#include <SENSORS.h>

// DHTXX
//#define DHTPIN 28        // what pin we're connected to
//#define DHTTYPE DHT22    // DHT 22  (AM2302)
//DHT dht(DHTPIN, DHTTYPE);

// 2 dimensions char array used to store data read from serail
const int MAX_COLS = 5; 
const int MAX_ROWS = 4;
char data[MAX_COLS][MAX_ROWS];

// serial parameters
const int BAUDRATE = 9600;
const int MAX_MESSAGE_SIZE = 20;
char message[MAX_MESSAGE_SIZE];
int index = 0;

// command parameters
const char SEPARATOR = ';';
char EOL[] = "EOL";
char EOC[] = "EOC";
const int BUFSIZE = 255;

// flag for message read completion
boolean messageComplete = false;

// do we need to print debug messages
boolean DEBUG = false;

//PINS FOR LEDS
const int  RED = 22;
const int  YELLOW = 24;
const int  GREEN = 26;
const boolean  USELEDS = true;
SEMAPHORE semaphore(RED,YELLOW,GREEN);

// Thresholds management
THRESHOLDS thresholds;

// Sensors
SENSORS sensors;


void resetBuffer(char* buf){
  int i = 0;
  for (i = 0;i<BUFSIZE+3;i++) buf[i] = '\0';
}

void processCommand(){
  char b[BUFSIZE+3];
  char command[MAX_COLS];
  char arg1[MAX_COLS];
  char arg2[MAX_COLS];  
  char arg3[MAX_COLS];    
  int length=0;
  
  getField(0,command);
  
  if ( strcmp(command,"t") == 0){
    
    getField(1,arg1);
    getField(2,arg2);
    getField(3,arg3);    
    int ivalue = atoi(arg3);
    thresholds.set(arg1[0],arg2[0],ivalue);
    eoc();
    
  }else if ( strcmp(command,"d") == 0) {
    getField(1,arg1);
    if (strcmp(arg1,"1") == 0){
      setDebug(true);
    }else if(strcmp(arg1,"0") == 0){
      setDebug(false);
    }
    eoc();
  }else if ( strcmp(command,"w") == 0 ) {
    eoc();
  } else if ( strcmp(command, "p") == 0) {
    Serial.print("pong");
    eoc();
  }else if ( strcmp(command,"r")  == 0) {
    char b[255];
    int temperature[2];
    int pressure[2];
    int humidity[2];
    thresholds.get('t',temperature);
    thresholds.get('h',humidity);
    thresholds.get('p',pressure);
    sprintf(b, "Temperature : w=%d, c=%d | Humidity : w=%d,c=%d | Pressure : w=%d,c=%d",temperature[0],temperature[1],humidity[0],humidity[1],pressure[0],pressure[1]);
    Serial.print(b);
    eoc();
  }else if ( strcmp(command, "l")  == 0 ){
    getField(1,arg1);    
    getField(2,arg2);
    int state = atoi(arg2);
    if ( state == 0 || state == 1 ) {
      if ( strcmp(arg1, "r")  == 0 ){
        semaphore.red(state);
      }else if ( strcmp(arg1, "y")  == 0 ){
        semaphore.yellow(state);
      }else if ( strcmp(arg1, "g")  == 0 ){
        semaphore.green(state);
      }
    }
    eoc();
  }else if( strcmp(command, "m") == 0 ){
    char type[MAX_COLS];
    int mesure;

    getField(1,type);
    sensors.mesure();
    if ( type[0] == 't' ){
      mesure = sensors.temperature();
      sprintf(b,"temperature:%i",mesure);
    }else if (type[0] == 'h'){
      mesure = sensors.humidity();
      sprintf(b,"humidity:%i",mesure);
    }else{
      eoc();
      return;
    }
    int state = thresholds.check(*type,mesure);
    semaphore.alarm(state);
    Serial.print(b);
    eoc();
  }
  clearMessageBuffer();
  clearData();
}

int getField(int row, char* field){
  int length=0;
  while (data[row][length] != '\0'){
    field[length] = data[row][length];
    length++;
  }
  field[length] = '\0';
  return length;
}

/*****************************************************************
*
* UTILITY FUNCTIONS
*
*****************************************************************/

// Active / Deactivate debug mode 
boolean setDebug(boolean debug){
  DEBUG = debug;  
  return true;
}

void logln(char* dlog){
  // debug data over serial with end of line
  if(DEBUG){
    log(dlog);
    log(EOL);
  }
}

void log(char* dlog){
  // debug data over serial 
  if (DEBUG) Serial.print(dlog);  
}

void eoc(){
  // send end of communication
  Serial.print(EOC);
}

void eol(){
  // send end of line
  Serial.print(EOL);
}

/*****************************************************************
 * 
 * RELATED TO SERIAL COMMAND READING
 * 
 ******************************************************************/

void clearMessageBuffer(){
  for ( int i = 0; i<MAX_MESSAGE_SIZE; i++) message[i] = '\0' ;
  index = 0;
}

// get number of fields
int getMessageSize(){
  int i = 0;
  while( message[i] != '\0' && message[i] != '\n' && message[i] != '\r' ){
    i++;
  }
  return i;
}

// clean up existing splitted data
void clearData(){
  for ( int r = 0; r < MAX_ROWS; r++ ){
    for ( int c = 0; c < MAX_COLS; c++ ){
      data[r][c] = '\0';
    }
  }  
}

void splitMessage(){
  // ok message is complete split fields and store it 
  int msize = getMessageSize(); 
  int row = 0;
  int col = 0;
  for(int i = 0; i<msize; i++){
    if (message[i] == SEPARATOR){
      // end of field
      data[row][col] = '\0';
      row++;
      col=0;
    }
    else{
      if (message[i] != '\0'){
        data[row][col] = message[i];
        col++;
      }
    }
  }  
}

void serialEvent(){
  clearData();
  while (Serial.available() && index < MAX_MESSAGE_SIZE) {
    message[index] = (char)Serial.read();
    if (message[index] == '\n' || message[index] == '\r') {
      messageComplete = true; 
      break;
    } 
    index++;
  }    
}

/*****************************************************************
 * 
 * INIT AND MAIN LOOP
 * 
 ******************************************************************/

void setup(){
  Serial.begin(BAUDRATE);
  sensors.begin();
  pinMode(RED, OUTPUT);  
  pinMode(GREEN, OUTPUT);  
  pinMode(YELLOW, OUTPUT);    
  
  //dht.begin();
 
  
  clearData();
  clearMessageBuffer();
}
  
void loop(){
  if ( messageComplete ){
    splitMessage();
    processCommand();
    messageComplete = false; 
  }
}



