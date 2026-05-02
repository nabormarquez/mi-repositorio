import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# --- CONFIGURACIÓN INICIAL ---
puerto_com = 'COM3'  # <--- ASEGÚRATE DE QUE ESTE SEA TU PUERTO
baudios = 115200

try:
    ser = serial.Serial(puerto_com, baudios, timeout=0.1)
    time.sleep(2)  # Espera a que el Arduino reinicie
    ser.reset_input_buffer() # LIMPIEZA INICIAL: Borra basura acumulada
    print(f"Conectado a {puerto_com} con éxito.")
except Exception as e:
    print(f"ERROR: No se pudo conectar. Revisa el puerto: {e}")
    exit()

# Listas para almacenar los datos
datos_pot = []
datos_temp = []

# Crear la figura con dos sub-gráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

def actualizar(i):
    # ANTI-LAG: Si hay muchos datos en espera, vaciamos el buffer
    if ser.in_waiting > 100:
        ser.reset_input_buffer()

    if ser.in_waiting > 0:
        try:
            # Leer línea y decodificar
            linea = ser.readline().decode('utf-8').strip()
            valores = linea.split(',')
            
            if len(valores) == 2:
                # 1. Procesar Potenciómetro (Convertir a Voltaje 0-5V)
                v_pot = (int(valores[0]) * 5.0) / 1023.0
                
                # 2. Procesar Sensor LM35 (Convertir a Celsius)
                # Fórmula: (Lectura * 5 / 1023) * 100
                v_temp = (int(valores[1]) * 5.0) / 1023.0
                celsius = v_temp * 100.0 + 14.0 # El + 14 es para ajustar la temperatura a una mas realista
                
                # Guardar datos en las listas
                datos_pot.append(v_pot)
                datos_temp.append(celsius)
                
                # Mantener solo los últimos 60 puntos para que no se amontone
                if len(datos_pot) > 60:
                    datos_pot.pop(0)
                    datos_temp.pop(0)

                # --- GRÁFICA 1: POTENCIÓMETRO ---
                ax1.cla()
                ax1.plot(datos_pot, color='cyan', linewidth=2, label='Voltaje')
                ax1.set_title(f"POTENCIÓMETRO: {v_pot:.2f} V", fontsize=14, color='blue')
                ax1.set_ylim(-0.2, 5.2)
                ax1.grid(True, alpha=0.3)
                ax1.set_ylabel("Voltios")

                # --- GRÁFICA 2: TEMPERATURA ---
                ax2.cla()
                ax2.plot(datos_temp, color='orange', linewidth=2, label='Temperatura')
                ax2.set_title(f"SENSOR LM35: {celsius:.1f} °C", fontsize=14, color='red')
                # Ajustamos el límite de temperatura según tu cuarto (ej: 15 a 40 grados)
                ax2.set_ylim(0, 45) 
                ax2.grid(True, alpha=0.3)
                ax2.set_ylabel("Grados Celsius")
                
                plt.tight_layout()
                
        except:
            pass # Ignora errores de lectura momentáneos

# Iniciar animación (intervalo de 30ms para fluidez total)
ani = FuncAnimation(fig, actualizar, interval=30, cache_frame_data=False)
plt.show()

# Cerrar puerto al cerrar la ventana
ser.close()