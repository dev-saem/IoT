import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import GPIO_EX
import RPi.GPIO as GPIO
from time import sleep

import numpy as np
import cv2
import pickle

import threading

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

res = ''

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

#-----------------------------------------------------------------------------------

is_obama = 0

def image():
    global is_obama

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            # print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w] # (ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                # print(5: #id_)
                # # print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
                if name == "obama":
                    is_obama = 1
                    
                elif name == "clinton":
                    is_obama = 2

                else:
                    is_obama = 0
                    
            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # subitems = smile_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in subitems:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    initTextlcd()
    print("start textlcd program ...")
    initKeypad()
    print("setup keypad pin")
    global res

    try:
        while(1):

            if is_obama == 1:
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
                sleep(1.0)

            elif is_obama == 2:
                line1 = "ACCESS DENIED"
                lcd.clear()
                displayText(line1,0,0)
                sleep(1.0)

            else:
                line2 = ""
                displayText(line2,0,0)

    except KeyboardInterrupt:
        clearTextlcd()
        GPIO.cleanup()

if __name__ == '__main__':
    global t
    t = threading.Thread(target = image)
    t.daemon = True
    t.start()
    main()