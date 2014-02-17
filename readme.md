# Current Cost Raspbery Pi Logger
This is a simple project to read power usage data from your main circuit breaker.  You first hook up the [Current Cost Envi](www.currentcost.com) monitor to your house.  Then connect the [Raspberry Pi](raspberrypi.org) to the serial port on the Current Cost Envi display unit.  Data is written to a csv file.  An LED blinks while the program is running. 

The Current Cost Envi sends two types of messages, real-time and historical.  At the moment, only real-time messages are parsed.

# System Requirements 
* Raspberry Pi running Rhasberian wheezy
* Current Cost Envi
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

# Output
Data is output as a CSV file on your Raspberry Pi.  Here's what it looks like in excel:

![sample data](https://github.com/sanmi/powermon/blob/master/samples/cc_data_screenshot.png?raw=true "Sample Data")