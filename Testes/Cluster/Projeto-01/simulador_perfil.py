import random
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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
            caos = z
            self.evolucao_caos.append(caos)

            introduzir_individuo = input("Deseja introduzir um novo indivíduo no sistema? (sim/não): ").lower()
            if introduzir_individuo == 'sim':
                print("Tipos de Perfis de Holland:")
                print("1. Realista")
                print("2. Investigativo")
                print("3. Artístico")
                print("4. Social")
                print("5. Empreendedor")
                print("6. Convencional")
                tipo_perfil = int(input("Escolha o tipo de perfil (1-6): "))
                tipo_perfil_map = {1: 'Realista', 2: 'Investigativo', 3: 'Artístico', 4: 'Social', 5: 'Empreendedor', 6: 'Convencional'}
                tipo_escolhido = tipo_perfil_map.get(tipo_perfil, None)
                if tipo_escolhido:
                    novo_individuo = self.criar_perfil_por_tipo(tipo_escolhido, caos)
                    self.grafo.add_node(novo_individuo)
                    self.contador_individuos += 1
                else:
                    print("Tipo de perfil inválido. Criando um perfil aleatório.")
                    novo_individuo = self.criar_perfil(caos)
                    self.grafo.add_node(novo_individuo)
                    self.contador_individuos += 1
            else:
                novo_individuo = self.criar_perfil(caos)
                self.grafo.add_node(novo_individuo)
                self.contador_individuos += 1

            menor_afinidade = float('inf')
            individuo_mais_proximo = None
            for individuo in self.grafo.nodes():
                if individuo != novo_individuo:
                    afinidade = self.calcular_afinidade(novo_individuo, individuo)
                    if afinidade < menor_afinidade:
                        menor_afinidade = afinidade
                        individuo_mais_proximo = individuo

            probabilidade = self.calcular_probabilidade_afinidade(menor_afinidade)

            if random.random() < probabilidade:
                self.grafo.add_edge(novo_individuo, individuo_mais_proximo, afinidade=menor_afinidade)

            afinidades_iteracao = [self.calcular_afinidade(novo_individuo, individuo) for individuo in self.grafo.nodes()]
            self.evolucao_afinidades.append(afinidades_iteracao)

            if input("Deseja ver a evolução do sistema? (sim/não): ").lower() != "sim":
                break

            plt.clf()
            pos = nx.spring_layout(self.grafo)
            nx.draw(self.grafo, pos, with_labels=False, node_size=50)
            labels = {(u, v): f'{d["afinidade"]:.2f}' for u, v, d in self.grafo.edges(data=True)}
            nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels)
            nx.draw_networkx_labels(self.grafo, pos, {individuo: str(i) for i, individuo in enumerate(self.grafo.nodes())})
            plt.title(f"Iteração {len(self.evolucao_afinidades)}, Caos: {caos:.2f}")
            plt.pause(0.001)
            time.sleep(0.1)

        plt.figure()
        plt.plot(self.evolucao_caos)
        plt.xlabel("Iteração")
        plt.ylabel("Valor do Caos")
        plt.title("Evolução do Caos ao Longo do Tempo")
        plt.show()

        X = np.array(list(self.grafo.nodes()))
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(X_scaled)

        cluster_labels = kmeans.labels_

        plt.figure()
        nx.draw(self.grafo, pos, with_labels=False, node_size=50, node_color=cluster_labels, cmap=plt.cm.Set1)
        plt.title("Grafo com Clusters")
        plt.show()

simulador = SimuladorPerfil()
simulador.simular()
