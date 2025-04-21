import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

# === Motor Pinleri ===
motor1_pin1 = 17
motor1_pin2 = 18
motor2_pin1 = 22
motor2_pin2 = 23

# === Ultrasonik Sensör Pinleri ===
TRIG = 5
ECHO = 6

# === GPIO Ayarları ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup([motor1_pin1, motor1_pin2, motor2_pin1, motor2_pin2], GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# === Motor Fonksiyonları ===
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

# === Mesafe Ölçümü ===
def mesafe_olc():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        baslangic = time.time()
    while GPIO.input(ECHO) == 1:
        bitis = time.time()

    sure = bitis - baslangic
    mesafe = sure * 34300 / 2
    return mesafe

# === Görüntü İşleme Fonksiyonu (Çizgi Takibi) ===
def takip_et(frame):
    height, width = frame.shape[:2]
    roi = frame[int(height/2):, :]  # Alt yarısını al

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])

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

# === Kamera Başlat ===
cap = cv2.VideoCapture(0)

try:
    while True:
        mesafe = mesafe_olc()
        ret, frame = cap.read()

        if not ret:
            print("Kamera görüntüsü alınamadı")
            break

        if mesafe < 20:
            print("Engel Algılandı! Mesafe:", mesafe)
            stop()
            time.sleep(1)
            turn_right()
            time.sleep(0.5)
        else:
            takip_et(frame)

        cv2.imshow("Çizgi Takip", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
