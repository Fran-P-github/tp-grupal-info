# Se importan los modulos o librerias necesarias
from machine import Pin
import utime        # Este modulo permite establecer un delay o retardo al programa
import tm1637       # Este modulo permite el control del display de 7 segmentos

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))  # Se crea un objeto del display y se le asignan los pines
                                            # 5 para el clock y 4 para el data input/output

# Se asignan los pines que se van a utilizar
buzz = Pin(10, Pin.OUT)     # Pin 10 -> buzzer (salida/output)
led1 = Pin(11, Pin.OUT)     # Pin 11 -> led 1  (salida/output)
led2 = Pin(12, Pin.OUT)     # Pin 12 -> led 2  (salida/output)
led3 = Pin(13, Pin.OUT)     # Pin 13 -> led 3  (salida/output)
led4 = Pin(14, Pin.OUT)     # Pin 14 -> led 4  (salida/output)
led5 = Pin(15, Pin.OUT)     # Pin 15 -> led 5  (salida/output)

trig = Pin(16, Pin.OUT)     # Pin 16 -> trigger del sensor (salida/output)
echo = Pin(17, Pin.IN)      # Pin 17 <- echo del sensor    (entrada/input)

# Se define una funcion para facilitar el encendido y apagado de las salidas
# (leds y buzzer)
# La funcion recibe como parametros (l1, ..., b) los valores a asignar a cada salida
# estos valores pueden ser (1 para encendido o 0 para apagado)
def out(l1, l2, l3, l4, l5, b):
        led1.value(l1)
        led2.value(l2)
        led3.value(l3)
        led4.value(l4)
        led5.value(l5)
        buzz.value(b)

# Se define una funcion para realizar la medicion de la distancia
# Segun las especificaciones del sensor, este debe recibir una señal
# que debe estar apagada por 2 microsegundos y encendida por 5 microsegundos
def distancia():
    # Se envia la señal al sensor
    trig.low()                      # Se apaga el pin asignado al trigger del sensor
    utime.sleep_us(2)               # Se realiza un delay de 2 microsegundos
    trig.high()                     # Se enciende el pin del trigger
    utime.sleep_us(5)               # Se realiza un delay de 5 microsegundos
    trig.low()                      # Se apaga el pin del trigger

    # Se mide el tiempo que tarda en volver la señal de sonido
    # que envia el sensor
    while echo.value() == 0:
        sigoff = utime.ticks_us()   # Se cuenta hasta el ultimo momento en que no vuelve
    while echo.value() == 1:
        sigon = utime.ticks_us()    # Se cuenta el momento en el que vuelve la señal

    timepassed = sigon - sigoff     # Para determinar el tiempo pasado se hace una diferencia
                                    # entre los dos tiempos capturados

    distance = int((timepassed * 0.0343) / 2)   # Con la formula de la velocidad se obtiene
                                                # la distancia total que recorre la señal de sonido en cm
                                                # la distancia al objeto es la mitad de la total

    return distance     # La funcion devuelve el valor de la distancia


# Se define una funcion para determinar las distancias a las que se enciende
# cada salida, para esto se tomo como rango de distancia maxima 20 cm
def rango(d):
    if d <= 4: out(1,1,1,1,1,1)             # Cuando la distancia es critica (menor a 4 cm) se encienden
    if d <= 8 and d > 4: out(1,1,1,1,0,0)   # todas las salidas
    if d <= 12 and d > 8: out(1,1,1,0,0,0)
    if d <= 16 and d > 12: out(1,1,0,0,0,0)
    if d <= 20 and d > 16: out(1,0,0,0,0,0)
    if d > 20: out(0,0,0,0,0,0)             # Cuando la distancia es mayor a 20 cm se apagan todas las salidas

# Se crea el loop principal del programa, donde se realizara constantemente
# la medicion de distancia y en funcion de esta se cambiaran los valores
# de las salidas
while True:
    d = distancia()     # Se obtiene la distancia llamando a la funcion definida previamente
    rango(d)            # Se realiza el control de las salidas en funcion de la distancia obtenida
    tm.number(d)        # Se escribe en el display de 7 segmentos la distancia obtenida
    utime.sleep(0.3)    # Se realiza un delay de 0.3 segundos para poder detectar los cambios facilmente
