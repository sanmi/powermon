# Copyright 2014 Frank San Miguel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import serial
from lxml import objectify
from lxml import etree
import time 
import sys, traceback
import RPi.GPIO as GPIO, feedparser, time
import logging
logging.basicConfig(filename='cc_logger.log',level=logging.DEBUG)

msg = "starting cc_logger " + time.asctime()
print msg
logging.info(msg)

#setup light. This is just an indicator that the program is running
GPIO.setmode(GPIO.BCM)
GREEN_LED = 17
GPIO.setup(GREEN_LED, GPIO.OUT)
lightState = True
GPIO.output(GREEN_LED, lightState)
BLINK_TIME = 1.4

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0, rtscts=0, timeout=1.5)


def parse(xml):
    return objectify.XML(xml)

blinkTimer = time.time()

def processBlink(led):
    global blinkTimer
    global lightState
    #print (time.clock() - blinkTimer)
    if ((time.time() - blinkTimer) > BLINK_TIME):
        #blink the light
        blinkTimer = time.time()
        lightState = not lightState
        GPIO.output(led, lightState)
    
line = ""
f = open("cc_data.csv", "a")
header = "systime, src, dsb, time, tmprF, ch1watts, ch2watts\n"
#print header
f.write(header)

try:
    while (True):
        processBlink(GREEN_LED)
        c = ser.read(1)
        if (c != '\n'):
            line += c
        else:
            try:
                msg = parse(line)
                # if it is a history record we do something different
                # for now, just ignore it
                if hasattr(msg, "hist"):
                    logging.debug("history record " + time.asctime())
                    line = ""
                elif hasattr(msg, "tmprF"):
                    formatted = \
                    str(time.asctime()) + "," +\
                    str(time.time()) + "," +\
                    msg.src + "," + \
                    str(msg.dsb) + "," + \
                    msg.time + "," + \
                    str(msg.tmprF) + "," + \
                    str(msg.ch1.watts) + "," + \
                    str(msg.ch2.watts)
                    f.write(formatted) 
                    f.write('\n')
                    f.flush()
                    line = ""
                else:
                     logging.warn("unknown message format " + line)
                     line = ""
            except etree.XMLSyntaxError:
                logging.error("xml syntax: " + "|" + line)
                line = ""
            except:
                logging.error( time.asctime() + "Unexpected error: " + str(sys.exc_info()[0]) + "|" + line) 
                #traceback.print_exc(file=sys.stdout)
		err = traceback.format_exc()
		logging.error(err)
                ser.close()
                ser.open()
                line = ""

except (KeyboardInterrupt, SystemExit):
    GPIO.output(GREEN_LED, False)
    GPIO.cleanup()
    f.close()    
    ser.close()          
    msg = "finished cc_logger " + time.asctime()
    print msg
    logging.info(msg)

