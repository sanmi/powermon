# Current Cost Raspbery Pi Logger
This is a simple project to read power usage data from your main circuit breaker.  You first hook up the Current Cost Envi monitor to your house.  Then connect the Raspberry Pi to the serial port on the Current Cost Envi display unit.  Data is written to a csv file.  An LED blinks while the program is running. 

The Current Cost Envi sends two types of messages, real-time and historical.  At the moment, only real-time messages are parsed.

# System Requirements 
* [Raspberry Pi running Rhasberian wheezy](raspberrypi.org)
* [Current Cost Envi](www.currentcost.com)
* USB to serial port adapter for your Current Cost device
* Breakout board with a green LED on channel 17 (just to indicate program status)  

# Python Setup
To setup your raspberry pi with the correct python libraries:
* sudo apt-get install python-dev
* sudo apt-get install python-rpi.gpio
* sudo pip install pyserial
* sudo apt-get install libxml2-dev
* sudo apt-get install libxslt-dev
* sudo pip install lxml
