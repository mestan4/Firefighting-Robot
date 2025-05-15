#ileri geri ve sensor testimiz 2

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# === Motor 1 Pinleri ===
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25
M1_LEN  = 16

# === Motor 2 Pinleri ===
M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5
M2_LEN  = 6

# === Ultrasonik Sensör Pinleri ===
TRIG = 23
ECHO = 24

# Pin ayarları
motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# PWM başlat
pwm_m1_r = GPIO.PWM(M1_RPWM, 1000)
pwm_m1_l = GPIO.PWM(M1_LPWM, 1000)
pwm_m2_r = GPIO.PWM(M2_RPWM, 1000)
pwm_m2_l = GPIO.PWM(M2_LPWM, 1000)

pwm_m1_r.start(0)
pwm_m1_l.start(0)
pwm_m2_r.start(0)
pwm_m2_l.start(0)

# Motor fonksiyonları
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

# Mesafe ölçüm fonksiyonu
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
    print("Engel algılamasıyla ileri gitme başlıyor...")
    motor1_forward()
    motor2_forward()

    while True:
        dist = measure_distance()
        print("Mesafe: %.1f cm" % dist)
        if dist < 10:
            print("Engel algılandı! Motorlar durduruluyor.")
            motor_stop()
            break
        time.sleep(0.2)

    print("Motorlar geri gidiyor...")
    motor1_backward()
    motor2_backward()
    time.sleep(2)

    print("Motorlar durdu.")
    motor_stop()

except KeyboardInterrupt:
    print("Klavye ile durduruldu.")

finally:
    motor_stop()
    pwm_m1_r.stop()
    pwm_m1_l.stop()
    pwm_m2_r.stop()
    pwm_m2_l.stop()
    GPIO.cleanup()
