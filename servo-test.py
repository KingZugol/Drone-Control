import RPi.GPIO as GPIO
import time
#GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
#Pin 18 als output
GPIO.setup(12,GPIO.OUT)
servo1=GPIO.PWM(12,50) #Pin 18 out, 50hz

servo1.start(0)
print("Rotating servo 180 degrees")
duty = 2

while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty +=duty
print("Resetting to 0")
time.sleep(1)    
servo1.ChangeDutyCycle(0)

servo1.stop()
GPIO.cleanup()
print("Exiting")