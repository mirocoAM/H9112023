from machine import Pin, ADC, PWM
import time

# Configuración del joystick
joystick_horz = ADC(Pin(32))
joystick_vert = ADC(Pin(33))

# Configuración del sensor de temperatura
sensor = ADC(Pin(35))

# Configuración de los LED
led_derecha = PWM(Pin(15), freq=1000)
led_izquierda = PWM(Pin(2), freq=1000)
led_abajo = PWM(Pin(4), freq=1000)
led_arriba = PWM(Pin(5), freq=1000)

# Configuración de las patitas RGB
patita_R = PWM(Pin(19), freq=1000)
patita_G = PWM(Pin(21), freq=1000)
patita_B = PWM(Pin(22), freq=1000)

# Bucle principal
while True:
    # Leer el valor del joystick horizontal
    x = joystick_horz.read()

    # Leer el valor del joystick vertical
    y = joystick_vert.read()

    # Controlar los LED basados en el joystick horizontal
    if x < 2000:
        led_izquierda.duty(1023)
    elif x > 3000:
        led_derecha.duty(1023)
    else:
        led_derecha.duty(0)
        led_izquierda.duty(0)

    # Controlar los LED basados en el joystick vertical
    if y < 2000:
        led_abajo.duty(1023)
    elif y > 3000:
        led_arriba.duty(1023)
    else:
        led_abajo.duty(0)
        led_arriba.duty(0)

    # Leer la temperatura
    temperatura = sensor.read()
    
    # Imprimir la temperatura
    print("Temperatura:", temperatura)

    # Controlar las patitas RGB basadas en la temperatura
    if temperatura < 1582:
        patita_R.duty(0)
        patita_G.duty(0)
        patita_B.duty(1023)
    elif temperatura < 3168:
        patita_R.duty(0)
        patita_G.duty(1023)
        patita_B.duty(0)
    else:
        patita_R.duty(1023)
        patita_G.duty(0)
        patita_B.duty(0)

    # Pausar un poco
    time.sleep(0.1)
