import sys
import time
import RPi.GPIO as GPIO

# Assign GPIO pins
direction_pin = 22
step_pin = 23
enable_pin = 24

# Create a boolean variable for stopping the motor
stop_motor = False


# Create a function to stop the motor
def motor_stop():

    # Set the boolean variable to true to the motor will stop
    stop_motor = True

    time.sleep(1)


# Create a function for automated runs
def auto_run(steps, stepdelay, initialdelay, waittime):

    # Set the boolean variable to false so the motor can run
    stop_motor = False

    # Set how you are referring to GPIO pins (BCM = Broadcom SOC Channel)
    GPIO.setmode(GPIO.BCM)

    # Disable GPIO warnings
    GPIO.setwarnings(False)

    # Setup the enable GPIO pin
    GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.output(enable_pin, GPIO.LOW)

    # Setup the direction and step GPIO pins
    GPIO.setup(direction_pin, GPIO.OUT)
    GPIO.setup(step_pin, GPIO.OUT)

    # Run the motor
    try:

        # Have the motor wait before starting
        time.sleep(initialdelay)

        # Rotate counterclockwise
        GPIO.output(direction_pin, False)

        # Loop through the steps going counterclockwise
        for i in range(steps):

            # Stop the motor if the boolean variable is changed to true
            if stop_motor:
                break

            # Otherwise run
            else:
                GPIO.output(step_pin, True)
                time.sleep(stepdelay)
                GPIO.output(step_pin, False)
                time.sleep(stepdelay)

        # Wait between directions
        time.sleep(waittime)

        # Rotate clockwise
        GPIO.output(direction_pin, True)

        # Loop through the steps going clockwise
        for i in range(steps):

            # Stop the motor if the boolean variable is changed to true
            if stop_motor:
                break

            # Otherwise run
            else:
                GPIO.output(step_pin, True)
                time.sleep(stepdelay)
                GPIO.output(step_pin, False)
                time.sleep(stepdelay)
        
    # Display an error
    except Exception as motor_error:
        print(sys.exc_info()[0])
        print(motor_error)
        print("Unexpected error")

    # Cleanup
    finally:
        GPIO.output(step_pin, False)
        GPIO.output(direction_pin, False)
        GPIO.cleanup()