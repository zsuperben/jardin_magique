# jardin_magique
Grow plants the easy way ! Some microcontroller watches most important parameters, and use any computer to log the data. 

## Arduino
Now using Arduino as sensors system, I have plans to port the code to mbed and STM32 microcontroller. 
The pin description is still reflecting my own little thing, I have to change some of the code to make it easier to understand. 


## Web server
On the server side you'll need python django and mysql server. 
This part is quiet a mess right now, code needs some architecture, and more thinking into what I want to do with it. 
Basically I choosed django framework to practice with it, not because it's specially fitted for the purpose. 

## Todo 
There are files named *notes* and *TODO* all around the repo, some of them contain actual things I want to do... 
Baseline is, I want to store mesurement done by the microcontrollers and compare them to ideal conditions. 
This means I have to build a directory of plant spiecies that would regroup ideal conditions for them. 
That's a long process, reading gardening books, contributions are quiet easy and welcomed.
I may move to the latin, biological names, this would ensure international usability. 
You can use the Django admin for that. There is a model name Plant type, and it has a admin form already working. 

One cool thing could be the ability to rewrite some configuration parameters to the microcontrollers with the web UI. But I can't how to do that right now. Any help is welcomed.


