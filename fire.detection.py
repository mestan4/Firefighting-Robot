from ultralytics import YOLO
import cv2

model = YOLO("your_model.pt")

def detect_fire(frame):
    results = model.predict(frame, conf=0.5, verbose=False)
    fire_detected = False
    fire_center = None

    if results and results[0].boxes:
        fire_detected = True
        fire_center = results[0].boxes.xywh[0][:2].cpu().numpy()  # (x, y) pozisyonu

    return fire_detected, fire_center
