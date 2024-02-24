import numpy as np
import matplotlib.pyplot as plt

class IntegralEstocastica:
    def __init__(self, mu, sigma, x0, T, dt):
        self.mu = mu
        self.sigma = sigma
        self.x0 = x0
        self.T = T
        self.dt = dt
        self.t = np.arange(0, self.T, self.dt)
        self.W = np.random.standard_normal(size=len(self.t))
        self.W = np.cumsum(self.W)*np.sqrt(self.dt)
        self.x = np.zeros(len(self.t))
        self.x[0] = x0

    def resolver(self):
        for i in range(1, len(self.t)):
            self.x[i] = self.x[i-1] + self.mu*self.x[i-1]*self.dt + self.sigma*self.x[i-1]*(self.W[i]-self.W[i-1])
        return self.t, self.x
    
# Parametros
mu = 0.1
sigma = 0.1
x0 = 1.0
t_grande = 1.0
dt = 0.01

# Cria uma instancia da classe IntegralEstocastica
integral_estocastica = IntegralEstocastica(mu=mu, sigma=sigma, x0=x0, T=t_grande, dt=dt)

# Resolve a equaçao diferencial estocastica e plota o resultado
t, x = integral_estocastica.resolver()
plt.plot(t, x)
plt.title('Movimento Browniano Geometrico')
plt.xlabel('Tempo')
plt.ylabel('X')
plt.show()
