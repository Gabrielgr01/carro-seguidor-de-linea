from machine import Pin, PWM, ADC
import time

# Definir los pines de control para el Motor A (usando el L298)
in1 = Pin(19, Pin.OUT)  # Pin para IN1 del Motor A
in2 = Pin(18, Pin.OUT)  # Pin para IN2 del Motor A
ena = PWM(Pin(17), freq=3000)  # Pin para ENA del Motor A (PWM)
                   # se puede usar esta frecuencia para tener mayor control de las velocidades bajas 

# Definir los pines de control para el Motor B
in3 = Pin(22, Pin.OUT)  # Pin para IN3 del Motor B
in4 = Pin(23, Pin.OUT)  # Pin para IN4 del Motor B
enb = PWM(Pin(21), freq=3000)  # Pin para ENB del Motor B (PWM)

# Definir los pines de los sensores infrarrojos ANALOGICOS
IR_derecha = ADC(Pin(32))  
IR_izquierda = ADC(Pin(33)) 
IR_atras = ADC(Pin(34)) 

# Configurar cada sensor para rango completo de 0 a 3.3V
IR_derecha.atten(ADC.ATTN_11DB)  # Sensor 1
IR_izquierda.atten(ADC.ATTN_11DB)  # Sensor 2
IR_atras.atten(ADC.ATTN_11DB)  # Sensor 3

threshold = 50  # menos de 50 es blanco 

# Función para controlar la dirección y velocidad del Motor A
def motor_a(direccion, velocidad):
    if direccion == "adelante":
        in1.off()
        in2.on()
    elif direccion == "atras":
        in1.on()
        in2.off()
    
    # Ajustar la velocidad (duty cycle de PWM: 0 a 1023)
    ena.duty(velocidad)

# Función para controlar la dirección y velocidad del Motor B
def motor_b(direccion, velocidad):
    if direccion == "adelante":
        in3.on()
        in4.off()
    elif direccion == "atras":
        in3.off()
        in4.on()
    
    # Ajustar la velocidad (duty cycle de PWM: 0 a 1023)
    enb.duty(velocidad)

# Función para detener ambos motores
def detener_motores():
    # Apagar las salidas de los motores
    in1.off()
    in2.off()
    in3.off()
    in4.off()
    
    # Ajustar la velocidad (duty cycle) a 0 para detener ambos motores
    ena.duty(0)
    enb.duty(0)

def seguir_linea():
    sensorR = IR_derecha.read()
    sensorL = IR_izquierda.read()
    sensorB = IR_atras.read()

    print("Sensor lado derecho:", sensorR)
    print("Sensor lado izquierdo:", sensorL)
    print("Sensor parte de atrás:", sensorB)

    # Verificar el sensor trasero
    if sensorB > threshold: # mide negro
        print("Línea centrada.")
        motor_a("adelante", 350)
        motor_b("adelante", 350)
        time.sleep(0.5)  # Retroceder un momento
        return  # Salir de la función
    # Verificar los sensores laterales
    if sensorR < threshold and sensorL < threshold: # tanto derecha como izq en blanco 
        print("Avanzando. Línea detectada en el centro.")
        motor_a("adelante", 350)
        motor_b("adelante", 350)
    elif sensorR > threshold: # detecta negro 
        # Solo el sensor izquierdo detecta blanco
        print("Corrigiendo a la derecha.")
        motor_a("adelante", 0)  # Detener motor A
        motor_b("adelante", 350)  # Motor B avanza
    elif sensorL > threshold:
        # Solo el sensor derecho detecta blanco
        print("Corrigiendo a la izquierda.")
        motor_a("adelante", 350)  # Motor A avanza
        motor_b("adelante", 0)  # Detener motor B

# Bucle principal
while True:
    seguir_linea()
    time.sleep(0.1)
    
"""    
try:
    seguir_linea()
    time_sleep(2)
finally:
    detener_motores()
"""  
