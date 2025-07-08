import RPi.GPIO as GPIO
import time

IA = 5   # A-IA
IB = 6   # A-IB

GPIO.setmode(GPIO.BCM)
GPIO.setup(IA, GPIO.OUT)
GPIO.setup(IB, GPIO.OUT)

pwm_ia = GPIO.PWM(IA, 1000)  # 1kHz PWM on IA
pwm_ib = GPIO.PWM(IB, 1000)  # 1kHz PWM on IB

pwm_ia.start(0)
pwm_ib.start(0)

def forward(speed=50):
    pwm_ia.ChangeDutyCycle(speed)
    pwm_ib.ChangeDutyCycle(0)

def backward(speed=50):
    pwm_ia.ChangeDutyCycle(0)
    pwm_ib.ChangeDutyCycle(speed)

def stop():
    pwm_ia.ChangeDutyCycle(0)
    pwm_ib.ChangeDutyCycle(0)

try:
    print("Forward")
    forward(60)
    time.sleep(2)

    print("Backward")
    backward(60)
    time.sleep(2)

    print("Stop")
    stop()

except KeyboardInterrupt:
    pwm_ia.stop()
    pwm_ib.stop()
    GPIO.cleanup()