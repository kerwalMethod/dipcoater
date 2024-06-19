import RPi.GPIO as GPIO
import RpiMotorLib
import time

direction = 22
step = 23
EN_pin = 24

mymotortest = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
GPIO.setup(EN_pin, GPIO.OUT)

GPIO.output(EN_pin, GPIO.LOW)
mymotortest.motor_go(False, "1/16", 1600, 0.000025, False, 0.05)

GPIO.cleanup()