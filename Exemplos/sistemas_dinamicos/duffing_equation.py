import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Definindo os parâmetros do oscilador de Duffing
delta = 0.2    # Coeficiente de amortecimento
alpha = -1.0   # Termo linear
beta = 1.0     # Termo cúbico (não-linear)
gamma = 0.3    # Amplitude da força externa
omega = 1.2    # Frequência angular da força externa

# Definindo a função para o oscilador de Duffing
def duffing_oscillator(t, y):
    x, v = y  # y[0] é x, y[1] é v
    dxdt = v
    dvdt = -delta * v - alpha * x - beta * x**3 + gamma * np.cos(omega * t)
    return [dxdt, dvdt]

# Condições iniciais: posição inicial x0 e velocidade inicial v0
x0 = 0.5  # Posição inicial
v0 = 0.0  # Velocidade inicial

# Intervalo de tempo e pontos de amostragem
t_span = (0, 50)  # Intervalo de tempo para a simulação
t_eval = np.linspace(t_span[0], t_span[1], 2000)  # Pontos de amostragem

# Resolvendo a EDO
sol = solve_ivp(duffing_oscillator, t_span, [x0, v0], t_eval=t_eval, method='RK45')

# Plotando os resultados
plt.figure(figsize=(12, 8))

# Plot da posição x(t)
plt.subplot(2, 1, 1)
plt.plot(sol.t, sol.y[0], label="x(t) - Posição", color='b')
plt.xlabel("Tempo (t)")
plt.ylabel("Posição (x)")
plt.grid()
plt.legend()

# Plot da velocidade v(t)
plt.subplot(2, 1, 2)
plt.plot(sol.t, sol.y[1], label="v(t) - Velocidade", color='r')
plt.xlabel("Tempo (t)")
plt.ylabel("Velocidade (v)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
