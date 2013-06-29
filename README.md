# Envuino Project

## Goals

  There was two main goals when i started this project. Having fun with electronics and create a cheap (really) environmental sensor.
  So there it is. Cheap, full featured and usable with either serial or ethernet connection. 
  
  Curently envduino only provide temperature, humidity, pressure and elevation. It should provide in the future light sensing and gaz sensing.

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

## Envduino serial commands

### Checking envduino is alive

```
   Syntax : p
   Return : pong\nEOF\n
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
    Return : 
```

#### Saving 

```
    Syntax : w
    Return : 
```

#### Visual status indicator

 Visual status is a way to define if mesured sensor values are within bounds or not by colored leds. 

 There are 3 leds on the project (red,yellow,gree). Each led is a visual status indicator. 
 * Green: OK
 * Yellow: WARNING
 * Red: CRITICAL

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
