from machine import Pin, ADC, PWM

buzzer = PWM(Pin(16))
buzzer.freq(1000)
pot = ADC(28)

while True:
    freq = pot.read_u16()
    buzzer.duty_u16(freq)