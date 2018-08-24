from Draw4Seg7LED import Draw4Seg7LED
from GetSensorTmp import GetSensorTmp
import time, sys
piMap = {
        # LED_PIN, GPIO_PIN
        'LED_PIN_1' :5,
        'LED_PIN_2' :6,
        'LED_PIN_3' :13,
        'LED_PIN_4' :19,
        'LED_PIN_5' :26,
        'LED_PIN_6' :21,
        'LED_PIN_7' :11,
        'LED_PIN_8' :9,
        'LED_PIN_9' :10,
        'LED_PIN_10':22,
        'LED_PIN_11':27,
        'LED_PIN_12':17,
}
sensorID = '28-0000098fdfa1'

def main():
    draw4Seg7LED = Draw4Seg7LED(piMap)
    try:
        gst = GetSensorTmp(sensorID)
    except IOError as e:
        print(e)
        draw4Seg7LED.cleanup()
        sys.exit(1)
    try:
        while True:
            tmp = gst.get()
            print(tmp)
            draw4Seg7LED.draw(tmp)
            time.sleep(1)
    except KeyboardInterrupt:
        draw4Seg7LED.cleanup()
        sys.exit()
    draw4Seg7LED.cleanup()


if __name__ == '__main__' :
    main()
