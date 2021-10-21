import RPi.GPIO as GPIO

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>')
def ledonoff(onoff):
    if onoff == "on":
        print("LED Turn on")
        GPIO.output(4,1)
        return "LED on"
    elif onoff == "off":
        print("LED Turn off")
        GPIO.output(4,0)
        return "LED off"

@app.route('/fan/<onoff>')
def fanonoff(onoff):
    if onoff == "on":
        print("FAN Turn on")
        GPIO.output(18,1)
        GPIO.output(27,0)
        return "FAN on"
    elif onoff == "off":
        print("FAN Turn off")
        GPIO.output(18,0)
        GPIO.output(27,0)
        return "FAN off"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(18, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(27, GPIO.OUT, initial = GPIO.LOW)
    app.run(host = '0.0.0.0', port = 5000, debug = True)