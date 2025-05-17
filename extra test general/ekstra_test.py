import cv2
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

# === MODEL YÜKLE ===
model = YOLO("best.pt")

# === MOTOR PİN AYARLARI ===
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25
M1_LEN  = 16

M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5
M2_LEN  = 6

# === ULTRASONİK PİNLER ===
TRIG = 23
ECHO = 24

# === GPIO AYARLARI ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# === PWM AYARLARI ===
pwm1 = GPIO.PWM(M1_REN, 1000)
pwm2 = GPIO.PWM(M1_LEN, 1000)
pwm3 = GPIO.PWM(M2_REN, 1000)
pwm4 = GPIO.PWM(M2_LEN, 1000)

for pwm in [pwm1, pwm2, pwm3, pwm4]:
    pwm.start(0)

# === MOTOR KONTROLLERİ ===
def motor_dur():
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, False)

def motor_ileri(hiz=80):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, True)
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.ChangeDutyCycle(hiz)

def motor_sola_don(hiz=50):
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, True)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, True)

def motor_saga_don(hiz=50):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)

# === ULTRASONİK MESAFE ÖLÇÜM ===
def mesafe_olc():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    
    return (TimeElapsed * 34300) / 2

# === KAMERA AÇ ===
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, verbose=False)[0]
        mesafe = mesafe_olc()

        fire_detected = False
        can_detected = False
        fire_x = None
        frame_center = frame.shape[1] // 2

        for box in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = box
            label = int(cls)
            center_x = int((x1 + x2) / 2)

            if label == 0:  # Ateş
                fire_detected = True
                fire_x = center_x

            elif label == 1:  # Kutu (can)
                can_detected = True

        print(f"Mesafe: {mesafe:.1f} cm | Ateş: {fire_detected} | Kutu: {can_detected}")

        if fire_detected:
            # Engel varsa kaç
            if can_detected and mesafe < 20:
                print("→ Engel var! Sola dönülüyor")
                motor_sola()
                time.sleep(1)
                continue

            if abs(fire_x - frame_center) < 40:
                print("→ Ateş ortalandı, DUR")
                motor_dur()
                break

            elif fire_x < frame_center:
                print("→ Ateş solda, sola dönülüyor")
                motor_sola()
                time.sleep(0.3)

            else:
                print("→ Ateş sağda, sağa dönülüyor")
                motor_saga()
                time.sleep(0.3)

        else:
            if can_detected and mesafe < 20:
                print("→ Ateş yok ama kutu var → Sola dön")
                motor_sola()
                time.sleep(1)
            else:
                print("→ Ateş yok → Sağa dönerek arıyor")
                motor_saga()
                time.sleep(0.5)

except KeyboardInterrupt:
    print("Kapatılıyor...")

finally:
    motor_dur()
    cap.release()
    GPIO.cleanup()