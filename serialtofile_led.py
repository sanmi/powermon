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

#setup lights
GPIO.setmode(GPIO.BCM)
GREEN_LED = 17
RED_LED = 22
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
lightState = True
GPIO.output(GREEN_LED, lightState)
GPIO.output(RED_LED, not lightState)
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
    GPIO.output(RED_LED, False)
    GPIO.cleanup()
    f.close()    
    ser.close()          
    msg = "finished cc_logger " + time.asctime()
    print msg
    logging.info(msg)

