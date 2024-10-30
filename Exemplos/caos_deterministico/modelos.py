import numpy as np

class ModelosCaos:
    def atrator_logistico(self, r, x0, n):
        """
        Simula o atrator logístico.
        
        Parâmetros:
        r : float : taxa de crescimento
        x0 : float : valor inicial
        n : int : número de iterações
        """
        x = np.zeros(n)
        x[0] = x0
        for i in range(1, n):
            x[i] = r * x[i - 1] * (1 - x[i - 1])
        return x

    def atrator_lorenz(self, sigma=10, beta=8/3, rho=28, x0=1, y0=1, z0=1, n=10000, dt=0.01):
        """
        Simula o sistema de Lorenz.
        
        Parâmetros:
        sigma : float : parâmetro sigma
        beta : float : parâmetro beta
        rho : float : parâmetro rho
        x0 : float : valor inicial para x
        y0 : float : valor inicial para y
        z0 : float : valor inicial para z
        n : int : número de iterações
        dt : float : intervalo de tempo entre iterações
        """
        x = np.zeros(n)
        y = np.zeros(n)
        z = np.zeros(n)
        x[0], y[0], z[0] = x0, y0, z0
        
        for i in range(1, n):
            x[i] = x[i - 1] + (sigma * (y[i - 1] - x[i - 1])) * dt
            y[i] = y[i - 1] + (x[i - 1] * (rho - z[i - 1]) - y[i - 1]) * dt
            z[i] = z[i - 1] + (x[i - 1] * y[i - 1] - beta * z[i - 1]) * dt
            
        return x, y, z
