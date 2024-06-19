import RPi.GPIO as GPIO
from RPiMotorLib import RPiMotorLib
import time

direction = 22
step = 23
EN_pin = 24

mymotortest = RPiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
GPIO.setup(EN_pin, GPIO.OUT)

GPIO.output(EN_pin, GPIO.LOW)
mymotortest.motor_go(False, "Full", 200, 0.0005, False, 0.05)

GPIO.cleanup()