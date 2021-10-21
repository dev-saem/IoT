import RPi.GPIO as GPIO
from time import sleep
import GPIO_EX

ROW0_PIN = 0
ROW1_PIN = 1
ROW2_PIN = 2
ROW3_PIN = 3
COL0_PIN = 4
COL1_PIN = 5
COL2_PIN = 6

COL_NUM = 3
ROW_NUM = 4

g_preData = 0
status1 = False
status2 = False
status3 = False
status4 = False

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)

def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
            sleep(0.001)
        else :
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
            sleep(0.001)
    return rowNum

def readCol():
    Keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            Keypadstate = Keypadstate + (i + 2)
            sleep(0.5)
    return Keypadstate

def readKeypad():
    global g_preData
    global status1
    global status2
    global status3
    global status4
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)
    sleep(0.001)
    if (row1Data != -1):
        keyData = row1Data

    if runningStep == 1:
        if keyData == -1:
            runningStep = selectRow(2)
            row2Data = readCol() 
            selectRow(0)
            sleep(0.001)
            if (row2Data != -1):
                keyData = row2Data + 3

    if runningStep == 2:
        if keyData == -1:
            runningStep = selectRow(3) 
            row3Data = readCol() 
            selectRow(0)
            sleep(0.001)
            if (row3Data != -1):
                keyData = row3Data + 6

    if runningStep == 3:
        if keyData == -1:
            runningStep = selectRow(4) 
            row4Data = readCol() 
            selectRow(0)
            sleep(0.001)
            if(row4Data ==1):
                keyData = "*"
            elif(row4Data ==2):
                keyData = 0
            elif(row4Data ==3):
                keyData = "#"    
    sleep(0.1)

    if keyData == -1:
        return -1
    else :
        if keyData == 1:
            if status1 == True:
                GPIO.output(LED_1, GPIO.LOW)
                status1 = False
            else :
                GPIO.output(LED_1, GPIO.HIGH)
                status1 = True
        elif keyData == 2:
            if status2 == True:
                GPIO.output(LED_2, GPIO.LOW)
                status2 = False
            else :
                GPIO.output(LED_2, GPIO.HIGH)
                status2 = True
        elif keyData == 3:
            if status3 == True:
                GPIO.output(LED_3, GPIO.LOW)
                status3 = False
            else :
                GPIO.output(LED_3, GPIO.HIGH)
                status3 = True
        elif keyData == 4:
            if status4 == True:
                GPIO.output(LED_4, GPIO.LOW)
                status4 = False
            else :
                GPIO.output(LED_4, GPIO.HIGH)
                status4 = True
        else:
            GPIO.output(LED_1, GPIO.LOW)
            GPIO.output(LED_2, GPIO.LOW)
            GPIO.output(LED_3, GPIO.LOW)
            GPIO.output(LED_4, GPIO.LOW)
            
    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    print("\r\nKeypad Data : %s" % keyData)

    return keyData

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_1, GPIO.OUT, initial = False)
    GPIO.setup(LED_2, GPIO.OUT, initial = False)
    GPIO.setup(LED_3, GPIO.OUT, initial = False)
    GPIO.setup(LED_4, GPIO.OUT, initial = False)

    initKeypad()
    print("setup keypad pin")
    try:
        while True:
            keyData = readKeypad()

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()