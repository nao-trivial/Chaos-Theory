import numpy as np
import matplotlib.pyplot as plt

# Definição da função de iteração baseada na equação logística
def f(x, r):
    return r * x * (1 - x)

# Configuração da iteração
x0 = 0.1  # Valor inicial da população (0 < x0 < 1)
r = 3.2   # Parâmetro de crescimento (varia para diferentes atratores)
num_iter = 100  # Número de iterações

# Listas para armazenar a evolução temporal
tempo = np.arange(num_iter + 1)  # Passo do tempo (0, 1, 2, ...)
x_values = [x0]

# Calculando a sequência iterativa
x = x0
for _ in range(num_iter):
    x = f(x, r)
    x_values.append(x)

# Criando o gráfico de evolução temporal
plt.figure(figsize=(10, 6))
plt.plot(tempo, x_values, 'bo-', label="Evolução da população", markersize=4)

# Configuração do gráfico
plt.xlabel("Tempo (iterações)")
plt.ylabel("População (x)")
plt.title(f"Evolução Temporal - Equação Logística (r = {r})")
plt.axhline(y=0.8, color='red', linestyle='--', linewidth=0.8, label="Eixo x = 0.8")
plt.axhline(y=0.513, color='green', linestyle='--', linewidth=0.8, label="Eixo x = 0.513")
plt.legend()
plt.grid()

# Exibir o gráfico
plt.show()
