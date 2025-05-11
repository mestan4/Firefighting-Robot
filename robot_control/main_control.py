import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# === Motor Pins ===
motor1_pin1 = 17
motor1_pin2 = 18
motor2_pin1 = 22
motor2_pin2 = 23

# === Ultrasonic Sensor Pins ===
TRIG = 5
ECHO = 6

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup([motor1_pin1, motor1_pin2, motor2_pin1, motor2_pin2], GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# === Motor Functions ===
def forward():
    GPIO.output(motor1_pin1, GPIO.HIGH)
    GPIO.output(motor1_pin2, GPIO.LOW)
    GPIO.output(motor2_pin1, GPIO.HIGH)
    GPIO.output(motor2_pin2, GPIO.LOW)

def stop():
    GPIO.output(motor1_pin1, GPIO.LOW)
    GPIO.output(motor1_pin2, GPIO.LOW)
    GPIO.output(motor2_pin1, GPIO.LOW)
    GPIO.output(motor2_pin2, GPIO.LOW)

def turn_left():
    GPIO.output(motor1_pin1, GPIO.LOW)
    GPIO.output(motor1_pin2, GPIO.HIGH)
    GPIO.output(motor2_pin1, GPIO.HIGH)
    GPIO.output(motor2_pin2, GPIO.LOW)

def turn_right():
    GPIO.output(motor1_pin1, GPIO.HIGH)
    GPIO.output(motor1_pin2, GPIO.LOW)
    GPIO.output(motor2_pin1, GPIO.LOW)
    GPIO.output(motor2_pin2, GPIO.HIGH)

# === Distance Measurement ===
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        end = time.time()

    duration = end - start
    distance = duration * 34300 / 2
    return distance

# === Image Processing Function (Line Following) ===
def follow_line(frame):
    height, width = frame.shape[:2]
    roi = frame[int(height / 2):, :]  # Take the bottom half

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])

            if cx < width / 3:
                turn_left()
            elif cx > 2 * width / 3:
                turn_right()
            else:
                forward()
        else:
            stop()
    else:
        stop()

# === Start Camera ===
cap = cv2.VideoCapture(0)

try:
    while True:
        distance = measure_distance()
        ret, frame = cap.read()

        if not ret:
            print("Camera frame could not be captured")
            break

        if distance < 20:
            print("Obstacle Detected! Distance:", distance)
            stop()
            time.sleep(1)
            turn_right()
            time.sleep(0.5)
        else:
            follow_line(frame)

        cv2.imshow("Line Following", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
