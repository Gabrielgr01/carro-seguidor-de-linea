from machine import Pin, PWM, ADC
import time

# Definir los pines de control para el Motor A (usando el L298)
in1 = Pin(19, Pin.OUT)  # Pin para IN1 del Motor A
in2 = Pin(18, Pin.OUT)  # Pin para IN2 del Motor A
ena = PWM(Pin(17), freq=2000)  # Pin para ENA del Motor A (PWM)

# Definir los pines de control para el Motor B
in3 = Pin(22, Pin.OUT)  # Pin para IN3 del Motor B
in4 = Pin(23, Pin.OUT)  # Pin para IN4 del Motor B
enb = PWM(Pin(21), freq=2000)  # Pin para ENB del Motor B (PWM)

# Definir los pines de los sensores infrarrojos ANALÓGICOS
IR_derecha = ADC(Pin(32))  
IR_izquierda = ADC(Pin(35)) 

# Configurar cada sensor para rango completo de 0 a 3.3V
IR_derecha.atten(ADC.ATTN_11DB)  
IR_izquierda.atten(ADC.ATTN_11DB)  

threshold = 900  # Menos de 900 es blanco, más de 900 es negro
velocidad_base = 700  # Velocidad base de los motores

# Función para controlar la dirección y velocidad del Motor A
def motor_a(direccion, velocidad):
    if direccion == "adelante":
        in1.off()
        in2.on()
    elif direccion == "atras":
        in1.on()
        in2.off()
    else:
        in1.off()
        in2.off()
    
    ena.duty(velocidad)

# Función para controlar la dirección y velocidad del Motor B
def motor_b(direccion, velocidad):
    if direccion == "adelante":
        in3.on()
        in4.off()
    elif direccion == "atras":
        in3.off()
        in4.on()
    else:
        in3.off()
        in4.off()
    
    enb.duty(velocidad)

# Función para detener ambos motores
def detener_motores():
    motor_a("detener", 0)
    motor_b("detener", 0)

# Función para seguir la lógica de movimiento
def seguir_linea():
    sensorR = IR_derecha.read()
    sensorL = IR_izquierda.read()

    print(f"Sensor Derecho: {sensorR}, Izquierdo: {sensorL}")

    # Si ambos sensores están en blanco, avanzar en línea recta
    if sensorL < threshold and sensorR < threshold:
        print("Línea centrada. Avanzando recto.")
        motor_a("adelante", velocidad_base)
        motor_b("adelante", velocidad_base)
    
    # Si el sensor izquierdo detecta negro, corregir hacia la izquierda
    elif sensorL > threshold:
        print("Corrigiendo hacia la izquierda.")
        motor_a("adelante", 0)  # Detener motor izquierdo
        motor_b("adelante", velocidad_base)
        #time.sleep(0.1)  # Pausa para corrección

    # Si el sensor derecho detecta negro, corregir hacia la derecha
    elif sensorR > threshold:
        print("Corrigiendo hacia la derecha.")
        motor_a("adelante", velocidad_base)
        motor_b("adelante", 0)  # Detener motor derecho
        #time.sleep(0.1)  # Pausa para corrección

# Bucle principal
try:
    while True:
        seguir_linea()
        time.sleep(0.1)  # Delay entre las actualizaciones
finally:
    detener_motores()
