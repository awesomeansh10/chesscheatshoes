from operator import truediv
import RPi.GPIO as GPIO
Pin=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin,GPIO.OUT)
GPIO.setwarnings(False)

while True:
    GPIO.output(Pin,1)
    time.sleep(0.15)
    GPIO.output(Pin,0)
    time.sleep(0.2)
