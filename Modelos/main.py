import threading
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as fm
import matplotlib as mpl
from analise_rede import AnaliseRedeSocial  # Mantido para análise posterior

# Configurações gerais de estilo
plt.style.use('ggplot')
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.facecolor'] = '#f8f8f8'

class RedeSocial:
    def __init__(self):
        self.grafo = nx.Graph()
        self.lock = threading.Lock()
        self.houve_mudanca = False
        self.fig = plt.figure(figsize=(16, 9), facecolor='#f0f0f0')
        self.gs = self.fig.add_gridspec(2, 3)
        self.ax_grafo = self.fig.add_subplot(self.gs[:, :2])
        self.ax_tabela = self.fig.add_subplot(self.gs[0, 2])
        self.ax_metricas = self.fig.add_subplot(self.gs[1, 2])
        
        # Área para controles
        self.ax_controls = plt.axes([0.15, 0.02, 0.7, 0.05])
        self.ax_controls.set_axis_off()
        
        self.running = True
        self.paused = False
        self.bem_estar_historico = []
        self.metricas_historico = []
        self.intervalo_criacao = 5
        self.intervalo_atualizacao = 3
        
        # Configurações de cores
        self.cmap = self.criar_mapa_cores()
        self.node_colors = []
        
        # Controles
        self.btn_pause = Button(
            plt.axes([0.05, 0.02, 0.08, 0.05]), 
            'Pausar' if not self.paused else 'Continuar',
            color='#4c72b0' if not self.paused else '#55a868'
        )
        self.btn_pause.on_clicked(self.toggle_pause)
        
        self.slider_criacao = Slider(
            plt.axes([0.15, 0.05, 0.2, 0.03]), 
            'Criação (s)', 1, 10, valinit=self.intervalo_criacao,
            color='#4c72b0', valfmt='%1.1f s'
        )
        self.slider_criacao.on_changed(self.set_intervalo_criacao)
        
        self.slider_atualizacao = Slider(
            plt.axes([0.4, 0.05, 0.2, 0.03]), 
            'Atualização (s)', 0.5, 10, valinit=self.intervalo_atualizacao,
            color='#c44e52', valfmt='%1.1f s'
        )
        self.slider_atualizacao.on_changed(self.set_intervalo_atualizacao)
        
        self.btn_reset = Button(
            plt.axes([0.65, 0.02, 0.08, 0.05]), 
            'Reiniciar', color='#dd8452'
        )
        self.btn_reset.on_clicked(self.reiniciar_simulacao)
        
        self.btn_export = Button(
            plt.axes([0.75, 0.02, 0.08, 0.05]), 
            'Exportar', color='#8172b3'
        )
        self.btn_export.on_clicked(self.exportar_dados)
        
        plt.subplots_adjust(bottom=0.15, top=0.95, left=0.05, right=0.98, hspace=0.3, wspace=0.2)

    def criar_mapa_cores(self):
        """Cria um mapa de cores personalizado para as arestas"""
        colors = [
            (0.0, '#8b0000'),   # darkred
            (0.3, '#ff0000'),   # red
            (0.5, '#1f77b4'),   # blue
            (0.7, '#2ca02c'),   # green
            (1.0, '#006400')    # darkgreen
        ]
        return LinearSegmentedColormap.from_list('affinity_cmap', colors)

    def adicionar_no(self, individuo):
        self.grafo.add_node(individuo)
        # Atribui uma cor aleatória suave para o nó
        self.node_colors.append((
            random.uniform(0.6, 0.9),
            random.uniform(0.6, 0.9),
            random.uniform(0.7, 1.0)
        ))

    def adicionar_aresta(self, no1, no2, peso):
        cor = self.cmap(peso)
        self.grafo.add_edge(no1, no2, weight=round(peso, 2), color=cor)

    def atualizar_afinidades(self):
        if not self.running or self.paused:
            return
            
        with self.lock:
            for u, v, data in self.grafo.edges(data=True):
                peso_atual = data['weight']
                
                # Ajuste mais suave para pesos extremos
                if peso_atual < 0.3:
                    ajuste = random.uniform(-0.03, 0.04)
                elif peso_atual > 0.7:
                    ajuste = random.uniform(-0.04, 0.03)
                else:
                    ajuste = random.uniform(-0.05, 0.05)
                    
                novo_peso = min(max(peso_atual + ajuste, 0), 1)
                cor_nova = self.cmap(novo_peso)
                self.grafo[u][v]['weight'] = round(novo_peso, 2)
                self.grafo[u][v]['color'] = cor_nova
            self.houve_mudanca = True

    def adicionar_no_com_interacoes(self, individuo):
        if not self.running or self.paused:
            return
            
        with self.lock:
            self.adicionar_no(individuo)
            nodes = list(self.grafo.nodes)
            
            if len(nodes) > 1:
                # Conexão preferencial: conecta mais fortemente a nós com alta centralidade
                degrees = nx.degree_centrality(self.grafo)
                popular_nodes = sorted(degrees, key=degrees.get, reverse=True)[:min(3, len(nodes)-1)]
                
                for no in nodes:
                    if no == individuo:
                        continue
                        
                    # Conexões mais fortes com nós populares
                    if no in popular_nodes:
                        peso_interacao = random.triangular(0.5, 1.0, 0.7)
                    else:
                        peso_interacao = random.triangular(0.0, 1.0, 0.5)
                        
                    self.adicionar_aresta(individuo, no, peso_interacao)
                    
            self.houve_mudanca = True

    def iniciar_adicao_progressiva(self):
        contador = 1
        while self.running:
            if not self.paused:
                individuo_nome = f"Indivíduo {contador}"
                self.adicionar_no_com_interacoes(individuo_nome)
                contador += 1
            sleep(self.intervalo_criacao)

    def iniciar_atualizacao_afinidades(self):
        while self.running:
            self.atualizar_afinidades()
            sleep(self.intervalo_atualizacao)

    def calcular_bem_estar_social(self):
        with self.lock:
            if self.grafo.number_of_edges() == 0:
                return 0.0
                
            # Calcula a média das afinidades
            soma_pesos = sum(data['weight'] for _, _, data in self.grafo.edges(data=True))
            bem_estar = soma_pesos / self.grafo.number_of_edges()
            
            # Penalização por nós isolados
            nos_isolados = [n for n in self.grafo.nodes if self.grafo.degree(n) == 0]
            fator_isolamento = len(nos_isolados) / self.grafo.number_of_nodes()
            
            # Penalização por fragmentação
            componentes = list(nx.connected_components(self.grafo))
            fator_fragmentacao = (len(componentes) - 1) / len(self.grafo.nodes)
            
            # Ajuste final
            return round(bem_estar * (1 - fator_isolamento) * (1 - fator_fragmentacao/2), 3)

    def calcular_metricas(self):
        """Calcula várias métricas da rede"""
        metricas = {}
        
        with self.lock:
            metricas['bem_estar'] = self.calcular_bem_estar_social()
            metricas['nós'] = self.grafo.number_of_nodes()
            metricas['arestas'] = self.grafo.number_of_edges()
            metricas['densidade'] = round(nx.density(self.grafo), 3)
            
            if metricas['nós'] > 0:
                metricas['isolados'] = sum(1 for n in self.grafo.nodes if self.grafo.degree(n) == 0)
                metricas['componentes'] = nx.number_connected_components(self.grafo)
                metricas['diâmetro'] = nx.diameter(self.grafo) if metricas['componentes'] == 1 else 'N/A'
                metricas['agrupamento'] = round(nx.average_clustering(self.grafo), 3)
            else:
                metricas['isolados'] = 0
                metricas['componentes'] = 0
                metricas['diâmetro'] = 'N/A'
                metricas['agrupamento'] = 0
                
        return metricas

    def visualizar_rede(self, i):
        with self.lock:
            if not plt.fignum_exists(self.fig.number):
                self.running = False
                return
                
            if self.houve_mudanca:
                # Atualiza a visualização da rede
                self.ax_grafo.clear()
                
                # Layout adaptativo
                if len(self.grafo.nodes) < 20:
                    pos = nx.spring_layout(self.grafo, seed=42, k=0.8)
                else:
                    pos = nx.kamada_kawai_layout(self.grafo)
                
                # Desenha arestas com cores gradientes
                edges = self.grafo.edges(data=True)
                edge_colors = [data['color'] for _, _, data in edges]
                edge_widths = [data['weight']*3 + 0.5 for _, _, data in edges]
                
                nx.draw_networkx_edges(
                    self.grafo, pos, ax=self.ax_grafo, 
                    edge_color=edge_colors, width=edge_widths, 
                    alpha=0.7
                )
                
                # Desenha nós com cores personalizadas
                if not self.node_colors or len(self.node_colors) != len(self.grafo.nodes):
                    self.node_colors = [(0.7, 0.7, 1.0) for _ in self.grafo.nodes]
                
                nx.draw_networkx_nodes(
                    self.grafo, pos, ax=self.ax_grafo, 
                    node_size=800, 
                    node_color=self.node_colors,
                    edgecolors='gray',
                    linewidths=0.8
                )
                
                # Rótulos dos nós
                nx.draw_networkx_labels(
                    self.grafo, pos, ax=self.ax_grafo, 
                    font_size=9, 
                    font_weight='bold',
                    font_color='#333333'
                )
                
                # Calcula e exibe métricas
                metricas = self.calcular_metricas()
                bem_estar = metricas['bem_estar']
                self.bem_estar_historico.append(bem_estar)
                self.metricas_historico.append(metricas)
                
                # Título com informações da rede
                titulo = f"Rede Social: {metricas['nós']} indivíduos, {metricas['arestas']} conexões\n"
                titulo += f"Bem-Estar Social: {bem_estar} - {self.interpretar_bem_estar(bem_estar)}"
                self.ax_grafo.set_title(titulo, fontsize=14, pad=20, color='#2a2a2a')
                
                # Legenda de cores
                legend_elements = [
                    plt.Line2D([0], [0], color=self.cmap(0.8), lw=4, label='Forte (≥0.7)'),
                    plt.Line2D([0], [0], color=self.cmap(0.6), lw=4, label='Boa (≥0.5)'),
                    plt.Line2D([0], [0], color=self.cmap(0.5), lw=4, label='Neutra (0.5)'),
                    plt.Line2D([0], [0], color=self.cmap(0.4), lw=4, label='Fraca (≥0.3)'),
                    plt.Line2D([0], [0], color=self.cmap(0.2), lw=4, label='Conflituosa (<0.3)')
                ]
                self.ax_grafo.legend(
                    handles=legend_elements, 
                    loc='upper right', 
                    fontsize=8,
                    title='Intensidade das Conexões',
                    title_fontsize=9
                )
                
                # Atualiza a tabela de afinidades
                self.ax_tabela.clear()
                self.exibir_tabela_afinidades()
                
                # Atualiza o painel de métricas
                self.ax_metricas.clear()
                self.exibir_painel_metricas(metricas)
                
                self.houve_mudanca = False

    def interpretar_bem_estar(self, valor):
        """Retorna interpretação textual do valor do bem-estar"""
        if valor >= 0.7:
            return "Alta coesão social"
        elif valor >= 0.5:
            return "Relações equilibradas"
        elif valor >= 0.4:
            return "Tensões moderadas"
        elif valor >= 0.3:
            return "Conflitos significativos"
        else:
            return "Crise social grave"

    def exibir_tabela_afinidades(self):
        """Exibe uma tabela de afinidades entre os indivíduos"""
        individuos = list(self.grafo.nodes)
        n = len(individuos)
        
        if n == 0:
            self.ax_tabela.text(0.5, 0.5, "Nenhum indivíduo na rede", 
                              ha='center', va='center', fontsize=12)
            self.ax_tabela.set_title("Matriz de Afinidades", fontsize=12)
            self.ax_tabela.axis('off')
            return
            
        # Limita a exibição para redes grandes
        if n > 15:
            self.ax_tabela.text(0.5, 0.5, f"Rede muito grande ({n} indivíduos)\nMatriz não exibida", 
                              ha='center', va='center', fontsize=10)
            self.ax_tabela.set_title("Matriz de Afinidades", fontsize=12)
            self.ax_tabela.axis('off')
            return
            
        afinidades = np.zeros((n, n))
        cores = np.empty((n, n), dtype=object)
        
        for i, u in enumerate(individuos):
            for j, v in enumerate(individuos):
                if u == v:
                    afinidades[i, j] = np.nan
                    cores[i, j] = '#f8f8f8'  # Fundo cinza claro
                elif self.grafo.has_edge(u, v):
                    peso = self.grafo[u][v]['weight']
                    afinidades[i, j] = peso
                    cores[i, j] = self.cmap(peso)
                else:
                    afinidades[i, j] = 0
                    cores[i, j] = '#ffffff'  # Branco

        # Cria a tabela
        self.ax_tabela.axis("off")
        tabela = self.ax_tabela.table(
            cellText=np.round(afinidades, 2),
            rowLabels=individuos,
            colLabels=individuos,
            cellColours=cores,
            cellLoc="center",
            loc="center",
            bbox=[0, 0, 1, 1]
        )
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(8)
        
        # Estiliza cabeçalhos
        for cell in tabela._cells:
            if cell[0] == 0 or cell[1] == -1:
                tabela._cells[cell].set_text_props(fontweight='bold', color='#333333')
                tabela._cells[cell].set_facecolor('#e0e0e0')
        
        self.ax_tabela.set_title("Matriz de Afinidades", fontsize=12, pad=10)

    def exibir_painel_metricas(self, metricas):
        """Exibe um painel com as principais métricas da rede"""
        self.ax_metricas.clear()
        self.ax_metricas.axis("off")
        
        # Configurações do painel
        bg_color = '#f0f0f0'
        header_color = '#4c72b0'
        text_color = '#333333'
        
        # Cabeçalho
        rect = Rectangle((0, 0.8), 1, 0.2, transform=self.ax_metricas.transAxes, 
                        color=header_color, alpha=0.8)
        self.ax_metricas.add_patch(rect)
        self.ax_metricas.text(0.5, 0.9, "MÉTRICAS DA REDE", 
                            ha='center', va='center', 
                            fontsize=12, color='white', fontweight='bold')
        
        # Corpo das métricas
        self.ax_metricas.text(0.05, 0.65, "Indivíduos:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.65, f"{metricas['nós']}", ha='right', color=text_color)
        
        self.ax_metricas.text(0.05, 0.55, "Conexões:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.55, f"{metricas['arestas']}", ha='right', color=text_color)
        
        self.ax_metricas.text(0.05, 0.45, "Densidade:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.45, f"{metricas['densidade']}", ha='right', color=text_color)
        
        self.ax_metricas.text(0.05, 0.35, "Componentes:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.35, f"{metricas['componentes']}", ha='right', color=text_color)
        
        self.ax_metricas.text(0.05, 0.25, "Isolados:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.25, f"{metricas['isolados']}", ha='right', color=text_color)
        
        self.ax_metricas.text(0.05, 0.15, "Coef. Agrupamento:", fontweight='bold', color=text_color)
        self.ax_metricas.text(0.55, 0.15, f"{metricas['agrupamento']}", ha='right', color=text_color)
        
        # Bem-estar com destaque
        self.ax_metricas.text(0.05, 0.05, "BEM-ESTAR SOCIAL:", fontweight='bold', 
                             fontsize=11, color='#2a2a2a')
        self.ax_metricas.text(0.55, 0.05, f"{metricas['bem_estar']}", 
                             ha='right', fontsize=11, fontweight='bold',
                             color='#c44e52' if metricas['bem_estar'] < 0.5 else '#55a868')
        
        # Barra de bem-estar
        bar_width = metricas['bem_estar'] * 0.5
        self.ax_metricas.add_patch(Rectangle(
            (0.6, 0.025), bar_width, 0.02, 
            color='#c44e52' if metricas['bem_estar'] < 0.5 else '#55a868'
        ))
        self.ax_metricas.text(0.6 + bar_width + 0.02, 0.03, 
                            self.interpretar_bem_estar(metricas['bem_estar']),
                            fontsize=8, color=text_color)

    # Funções de controle da interface
    def toggle_pause(self, event):
        self.paused = not self.paused
        self.btn_pause.label.set_text('Continuar' if self.paused else 'Pausar')
        self.btn_pause.color = '#55a868' if self.paused else '#4c72b0'
        
    def set_intervalo_criacao(self, valor):
        self.intervalo_criacao = valor
        
    def set_intervalo_atualizacao(self, valor):
        self.intervalo_atualizacao = valor
        
    def reiniciar_simulacao(self, event):
        with self.lock:
            self.grafo = nx.Graph()
            self.node_colors = []
            self.houve_mudanca = True
            self.bem_estar_historico = []
            self.metricas_historico = []
            
    def exportar_dados(self, event):
        print("Exportando dados da rede...")
        # Implementação real salvaria em arquivo
        with self.lock:
            print(f"Total de indivíduos: {len(self.grafo.nodes)}")
            print(f"Total de conexões: {len(self.grafo.edges)}")
            print(f"Último bem-estar: {self.bem_estar_historico[-1] if self.bem_estar_historico else 'N/A'}")

# Instância da Rede Social
rede_social = RedeSocial()

# Iniciando threads
thread_criacao = threading.Thread(target=rede_social.iniciar_adicao_progressiva)
thread_atualizacao = threading.Thread(target=rede_social.iniciar_atualizacao_afinidades)

thread_criacao.start()
thread_atualizacao.start()

# Configuração da animação
ani = FuncAnimation(
    rede_social.fig, 
    rede_social.visualizar_rede, 
    interval=500, 
    cache_frame_data=False
)
plt.tight_layout()
plt.show()

# Finalizando as threads
rede_social.running = False
thread_criacao.join()
thread_atualizacao.join()

# Análise da Rede e Geração do Relatório Final
analise = AnaliseRedeSocial(rede_social)
analise.gerar_relatorio()

# Plot do histórico de bem-estar
if rede_social.bem_estar_historico:
    plt.figure(figsize=(10, 5))
    plt.plot(rede_social.bem_estar_historico, 'o-', linewidth=2, color='#4c72b0')
    plt.title('Evolução do Bem-Estar Social', fontsize=14)
    plt.xlabel('Iterações', fontsize=12)
    plt.ylabel('BS (Bem-Estar Social)', fontsize=12)
    
    # Adiciona média móvel
    window_size = max(1, len(rede_social.bem_estar_historico) // 10)
    if window_size > 1:
        weights = np.ones(window_size) / window_size
        media_movel = np.convolve(rede_social.bem_estar_historico, weights, mode='valid')
        plt.plot(range(window_size-1, len(rede_social.bem_estar_historico)), media_