from machine import Pin
import utime
import tm1637

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))

buzz = Pin(10, Pin.OUT)
led1 = Pin(11, Pin.OUT)
led2 = Pin(12, Pin.OUT)
led3 = Pin(13, Pin.OUT)
led4 = Pin(14, Pin.OUT)
led5 = Pin(15, Pin.OUT)

trig = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)

def out(l1, l2, l3, l4, l5, b):
        led1.value(l1)
        led2.value(l2)
        led3.value(l3)
        led4.value(l4)
        led5.value(l5)
        buzz.value(b)

def distancia():
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(5)
    trig.low()
    while echo.value() == 0:
        sigoff = utime.ticks_us()
    while echo.value() == 1:
        sigon = utime.ticks_us()
    timepassed = sigon - sigoff
    distance = int((timepassed * 0.0343) / 2)
    return distance

def rango(d):
    if d <= 4: out(1,1,1,1,1,1)
    if d <= 8 and d > 4: out(1,1,1,1,0,0)
    if d <= 12 and d > 8: out(1,1,1,0,0,0)
    if d <= 16 and d > 12: out(1,1,0,0,0,0)
    if d <= 20 and d > 16: out(1,0,0,0,0,0)
    if d > 20: out(0,0,0,0,0,0)

while True:
    d = distancia()
    rango(d)
    tm.number(d)
    utime.sleep(0.3)