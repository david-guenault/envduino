# Envuino Project

## Goals

### Thresholds

#### Visual status indicator

 Visual status is a way to define if mesured sensor values are within bounds or not by colored leds. 

 There are 3 leds on the project (red,yellow,gree). Each led is a visual status indicator. 
 * Green: OK
 * Yellow: WARNING
 * Red: CRITICAL

 Settings thresholds is done through the envduino shell tool or through arduino serial console.

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
