import numpy as np
import matplotlib.pyplot as plt

# Definição da função de iteração
def f(x):
    return x**2 - 1

# Configuração da iteração
x0 = 0.75  # Valor inicial (próximo ao repulsor)
num_iter = 20  # Número de iterações

# Listas para armazenar a evolução temporal
tempo = np.arange(num_iter + 1)  # Passo do tempo (0, 1, 2, ...)
x_values = [x0]

# Calculando a sequência iterativa
x = x0
for _ in range(num_iter):
    x = f(x)
    x_values.append(x)

# Criando o gráfico de evolução temporal
plt.figure(figsize=(10, 6))
plt.plot(tempo, x_values, 'bo-', label="Evolução de x", markersize=6)

# Configuração do gráfico
plt.xlabel("Tempo (iterações)")
plt.ylabel("Valor de x")
plt.title("Evolução Temporal com Repulsor (f(x) = x² - 1)")
plt.axhline(y=0, color='gray', linestyle='--', label="Eixo x = 0")
plt.axhline(y=-1, color='g', linestyle='--', label="Atrator (x = -1)")
plt.axhline(y=1, color='r', linestyle='--', label="Repulsor (x = 1)")
plt.legend()
plt.grid()

# Exibir o gráfico
plt.show()
