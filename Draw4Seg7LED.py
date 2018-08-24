import RPi.GPIO as GPIO
from threading import (Event, Thread)
import time, re

class Draw4Seg7LED():
    def __init__(self, pinMap):
        self.outPutStr = ''
        self.pinMap = pinMap
        GPIO.setmode(GPIO.BCM)
        for pinName in pinMap:
            GPIO.setup(pinMap[pinName], GPIO.OUT)
            GPIO.output(pinMap[pinName], 0)

        self.anodePins = [
            'LED_PIN_12',
            'LED_PIN_9',
            'LED_PIN_8',
            'LED_PIN_6'
        ]
        self.cathodePins = [
            'LED_PIN_11',#A
            'LED_PIN_7' ,#B
            'LED_PIN_4' ,#C
            'LED_PIN_2' ,#D
            'LED_PIN_1' ,#E
            'LED_PIN_10',#F
            'LED_PIN_5' ,#G
            'LED_PIN_3'  #DP
        ]
        self.__drawThreadStopFlag = 'RUN'
        self.__drawThread = Thread(target=self.__drawStr)
        self.__drawThread.start()

    def draw(self, s):
        reg = r'^(\d\.?){4}$'
        if not re.match(reg, s):
            raise Exception('The format of the input character string is incorrect.') 
        self.outPutStr = s

    def cleanup(self):
        self.__drawThreadStopFlag = 'END'
        self.__drawThread.join()
        GPIO.cleanup(self.pinMap.values())

    def __drawStr(self):
        while self.__drawThreadStopFlag == 'RUN':
            if self.outPutStr == '':
                self.__clearLED()
                time.sleep(0.001)
                continue
            outPutStrList = list(self.outPutStr)
            for i in range(len(outPutStrList)-1):
                if outPutStrList[i] == '.':
                    outPutStrList[i-1] = outPutStrList[i-1] + outPutStrList.pop(i)
            for i in range(4):
                outPutOneSeqStr = outPutStrList[i]
                anodeLowPin = self.anodePins[i]
                self.__drawOneSeg(anodeLowPin, outPutOneSeqStr)
                time.sleep(0.001)
                self.__clearLED()
                time.sleep(0.001)

    def __clearLED(self):
        GPIO.output(self.pinMap.values(), 0)

    def __drawOneSeg(self, anodeLowPin, s):
        anodeHighPins = self.anodePins[:]
        anodeHighPins.remove(anodeLowPin)
        GPIO.output(self.pinMap[anodeLowPin], 0)
        for anodeHighPin in anodeHighPins:
            GPIO.output(self.pinMap[anodeHighPin], 1)

        numList = {
            #      A  B  C  D  E  F  G  DP
            '1':  [0, 1, 1, 0, 0, 0, 0, 0],
            '2':  [1, 1, 0, 1, 1, 0, 1, 0],
            '3':  [1, 1, 1, 1, 0, 0, 1, 0],
            '4':  [0, 1, 1, 0, 0, 1, 1, 0],
            '5':  [1, 0, 1, 1, 0, 1, 1, 0],
            '6':  [1, 0, 1, 1, 1, 1, 1, 0],
            '7':  [1, 1, 1, 0, 0, 0, 0, 0],
            '8':  [1, 1, 1, 1, 1, 1, 1, 0],
            '9':  [1, 1, 1, 1, 0, 1, 1, 0],
            '0':  [1, 1, 1, 1, 1, 1, 0, 0],
            '1.': [0, 1, 1, 0, 0, 0, 0, 1],
            '2.': [1, 1, 0, 1, 1, 0, 1, 1],
            '3.': [1, 1, 1, 1, 0, 0, 1, 1],
            '4.': [0, 1, 1, 0, 0, 1, 1, 1],
            '5.': [1, 0, 1, 1, 0, 1, 1, 1],
            '6.': [1, 0, 1, 1, 1, 1, 1, 1],
            '7.': [1, 1, 1, 0, 0, 0, 0, 1],
            '8.': [1, 1, 1, 1, 1, 1, 1, 1],
            '9.': [1, 1, 1, 1, 0, 1, 1, 1],
            '0.': [1, 1, 1, 1, 1, 1, 0, 1],
            'None': [0, 0, 0, 0, 0, 0, 0, 0],
            }
        for i in range(8):
            cathodePin = self.cathodePins[i]
            GPIO.output(self.pinMap[cathodePin], numList[s][i])
