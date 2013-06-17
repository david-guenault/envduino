#include <EEPROM.h>

// 2 dimensions char array used to store data read from serail
const int MAX_COLS = 5; 
const int MAX_ROWS = 4;
char data[MAX_COLS][MAX_ROWS];

// serial buffer and index
const int MAX_MESSAGE_SIZE = 20;
char message[MAX_MESSAGE_SIZE];
int index = 0;

// command separator
const char SEPARATOR = ';';

// flag for message read completion
boolean messageComplete = false;

// do we need to print debug messages
boolean DEBUG = 1;

/*
* 0 => temperature warning threshold
* 1 => temperature criticial threshold
* 2 => humidity warning threshold
* 3 => humidity critical threshold
* 4 => pressure warning threshold
* 4 => pressure critical threshold
*/
int thresholds[6] = {-1,-1,-1,-1,-1,-1};

/*****************************************************************
 * Command protocol
 * ~~~~~~~~~~~~~~~~
 * 
 * the command protocol allow to retrieve sensor metric, configure the envduino and save configuration
 * it only work on usb connection. 
 * 
 * Set thresholds
 * ~~~~~~~~~~~~~~  
 * 
 * thresholds are used for visual alert through leds and/or passive alerts (only ethernet)
 * 
 * t;s;l;v
 *   t => command is a threshold settings command
 *   s => sensor type 
 *     t => temperature
 *     h => humidity
 *     p => pressure
 *     e => elevation
 *   l => threshold level 
 *     w => set a warning threshold
 *     c => set a critical warning
 *   v => Threshold value
 *     if l is warning and critical not set raise a warning alert if metric >= value
 *     if l is critical and warning not set raise a critical alert if metric >= value
 *     if both warning and critical thresholds are set 
 *       raise a warning if metric >= warning threshold and metric < critical threshold
 *       raise a critical if metric >= critical threshold
 * 
 * getThresholds
 * ~~~~~~~~~~~~~
 * 
 ********************************************************************/

void processCommand(){
  
  log(" > Processing command : ");
  if (strEqual(data[0], "t")){ // process threshold command
    logln("set threshold");
    if( (strEqual(data[1], "t")) || (strEqual(data[1], "h")) || (strEqual(data[1], "p")) || (strEqual(data[1], "e")) ){ // verify sensor type
      log(" > sensor : ");
      logln(data[1]);
      if( (strEqual(data[2],"w")) || (strEqual(data[2],"c")) ){
        log(" > threshold type : ");
        logln(data[2]);
        int ivalue = atoi(data[3]);
        setThreshold(data[1][0],data[2][0],ivalue);
      }else{
        logln(" > Invalid threshold type (should be w or c)");
      }
    }else{
      logln(" > Invalid sensor");
    }
  }else if ( strEqual(data[0], "d")) {
    if( (strEqual(data[1],"0")) || (strEqual(data[1],"1")) ){
      log(" > Setting debug mode to : ");
      logln(data[1]);
      boolean debug=false;
      if( strEqual(data[1],"0") ) debug = false;
      if( strEqual(data[1],"1") ) debug = true;
      setDebug(debug);
    }else{
      log(" > Unknown debug mode :");
      logln(data[1]);
    }
  }else if ( strEqual(data[0], "w")) {
    logln("Save to eeprom");
  } else if ( strEqual(data[0], "p")) {
    Serial.println("pong");
  }else if ( strEqual(data[0], "r")) {
    logln(" > read configuration : ");
    char b[255];
    logln(" > Thresholds configuration");
    sprintf(b, " > Temperature : w=%d, c=%d | Humidity : w=%d,c=%d | Pressure : w=%d,c=%d",thresholds[0],thresholds[1],thresholds[2],thresholds[3],thresholds[4],thresholds[5]);
    logln(b);    
  }else{
    logln(" > Unknown command");
  }
  clearMessageBuffer();
  clearData();
}


/*****************************************************************
*
* UTILITY FUNCTIONS
*
*****************************************************************/

// Active / Deactivate debug mode 
boolean setDebug(boolean debug){
  DEBUG = debug;  
}
// check a sensor is present by getting data from it
boolean checkSensor(char sensor){
  return true; 
}

// set a sensor threshold
void setThreshold(char sensor, char threshold, int value){
  
  /*
  * sensor (t,h,p)
  * threshold (w,c)
  * value (int threshold value)
  */
  
  /*
  * eeprom storage model
  *  2 bytes -> warning temperature
  *  2 bytes -> critical temperature
  *
  * t(w,c) : 2 bytes (0,1) thresholds for temperature sensor
  * t(w,c) : 2 bytes (2,3) thresholds for humidity sensor
  * t(w,c) : 2 bytes (4,5) thresholds for pressure sensor
  */

  int p1 = -1;
  char code[] = { sensor, threshold, '\0' };
  
  logln(" > Saving threshold");  

  if ( strEqual(code,"tw") ) p1 = 0;
  if ( strEqual(code,"tc") ) p1 = 1;
  if ( strEqual(code,"hw") ) p1 = 2;
  if ( strEqual(code,"hc") ) p1 = 3;
  if ( strEqual(code,"pw") ) p1 = 4;
  if ( strEqual(code,"pc") ) p1 = 5;

  char b[10];
  sprintf(b,"%d",p1);
  
  log(" > code is : ");
  log(code);
  log(", position is : ");
  logln(b);
  
  if ( p1 >= 0 ){
    log(" > Set Threshold : ");
    sprintf(b,"%d",value);
    logln(b);
    thresholds[p1] = value;
    //EEPROM.write(p1,(bytye)value);
  }else{
    logln(" > Error while writing threshold value"); 
  }
  
}

// check equality of two char arrays
boolean strEqual(char* str1, char* str2){
  if (strcmp(str1, str2) == 0){
    return true;
  }else{
    return false;
  }
}

void logln(char* dlog){
  log(dlog);
  log("\n");
  
}

void log(char* dlog){
  if (DEBUG) Serial.print(dlog);  
}

int convertThresholdValue(char* svalue){
  int threshold = 0;
  int s = 0;
  while ( svalue[s] != '\0' ) s++;
  return atoi(svalue);
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
//  clearData();
//  while (Serial.available() && index < MAX_MESSAGE_SIZE) {
//    message[index] = (char)Serial.read();
//    if (message[index] == '\n' || message[index] == '\r') {
//      messageComplete = true; 
//      break;
//    } 
//    index++;
//  }    
}

/*****************************************************************
 * 
 * INIT AND MAIN LOOP
 * 
 ******************************************************************/

void setup(){
  Serial.begin(9600);
  clearData();
  clearMessageBuffer();
}

void loop(){
  Serial.print(".");
  delay(1000);
//  if ( messageComplete ){
//    log(" > Message Complete : ");
//    logln(message);
//    // you've got a message !
//    splitMessage();
//    processCommand();
//    messageComplete = false; 
//  }
}



