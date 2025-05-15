#=== ileri geri testimiz ==

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

# === Ultrasonic Sensor Pins ===
TRIG = 23
ECHO = 24

# Tüm pinleri çıkış olarak ayarla
motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# PWM oluştur
pwm_m1_r = GPIO.PWM(M1_RPWM, 1000)
pwm_m1_l = GPIO.PWM(M1_LPWM, 1000)
pwm_m2_r = GPIO.PWM(M2_RPWM, 1000)
pwm_m2_l = GPIO.PWM(M2_LPWM, 1000)

pwm_m1_r.start(0)
pwm_m1_l.start(0)
pwm_m2_r.start(0)
pwm_m2_l.start(0)

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
    pwm_m2_r.ChangeDutyCycle(70)
    pwm_m2_l.ChangeDutyCycle(0)

def motor2_backward():
    GPIO.output(M2_REN, True)
    GPIO.output(M2_LEN, True)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m2_l.ChangeDutyCycle(70)

def motor_stop():
    pwm_m1_r.ChangeDutyCycle(0)
    pwm_m1_l.ChangeDutyCycle(0)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m2_l.ChangeDutyCycle(0)

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

try:
    print("Motorlar ileri...")
    motor1_forward()
    motor2_forward()
    time.sleep(2)

    print("Motorlar geri...")
    motor1_backward()
    motor2_backward()
    time.sleep(2)

    print("Motorlar duruyor...")
    motor_stop()

except KeyboardInterrupt:
    pass

finally:
    motor_stop()
    pwm_m1_r.stop()
    pwm_m1_l.stop()
    pwm_m2_r.stop()
    pwm_m2_l.stop()
    GPIO.cleanup()
