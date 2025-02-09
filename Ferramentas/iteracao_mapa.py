import numpy as np
import matplotlib.pyplot as plt

# Definição da função de iteração
def f(x):
    return -x / 2 + 3

# Configuração da iteração
x0 = 5  # Valor inicial
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
plt.figure(figsize=(8, 6))
plt.plot(tempo, x_values, 'bo-', label="Evolução de x", markersize=6)

# Configuração do gráfico
plt.xlabel("Tempo (iterações)")
plt.ylabel("Valor de x")
plt.title("Evolução Temporal da Sequência Iterativa")
plt.axhline(y=2, color='r', linestyle='--', label="Ponto Fixo (x = 2)")
plt.legend()
plt.grid()

# Exibir o gráfico
plt.show()
