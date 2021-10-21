import RPi.GPIO as GPIO
from flask import Flask
from time import sleep

app = Flask(__name__)
LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>/<mode>')
def ledonoff(onoff, mode):
    if (onoff == "on") and (mode == "nomode"):
        print("LED Turn on")
        GPIO.output(LED_1, GPIO.HIGH)
        GPIO.output(LED_2, GPIO.HIGH)
        GPIO.output(LED_3, GPIO.HIGH)
        GPIO.output(LED_4, GPIO.HIGH)
        return "LED on"

    elif (onoff == "off") and (mode == "nomode"):
        print("LED Turn off")
        GPIO.output(LED_1, GPIO.LOW)
        GPIO.output(LED_2, GPIO.LOW)
        GPIO.output(LED_3, GPIO.LOW)
        GPIO.output(LED_4, GPIO.LOW)
        return "LED off"

    elif (onoff == "on") and (mode == "partymode"):
        print("LED Party mode")
        for i in range(5):
            GPIO.output(LED_1, GPIO.LOW)
            GPIO.output(LED_2, GPIO.LOW)
            GPIO.output(LED_3, GPIO.LOW)
            GPIO.output(LED_4, GPIO.LOW)
            sleep(0.5)
            GPIO.output(LED_1, GPIO.HIGH)
            GPIO.output(LED_2, GPIO.HIGH)
            GPIO.output(LED_3, GPIO.HIGH)
            GPIO.output(LED_4, GPIO.HIGH)
            sleep(0.5)
        return "Party mode"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_1, GPIO.OUT, initial = False)
    GPIO.setup(LED_2, GPIO.OUT, initial = False)
    GPIO.setup(LED_3, GPIO.OUT, initial = False)
    GPIO.setup(LED_4, GPIO.OUT, initial = False)
    app.run(host = '0.0.0.0', port = 5000, debug = True)