#include "DHT.h"
#include <stdio.h>

// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is (PWM port)
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

#define DHTPIN 2         // what pin we're connected to
#define DHTTYPE DHT22    // DHT 22  (AM2302)
//#define DHTTYPE DHT11  // DHT 11 
//#define DHlTTYPE DHT21 // DHT 21 (AM2301)

//STATUS LEDS
#define RED 22
#define YELLOW 24
#define GREEN 26

DHT dht(DHTPIN, DHTTYPE);

// var used for reading usb/serial commands
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int commaPosition = 0;

//thresholds for visual display
int warningH = 0;
int criticalH = 0;
int warningT = 0;
int criticalT = 0;
int useHThresholds = 0;
int useTThresholds = 0;

int useLeds = 1; // use visual status display ... or not

// code

void setup() {
  
  //configure pins for led output
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
  
  // light on all of the leds
  setleds(1,1,1);
  
  delay(2000);
  
  Serial.begin(9600); 
  dht.begin();

  // light on only green led
  setleds(0,0,1);  
  
}

// set leds on or off in one line
// values are 0 = off, 1 = on, 2 = unchanged
void setleds(int red, int yellow, int green){
  if ( useLeds == 1 ){
    if (red == 0 || red == 1) digitalWrite(RED, red);
    if (yellow == 0 || yellow == 1) digitalWrite(YELLOW, yellow);
    if (green == 0 || green == 1) digitalWrite(GREEN, green);
  }else{
      digitalWrite(RED, LOW);
      digitalWrite(YELLOW, LOW);    
      digitalWrite(GREEN, LOW);          
  }
}

// display status via led
// curently only put the defined led on and off for all others
void setstatus(int status){
  setleds(0,0,0);
  if( useLeds == 1 ) digitalWrite(status, HIGH);
}

void setLedsDisplay(String message){
      char cvalue[1] = {message.charAt(2)};
      useLeds = atoi(cvalue);
      if(useLeds == 0) setleds(0,0,0);
}

void serialEvent() {
  // visually display incoming serial data
  setleds(2,1,2);
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n'){
      inputString.replace("\n","");
      inputString.replace("\r","");
      Serial.println(inputString);
      stringComplete = true;
    }
  }
}


void split(String message){
  message.replace("\n","");
  message.replace("\r","");
  int commaPosition = 0;
  String buffer = "";
  do{
    commaPosition = message.indexOf(';');
    if(commaPosition != -1){
      buffer = message.substring(0,commaPosition);
      message = message.substring(commaPosition+1, message.length());
    }else{
      if(message.length() > 0){
        buffer = message;
      }
    }
    if (buffer.length() > 0){
      Serial.println(buffer);  
    }
  }while(commaPosition >=0);
}

int countElements(String data, char separator){
  int position = 0;
  int count = 0;
  do{
    position = data.indexOf(separator);
    data = data.substring(position+1,data.length());
    if ( position >= 0){
      count++;
    }
  } while ( position >= 0 ); 
  return count+1;
}



void setThreshold(String message){
    //count fields in message with separator
    int elements = countElements(inputString,';');
    String *ptr;
    ptr = &message;
    //int titi = test(ptr,elements);    
    //split(message);
  
    // set thresholds
    // format is c;s;t;v
    // c => declare that we are setting a threshold
    // s => sensor type (here we are using t for temperature and h for humidity
    // t => threshold type (w for warning, c for critical, n for no threshold)
    // v => threshold value (only int allowed
   
}

int test(String message,String *parr,int size){
  for (int index = 0; index < size; index++){
    Serial.println(*(parr+index));
  }
  return 0;  
}



void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  char buffer[27];

  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h)) {
    Serial.println("ERROR");
    setleds(1,2,2);
  } else {
    setleds(2,0,1);      
    int dh = (h - (int)h) * 100;
    int dt = (t - (int)t) * 100;
    sprintf(buffer,"data;%0d.%d;%0d.%d",(int)h,dh,(int)t,dt);
    Serial.println(buffer);
  }
  
  if (stringComplete) {
    setThreshold(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  delay(3000);
}
