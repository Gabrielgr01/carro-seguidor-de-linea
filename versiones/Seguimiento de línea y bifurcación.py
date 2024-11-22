from machine import Pin, PWM, ADC
import time

# Selector de la dirección de viraje cuando se da una bifurcación
# 0 --> derecha
# 1 --> izquierda
bifur_sel = 0

# Definir los pines de control para el Motor A (usando el L298)
in1 = Pin(19, Pin.OUT)  # Pin para IN1 del Motor A
in2 = Pin(18, Pin.OUT)  # Pin para IN2 del Motor A
ena = PWM(Pin(5), freq=2000)  # Pin para ENA del Motor A (PWM)

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
velocidad_base = 550  # Velocidad base de los motores
velocidad_inicial = 550

# Función para controlar la dirección y velocidad del Motor A
# El motor A es le izquierdo
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
# El motor B es el derecho
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
# El parámetro dir indíca la dirección en la que avanza el carro
def seguir_linea(dir):
    sensorR = IR_derecha.read()
    sensorL = IR_izquierda.read()
    giro_a = velocidad_base
    giro_b = 0

    if (dir == "adelante"):
        giro_a = velocidad_base
        giro_b = 0
    elif (dir == "atras"):
        giro_a = 0
        giro_b = velocidad_base


    #print(f"Sensor Derecho: {sensorR}, Izquierdo: {sensorL}")

    # Si ambos sensores están en blanco, avanzar en línea recta
    if sensorL < threshold and sensorR < threshold:
        motor_a(dir , velocidad_base)
        motor_b(dir , velocidad_base)
    
    # Si el sensor izquierdo detecta negro, corregir hacia la izquierda
    elif (sensorL > threshold) and (sensorR < threshold):
        motor_a(dir , giro_b)  # Detener motor izquierdo
        motor_b(dir , giro_a)
    
    # Si el sensor derecho detecta negro, corregir hacia la derecha
    elif (sensorR > threshold) and (sensorL < threshold):
        motor_a(dir , giro_a)
        motor_b(dir , giro_b)  # Detener motor derecho

    # Manejo de la bifurcación
    # Si ambos sensores detectan negro se gira en una dirección seleccionada 
    # con la variable global bifur_sel
    elif (sensorR > threshold) and (sensorL > threshold):
        
        if (bifur_sel == 0):
            motor_a(dir , giro_a)
            motor_b(dir , giro_b) 

        elif (bifur_sel == 1):
            motor_a(dir , giro_b)
            motor_b(dir , giro_a)
        

def arranque():
    motor_a("adelante", velocidad_inicial)
    motor_b("adelante", velocidad_inicial)
    time.sleep(0.2)

def retroceso():
    star_time = time.time()
    while end_time - start_time < 3:
        seguir_linea("atras")
        end_time
    

# Bucle principal
try:
    time.sleep(15)
    arranque()
    while True:
        seguir_linea("atras")
        time.sleep(0.08)  # Delay entre las actualizaciones
        detener_motores()
        time.sleep(0.1)
finally:
    detener_motores()

