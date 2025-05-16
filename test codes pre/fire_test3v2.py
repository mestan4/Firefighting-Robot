import cv2
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

model = YOLO("best.pt")

# === Motor 1 (Sol) ===
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25
M1_LEN  = 16

# === Motor 2 (Sağ) ===
M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5
M2_LEN  = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

pwm1 = GPIO.PWM(M1_REN, 1000)
pwm2 = GPIO.PWM(M1_LEN, 1000)
pwm3 = GPIO.PWM(M2_REN, 1000)
pwm4 = GPIO.PWM(M2_LEN, 1000)

for pwm in [pwm1, pwm2, pwm3, pwm4]:
    pwm.start(0)

def ileri(hiz=50):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.ChangeDutyCycle(hiz)

def sola(hiz=50):
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, True)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, True)
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.ChangeDutyCycle(hiz)

def saga(hiz=50):
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.ChangeDutyCycle(hiz)

def dur():
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, False)
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, False)
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.ChangeDutyCycle(0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

start_time = time.time()
frame_count = 0
fire_lost_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        results = model(frame, imgsz=320)[0]
        boxes = results.boxes

        if len(boxes) > 0:
            fire_lost_count = 0
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
                print("🔥 Yangın solda → SOLA dönülüyor")
                sola(50)
                time.sleep(0.1)
                dur()
            elif center_x > center_screen + tolerance:
                print("🔥 Yangın sağda → SAĞA dönülüyor")
                saga(50)
                time.sleep(0.1)
                dur()
            else:
                if area > 20000:
                    print("🚩 Yangın ortada ve yakın → dur")
                    dur()
                else:
                    print("🔥 Yangın ortada ama uzak → ileri gidiliyor")
                    ileri(60)
                    time.sleep(0.3)
                    dur()
        else:
            fire_lost_count += 1
            print(f"❌ Yangın tespit edilmedi ({fire_lost_count})")

            if fire_lost_count >= 3:
                print("🛑 Yangın kayboldu → duruluyor")
                dur()

        # FPS ölç ve yaz
        if frame_count % 10 == 0:
            end_time = time.time()
            fps = 10 / (end_time - start_time)
            print(f"📸 FPS: {fps:.2f}")
            start_time = time.time()

except KeyboardInterrupt:
    print("🛑 Kullanıcı tarafından durduruldu")

finally:
    dur()
    for pwm in [pwm1, pwm2, pwm3, pwm4]:
        pwm.stop()
    GPIO.cleanup()
    cap.release()
