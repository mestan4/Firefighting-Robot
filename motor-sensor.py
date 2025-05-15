import RPi.GPIO as GPIO
import time

# Pin tanımlamaları
TRIG = 23
ECHO = 24

IN1 = 17  # Motor A
IN2 = 18
IN3 = 27  # Motor B
IN4 = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Ultrasonik sensör pinleri
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # Motor pinleri
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Motor hareketleri
def forward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def backward():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def turn_right():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def turn_left():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

# Ana döngü
setup()

try:
    while True:
        distance = get_distance()
        print("Mesafe:", distance, "cm")
        
        if distance < 20:
            print("Engel algılandı! Geri çekiliyor...")
            stop()
            time.sleep(0.5)
            backward()
            time.sleep(1)
            turn_right()
            time.sleep(0.5)
        else:
            forward()
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Durduruluyor...")
    stop()
    GPIO.cleanup()
