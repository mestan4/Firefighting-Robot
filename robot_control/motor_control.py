from robot_control.motor_control import move_forward, turn_left, turn_right, stop

def control_robot_based_on_fire(x):
    if x is None:
        print("Yangın tespit edilmedi. İleri gidiliyor.")
        move_forward()
    elif x < 200:
        print("Yangın solda. Sola dönülüyor.")
        turn_left()
    elif x > 400:
        print("Yangın sağda. Sağa dönülüyor.")
        turn_right()
    else:
        print("Yangın ortada. İleri gidiliyor.")
        move_forward()
