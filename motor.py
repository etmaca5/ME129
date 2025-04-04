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

MOTOR1_TO_MOTOR2_RATIO = 1.2/1.0

class Motor:
    """
     Motor object code:
    
    - clear all pins
    - set_level method
    - Params:
    - Level
    - Uses io.set_PWM_dutycycle to set power for a single motor, will
    compensate based on differing gear ratios/powers (part of the motor
    object)
    - stop method
    """
    def __init__(self, pin_legA, pin_legB, is_motor1, io):
        # TODO: crowley  - all code
        self.pin_legA = pin_legA
        self.pin_legB = pin_legB
        self.is_motor1 = is_motor1
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

    # -1.0 to 1.0
    def set_level(self, level):
        level = int(level * 255)
        assert level <= 255 and level >= -255
        zero_pin = self.pin_legA
        nonzero_pin = self.pin_legB

        if level <= 0:
            # swap zero pin
            zero_pin, nonzero_pin = nonzero_pin, zero_pin

        io.set_PWM_dutycycle(zero_pin, 0)
        io.set_PWM_dutycycle(nonzero_pin, abs(level))

    def stop(self):
        self.set_level(0)

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

    try:
        motor1.set_level(0.5)
        motor2.set_level(0.5 * MOTOR1_TO_MOTOR2_RATIO)
        time.sleep(3)
        motor1.stop()
        motor2.stop()
    except BaseException as ex:
        # Report the error, but continue with the normal shutdown.
        print("Ending due to exception: %s" % repr(ex))
        traceback.print_exc()

    print("Turning off...")

    # Clear the PINs (commands).
    motor1.stop()
    motor2.stop()
    
    # Also stop the interface.
    io.stop()