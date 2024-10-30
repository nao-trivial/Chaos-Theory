import threading
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from analise_rede import AnaliseRedeSocial

class RedeSocial:
    def __init__(self):
        self.grafo = nx.Graph()
        self.lock = threading.Lock()
        self.houve_mudanca = False
        self.fig, (self.ax_grafo, self.ax_tabela) = plt.subplots(1, 2, figsize=(12, 6))
        self.running = True

    def adicionar_no(self, individuo):
        self.grafo.add_node(individuo)

    def adicionar_aresta(self, no1, no2, peso):
        cor = self.definir_cor_aresta(peso)
        self.grafo.add_edge(no1, no2, weight=round(peso, 2), color=cor)

    def definir_cor_aresta(self, peso):
        if peso < 0.3:
            return 'darkred'
        elif peso < 0.5:
            return 'red'
        elif peso == 0.5:
            return 'blue'
        elif peso < 0.7:
            return 'lightgreen'
        else:
            return 'green'

    def atualizar_afinidades(self):
        with self.lock:
            for u, v, data in self.grafo.edges(data=True):
                peso_atual = data['weight']
                ajuste = random.uniform(-0.05, 0.05)
                novo_peso = min(max(peso_atual + ajuste, 0), 1)
                cor_nova = self.definir_cor_aresta(novo_peso)
                self.grafo[u][v]['weight'] = round(novo_peso, 2)
                self.grafo[u][v]['color'] = cor_nova
            self.houve_mudanca = True

    def adicionar_no_com_interacoes(self, individuo):
        with self.lock:
            if not self.running:
                return
            self.adicionar_no(individuo)
            for no in self.grafo.nodes:
                if no != individuo:
                    peso_interacao = random.uniform(0.0, 1.0)
                    self.adicionar_aresta(individuo, no, peso_interacao)
            self.houve_mudanca = True

    def iniciar_adicao_progressiva(self, intervalo):
        contador = 1
        while self.running:
            individuo_nome = f"Indivíduo {contador}"
            self.adicionar_no_com_interacoes(individuo_nome)
            if not self.running:
                break
            contador += 1
            sleep(intervalo)

    def iniciar_atualizacao_afinidades(self, intervalo):
        while self.running:
            self.atualizar_afinidades()
            sleep(intervalo)

    def visualizar_rede(self, i):
        with self.lock:
            if self.houve_mudanca:
                # Atualiza a visualização da rede
                self.ax_grafo.clear()
                pos = nx.spring_layout(self.grafo, seed=42)
                edges = self.grafo.edges(data=True)
                colors = [edge[2]['color'] for edge in edges]
                nx.draw(self.grafo, pos, ax=self.ax_grafo, with_labels=True, font_weight='bold', edge_color=colors, width=2)

                # Atualiza a tabela de afinidades
                self.ax_tabela.clear()
                self.exibir_tabela_afinidades()

                self.houve_mudanca = False
            if not plt.fignum_exists(self.fig.number):
                self.running = False

    def exibir_tabela_afinidades(self):
        """Exibe uma tabela de afinidades entre os indivíduos."""
        individuos = list(self.grafo.nodes)
        afinidades = np.zeros((len(individuos), len(individuos)))

        for i, u in enumerate(individuos):
            for j, v in enumerate(individuos):
                if u == v:
                    afinidades[i, j] = np.nan  # Diagonal principal (não há afinidade consigo mesmo)
                elif self.grafo.has_edge(u, v):
                    afinidades[i, j] = self.grafo[u][v]['weight']
                else:
                    afinidades[i, j] = 0  # Sem conexão

        # Cria a tabela e configura para exibir na interface
        self.ax_tabela.axis("off")
        tabela = self.ax_tabela.table(
            cellText=np.round(afinidades, 2),
            rowLabels=individuos,
            colLabels=individuos,
            cellLoc="center",
            loc="center"
        )
        tabela.scale(1, 1.5)

# Instância da Rede Social
rede_social = RedeSocial()

# Parâmetro para o intervalo de criação de indivíduos (em segundos)
intervalo_criacao = 5

# Iniciando a adição progressiva de indivíduos em uma thread separada
thread_criacao = threading.Thread(target=rede_social.iniciar_adicao_progressiva, args=(intervalo_criacao,))
thread_criacao.start()

# Configuração da animação da visualização da rede
ani = FuncAnimation(rede_social.fig, rede_social.visualizar_rede, interval=1000, cache_frame_data=False, save_count=50)
plt.show()

# Finalizando a criação de indivíduos
rede_social.running = False
thread_criacao.join()

# Análise da Rede e Geração do Relatório Final
analise = AnaliseRedeSocial(rede_social)
analise.gerar_relatorio()