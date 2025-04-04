# imports
import pigpio
import sys
import time
import traceback
from utils import *

# TODO: add all constants and calibrations here
PIN_MOTOR1_LEGA = 8
PIN_MOTOR1_LEGB = 7

PIN_MOTOR2_LEGA = 5
PIN_MOTOR2_LEGB = 6

class Motor:
    """
     Motor object code:
    - __init__ parameters
    - Parameters:
    - pin_legA, pin_legB
    - Left or right motor
    - Relative power calibration (in case one motor is stronger than the
    other)
    - Prepare the PWM range
    - prepare PWM frequency
    - clear all pins
    - set_level method
    - Params:
    - Level
    - Uses io.set_PWM_dutycycle to set power for a single motor, will
    compensate based on differing gear ratios/powers (part of the motor
    object)
    - stop method
    """
    def __init__(self, pin_legA, pin_legB, is_left, io):
        # TODO: crowley  - all code
        self.pin_legA = pin_legA
        self.pin_legB = pin_legB
        self.is_left = is_left
        self.io = io

        # Set up the four pins as output (commanding the motors).
        self.io.set_mode(self.pin_legA, pigpio.OUTPUT)
        self.io.set_mode(self.pin_legB, pigpio.OUTPUT)

        # Prepare the PWM.  The range gives the maximum value for 100%
        # duty cycle, using integer commands (1 up to max).
        self.io.set_PWM_range(self.pin_legA, 255)
        self.io.set_PWM_range(self.pin_legB, 255)
        
        # Set the PWM frequency to 1000Hz.
        self.io.set_PWM_frequency(self.pin_legA, 1000)
        self.io.set_PWM_frequency(self.pin_legB, 1000)

        # Clear all pins, just in case.
        self.io.set_PWM_dutycycle(self.pin_legA, 0)
        self.io.set_PWM_dutycycle(self.pin_legB, 0)

    def set_level(self, level):
        pass

    def stop(self):
        # hint from ta: we can just call another method within this class to shorten this?
        pass

# TODO: do we want to add this to a utils.py



if __name__ == "__main__":
    print("Setting up the GPIO...")
    io = pigpio.pi()
    if not io.connected:
        print("Unable to connection to pigpio daemon!")
        sys.exit(0)
    print("GPIO ready...")

    motor1 = Motor(PIN_MOTOR1_LEGA, PIN_MOTOR1_LEGB, True, io)
    motor2 = Motor(PIN_MOTOR2_LEGA, PIN_MOTOR2_LEGB, False, io)
    print("Motors ready...")

    
    
    # TODO:
    """
    Main code:
    Initialize two Motor objects - left and right motor
    Using the motor object's setlevel methods, Loop four times: move forward 1 meter, then turn 90 degrees
    How to get it to move forward 1 meter exactly:
    Trial and error: try different PWN levels and different times
    How to get it to turn 90 degrees exactly:
    Also trial and error: try different PWN levels for one of the legs for different times, while stopping the other leg. Will calibrate this so that we can turn either direction based on an input angle
    Helper function with set angle - which will do exactly what is described in the above bullet
    Once down with square, will stop both motors
    Notes from meeting
    EStimate distance by spins per voltage and gear ratio/ wheel circumference
    """

    # also make sure we call set angle function here 
    # TODO: move the set angle function a different file - probably utils.py, which can contain all our helper functions


    """
    angle from 0 -270
    likely will not be linear
    """


    


    ############################################################
    # Drive.
    # Place this is a try-except structure, so we can turn off the
    # motors even if the code crashes.
    try:
        # Example 1: Ramp ONE PIN up/down.  Keep the other pin at zero.
        print("Ramping Motor 2 (backward) up/down...") 
        pinNonzero = PIN_MOTOR2_LEGB
        pinZero    = PIN_MOTOR2_LEGA

        for pwmlevel in [50, 100, 150, 200, 255, 200, 150, 100, 50, 0]:
            print("Pin %d at level %3d, Pin %d at zero" %
                  (pinNonzero, pwmlevel, pinZero))
            io.set_PWM_dutycycle(pinNonzero, pwmlevel)
            io.set_PWM_dutycycle(pinZero, 0)
            time.sleep(1)

        # Example 2: Drive ONE motor forward/backward.
        print("Driving Motor 1 forward, stopping, then reversing...")
        io.set_PWM_dutycycle(PIN_MOTOR1_LEGA, 170)
        io.set_PWM_dutycycle(PIN_MOTOR1_LEGB,   0)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTOR1_LEGA,   0)
        io.set_PWM_dutycycle(PIN_MOTOR1_LEGB,   0)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTOR1_LEGA,   0)
        io.set_PWM_dutycycle(PIN_MOTOR1_LEGB, 170)
        time.sleep(1)

        io.set_PWM_dutycycle(PIN_MOTOR1_LEGA,   0)
        io.set_PWM_dutycycle(PIN_MOTOR1_LEGB,   0)
        time.sleep(1)

    except BaseException as ex:
        # Report the error, but continue with the normal shutdown.
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()
        

    ############################################################
    # Turn Off.
    # Note the PWM will stay at the last commanded value.  So you want
    # to be sure to set to zero before the program closes.  Else your
    # robot will run away...
    print("Turning off...")

    # Clear the PINs (commands).
    io.set_PWM_dutycycle(PIN_MOTOR1_LEGA, 0)
    io.set_PWM_dutycycle(PIN_MOTOR1_LEGB, 0)
    io.set_PWM_dutycycle(PIN_MOTOR2_LEGA, 0)
    io.set_PWM_dutycycle(PIN_MOTOR2_LEGB, 0)
    
    # Also stop the interface.
    io.stop()
    

# TODO: Step 1: motor clas
# Step 2: move in a line
# Step 3: angle moving correctly
# step 4: move in a square