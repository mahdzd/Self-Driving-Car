import RPi.GPIO as GPIO
import time

clk = 17
dt = 27
sw = 22  # Optional push button

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
last_clk = GPIO.input(clk)

def sw_pressed(channel):
    global counter
    counter = 0
    print("Button pressed! Counter reset.")

GPIO.add_event_detect(sw, GPIO.FALLING, callback=sw_pressed, bouncetime=300)

try:
    while True:
        current_clk = GPIO.input(clk)
        current_dt = GPIO.input(dt)

        if current_clk != last_clk:
            if current_dt != current_clk:
                counter += 1
            else:
                counter -= 1
            print(f"Counter: {counter}")

        last_clk = current_clk
        time.sleep(0.001)

except KeyboardInterrupt:
    GPIO.cleanup()
