import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import RPi.GPIO as GPIO
import GPIO_EX
from time import sleep

lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D19)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs,lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

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

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

li = []

password = [1,2,3,4]

def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0,0)
    sleep(1.0)

def displayText(text='',col=0,row=0):
    lcd.cursor_position(col,row)
    lcd.message = text

def clearTextlcd():
    lcd.clear()
    lcd.message = 'clear LCD\nGoodbye!'
    sleep(2.0)
    lcd.clear()

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
    global li
    global password
    global res
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

    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    print("\r\nKeypad Data : %s" % keyData)

    return keyData

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    initTextlcd()
    print("start textlcd program ...")
    initKeypad()
    print("setup keypad pin")

    try:
        while(1):

            keyData = readKeypad()
            if (keyData != -1) and (len(li) < 4):
                li.append(keyData)
            elif len(li) == 4:
                li.clear()
            if keyData == "*":
                li.clear()
        
            if (li == password):
                res = "\nCORRECT"
            elif ((li != password) and (len(li) == 4)):
                res = "\nFAIL"
            else:
                res = "\n"

            line = str(li) + res
            lcd.clear()
            displayText(line,0,0)
            sleep(1)
    
    except KeyboardInterrupt:
        clearTextlcd()
        GPIO.cleanup()

if __name__ == '__main__':
    main()