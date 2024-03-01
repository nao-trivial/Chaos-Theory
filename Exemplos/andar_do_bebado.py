import numpy as np
import matplotlib.pyplot as plt

# Número de passos
N = 1000

# Passos aleatórios
passos = np.random.choice([-1, 1], size=N)

# Posição do bêbado
posicao = np.cumsum(passos)

# Plotar a posição do bêbado
plt.plot(posicao)
plt.title('Andar do Bêbado')
plt.xlabel('Passo')
plt.ylabel('Posição')
plt.show()
