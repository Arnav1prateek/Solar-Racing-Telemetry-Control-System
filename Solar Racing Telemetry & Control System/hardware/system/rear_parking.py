import RPi.GPIO as GPIO
import time

# GPIO setup specifically for the parking script
GPIO.setmode(GPIO.BCM)
BUZZER = 24
# TRIGGER and ECHO should be your ultrasonic sensor pins
TRIG = 23 
ECHO = 24 

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0: start_time = time.time()
    while GPIO.input(ECHO) == 1: stop_time = time.time()
    
    duration = stop_time - start_time
    distance = (duration * 34300) / 2
    return distance

try:
    print("Rear Parking Assist Active...")
    while True:
        dist = get_distance()
        if dist < 30: # Beep faster as object gets closer
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(dist/100)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
