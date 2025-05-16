# == ateşe gidiş testi

import cv2
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

# 🔥 Modeli yükle
model = YOLO("best.pt")  # kendi model dosya adını yaz

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

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# PWM başlat
pwm1 = GPIO.PWM(M1_REN, 1000)  # Sol motor
pwm2 = GPIO.PWM(M2_REN, 1000)  # Sağ motor
pwm1.start(0)
pwm2.start(0)

# 🚗 Motor kontrol fonksiyonları
def ileri(hiz=50):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)
    GPIO.output(M1_LEN, True)
    GPIO.output(M2_LEN, True)
    pwm1.ChangeDutyCycle(hiz)
    pwm2.ChangeDutyCycle(hiz)

def sola(hiz=50):
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, True)
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)
    GPIO.output(M1_LEN, True)
    GPIO.output(M2_LEN, True)
    pwm1.ChangeDutyCycle(hiz)
    pwm2.ChangeDutyCycle(hiz)

def saga(hiz=50):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, True)
    GPIO.output(M1_LEN, True)
    GPIO.output(M2_LEN, True)
    pwm1.ChangeDutyCycle(hiz)
    pwm2.ChangeDutyCycle(hiz)

def dur():
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, False)
    GPIO.output(M1_LEN, False)
    GPIO.output(M2_LEN, False)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

# 📷 Kamera başlat
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        boxes = results.boxes

        if len(boxes) > 0:
            # En büyük yangını seç
            largest_box = max(boxes, key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1]))
            x1, y1, x2, y2 = largest_box.xyxy[0]
            center_x = int((x1 + x2) / 2)

            # 🔄 Ortalamaya göre karar
            center_screen = frame_width // 2
            tolerance = 40  # piksel toleransı

            if center_x < center_screen - tolerance:
                print("🔥 Yangın solda → sola dön")
                sola(50)
                time.sleep(0.2)
                dur()
            elif center_x > center_screen + tolerance:
                print("🔥 Yangın sağda → sağa dön")
                saga(50)
                time.sleep(0.2)
                dur()
            else:
                print("✅ Yangın ortada → ileri")
                ileri(60)
                time.sleep(0.3)
                dur()
        else:
            print("❌ Yangın tespit edilmedi")
            dur()

        # Görüntü göster (test için)
        cv2.imshow("Kamera", frame)
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("🛑 Kullanıcı durdurdu")

finally:
    dur()
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
