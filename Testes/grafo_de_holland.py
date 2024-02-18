import random
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Função para criar características aleatórias para o perfil
def criar_perfil(caos):
    return (
        random.randint(0, 10) + caos,
        random.randint(0, 10) + caos,
        random.randint(0, 10) + caos,
        random.randint(0, 10) + caos
    )

# Função para calcular a afinidade entre dois perfis
def calcular_afinidade(perfil1, perfil2):
    afinidade = 0
    for i in range(len(perfil1)):
        afinidade += abs(perfil1[i] - perfil2[i])
    return afinidade

# Parâmetros da equação de Lorenz
sigma = 10
rho = 28
beta = 8/3
dt = 0.01

# Condições iniciais
x, y, z = 0.1, 0.1, 0.1

# Criar grafo vazio
grafo = nx.Graph()

# Listas para armazenar a evolução das afinidades e do caos ao longo do tempo
evolucao_afinidades = []
evolucao_caos = []

# Função para calcular a probabilidade de formação de aresta com base na afinidade
def calcular_probabilidade_afinidade(afinidade):
    # Ajustar a função de probabilidade conforme necessário
    return max(0, 1 - afinidade / 50)

while True:
    # Resolver equação de Lorenz
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    x += dx
    y += dy
    z += dz
    
    # Atualizar valor do caos
    caos = z
    
    # Armazenar valor do caos
    evolucao_caos.append(caos)
    
    # Criar novo indivíduo
    novo_individuo = criar_perfil(caos)
    grafo.add_node(novo_individuo)
    
    # Procurar indivíduo mais próximo para criar uma aresta
    menor_afinidade = float('inf')
    individuo_mais_proximo = None
    for individuo in grafo.nodes():
        if individuo != novo_individuo:
            afinidade = calcular_afinidade(novo_individuo, individuo)
            if afinidade < menor_afinidade:
                menor_afinidade = afinidade
                individuo_mais_proximo = individuo
    
    # Calcular probabilidade de formação de aresta com base na afinidade
    probabilidade = calcular_probabilidade_afinidade(menor_afinidade)
    
    # Gerar número aleatório para decidir se a aresta será formada
    if random.random() < probabilidade:
        grafo.add_edge(novo_individuo, individuo_mais_proximo)
    
    # Armazenar evolução das afinidades
    afinidades_iteracao = [calcular_afinidade(novo_individuo, individuo) for individuo in grafo.nodes()]
    evolucao_afinidades.append(afinidades_iteracao)
    
    # Desenhar o grafo
    plt.clf()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=False, node_size=50)
    plt.title(f"Iteração {len(evolucao_afinidades)}, Caos: {caos:.2f}")
    plt.pause(3)
    
    # Aguardar um curto período de tempo entre iterações
    time.sleep(1)

    # Verificar se a simulação deve ser encerrada
    if len(evolucao_afinidades) >= 1000:
        break

# Exibir gráfico da evolução do caos
plt.figure()
plt.plot(evolucao_caos)
plt.xlabel("Iteração")
plt.ylabel("Valor do Caos")
plt.title("Evolução do Caos ao Longo do Tempo")
plt.show()

# Exibir gráfico da evolução das afinidades
plt.figure(figsize=(10, 6))
plt.imshow(evolucao_afinidades, cmap='viridis', aspect='auto', interpolation='nearest')
plt.colorbar(label="Afinidade")
plt.xlabel("Indivíduo")
plt.ylabel("Iteração")
plt.title("Evolução das Afinidades ao Longo do Tempo")
plt.show()
