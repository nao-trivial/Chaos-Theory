import numpy as np
import matplotlib.pyplot as plt
from modelos import ModelosCaos

class AnalisesCaos:
    def __init__(self):
        self.modelos = ModelosCaos()

    def analise_atrator_logistico(self, r, x0, n):
        """
        Realiza a análise do atrator logístico.
        
        Parâmetros:
        r : float : taxa de crescimento
        x0 : float : valor inicial
        n : int : número de iterações
        """
        x_logistico = self.modelos.atrator_logistico(r, x0, n)
        
        media = np.mean(x_logistico)
        variancia = np.var(x_logistico)
        desvio_padrao = np.std(x_logistico)

        print(f"Análise do Atrator Logístico (r={r}, x0={x0}):")
        print(f"Média: {media:.4f}, Variância: {variancia:.4f}, Desvio Padrão: {desvio_padrao:.4f}\n")
        
        plt.figure(figsize=(10, 5))
        plt.plot(x_logistico)
        plt.title("Comportamento do Atrator Logístico")
        plt.xlabel("Iterações")
        plt.ylabel("População")
        plt.axhline(y=media, color='r', linestyle='--', label='Média')
        plt.legend()
        plt.grid()
        plt.show()

    def analise_atrator_lorenz(self, sigma=10, beta=8/3, rho=28, x0=1, y0=1, z0=1, n=10000, dt=0.01):
        """
        Realiza a análise do sistema de Lorenz.
        
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
        trajectoria_lorenz = self.modelos.atrator_lorenz(sigma, beta, rho, x0, y0, z0, n, dt)

        x, y, z = trajectoria_lorenz
        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection='3d')
        ax.plot(x, y, z, lw=0.5)
        ax.set_title("Trajetória do Sistema de Lorenz")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

if __name__ == "__main__":
    analise = AnalisesCaos()
    # Exemplos de uso
    analise.analise_atrator_logistico(r=3.5, x0=0.1, n=100)
    analise.analise_atrator_lorenz()
