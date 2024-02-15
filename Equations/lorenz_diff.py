import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parametros de Lorenz

sigma = 10
beta = 8/3
rho = 28

# Sistema de Lorenz 
def lorenz(t, y):
    return [
        sigma * (y[1] - y[0]), 
        y[0] * (rho - y[2]) - y[1], 
        y[0] * y[1] - beta * y[2]
    ]

# Condiçoes iniciais
y0 = [1, 1, 1]

# Intervalo de tempo 
t = (0, 40)

# Resolver o Sistema
sol = solve_ivp(lorenz, t, y0, t_eval=np.linspace(*t, 10000))

# Plotar o atrator de Lorenz
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(sol.y[0], sol.y[1], sol.y[2])
plt.show()