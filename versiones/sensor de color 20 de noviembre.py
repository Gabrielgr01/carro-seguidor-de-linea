from machine import Pin, time_pulse_us
import time

# Pines de conexión
S0 = Pin(16, Pin.OUT)
S1 = Pin(15, Pin.OUT)
S2 = Pin(12, Pin.OUT)
S3 = Pin(14, Pin.OUT)
OUT = Pin(13, Pin.IN)

# Configuración de frecuencia (S0 y S1)
S0.value(0)  # media frecuencia para 2%
S1.value(1)

# Función para medir la frecuencia
def read_frequency(color_filter):
    # Configuración del filtro de color (S2 y S3)
    S2.value(color_filter[0])
    S3.value(color_filter[1])
    time.sleep(0.01)  # Pequeña pausa para estabilizar
    pulse_time = time_pulse_us(OUT, 1, 1000000)  # Tiempo de pulso en microsegundos
    if pulse_time < 0:
        return 0  # Error de lectura
    return 10000 // pulse_time  # Convertir a frecuencia en Hz

# Detectar color dominante
def detect_color():
    # Lecturas de cada canal
    red = read_frequency((0, 0))
    green = read_frequency((1, 1))
    blue = read_frequency((0, 1))
    
    print(f"R: {red}, G: {green}, B: {blue}")
    
    # Criterios para detectar colores
#    if red < 5000 and green < 5000 and blue < 5000:
#        return "Negro"
    if red > 60 and green > 60 and blue > 60:
        return "Blanco"
    elif red > green and red > blue :
        return "Rojo"
    elif green > red  and green > blue :
        return "Verde"
    elif blue > red  and blue > green :
        return "Azul"
    else:
        return "Desconocido"

# Bucle principal
while True:
    color = detect_color()
    print(f"Color detectado: {color}")
    #time.sleep(1)
