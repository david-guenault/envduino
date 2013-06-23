Envuino Project

Goals

The envduino module

Serial command référence

Thresholds

Setting visual thresholds

    Visual threshold is a way to define if mesured sensor values are within bounds or not by displaying colored leds. 

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
