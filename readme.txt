This is a simple project to read power usage data from your main circuit breaker.  You first hook up the Current Cost Envi monitor to your house.  Then connect the Raspberry Pi to the serial port on the Current Cost Envi display unit.  Data is written to a csv file.  An LED blinks while the program is running. 

The Current Cost Envi sends two types of messages, real-time and historical.  At the moment, only real-time messages are parsed.

System requirements: 
* Raspberry Pi running Rhasberian wheezy (http://raspberrypi.org)
* Current Cost Envi (http://www.currentcost.com/)
* USB to serial port adapter for your Current Cost device
* Breakout board with green and red LEDs (just to indicate program status)  
** GREEN_LED = 17


to setup your raspberry pi with the correct python libraries:
* sudo pip install pyserial
* sudo apt-get install libxml2-dev
* sudo apt-get install libxslt-dev
* sudo pip install lxml
