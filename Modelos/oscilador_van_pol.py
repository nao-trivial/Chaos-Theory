import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parâmetros do oscilador de Van der Pol
mu = 2.0

# Definição do sistema de equações diferenciais
def van_der_pol(t, z):
    x, y = z
    dxdt = y
    dydt = mu * (1 - x**2) * y - x
    return [dxdt, dydt]

# Condições iniciais e tempo de simulação
z0 = [2.0, 0.0]  # Estado inicial
t_span = (0, 50)  # Intervalo de tempo
t_eval = np.linspace(*t_span, 1000)  # Pontos para avaliação

# Resolver o sistema de equações
sol = solve_ivp(van_der_pol, t_span, z0, t_eval=t_eval)

# Extrair soluções
x, y = sol.y

# Gráfico do espaço de fases
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="Trajetória no espaço de fases", color="blue")
plt.title("Oscilador de Van der Pol: Ciclo Limite")
plt.xlabel("x")
plt.ylabel("y (dx/dt)")
plt.grid()
plt.legend()
plt.show()
