#import libraries
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

#GPIO setup -- pin 29 = moisture sensor; pin 7 = LED
#Sensor: GPIO 29, Relay 1: GPIO 37, Relay 2: GPIO 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.IN)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)

#Setup camera: max resolution, frame rate to support the same
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

#Set up variables: internal in minutes, water in seconds
interval = 15
water = 12
pic_num = 1

try:
    while True:
        #Turn on LED :)
        GPIO.output(7,True)
        #Turn on sensor & camera & allow to settle
        camera.start_preview()
        GPIO.output(38,True)
        time.sleep(5)
        #Check if dry, and if so open valve for water(ing) time
        if (GPIO.input(29))==1:
            GPIO.output(37,True)
            time.sleep(water)
            GPIO.output(37,False)
        #Turn off sensor, take picture, increment pic_num & turn off LED
        GPIO.output(38,False)
        camera.capture('/home/pi/Pictures/pic_%03d.jpg' % (pic_num))
        camera.stop_preview()
        pic_num = pic_num + 1
        GPIO.output(7,False)
        
        #Wait for interval period, flashing LED every 30 seconds
        count_AA = 0
        while count_AA < (interval * 2):
            count_BB = 0
            while count_BB < 5:
                GPIO.output(7,True)
                time.sleep(0.5)
                GPIO.output(7,False)
                time.sleep(0.5)
                count_BB = count_BB + 1
            time.sleep(25)
            count_AA = count_AA + 1

finally:
    #cleanup the GPIO pins before ending
    GPIO.cleanup()