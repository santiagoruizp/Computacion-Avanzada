from ising_model import IsingModel2D
import multiprocessing as mp
import pandas as pd
import numpy as np
import time

# --- Parámetros ---
L = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
nsteps = [l * 1000 for l in L]  # Pasos para cada L
Temp = np.linspace(0.1, 10, 100)  # 100 temperaturas
args = [[(T, l, steps) for T in Temp] for l, steps in zip(L, nsteps)]  # Argumentos para cada simulación

numero_procesadores = 12
print("Programa para el conjunto L = {} y 100 diferentes valores de temperatura.".format(L))
print("Total de procesadores disponibles:", mp.cpu_count())
print("Número de procesadores usados:", numero_procesadores)

# --- Función que se ejecuta en paralelo ---
def simulate_single_temp(T, l, steps):
    model = IsingModel2D(L=l)
    S = model.ordered_state()  # Estado inicial ordenado
    Energia, Magnetizacion, S_final, time_duration = model.simulate(S, T=T, nsteps=steps)
    return T, Energia, Magnetizacion, time_duration

print("\n---\n")

# --- Medir tiempo externo ---
start_time = time.time()

# Crear un diccionario para almacenar los resultados por cada L
tiempo_total_externo = {}
Tiempos_internos = {}
Energias = {}
Magnetizaciones = {}

# Procesar cada L con la paralelización
for idx, l in enumerate(L):
    with mp.Pool(processes=numero_procesadores) as pool:
        results = pool.starmap(simulate_single_temp, args[idx])

    end_time = time.time()
    
    tiempo_total_externo_l = end_time - start_time
    Temps_l = [res[0] for res in results]
    Energias_l = [res[1] for res in results]
    Magnetizaciones_l = [res[2] for res in results]
    Tiempos_internos_l = [res[3] for res in results]
    
    Tiempos_internos_mean_l = np.mean(Tiempos_internos_l)

    # Almacenar los resultados por cada L
    tiempo_total_externo[l] = tiempo_total_externo_l
    Tiempos_internos[l] = Tiempos_internos_l
    Energias[l] = Energias_l
    Magnetizaciones[l] = Magnetizaciones_l

    print(f"Para L = {l}, para {len(Temp)} valores de temperatura, con {nsteps[idx]} pasos Montecarlo: ")
    print(f"Tiempo total externo: {tiempo_total_externo_l:.5f} s")
    print(f"Tiempo interno promedio: {Tiempos_internos_mean_l:.5f} s")
    print("\n---\n")

# --- Crear las gráficas ---
print("\n---\n")

# Graficar tiempos de duración
Tiempos_internos_promedio = [np.mean(Tiempos_internos[l]) for l in L]
Tiempos_externos = [tiempo_total_externo[l] for l in L]

# Crear un DataFrame con los tiempos de ejecución
df_times = pd.DataFrame({
    'L': L,
    'Execution internal time (s)': Tiempos_internos_promedio,
    'Execution external time (s)': Tiempos_externos
})

# Guardar el DataFrame con los tiempos en un archivo CSV
df_times.to_csv("simulation_times_completo.csv", index=False)

# Graficar Energía y Magnetización normalizadas
fig, axes = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1.2]})

for idx, l in enumerate(L):
    energias_medias = np.array([np.mean(e) for e in Energias[l]])
    magnetizaciones_medias = np.array([np.mean(m) for m in Magnetizaciones[l]])

    # Normalizar y graficar Energía
    axes[0].plot(Temps, energias_medias / abs(max(energias_medias)), label=f"L = {l}", linestyle='-', marker='o')
    
    # Normalizar y graficar Magnetización
    axes[1].plot(Temps, magnetizaciones_medias / abs(max(magnetizaciones_medias)), label=f"L = {l}", linestyle='-', marker='o')

# Mejorar la presentación de las gráficas
axes[0].set_xlabel("Temperatura (T)")
axes[0].set_ylabel("Energía Normalizada")
axes[0].legend(loc="best")
axes[0].set_title("Energía Normalizada vs Temperatura")

axes[1].set_xlabel("Temperatura (T)")
axes[1].set_ylabel("Magnetización Normalizada")
axes[1].legend(loc="best")
axes[1].set_title("Magnetización Normalizada vs Temperatura")

# Mostrar las gráficas
plt.tight_layout()
plt.show()

# Crear el DataFrame con los resultados de energía y magnetización para guardar
df_resultados = pd.DataFrame({
    'Temperatura': Temps,  # Se asume que todos los Temps son iguales
})

# Agregar columnas para Energía y Magnetización de cada L
for l in L:
    energias_medias = np.array([np.mean(e) for e in Energias[l]])
    magnetizaciones_medias = np.array([np.mean(m) for m in Magnetizaciones[l]])
    df_resultados[f'E_L{l}'] = energias_medias / abs(max(energias_medias))
    df_resultados[f'M_L{l}'] = magnetizaciones_medias / abs(max(magnetizaciones_medias))

# Guardar los resultados en un archivo CSV
df_resultados.to_csv("resultados_energia_magnetizacion_paralelizacion_completos.csv", index=False)
