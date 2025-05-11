from fire_detection import detect_fire
from obstacle_avoidance import setup_ultrasonic, get_distance
from motor_driver import setup_motors, move_forward, stop_motors, turn_left, turn_right
from camera import open_camera
from config import FIRE_DETECTION_CONFIDENCE, OBSTACLE_DISTANCE_THRESHOLD
import time

setup_motors()
setup_ultrasonic()
cap = open_camera()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        fire_detected, fire_center = detect_fire(frame)
        distance = get_distance()

        if distance < OBSTACLE_DISTANCE_THRESHOLD:
            stop_motors()
            time.sleep(0.5)
            turn_right()
            time.sleep(0.5)
            move_forward()
        elif fire_detected:
            if fire_center[0] > frame.shape[1] * 0.6:
                turn_right()
            elif fire_center[0] < frame.shape[1] * 0.4:
                turn_left()
            else:
                move_forward()
        else:
            move_forward()

except KeyboardInterrupt:
    print("Durduruluyor...")
    cap.release()
    stop_motors()
    GPIO.cleanup()
