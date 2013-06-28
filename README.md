# Envuino Project

## Goals

  There was two main goals when i started this project. Having fun with electronics and create a cheap (really) environmental sensor.
  So there it is. Cheap, full featured and usable with either serial or ethernet connection. 
  
  Curently envduino only provide temperature, humidity, pressure and elevation. It should provide in the future light sensing and gaz sensing.

## Envduino prototype wiring



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

