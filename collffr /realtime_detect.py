from ultralytics import YOLO
import cv2

# Modeli yükle
model = YOLO('best.pt')  # kendi model dosyanın yolu

# Kamerayı aç
cap = cv2.VideoCapture(0)  # 0, varsayılan Macbook kamerası için

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Frame üzerinde tahmin yap
    results = model.predict(source=frame, conf=0.25, save=False, show=False, verbose=False)

    # Detected nesneleri çiz
    annotated_frame = results[0].plot()

    # Frame'i göster
    cv2.imshow('YOLOv8 Real-Time Detection', annotated_frame)

    # 'q' tuşuna basınca çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizle
cap.release()
cv2.destroyAllWindows()
