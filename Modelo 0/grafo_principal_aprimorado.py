import threading
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

class RedeSocial:
    def __init__(self):
        self.grafo = nx.Graph()
        self.parametros_modelo = {}
        self.lock = threading.Lock()
        self.houve_mudanca = False
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.running = True

    def adicionar_no(self, individuo):
        self.grafo.add_node(individuo)

    def adicionar_aresta(self, no1, no2, peso):
        cor = self.definir_cor_aresta(peso)
        self.grafo.add_edge(no1, no2, weight=round(peso, 2), color=cor)

    def adicionar_no_com_interacoes(self, individuo):
        with self.lock:
            if not self.running:
                return
            peso_interacao = random.uniform(0.0, 1.0)
            self.adicionar_no(individuo)
            for no in self.grafo.nodes:
                if no != individuo:
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

    def definir_cor_aresta(self, peso):
        if peso < 0.5:
            return 'red'
        elif peso > 0.5:
            return 'green'
        else:
            return 'blue'

    def visualizar_rede(self, i):
        with self.lock:
            if self.houve_mudanca:
                self.ax.clear()
                pos = nx.spring_layout(self.grafo, seed=42)
                edges = self.grafo.edges(data=True)
                colors = [edge[2]['color'] for edge in edges]
                labels = {(edge[0], edge[1]): f"{edge[2]['weight']:.2f}" for edge in edges}
                nx.draw(self.grafo, pos, ax=self.ax, with_labels=True, font_weight='bold', edge_color=colors, width=2)
                nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels)
                self.houve_mudanca = False
            if not plt.fignum_exists(self.fig.number):
                self.running = False

rede_social = RedeSocial()

intervalo_criacao = 5

thread_criacao = threading.Thread(target=rede_social.iniciar_adicao_progressiva, args=(intervalo_criacao,))
thread_criacao.start()

ani = FuncAnimation(rede_social.fig, rede_social.visualizar_rede, interval=1000, cache_frame_data=False, save_count=50)
plt.show()

rede_social.running = False
thread_criacao.join()