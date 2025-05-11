# camera_test.py
import cv2

cap = cv2.VideoCapture(0)  # USB Kamera için

if not cap.isOpened():
    print("Kamera bulunamadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı!")
        break

    cv2.imshow("Kamera Testi", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
