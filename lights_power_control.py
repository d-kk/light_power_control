#!/usr/bin/env python

## Control power outlet for lights. On sunrise to sunset, off sunset to sunrise

import sys
import time
import datetime
from astral import Astral
import RPi.GPIO as GPIO

log = 1
pin = 18
power = 0

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

a = Astral()
a.solar_depression = 'civil'

while (1):
    
    today = datetime.date.today()
    today_dawn = a.sunrise_utc(today, 38.641226, -90.323916).replace(tzinfo=None, microsecond=0)
    today_dusk = a.sunset_utc(today, 38.641226, -90.323916).replace(tzinfo=None, microsecond=0)
    
    utc_datetime =  datetime.datetime.utcnow().replace(microsecond=0)
    today_datetime = datetime.datetime.now().replace(microsecond=0)  

    if (utc_datetime < today_dawn):
        GPIO.output(pin, False)
        if (log == 2):
            print('The time is: %s\t UTC time: %s\t Today\'s UTC Sunrise: %s\t  Today\'s UTC Sunset: %s, it is before dawn, power on' % (today_datetime, utc_datetime, today_dawn, today_dusk))
        power = 1
    elif (utc_datetime > today_dusk):
        GPIO.output(pin, False)
        if (log == 1 and power == 0):
            print('Turining power on at night\t the time is: %s\t UTC is: %s\t UTC Sunset: %s' % (today_datetime, utc_datetime, today_dusk))
        if (log == 2):
            print ('The time is: %s\t UTC time: %s\t Today\'s UTC Sunrise: %s\t  Today\'s UTC Sunset: %s, it is after dusk, power on' % (today_datetime, utc_datetime, today_dawn, today_dusk))
        power = 1
    else:
        GPIO.output(pin, True)
        if (log == 1 and power == 1):
            print('Turining power off in the morning\t the time is: %s\t UTC is: %s\t UTC Sunrise: %s' % (today_datetime, utc_datetime, today_dawn))
        if (log == 2):
            print ('The time is: %s\t UTC time: %s\t Today\'s UTC Sunrise: %s\t  Today\'s UTC Sunset: %s, it is daytime, power off' % (today_datetime, utc_datetime, today_dawn, today_dusk))
        power = 0

    sys.stdout.flush() 
    time.sleep(30)
