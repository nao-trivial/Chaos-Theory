import numpy as np
import matplotlib.pyplot as plt

def logistic_map(x, r):
    return r * x * (1 - x)

def generate_bifurcation_diagram(r_values, iterations=1000, last=100):
    bifurcation_diagram = []
    for r in r_values:
        x = 0.5  # Valor inicial de x
        for _ in range(iterations):
            x = logistic_map(x, r)
        for _ in range(last):
            x = logistic_map(x, r)
            bifurcation_diagram.append((r, x))
    return bifurcation_diagram

# Parâmetros
r_values = np.linspace(2.5, 4.0, 10000)  # Intervalo de valores de r
iterations = 1000  # Número de iterações para estabilizar
last = 100  # Número de pontos para plotar por valor de r

# Gerar o diagrama de bifurcação
bifurcation_data = generate_bifurcation_diagram(r_values, iterations, last)

# Plotar o diagrama de bifurcação
r_values_plot = [point[0] for point in bifurcation_data]
x_values_plot = [point[1] for point in bifurcation_data]

plt.figure(figsize=(10, 6))
plt.plot(r_values_plot, x_values_plot, ',', markersize=0.1, color='black')
plt.title('Diagrama de Bifurcação da Equação Logística')
plt.xlabel('r')
plt.ylabel('x')
plt.show()