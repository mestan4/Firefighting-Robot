from robot_control.motor_control import move_forward, turn_left, turn_right, stop

def control_robot_based_on_fire(x):
    """
    Controls the robot's direction based on the horizontal position (x) of the detected fire.
    """
    if x is None:
        print("No fire detected. Moving forward.")
        move_forward()
    elif x < 200:
        print("Fire detected on the left. Turning left.")
        turn_left()
    elif x > 400:
        print("Fire detected on the right. Turning right.")
        turn_right()
    else:
        print("Fire detected in the center. Moving forward.")
        move_forward()
