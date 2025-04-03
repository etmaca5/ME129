# TODO: add all constants and calibrations here


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
    def __init__(self):
        # TODO: crowley  - all code
        pass

    def set_level(self, level):
        pass

    def stop(self):
        # hint from ta: we can just call another method within this class to shorten this?
        pass



if __name__ == "__main__":
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

