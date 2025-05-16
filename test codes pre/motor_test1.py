# motor_test.py
import RPi.GPIO as GPIO
import time

# === Motor 1 (Sol) ===
M1_RPWM = 18
M1_LPWM = 19
M1_REN  = 25  # PWM
M1_LEN  = 16  # Enable

# === Motor 2 (Sağ) ===
M2_RPWM = 13
M2_LPWM = 12
M2_REN  = 5   # PWM
M2_LEN  = 6   # Enable

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [M1_RPWM, M1_LPWM, M1_REN, M1_LEN, M2_RPWM, M2_LPWM, M2_REN, M2_LEN]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Enable pinlerini HIGH yap
GPIO.output(M1_LEN, True)
GPIO.output(M2_LEN, True)

# PWM başlat
pwm1 = GPIO.PWM(M1_REN, 1000)  # Sol motor
pwm2 = GPIO.PWM(M2_REN, 1000)  # Sağ motor
pwm1.start(0)
pwm2.start(0)

try:
    print("🧪 Sol motor ileri")
    GPIO.output(M1_RPWM, True)
    GPIO.output(M1_LPWM, False)
    pwm1.ChangeDutyCycle(70)
    time.sleep(2)

    print("🧪 Sol motor geri")
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, True)
    pwm1.ChangeDutyCycle(70)
    time.sleep(2)

    # Sol motor durdur
    GPIO.output(M1_RPWM, False)
    GPIO.output(M1_LPWM, False)
    pwm1.ChangeDutyCycle(0)

    print("🧪 Sağ motor ileri")
    GPIO.output(M2_RPWM, True)
    GPIO.output(M2_LPWM, False)
    pwm2.ChangeDutyCycle(70)
    time.sleep(2)

    print("🧪 Sağ motor geri")
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, True)
    pwm2.ChangeDutyCycle(70)
    time.sleep(2)

    # Sağ motor durdur
    GPIO.output(M2_RPWM, False)
    GPIO.output(M2_LPWM, False)
    pwm2.ChangeDutyCycle(0)

finally:
    print("🧹 GPIO temizleniyor...")
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("✅ Test tamamlandı.")
