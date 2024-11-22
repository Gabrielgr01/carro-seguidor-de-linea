from machine import Pin, time_pulse_us
import time

# Pines de conexión
S0 = Pin(2, Pin.OUT)
S1 = Pin(15, Pin.OUT)
S2 = Pin(12, Pin.OUT)
S3 = Pin(14, Pin.OUT)
OUT = Pin(13, Pin.IN)

# Configuración de frecuencia (S0 y S1)
S0.value(0)  # Media frecuencia para 2%
S1.value(1)

# Función para medir la frecuencia
def read_frequency(color_filter):
    # Configuración del filtro de color (S2 y S3)
    S2.value(color_filter[0])
    S3.value(color_filter[1])
    time.sleep(0.05)  # Pequeña pausa para estabilizar 0.05 mejor valor hasta ahora
    pulse_time = time_pulse_us(OUT, 1, 10000)  # Tiempo de pulso en microsegundos
    if pulse_time <= 0:
        return 0  # Error de lectura
    return 10000 // pulse_time  # Convertir a frecuencia en Hz

# Detectar color en una medición
def detect_single_color():
    red = read_frequency((0, 0))
    green = read_frequency((1, 1))
    blue = read_frequency((0, 1))
    print(f"R: {red}, G: {green}, B: {blue}")
    
    # Criterios para detectar colores
    if red < 40 and green < 40 and blue < 40:
        return "Negro"
    elif red > 50 and green > 50 and blue > 50:
        return "Blanco"
    elif red > green and red > blue:
        return "Rojo"
    elif green > red and green > blue:
        return "Verde"
    elif blue > red and blue > green:
        return "Azul"
    else:
        return "Desconocido"

# Detectar color dominante en 10 mediciones
def detect_color():
    counts = {"Blanco": 0, "Rojo": 0, "Verde": 0, "Azul": 0, "Negro": 0}

    for _ in range(10):  # Realizar 10 mediciones
        color = detect_single_color()
        if color in counts:
            counts[color] += 1
        #time.sleep(0.1)  # Breve pausa entre mediciones

    # Determinar el color con más ocurrencias
    detected_color = max(counts, key=counts.get)
    print(f"Conteo de colores: {counts}")
    return detected_color

# Bucle principal
try:
    while True:
        color = detect_color()
        print(f"Color dominante detectado: {color}")
        time.sleep(1)  # Pausa antes de repetir
finally:
    print("Finalizando...")
