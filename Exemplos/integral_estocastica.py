'''import numpy as np
import matplotlib.pyplot as plt

class IntegralEstocastica:
    def __init__(self, mu, sigma, X0, T, dt):
        self.mu = mu
        self.sigma = sigma
        self.X0 = X0
        self.T = T
        self.dt = dt
        self.t = np.arange(0, self.T, self.dt)
        self.W = np.random.standard_normal(size = len(self.t))
        self.W = np.cumsum(self.W)*np.sqrt(self.dt) # integral estocástica
        self.X = np.zeros(len(self.t))
        self.X[0] = X0

    def resolver(self):
        for i in range(1, len(self.t)):
            self.X[i] = self.X[i-1] + self.mu*self.X[i-1]*self.dt + self.sigma*self.X[i-1]*(self.W[i]-self.W[i-1])
        return self.t, self.X

# Parâmetros
mu = 0.1
sigma = 0.1
X0 = 1.0
T = 1.0
dt = 0.01

# Cria uma instância da classe IntegralEstocastica
integral_estocastica = IntegralEstocastica(mu=mu, sigma=sigma, X0=X0, T=T, dt=dt)

# Resolve a equação diferencial estocástica e plota o resultado
t, X = integral_estocastica.resolver()
plt.plot(t, X)
plt.title('Movimento Browniano Geométrico')
plt.xlabel('Tempo')
plt.ylabel('X')
plt.show()
'''