import random
import time
import networkx as nx

class SimuladorPerfil:
    def __init__(self):
        self.grafo = nx.Graph()
        self.evolucao_afinidades = []
        self.evolucao_caos = []
        self.contador_individuos = 0

    def criar_perfil(self, caos):
        return (
            random.randint(0, 10) + caos,
            random.randint(0, 10) + caos,
            random.randint(0, 10) + caos,
            random.randint(0, 10) + caos
        )

    def criar_perfil_por_tipo(self, tipo, caos):
        if tipo == 'Realista':
            return (10 + caos, random.randint(0, 10) + caos, 0 + caos, random.randint(0, 10) + caos)
        elif tipo == 'Investigativo':
            return (random.randint(0, 10) + caos, 10 + caos, random.randint(0, 10) + caos, 0 + caos)
        elif tipo == 'Artístico':
            return (random.randint(0, 10) + caos, 0 + caos, 10 + caos, random.randint(0, 10) + caos)
        elif tipo == 'Social':
            return (0 + caos, random.randint(0, 10) + caos, random.randint(0, 10) + caos, 10 + caos)
        elif tipo == 'Empreendedor':
            return (0 + caos, 10 + caos, random.randint(0, 10) + caos, random.randint(0, 10) + caos)
        elif tipo == 'Convencional':
            return (random.randint(0, 10) + caos, 0 + caos, random.randint(0, 10) + caos, 10 + caos)
        else:
            return self.criar_perfil(caos)

    def calcular_afinidade(self, perfil1, perfil2):
        afinidade = 0
        for i in range(len(perfil1)):
            afinidade += abs(perfil1[i] - perfil2[i])
        return round(afinidade, 2)

    def calcular_probabilidade_afinidade(self, afinidade):
        return max(0, 1 - afinidade / 50)

    def simular(self):
        sigma = 10
        rho = 28
        beta = 8/3
        dt = 0.01
        x, y, z = 0.1, 0.1, 0.1

        while True:
            dx = sigma * (y - x) * dt
            dy = (x * (rho - z) - y) * dt
            dz = (x * y - beta * z) * dt

            x += dx
            y += dy
            z += dz

            # Atualize o grafo com os perfis e suas afinidades
            # (você pode adicionar essa parte aqui)

            # Registre a evolução das afinidades e do caos
            # (você pode adicionar essa parte aqui)

            # Aguarde um intervalo de tempo antes de calcular a próxima iteração
            time.sleep(0.1)

if __name__ == "__main__":
    simulador = SimuladorPerfil()
    simulador.simular()
