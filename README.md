# Envduino Project

## Goals

  There was two main goals when i started this project. Having fun with electronics and create a cheap (really) environmental sensor.
  So there it is. Cheap, full featured and usable with either serial or ethernet connection. 
  
  Curently envduino only provide temperature, humidity, pressure and elevation. It should provide in the future light sensing and gaz sensing.

## Included

  envduino is made of a sketch file for arduino (only tested on mega and should not work en leonardo), a shell for getting values and settings preferences (saving not ready at the moment), a nagios/shinken/icinga plugin for checking environmental status and a little webapp for getting metrics and graph them.

## Envduino prototype wiring

### DHT22 

  DHT22 come with 4 pins from left to right when facing the grid
  
  ```

    DHT22                       ARDUINO MEGA 2560

    1 - VCC (3 to 5V)   -->     PIN 3.3V 
    2 - Data Out        -->     PIN 2 (this can be changed in the arduino sketch)
    3 - Not connected
    4 - Ground          -->     GROUND PIN

  ```

  Also connect a 10k resistor between DHT22's VCC AND DATA pins

### BMP085

  There are 7 pins from left to right (1 to 7). This is an i2c module. 

```
    BMP085                      ARDUINO MEGA 2560

    1 - 5V             
    2 - 3.3V            -->     3.3V
    3 - GROUND          -->     Ground
    4 - SDA             -->     PIN 43 SDA
    5 - SCL             -->     PIN 42 SCL
    6 - XCLR
    7 - EOC
```

### Schematic 

#### breadboard

![alt tag](https://raw.github.com/david-guenault/envduino/master/schematic/envduino_bb.png)

#### logical 

![alt tag](https://raw.github.com/david-guenault/envduino/master/schematic/envduino_schema.png)

## Envduino Shell

This shell allow to test envduino module and configure envduino module settings

```
------------------------------------------------

Welcome to Envduino Shell

(c) David GUENAULT

david.guenault@gmail.com

Released under GNU Affero General Public License

http://www.gnu.org/licenses

------------------------------------------------


> connect
Using default port and baudrate (/dev/ttyACM1,9600)
Connection to serial port OK

> temperature
temperature:24
> humidity
humidity:55
> 
```

## Envduino serial commands protocol

### Checking envduino is alive

```
   Syntax : ping
   Return : pong
```

### Thresholds

#### Setting 

 Settings thresholds is done through the envduino shell tool or through arduino serial console.

```
    syntax : t;[s];[t];[v]
    t define that the current command is a threshold setting command
    [s] is the sensor :
        h for humidity
        t for temperature
        p for pressure
    [t] is the threshold type. For the thow levels of alert (warning and critical)
        w for warning
        c for critical
    [v] is the threshold value. It's an integer within bounds of your sensor.
````

#### Reading 

```
    syntax : r
    Return : Temperature : w=-9999, c=-9999 | Humidity : w=-9999,c=-9999 | Pressure : w=-9999,c=-9999
```

#### Saving 

```
    Syntax : w (NOT IMPLEMENTED)
    Return : 
```

#### Visual status indicator

 Visual status is a way to define if mesured sensor values are within bounds or not by colored leds. 

 There are 3 leds on the project (red,yellow,gree). Each led is a visual status indicator. 
 * Green: OK
 * Yellow: WARNING
 * Red: CRITICAL

##### Controling leds

```
    Syntax : l;[led];[state]
    Return : 

    led should be one of the following :
    r for red
    y for yellow
    g for green

    state should be one of the following :
    0 for off
    1 for on
```

### geting sensors values

```
    Syntax : m;[sensor]
    Return : temperature:25

    sensor should be one of the following :
    h for humidity
    t for temperature
    p for pressure
```

## Preparing the environment

### DEBIAN/UBUNTU

envduino use the following libraries (allready included in this github space).

 * Adafruit DHT22 library : https://github.com/adafruit/DHT-sensor-library
 * Adafruit BMP085 library : https://github.com/adafruit/Adafruit-BMP085-Library
 
## Parts

### List


 * 1		10k Ω Resistance				
 * 3		330 Ω Resistance	
 * 1		DHT22 Humidity and Temperature Sensor	
 * 1		Arduino Mega	
 * 1		BMP085 Breakout (pressure and elevation)	
 * 1		Yellow LED 
 * 1		Red LED 
 * 1		Green LED 


### Where to buy 

I bought everything on amazon (no pub but it was cheaper). 
  
  * BMP085 pressure, elevation and temperature sensor (http://www.amazon.fr/gp/product/B0090XB5GQ/ref=oh_details_o02_s00_i00?ie=UTF8&psc=1)
  * DHT22 humidity and tempertature sensor (http://www.amazon.fr/gp/product/B005A9KJ4I/ref=oh_details_o04_s00_i00?ie=UTF8&psc=1)
  * Ethernet Shield (http://www.amazon.fr/gp/product/B00D6BGCO8/ref=oh_details_o03_s00_i00?ie=UTF8&psc=1)
  * Arduino mega clone (http://www.amazon.fr/Arduino-MEGA-2560-Board-Conseil/dp/B00C04P9VO/ref=sr_1_17?s=electronics&ie=UTF8&qid=1372398504&sr=1-17&keywords=arduino+mega)
  * 10k resistor

You can also find the parts at the following websites
  
  * http://www.adafruit.com (US)
  * http://www.arduino.cc (for arduino mega and ethernet shield) (EU)
  * http://https://www.sparkfun.com (US)

As an alternative you can use the sainsmart bmp085 (cheaper) from : http://www.sainsmart.com/sainsmart-bmp085-digital-pressure-sensor-module-board.html
