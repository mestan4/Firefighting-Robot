#ileri sensor uyarı verince saga dönüşü test=

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# === Motor 1 Pinleri (Sol) ===
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25
M1_LEN  = 16

# === Motor 2 Pinleri (Sağ) ===
M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5
M2_LEN  = 6

# === Ultrasonik Sensör Pinleri ===
TRIG = 23
ECHO = 24

# Pin Ayarları
motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# PWM Başlat
pwm_m1_r = GPIO.PWM(M1_RPWM, 1000)
pwm_m1_l = GPIO.PWM(M1_LPWM, 1000)
pwm_m2_r = GPIO.PWM(M2_RPWM, 1000)
pwm_m2_l = GPIO.PWM(M2_LPWM, 1000)

pwm_m1_r.start(0)
pwm_m1_l.start(0)
pwm_m2_r.start(0)
pwm_m2_l.start(0)

# === Motor Fonksiyonları ===
def motor1_forward():
    GPIO.output(M1_REN, True)
    GPIO.output(M1_LEN, True)
    pwm_m1_r.ChangeDutyCycle(70)
    pwm_m1_l.ChangeDutyCycle(0)

def motor1_backward():
    GPIO.output(M1_REN, True)
    GPIO.output(M1_LEN, True)
    pwm_m1_r.ChangeDutyCycle(0)
    pwm_m1_l.ChangeDutyCycle(70)

def motor2_forward():
    GPIO.output(M2_REN, True)
    GPIO.output(M2_LEN, True)
    pwm_m2_r.ChangeDutyCycle(0)    # TERS
    pwm_m2_l.ChangeDutyCycle(70)   # TERS

def motor2_backward():
    GPIO.output(M2_REN, True)
    GPIO.output(M2_LEN, True)
    pwm_m2_r.ChangeDutyCycle(70)   # TERS
    pwm_m2_l.ChangeDutyCycle(0)    # TERS

def motor_stop():
    pwm_m1_r.ChangeDutyCycle(0)
    pwm_m1_l.ChangeDutyCycle(0)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m2_l.ChangeDutyCycle(0)

def rotate_right(degree=40):
    print(f"{degree} derece sağa dönülüyor...")
    motor1_forward()
    motor2_backward()
    time.sleep(0.5)  # Bu süreyi test edip ayarlayacağız
    motor_stop()

# === Mesafe Ölçüm Fonksiyonu ===
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    stop = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()

    duration = stop - start
    distance = duration * 34300 / 2
    return distance

try:
    print("İleri gidiliyor, engel kontrolü aktif.")
    motor1_forward()
    motor2_forward()

    while True:
        dist = measure_distance()
        print("Mesafe: %.1f cm" % dist)
        if dist < 20:
            print("Engel algılandı! Duruluyor ve sağa dönülüyor.")
            motor_stop()
            time.sleep(0.3)
            rotate_right()
            break
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Klavye ile durduruldu.")

finally:
    motor_stop()
    pwm_m1_r.stop()
    pwm_m1_l.stop()
    pwm_m2_r.stop()
    pwm_m2_l.stop()
    GPIO.cleanup()
