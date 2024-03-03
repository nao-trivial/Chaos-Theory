import random
import networkx as nx
import matplotlib.pyplot as plt

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
        while True:
            caos = random.randint(0, 5)
            tipo = random.choice(['Realista', 'Investigativo', 'Artístico', 'Social', 'Empreendedor', 'Convencional'])
            perfil = self.criar_perfil_por_tipo(tipo, caos)
            self.grafo.add_node(self.contador_individuos, perfil=perfil, tipo=tipo, caos=caos)
            self.contador_individuos += 1

            if self.contador_individuos % 10 == 0:
                # Mostra o grafo a cada 10 indivíduos
                nx.draw(self.grafo, with_labels=True, font_weight='bold')
                plt.show()

                # Pergunta ao usuário se deseja inserir um novo indivíduo
                resposta = input("Deseja inserir um novo indivíduo? (S/N): ")
                if resposta.lower() != 's':
                    tipo = input("Digite o tipo de perfil (Realista, Investigativo, Artístico, Social, Empreendedor, Convencional): ")
                    self.simulador.adicionar_perfil(tipo)
                else:
                    break