from ising_model import IsingModel2D
import pandas as pd
import numpy as np

# Definimos los tamaños del sistema y las temperaturas
L = [20,40,60,80,100]  # Tamaños de la cuadrícula
nsteps = [l * 1000 for l in L]  # Número de pasos Montecarlo, aumenta con L
Temp = np.linspace(0.1, 10, 30)  # Rango de temperaturas
print("Programa para el conjunto L = {} y diferentes valores de temperatura.".format(L))

# Inicializamos listas para almacenar tiempos de ejecución y otros resultados
tiempos = []
energias = {}
magnetizaciones = {}

# Bucle sobre cada tamaño L para simular y almacenar resultados
for i, l in enumerate(L):
    # Crear el modelo de Ising para el tamaño L actual
    ising_model = IsingModel2D(L=l)
    S = ising_model.ordered_state()  # Estado ordenado inicial
    
    # Simulación de Monte Carlo para cada temperatura y número de pasos
    Energia, Magnetizacion, time_duration = ising_model.simulate(S, T=Temp, nsteps=nsteps[i])
    
    # Almacenamos el tiempo de ejecución
    tiempos.append(time_duration)
    
    # Normalizamos energía y magnetización y las almacenamos
    energias[f"E_L={l}"] = ising_model.mean_energy(Energia) / abs(max(ising_model.mean_energy(Energia)))
    magnetizaciones[f"M_L={l}"] = ising_model.mean_magnetization(Magnetizacion) / abs(max(ising_model.mean_magnetization(Magnetizacion)))
    
    # Imprimimos los resultados para el tamaño L actual
    print(f"Para L = {l}, para {len(Temp)} valores de temperatura, con {nsteps[i]} pasos Montecarlo, se demora {time_duration:.5f} s")
    print("\n---\n")

# Crear un DataFrame con los tiempos de ejecución
df_time = pd.DataFrame({
    'L': L,
    'Execution time (s)': tiempos
})

# Guardar los tiempos de ejecución en un archivo CSV
df_time.to_csv("simulation_times_3_paral.csv", index=False)

# Crear un DataFrame para almacenar las energías y magnetizaciones normalizadas
df_total = pd.DataFrame({
    "Temperatura": Temp,
    **energias,
    **magnetizaciones
})

# Guardar los observables en un archivo CSV
df_total.to_csv("observables_energia_magnetizacion.csv", index=False)
