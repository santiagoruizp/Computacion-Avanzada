from ising_model import IsingModel2D
import pandas as pd
import numpy as np

# Definimos los tamaños de red y los pasos de simulación
L_values = np.arange(5,155,5)  # Tamaños de la red L
nsteps = [l * 1000 for l in L_values]  # Pasos de simulación
Temp = 5.0  # Temperatura

tiempos_simulacion = []  # Lista para almacenar los tiempos de simulación

print(f"Programa para el conjunto L $\in$ [5,150] \n")

# Iteramos sobre cada tamaño de red L
for i, L in enumerate(L_values):
    model = IsingModel2D(L=L)  # Inicializamos el modelo de Ising
    S_init = model.ordered_state()  # Estado inicial
    Energia, Magnetizacion, S_final, tiempo = model.simulate(S_init, T=Temp, nsteps=nsteps[i])  # Simulamos
    tiempos_simulacion.append(tiempo)  # Guardamos el tiempo de simulación

    # Solo imprimimos el resultado para el último tamaño de red
    if i == len(L_values) - 1:
        print(f"Para L = {L}, T = {Temp}, con {nsteps[i]} pasos, se demora {tiempo:.5f} s")

# Creamos un DataFrame con los tiempos de simulación
df = pd.DataFrame({
    'L': L_values,
    'Execution time (s)': tiempos_simulacion
})

# Guardamos los resultados en un archivo CSV
df.to_csv("simulation_times_2_paral.csv", index=False)
