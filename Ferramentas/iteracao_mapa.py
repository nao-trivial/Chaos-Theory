import numpy as np import matplotlib.pyplot as plt

def plot_evolution(f, x0, num_iter, title="Evolução Temporal"): """ Plota a evolução temporal de uma função iterativa.

Parâmetros:
    f (function): Função iterativa f(x)
    x0 (float): Condição inicial
    num_iter (int): Número de iterações
    title (str): Título do gráfico
"""
tempo = np.arange(num_iter + 1)  # Passos de tempo (0, 1, 2, ...)
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
plt.title(title)
plt.axhline(y=0, color='gray', linestyle='--', label="Eixo x = 0")
plt.legend()
plt.grid()

# Exibir o gráfico
plt.show()

Exemplo de uso

def f(x): return x**2 - 1

plot_evolution(f, x0=0.75, num_iter=20, title="Evolução Temporal com Repulsor (f(x) = x² - 1)")

