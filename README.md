# 🔥 Firefighting Robot Project

This is a collaborative project where we design an autonomous robot that can:
- Detect fire using a camera and computer vision 🔥
- Detect and avoid obstacles (like cups, walls, etc.) 🚧
- Navigate toward the fire source and stop nearby 🚶‍♂️💥

## 🎯 Goals

- ✅ Real-time fire detection with Roboflow-trained model
- ✅ Obstacle detection using image processing
- 🛠️ Integration with hardware (motors, sensors)

## 🧰 Technologies Used

- Python (OpenCV, Roboflow API)
- Google Colab
- Arduino / Raspberry Pi (optional)
- GitHub for version control

## 🧠 Core Logic

### 🔹 robot_control/main_control.py
This script handles the **core control logic** of the robot:

- Controls motor movement (forward, left, right, stop)
- Reads distance from the ultrasonic sensor to detect obstacles
- Captures live camera feed and performs basic **line following** using OpenCV
- Integrates all decision-making in a single loop

## 🤝 Contributors
- @mestan4 - Tolgahan Mestan Kaya 
- @caginhakan1 - Çağın Hakan Denizci
- @yigitd07 - Yiğit Dilek

## 📁 Folder Structure

