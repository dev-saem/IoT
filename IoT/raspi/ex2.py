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

COL_NUM = 3 # 행
ROW_NUM = 4 # 열

g_preData = 0

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

def initKeypad(): # PIN 설정
    for i in range(0, COL_NUM): # col input
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM): # row output, HIGH 상태
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)

def selectRow(rowNum): # 행은 신호를 줌, 
    # 받아오는 데이터가 없으면 두번째 데이터에 신호를 줌, 두번째 행에서 데이터 처리 등 반복
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
            sleep(0.001)
        else :
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
            sleep(0.001)
    return rowNum

def readCol(): # 키패드가 몇 번 col에서 눌렸는지 
    Keypadstate = -1 # 몇 번 col인지
    for i in range(0, COL_NUM): # COL_NUM : 0,1,2
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            Keypadstate = Keypadstate + (i + 2) # 1,2,3
            sleep(0.5)
    return Keypadstate

def readKeypad(): # 키패드 입력 감지 함수
    global g_preData
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)
    sleep(0.001)
    if (row1Data != -1): # row1Data가 신호가 없는 상태
        keyData = row1Data

    if runningStep == 1: # 첫 번째 행 검사
        if keyData == -1: # 첫 번째 행에서 눌린 버튼이 없음
            runningStep = selectRow(2) # 두 번째 행 검사
            row2Data = readCol() 
            selectRow(0)
            sleep(0.001)
            if (row2Data != -1): # row2Data는 신호가 들어오는 col값에서 +3
                keyData = row2Data + 3 # 4,5,6

    sleep(0.1)

    if keyData == -1:
        return -1

    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    print("\r\nKeypad Data : %d" % keyData)

    return keyData

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    initKeypad()
    print("setup keypad pin")
    try:
        while True:
            keyData = readKeypad()

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()