# jardin_magique
Grow plants the easy way ! Some microcontroller watches most important parameters, and use any computer to log the data. 

## Arduino
Now using Arduino as sensors system, I had plans to port the code to mbed and STM32 microcontroller. 
The pin description is still reflecting my own little thing.
Only one sketch really works with latest server version, the ethernet_uno one. 

## Web server
Running on a Rpi, you'll need a mariadb and what's in the requirement file. It runs with python3.
This part is getting some love lately, a backend server running tornado serves what would be a JSON API to the most important funtions of the garden. For now it only does actionning the relays for my pumps/lights/electrovalves, and stores sensors data.

## Todo 
A lot,
- Want to do a JS frontend
- More anf higher level API functions
- Start storing knowledge in that soft. (what plant likes what neighbor, this sort of stuff) 
- One cool thing could be the ability to rewrite some configuration parameters to the microcontrollers with the web UI. but I don't know how to do that right now. Any help is welcomed.


