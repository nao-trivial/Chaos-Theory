import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Definindo os parâmetros
omega = 1.0  # Frequência angular

# Definindo a equação diferencial do oscilador harmônico
def harmonic_oscillator(t, y):
    x, v = y  # y[0] é x, y[1] é v
    dxdt = v
    dvdt = -omega**2 * x
    return [dxdt, dvdt]

# Condições iniciais: posição inicial x0 e velocidade inicial v0
x0 = 1.0  # Posição inicial
v0 = 0.0  # Velocidade inicial

# Intervalo de tempo e pontos de amostragem
t_span = (0, 20)  # Intervalo de tempo para a simulação
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Pontos de amostragem para visualização

# Resolvendo a EDO
sol = solve_ivp(harmonic_oscillator, t_span, [x0, v0], t_eval=t_eval)

# Plotando os resultados
plt.figure(figsize=(12, 6))

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
