from machine import Pin, ADC
import time

# Configuración de LEDs y pines
led_pins = [15, 2, 4, 17]  # Cambiar los pines según la configuración real
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

rgb_led_pins = [16, 21, 19]  # Cambiar los pines según la configuración real para la LED RGB
rgb_leds = [Pin(pin, Pin.OUT) for pin in rgb_led_pins]

# Configuración del sensor de temperatura NTC
temp_sensor_pin = 35  # Cambiar el pin según la configuración real
adc_temp_sensor = ADC(Pin(temp_sensor_pin))
adc_temp_sensor.atten(ADC.ATTN_11DB)  # Ajusta la ganancia del ADC según sea necesario

joy_x_pin = 33  # Cambiar el pin según la configuración real
joy_y_pin = 32  # Cambiar el pin según la configuración real

adc_x = ADC(Pin(joy_x_pin))
adc_y = ADC(Pin(joy_y_pin))

adc_x.atten(ADC.ATTN_11DB)  # Cambiar la ganancia del ADC según sea necesario
adc_y.atten(ADC.ATTN_11DB)  # Cambiar la ganancia del ADC según sea necesario

# Establece los valores mínimo y máximo del joystick según tu sensibilidad deseada
x_min = 1000
x_max = 4000
y_min = 1000
y_max = 4000

# Función para mapear un valor de un rango a otro
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Función para controlar los LEDs en función de los valores del joystick
def control_leds(x_value, y_value):
    for led in leds:
        led.off()

    x_value_mapped = map_value(x_value, x_min, x_max, 0, 1023)
    y_value_mapped = map_value(y_value, y_min, y_max, 0, 1023)

    if x_value_mapped < 300:
        leds[0].on()  # Izquierda
    elif x_value_mapped > 700:
        leds[1].on()  # Derecha

    if y_value_mapped < 300:
        leds[2].on()  # Arriba
    elif y_value_mapped > 700:
        leds[3].on()  # Abajo

# Función para controlar la LED RGB en base a los valores brutos del sensor NTC
def control_rgb_led(temp_reading):
    for led in rgb_leds:
        led.off()
    
    if temp_reading > 3000:  # Ajusta este valor según tu escala
        # Rojo
        rgb_leds[0].on()
    elif temp_reading > 2000:  # Ajusta este valor según tu escala
        # Verde
        rgb_leds[1].on()
    else:
        # Azul
        rgb_leds[2].on()


try:
    while True:
        x_value = adc_x.read()
        y_value = adc_y.read()
        
        control_leds(x_value, y_value)
        
        # Lee la temperatura desde el sensor NTC
        temp_reading = adc_temp_sensor.read()
        
        # Imprime la lectura en la consola
        print("Lectura de temperatura NTC:", temp_reading)
        
        # Controla la LED RGB según la lectura bruta del sensor
        control_rgb_led(temp_reading)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
