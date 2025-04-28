import numpy as np
import random
import time
import math

class IsingModel2D:
    """
    Clase para simular el modelo de Ising en 2D con condiciones de frontera periódicas.
    """

    def __init__(self, L, J=1.0, h=0.0):
        """
        Inicializa el modelo.
        
        Parámetros:
        - L: tamaño del lado de la cuadrícula (sistema L x L)
        - J: constante de acoplamiento entre espines
        - h: campo magnético externo
        """
        self.L = L
        self.N = L * L  # Número total de sitios
        self.J = J
        self.h = h
        self.nbr = self._compute_periodic_neighbors()  # Vecinos periódicos precomputados

    def _compute_periodic_neighbors(self):
        """
        Calcula los vecinos periódicos para cada sitio en la red.
        
        Devuelve un diccionario donde cada clave es un sitio y el valor es una tupla con sus 4 vecinos.
        """
        return {
            i: ((i // self.L) * self.L + (i + 1) % self.L,   # vecino a la derecha
                (i + self.L) % self.N,                      # vecino de abajo
                (i // self.L) * self.L + (i - 1) % self.L,   # vecino a la izquierda
                (i - self.L) % self.N)                       # vecino de arriba
            for i in range(self.N)
        }

    def random_state(self):
        """
        Genera un estado inicial aleatorio de espines (+1 o -1).
        
        Devuelve una lista de tamaño N.
        """
        return [random.choice([1, -1]) for _ in range(self.N)]

    def ordered_state(self, value=1):
        """
        Genera un estado ordenado donde todos los espines son iguales (1 o -1).
        
        Parámetros:
        - value: valor del espín (por defecto +1)
        
        Devuelve una lista de tamaño N.
        """
        return [value] * self.N

    def reshape_state(self, S):
        """
        Convierte un estado 1D en una matriz 2D (LxL).
        
        Parámetros:
        - S: estado en forma de lista
        
        Devuelve un array de numpy de forma (L, L).
        """
        return np.reshape(S, (self.L, self.L))

    def energy(self, S):
        """
        Calcula la energía total del sistema para un estado dado.
        
        Parámetros:
        - S: lista de espines
        
        Devuelve un valor flotante.
        """
        E = 0.
        for k in range(self.N):
            E += -self.J * S[k] * sum(S[nn] for nn in self.nbr[k])  # Interacción con vecinos
        E *= 0.5  # Corrige doble conteo
        E -= self.h * sum(S)  # Interacción con el campo externo
        return E

    def magnetization(self, S):
        """
        Calcula la magnetización total del sistema.
        
        Parámetros:
        - S: lista de espines
        
        Devuelve un valor entero.
        """
        return sum(S)

    def simulate(self, S_ini, T, nsteps=20000):
        """
        Realiza una simulación de Monte Carlo usando el algoritmo de Metropolis.
        
        Parámetros:
        - S_ini: estado inicial
        - T: temperatura (o arreglo de temperaturas)
        - nsteps: número de pasos de Monte Carlo
        
        Devuelve:
        - Energías a lo largo del tiempo
        - Magnetizaciones a lo largo del tiempo
        - Estado final (si solo una temperatura)
        - Tiempo total de simulación
        """
        T = np.atleast_1d(T)  # Asegura que T sea un array
        beta = 1.0 / T

        E_total = []
        M_total = []

        start = time.perf_counter()

        for i in range(len(T)):
            E = self.energy(S_ini)
            Energy = [E]
            S = S_ini.copy()
            Magn = [self.magnetization(S)]

            for step in range(nsteps):
                # Elige un espín aleatorio
                k = random.randint(0, self.N - 1)
                
                # Calcula el cambio de energía si se invierte el espín
                delta_E = 2.0 * S[k] * (sum(S[nn] for nn in self.nbr[k]) + self.h)

                # Criterio de Metropolis para aceptar el cambio
                if random.uniform(0.0, 1.0) < math.exp(-beta[i] * delta_E):
                    S[k] *= -1  # Invierte el espín
                    E += delta_E  # Actualiza energía

                Energy.append(E)
                Magn.append(self.magnetization(S))

            E_total.append(Energy)
            M_total.append(Magn)

        end = time.perf_counter()

        # Devuelve diferentes formatos dependiendo si se simula una o varias temperaturas
        if len(T) == 1:
            return [E_total, M_total, S, end - start]
        
        return [E_total, M_total, end - start]

    def mean_energy(self, energy_configs):
        """
        Calcula la energía promedio a partir de varias configuraciones.
        
        Parámetros:
        - energy_configs: lista de listas de energías
        
        Devuelve un array de numpy.
        """
        return np.array([np.mean(E) for E in energy_configs])

    def mean_magnetization(self, magnetization_configs):
        """
        Calcula la magnetización promedio a partir de varias configuraciones.
        
        Parámetros:
        - magnetization_configs: lista de listas de magnetizaciones
        
        Devuelve un array de numpy.
        """
        return np.array([np.mean(M) for M in magnetization_configs])

    def heat_capacity(self, energy_configs, temperatures):
        """
        Calcula la capacidad calorífica C_V del sistema.
        
        Parámetros:
        - energy_configs: lista de listas de energías
        - temperatures: arreglo de temperaturas
        
        Devuelve un array de numpy con C_V en función de T.
        """
        K_B = 1.0  # Constante de Boltzmann (unidades naturales)
        mean_E = self.mean_energy(energy_configs)
        mean_E2 = np.array([np.mean(np.array(E) ** 2) for E in energy_configs])
        C_V = (mean_E2 - mean_E ** 2) / ((temperatures ** 2) * K_B)
        return C_V

    def magnetic_susceptibility(self, magnetization_configs, temperatures):
        """
        Calcula la susceptibilidad magnética chi del sistema.
        
        Parámetros:
        - magnetization_configs: lista de listas de magnetizaciones
        - temperatures: arreglo de temperaturas
        
        Devuelve un array de numpy con chi en función de T.
        """
        K_B = 1.0  # Constante de Boltzmann (unidades naturales)
        mean_M = self.mean_magnetization(magnetization_configs)
        mean_M2 = np.array([np.mean(np.array(M) ** 2) for M in magnetization_configs])
        chi = (mean_M2 - mean_M ** 2) / (temperatures * K_B)
        return chi
