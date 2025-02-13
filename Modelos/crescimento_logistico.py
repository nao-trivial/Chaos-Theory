import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo logístico
r = 0.5  # Taxa de crescimento
K = 100  # Capacidade de suporte

# Função para a taxa de variação
def logistic_growth(P, r, K):
    return r * P * (1 - P / K)

# Configuração do espaço de estados
P_values = np.linspace(-10, 120, 500)  # População (com valores negativos para ilustrar repulsor)
dP_values = logistic_growth(P_values, r, K)

# Gráfico
plt.figure(figsize=(10, 6))
plt.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Linha y=0
plt.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Linha P=0
plt.plot(P_values, dP_values, label="dP/dt = rP(1 - P/K)", color="blue")

# Destaque dos pontos fixos
plt.scatter(0, 0, color="red", label="Repulsor (P=0)", zorder=5)
plt.scatter(K, 0, color="green", label="Atrator (P=K)", zorder=5)

# Configuração do gráfico
plt.title("Campo de Direções: Modelo Logístico")
plt.xlabel("População (P)")
plt.ylabel("dP/dt")
plt.legend()
plt.grid()
plt.show()
