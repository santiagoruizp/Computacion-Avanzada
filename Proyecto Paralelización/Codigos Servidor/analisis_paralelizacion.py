from ising_model import IsingModel2D
import multiprocessing as mp
import pandas as pd
import numpy as np
import time

# --- Parámetros ---
L = [20, 40, 60, 80, 100]  # Tamaños de sistema a evaluar
nsteps = [l * 1000 for l in L]  # Número de pasos Monte Carlo para cada L
Temp = np.linspace(0.1, 10, 100)  # Rango de temperaturas
args = [[(T, l, steps) for T in Temp] for l, steps in zip(L, nsteps)]  # Argumentos para cada simulación

numero_procesadores = 6  # Número de procesadores para paralelización
print("Programa para el conjunto L = {} y 100 diferentes valores de temperatura.".format(L))
print("Total de procesadores disponibles:", mp.cpu_count())
print("Número de procesadores usados:", numero_procesadores)

# --- Función que se ejecuta en paralelo ---
def simulate_single_temp(T, l, steps):
    """
    Simula el modelo de Ising para una temperatura T, tamaño de sistema l y número de pasos.
    Args:
        T: Temperatura en la simulación.
        l: Tamaño del sistema L.
        steps: Número de pasos Monte Carlo.
    Returns:
        Tuple: Contiene la temperatura, energía, magnetización, y tiempo de simulación.
    """
    model = IsingModel2D(L=l)  # Crear el modelo Ising 2D
    S = model.ordered_state()  # Estado inicial ordenado
    # Ejecutar simulación y obtener resultados
    Energia, Magnetizacion, S_final, time_duration = model.simulate(S, T=T, nsteps=steps)
    return T, Energia, Magnetizacion, time_duration  # Retornar los resultados

# Lista para almacenar los resultados de las simulaciones
tiempos_totales_externos = []
tiempos_internos_promedio = []
energias_medias = []
magnetizaciones_medias = []

# Iterar sobre los tamaños de sistema L
for i, l in enumerate(L):
    # Medir el tiempo de simulación externa
    start_time = time.time()

    # Ejecutar simulaciones en paralelo
    with mp.Pool(processes=numero_procesadores) as pool:
        results = pool.starmap(simulate_single_temp, args[i])

    end_time = time.time()  # Medir tiempo de ejecución total

    # Procesar los resultados de la simulación
    tiempo_total_externo = end_time - start_time
    Temps = [res[0] for res in results]  # Temperaturas
    Energias = [res[1] for res in results]  # Energías
    Magnetizaciones = [res[2] for res in results]  # Magnetizaciones
    Tiempos_internos = [res[3] for res in results]  # Tiempos de simulación interna
    Tiempos_internos_mean = np.mean(Tiempos_internos)  # Tiempo promedio interno

    # Calcular la energía y magnetización media para cada temperatura
    energias_medias_l = np.array([np.mean(e) for e in Energias])
    magnetizaciones_medias_l = np.array([np.mean(m) for m in Magnetizaciones])

    # Guardar los resultados
    tiempos_totales_externos.append(tiempo_total_externo)
    tiempos_internos_promedio.append(Tiempos_internos_mean)
    energias_medias.append(energias_medias_l)
    magnetizaciones_medias.append(magnetizaciones_medias_l)

    # Imprimir resultados por tamaño de sistema
    print("Para L = {}, para {} valores de temperatura, con {} pasos Montecarlo: ".format(l, len(Temp), nsteps[i]))
    print("Tiempo total externo: {:.5f} s".format(tiempo_total_externo))
    print("Tiempo interno promedio: {:.5f} s".format(Tiempos_internos_mean))
    print("\n---\n")

# --- Procesamiento de los resultados ---
# Normalización de energía y magnetización
def normalizar(resultados):
    """
    Normaliza los resultados de energía o magnetización.
    Normaliza los valores dividiendo por el valor absoluto del máximo de los resultados.
    """
    return [r / abs(max(r)) for r in resultados]

# Normalizamos los resultados para cada tamaño L
energias_medias_normalizadas = normalizar(energias_medias)
magnetizaciones_medias_normalizadas = normalizar(magnetizaciones_medias)

# --- Crear el DataFrame con los resultados ---
# Crear un DataFrame con los tiempos de simulación
df_tiempos = pd.DataFrame({
    'L': L,
    'Execution internal time (s)': tiempos_internos_promedio,
    'Execution external time (s)': tiempos_totales_externos
})

# Guardar el DataFrame de tiempos en un archivo CSV
df_tiempos.to_csv("simulation_times_completo.csv", index=False)

# Crear el DataFrame con los resultados de energía y magnetización normalizados
df_resultados = pd.DataFrame({
    'Temperatura': Temps,  # Se asume que todos los Temps son iguales
    'E_L20': energias_medias_normalizadas[0],
    'E_L40': energias_medias_normalizadas[1],
    'E_L60': energias_medias_normalizadas[2],
    'E_L80': energias_medias_normalizadas[3],
    'E_L100': energias_medias_normalizadas[4],
    'M_L20': magnetizaciones_medias_normalizadas[0],
    'M_L40': magnetizaciones_medias_normalizadas[1],
    'M_L60': magnetizaciones_medias_normalizadas[2],
    'M_L80': magnetizaciones_medias_normalizadas[3],
    'M_L100': magnetizaciones_medias_normalizadas[4]
})

# Guardar los resultados de energía y magnetización normalizados en un archivo CSV
df_resultados.to_csv("resultados_energia_magnetizacion_paralelizacion_completos.csv", index=False)
