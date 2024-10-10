import numpy as np
import matplotlib.pyplot as plt

# Definindo as constantes
G = 1  # Constante gravitacional
m = 1  # Massa dos corpos
dt = 0.01  # Passo de tempo
t_final = 10  # Tempo final
n = int(t_final / dt)  # Número de passos de tempo

# Inicializando as posições e velocidades
r = np.zeros((3, 2, n+1))
v = np.zeros((3, 2, n+1))

# Condições iniciais
r[0, :, 0] = [-0.5, 0]
r[1, :, 0] = [0.5, 0]
r[2, :, 0] = [0, 1]

# Método de Euler
for t in range(n):
    for i in range(3):
        F = np.zeros(2)
        for j in range(3):
            if i != j:
                rij = r[j, :, t] - r[i, :, t]
                F += G * m**2 * rij / np.hypot(rij[0], rij[1])**3
        a = F / m
        v[i, :, t+1] = v[i, :, t] + a * dt
        r[i, :, t+1] = r[i, :, t] + v[i, :, t] * dt

# Plotando as trajetórias
for i in range(3):
    plt.plot(r[i, 0, :], r[i, 1, :])
plt.show()
