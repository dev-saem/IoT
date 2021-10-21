import RPi.GPIO as GPIO # 라즈베리파이의 GPIO 사용하게 해주는 모듈
from time import sleep # 시간과 관련된 모듈

LED_1 = 4 # 핀 번호 입력

def main():
    GPIO.setmode(GPIO.BCM) # GPIO의 사용할 핀모드 설정 (BCM모드 : GPIO의 핀넘버로 핀을 셋팅)
    GPIO.setwarnings(False)
    GPIO.setup(LED_1, GPIO.OUT, initial = False) # 지정한 핀번호의 입출력모드 지정, 초기화
    print("main() program running...")

    try :
        while True:
            GPIO.output(LED_1, GPIO.HIGH) # true, 1, GPIO.HIGH : 켜진 상태
            sleep(0.5) # 딜레이
            GPIO.output(LED_1, GPIO.LOW) # false, 0, GPIO.LOW : 꺼진 상태
            sleep(0.5) # 딜레이

    except KeyboardInterrupt:
        GPIO.cleanup() # GPIO 핀 초기화

if __name__ == '__main__':
    main()
