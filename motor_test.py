# motor_test.py
import RPi.GPIO as GPIO
import time

# Motor sürücü pinleri
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def ileri():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def dur():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

ileri()
print("Motorlar ileri dönüyor!")
time.sleep(2)  # 2 saniye ileri dön
dur()
print("Motorlar durdu.")

GPIO.cleanup()
