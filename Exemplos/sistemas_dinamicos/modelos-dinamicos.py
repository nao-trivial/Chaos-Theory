import numpy as np

class ModelosDinamicos:
    def sistema_pendulo(self, theta0, omega0, g=9.81, L=1.0, t_max=10, dt=0.01):
        """
        Simula o movimento de um pêndulo simples.
        
        Parâmetros:
        theta0 : float : ângulo inicial (rad)
        omega0 : float : velocidade angular inicial (rad/s)
        g : float : aceleração da gravidade (m/s²)
        L : float : comprimento do pêndulo (m)
        t_max : float : tempo total da simulação (s)
        dt : float : intervalo de tempo entre iterações (s)
        """
        n = int(t_max / dt)
        theta = np.zeros(n)
        omega = np.zeros(n)
        theta[0] = theta0
        omega[0] = omega0
        
        for i in range(1, n):
            omega[i] = omega[i - 1] - (g / L) * np.sin(theta[i - 1]) * dt
            theta[i] = theta[i - 1] + omega[i - 1] * dt
            
        return theta, omega
