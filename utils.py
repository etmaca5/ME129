import time

# MOTOR 1 is the left motor
MOTOR1_TO_MOTOR2_FORWARD_RATIO = 255.0 / 243.0
MOTOR1_TO_MOTOR2_BACKWARD_RATIO = 255.0 / 250.0

# Turning constants
TIME_FOR_90_TURN = 0.6
TIME_FOR_NEGATIVE_90_TURN = 0.65
MOTOR1_FORWARD_TO_MOTOR2_BACKWARD_RATIO = 255.0 / 230.0
MOTOR2_FORWARD_TO_MOTOR1_BACKWARD_RATIO = 255.0 / 220.0


# Distance constants
TIME_FOR_1M = 1.8
BACKWARD_1M = 2.2


# Angle is in degrees (positive or negative)
def set_angle(motor1, motor2, angle):
    base_power = 0.7
    if angle > 0:
        power1 = base_power
        power2 = - base_power * MOTOR1_FORWARD_TO_MOTOR2_BACKWARD_RATIO
        time_for_90 = TIME_FOR_90_TURN
    else: 
        power1 = - base_power * MOTOR2_FORWARD_TO_MOTOR1_BACKWARD_RATIO
        power2 = base_power
        time_for_90 = TIME_FOR_NEGATIVE_90_TURN
    angle = abs(angle)

    motor1.set_level(power1)
    motor2.set_level(power2)
    time.sleep(time_for_90 * angle / 90)
    motor1.stop()
    motor2.stop()
    time.sleep(0.5)

# Distance in meters
def move_dist(motor1, motor2, dist):
    power = 1.0
    if dist < 0:
        power = -1.0
        ratio = MOTOR1_TO_MOTOR2_BACKWARD_RATIO
        time_for_1m = TIME_FOR_1M
    else:
        ratio = MOTOR1_TO_MOTOR2_FORWARD_RATIO
        time_for_1m = BACKWARD_1M 
    dist = abs(dist)

    motor1.set_level(power / ratio)
    motor2.set_level(power)
    time.sleep(dist * time_for_1m)
    motor1.stop()
    motor2.stop()
    time.sleep(0.5)

def square(motor1, motor2, is_right=True):
    angle = 90 if is_right else -90
    for _ in range(4):
        move_dist(motor1, motor2, 1)
        set_angle(motor1, motor2, angle)

def triangle(motor1, motor2, is_right=True):
    angle = 120 if is_right else -120
    for _ in range(3):
        move_dist(motor1, motor2, 1)
        set_angle(motor1, motor2, angle)