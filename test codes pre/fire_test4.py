import cv2
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

# === Model yükle ===
model = YOLO("fire_model.pt")  # YOLOv8n ile eğitilmiş özel model dosyan

# === GPIO pin tanımlamaları ===
# Sol motor
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25
M1_LEN  = 16

# Sağ motor
M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5
M2_LEN  = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Enable pinlerini aktif et (HIGH)
GPIO.output(M1_REN, True)
GPIO.output(M1_LEN, True)
GPIO.output(M2_REN, True)
GPIO.output(M2_LEN, True)

# PWM pinleri (sadece yön pinlerine uygulanır)
pwm_r1 = GPIO.PWM(M1_RPWM, 1000)
pwm_l1 = GPIO.PWM(M1_LPWM, 1000)
pwm_r2 = GPIO.PWM(M2_RPWM, 1000)
pwm_l2 = GPIO.PWM(M2_LPWM, 1000)

for pwm in [pwm_r1, pwm_l1, pwm_r2, pwm_l2]:
    pwm.start(0)

# === Motor fonksiyonları ===
def ileri(hiz=50):
    pwm_r1.ChangeDutyCycle(hiz)
    pwm_l1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(hiz)
    pwm_l2.ChangeDutyCycle(0)

def geri(hiz=50):
    pwm_r1.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(hiz)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(hiz)

def sola(hiz=50):
    pwm_r1.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(hiz)
    pwm_r2.ChangeDutyCycle(hiz)
    pwm_l2.ChangeDutyCycle(0)

def saga(hiz=50):
    pwm_r1.ChangeDutyCycle(hiz)
    pwm_l1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(hiz)

def dur():
    for pwm in [pwm_r1, pwm_l1, pwm_r2, pwm_l2]:
        pwm.ChangeDutyCycle(0)

# === Kamera ayarları ===
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# === Döngü ===
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Sadece her 3 karede 1 çalış (performans için)
        if time.time() % 0.15 > 0.05:
            continue

        results = model(frame, imgsz=320)[0]
        boxes = results.boxes

        if len(boxes) > 0:
            # En büyük kutuyu seç (yangına odaklan)
            largest_box = max(
                boxes,
                key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1])
            )
            x1, y1, x2, y2 = largest_box.xyxy[0]
            center_x = int((x1 + x2) / 2)
            area = (x2 - x1) * (y2 - y1)

            center_screen = frame_width // 2
            tolerance = 40

            if center_x < center_screen - tolerance:
                print("🔥 Yangın solda → sola dön")
                sola(50)
                time.sleep(0.3)
                dur()
            elif center_x > center_screen + tolerance:
                print("🔥 Yangın sağda → sağa dön")
                saga(50)
                time.sleep(0.3)
                dur()
            else:
                if area > 20000:
                    print("🚩 Yangın ortada ve yakın → dur")
                    dur()
                else:
                    print("🔥 Yangın ortada ama uzak → ileri")
                    ileri(60)
                    time.sleep(0.3)
                    dur()
        else:
            print("❌ Yangın yok → dur")
            dur()

except KeyboardInterrupt:
    print("🛑 Kullanıcı tarafından durduruldu")

finally:
    dur()
    for pwm in [pwm_r1, pwm_l1, pwm_r2, pwm_l2]:
        pwm.stop()
    GPIO.cleanup()
    cap.release()