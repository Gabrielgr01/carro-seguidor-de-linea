from machine import ADC, Pin
import time

# Definir el pin del sensor infrarrojo
sensorPin = ADC(Pin(33))  # Pin 32 es ADC1_CH4
sensorPin.atten(ADC.ATTN_11DB)  # Configurar para rango completo de 0 a 3.3V

threshold = 100  # Ajustar el umbral según las lecturas

# Bucle principal
while True:
    sensorValue = sensorPin.read()  # Leer valor del sensor infrarrojo
    print("Valor del sensor:", sensorValue)  # Mostrar el valor

    # Comparar el valor del sensor con el umbral
    if sensorValue > threshold:
        print("Línea Negra Detectada")
    else:
        print("Espacio Blanco Detectado")

    time.sleep(0.5)  # Pausa para facilitar la lectura
