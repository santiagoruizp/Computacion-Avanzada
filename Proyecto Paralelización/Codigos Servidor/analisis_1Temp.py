from ising_model import IsingModel2D
import pandas as pd

# Definimos los tamaños de red a estudiar y la temperatura
L = [20, 40, 60, 80, 100]
nsteps = [l * 1000 for l in L]
Temp = 5.0

print("Programa para el conjunto L = {}".format(L))
print("\n---\n")

# Lista para almacenar los tiempos de ejecución
tiempos = []

# Simulaciones en un bucle
for i, l in enumerate(L):
    ising_model = IsingModel2D(L=l)
    S_init = ising_model.ordered_state()
    Energia, Magnetizacion, S_final, time_duration = ising_model.simulate(S_init, T=Temp, nsteps=nsteps[i])
    
    tiempos.append(time_duration)
    
    print("Para L = {}, para T = {}, con {} pasos, se demora {:.5f} s".format(l, Temp, nsteps[i], time_duration))
    print("\n---\n")

# Crear un DataFrame con los datos
df = pd.DataFrame({
    'L': L,
    'Execution time (s)': tiempos
})

# Guardar el DataFrame en un archivo CSV
df.to_csv("simulation_times_1_paral.csv", index=False)
