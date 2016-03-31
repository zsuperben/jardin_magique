__author__ = 'zsb'

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(20, gpio.OUT) # Switch 1
gpio.setup(21, gpio.OUT) # Switch 2
gpio.setup(13, gpio.OUT) # Switch 3
gpio.setup(26, gpio.OUT) # Switch 4
gpio.setup(16, gpio.OUT) # Switch 5
gpio.setup(6, gpio.OUT) # Switch 6
gpio.setup(5, gpio.OUT) # Switch 7
gpio.setup(19, gpio.OUT) # Switch 8
gpio.setup(12, gpio.OUT) # Switch 9
gpio.setup(25, gpio.OUT) # Switch 10
gpio.setup(24, gpio.OUT) # Switch 11
gpio.setup(23, gpio.OUT) # Switch 12
gpio.setup(22, gpio.OUT) # Switch 13
gpio.setup(27, gpio.OUT) # Switch 14
gpio.setup(17, gpio.OUT) # Switch 15
gpio.setup(18, gpio.OUT) # Switch 16







switches = {
"SW1": 20,
"SW2": 21,
"SW3": 13,
"SW4": 26,
"SW5": 16,
"SW6": 6,
"SW7": 5,
"SW8": 19,
"SW9": 12,
"SW10": 25,
"SW11": 24,
"SW12": 23,
"SW13": 18,
"SW14": 17,
"SW15": 27,
"SW16": 22,
}



def turnOn(sw):
    try:
        gpio.output(switches[sw], gpio.HIGH)
        return True
    except KeyError:
        return False


def turnOff(sw):
    try:
        gpio.output(switches[sw], gpio.LOW)
        return True
    except KeyError:
        return False

def readOne(sw):
    try:
        return gpio.input(switches[sw])
    except KeyError:
        return None

