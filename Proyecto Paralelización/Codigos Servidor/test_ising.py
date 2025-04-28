from ising_model import IsingModel2D  # Importa la clase del modelo de Ising 2D

# Análisis de testeo del modelo

L = 20  # Tamaño de la red
Temp = 5.0  # Temperatura de simulación

print("Programa de testeo para L = {}".format(L))

# Inicialización del modelo y del estado ordenado
ising_model_L_20_test = IsingModel2D(L=L)
S = ising_model_L_20_test.ordered_state()

# Simulación mediante el algoritmo de Metropolis
Energia, Magnetizacion, S_final, time_duration = ising_model_L_20_test.simulate(S, T=Temp, nsteps=L * 1000)

# Reporte del tiempo de simulación
print("El testeo para L = {}, para T = {}, se demora {:.5f} s".format(L, Temp, time_duration))
