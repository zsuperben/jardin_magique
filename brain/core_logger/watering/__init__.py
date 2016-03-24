__author__ = 'zsb'

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)


gpio.setup(20, gpio.OUT, initial=gpio.LOW) # Switch 1
gpio.setup(21, gpio.OUT, initial=gpio.LOW) # Switch 2
gpio.setup(13, gpio.OUT, initial=gpio.LOW) # Switch 3
gpio.setup(26, gpio.OUT, initial=gpio.LOW) # Switch 4
gpio.setup(16, gpio.OUT, initial=gpio.LOW) # Switch 5
gpio.setup(6, gpio.OUT, initial=gpio.LOW) # Switch 6
gpio.setup(5, gpio.OUT, initial=gpio.LOW) # Switch 7
gpio.setup(19, gpio.OUT, initial=gpio.LOW) # Switch 8

switches = {"SW1": 20,
"SW2": 21,
"SW3": 13,
"SW4": 26,
"SW5": 16,
"SW6": 6,
"SW7": 5,
"SW8": 19}



def sw1on():
    try:
        gpio.output(SW1, gpio.HIGH)
        return True
    except:
        return False

def sw1off():
    try:
        gpio.output(SW1, gpio.LOW)
        return True
    except:
        return False

def sw2on():
    try:
        gpio.output(SW2, gpio.HIGH)
        return True
    except:
        return False

def sw2off():
    try:
        gpio.output(SW2, gpio.LOW)
        return True
    except:
        return False

def sw3on():
    try:
        gpio.output(SW3, gpio.HIGH)
        return True
    except:
        return False

def sw3off():
    try:
        gpio.output(SW3, gpio.LOW)
        return True
    except:
        return False

def sw4on():
    try:
        gpio.output(SW4, gpio.HIGH)
        return True
    except:
        return False

def sw4off():
    try:
        gpio.output(SW4, gpio.LOW)
        return True
    except:
        return False

def sw5on():
    try:
        gpio.output(SW5, gpio.HIGH)
        return True
    except:
        return False


def sw5off():
    try:
        gpio.output(SW5, gpio.LOW)
        return True
    except:
        return False

def sw6on():
    try:
        gpio.output(SW6, gpio.HIGH)
        return True
    except:
        return False

def sw6off():
    try:
        gpio.output(SW6, gpio.LOW)
        return True
    except:
        return False

def sw7on():
    try:
        gpio.output(SW7, gpio.HIGH)
        return True
    except:
        return False

def sw7off():
    try:
        gpio.output(SW7, gpio.LOW)
        return True
    except:
        return False

def sw8on():
    try:
        gpio.output(SW8, gpio.HIGH)
        return True
    except:
        return False


def sw8off():
    try:
        gpio.output(SW8, gpio.LOW)
        return True
    except:
        return False


def turnOn(sw):
    try:
        gpio.output(switches[sw], gpio.HIGH)
        return True
    except:
        return False


def turnOff(sw):
    try:
        gpio.output(switches[sw], gpio.LOW)
        return True
    except:
        return False

def readOne(sw):
    try:
        return gpio.input(switches[sw])
    except:
        return None

