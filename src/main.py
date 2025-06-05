from machine import Pin, I2C
import time
import ssd1306

PIN_IN1 = 0
PIN_IN2 = 1

motor_in1 = Pin(PIN_IN1, Pin.OUT)
motor_in2 = Pin(PIN_IN2, Pin.OUT)

PIN_BOTAO1 = 2
PIN_BOTAO2 = 3
PIN_BOTAO3 = 6

botao1 = Pin(PIN_BOTAO1, Pin.IN, Pin.PULL_UP)
botao2 = Pin(PIN_BOTAO2, Pin.IN, Pin.PULL_UP)
botao3 = Pin(PIN_BOTAO3, Pin.IN, Pin.PULL_UP)

OLED_WIDTH = 128
OLED_HEIGHT = 32

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def parar_motor():
    motor_in1.value(0)
    motor_in2.value(0)
    print("Motor parado.")
    oled.fill(0)
    oled.text("QUANTAS CARTAS?", 0, 0, 1)
    oled.text("1:40 2:52 3:104", 0, 20, 1)
    oled.show()

def girar_motor(tempo_segundos, n):
    motor_in1.value(1)
    motor_in2.value(0)
    print(f"Motor girando por {tempo_segundos} segundos.")

    for i in range(tempo_segundos, 0, -1):
        oled.fill(0)
        oled.text("EMBARALHANDO", 0, 0, 1)
        oled.text(f"OPCAO {n}", 0, 14, 1)
        oled.text(f"Tempo: {i}s", 0, 24, 1)

        oled.show()
        time.sleep(1)

    parar_motor()
    print("Motor parou.")

def debounce(pin_object, tempo_debounce_ms=50):
    time.sleep_ms(tempo_debounce_ms)
    return pin_object.value() == 0


parar_motor()

try:
    while True:
        if botao1.value() == 0:
            if debounce(botao1):
                girar_motor(10, 1)
                while botao1.value() == 0:
                    time.sleep_ms(10)

        if botao2.value() == 0:
            if debounce(botao2):
                girar_motor(12, 2)
                while botao2.value() == 0:
                    time.sleep_ms(10)

        if botao3.value() == 0:
            if debounce(botao3):
                girar_motor(15, 3)
                while botao3.value() == 0:
                    time.sleep_ms(10)

        time.sleep_ms(10)

finally:
    parar_motor()
    oled.fill(0)
    oled.text("PROGRAMA FINALIZADO", 0, 0, 1)
    oled.show()