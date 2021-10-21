import RPi.GPIO as GPIO
from flask import Flask
from time import sleep

app = Flask(__name__)
LED_1 = 4
LED_2 = 5
LED_3 = 15
LED_4 = 14

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>/<number>')
def ledonoff(onoff, number):
    if (onoff == "on") and (number == "1"):
        print("Turn on LED number 1")
        GPIO.output(LED_1, GPIO.HIGH)
        return "LED 1 on"

    elif (onoff == "on") and (number == "2"):
        print("Turn on LED number 2")
        GPIO.output(LED_2, GPIO.HIGH)
        return "LED 2 on"

    elif (onoff == "on") and (number == "3"):
        print("Turn on LED number 3")
        GPIO.output(LED_3, GPIO.HIGH)
        return "LED 3 on"

    elif (onoff == "on") and (number == "4"):
        print("Turn on LED number 4")
        GPIO.output(LED_4, GPIO.HIGH)
        return "LED 4 on"

    elif (onoff == "off") and (number == "1"):
        print("Turn off LED number 1")
        GPIO.output(LED_1, GPIO.LOW)
        return "LED 1 off"

    elif (onoff == "off") and (number == "2"):
        print("Turn off LED number 2")
        GPIO.output(LED_2, GPIO.LOW)
        return "LED 2 off"

    elif (onoff == "off") and (number == "3"):
        print("Turn off LED number 3")
        GPIO.output(LED_3, GPIO.LOW)
        return "LED 3 off"

    elif (onoff == "off") and (number == "4"):
        print("Turn off LED number 4")
        GPIO.output(LED_4, GPIO.LOW)
        return "LED 4 off"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_1, GPIO.OUT, initial = False)
    GPIO.setup(LED_2, GPIO.OUT, initial = False)
    GPIO.setup(LED_3, GPIO.OUT, initial = False)
    GPIO.setup(LED_4, GPIO.OUT, initial = False)
    app.run(host = '0.0.0.0', port = 5000, debug = True)