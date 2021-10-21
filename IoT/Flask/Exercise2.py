import RPi.GPIO as GPIO
from flask import Flask
from time import sleep

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/fan/<onoff>/<time>')
def fanonoff(onoff, time):
    if (onoff == "on") and (time == "1"):
        print("FAN on for one second")
        GPIO.output(18,1)
        GPIO.output(27,0)
        sleep(1.0)
        GPIO.output(18,0)
        GPIO.output(27,0)
        return "FAN on for 1 second"

    elif (onoff == "on") and (time == "2"):
        print("FAN on for two second")
        GPIO.output(18,1)
        GPIO.output(27,0)
        sleep(2.0)
        GPIO.output(18,0)
        GPIO.output(27,0)
        return "FAN on for 2 seconds"

    elif (onoff == "on") and (time == "3"):
        print("FAN on for three second")
        GPIO.output(18,1)
        GPIO.output(27,0)
        sleep(3.0)
        GPIO.output(18,0)
        GPIO.output(27,0)
        return "FAN on for 3 seconds"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(18, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(27, GPIO.OUT, initial = GPIO.LOW)
    app.run(host = '0.0.0.0', port = 5000, debug = True)