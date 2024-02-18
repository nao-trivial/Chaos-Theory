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

# Função para criar um perfil com base no tipo de Holland escolhido
def criar_perfil_por_tipo(tipo, caos):
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
        return criar_perfil(caos)  # Se o tipo não for reconhecido, crie um perfil aleatório

# Função para calcular a afinidade entre dois perfis
def calcular_afinidade(perfil1, perfil2):
    afinidade = 0
    for i in range(len(perfil1)):
        afinidade += abs(perfil1[i] - perfil2[i])
    return round(afinidade, 2)  # Arredonda a afinidade para até duas casas decimais

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
    
    # Perguntar ao usuário se deseja introduzir um novo indivíduo
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
            novo_individuo = criar_perfil_por_tipo(tipo_escolhido, caos)
            grafo.add_node(novo_individuo)
        else:
            print("Tipo de perfil inválido. Criando um perfil aleatório.")
            novo_individuo = criar_perfil(caos)
            grafo.add_node(novo_individuo)
    else:
        # Criar novo indivíduo aleatório
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
        grafo.add_edge(novo_individuo, individuo_mais_proximo, afinidade=menor_afinidade)
    
    # Armazenar evolução das afinidades
    afinidades_iteracao = [calcular_afinidade(novo_individuo, individuo) for individuo in grafo.nodes()]
    evolucao_afinidades.append(afinidades_iteracao)
    
    # Perguntar ao usuário se deseja ver a evolução do sistema
    if input("Deseja ver a evolução do sistema? (sim/não): ").lower() != "sim":
        break
    
    # Desenhar o grafo
    plt.clf()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=False, node_size=50)
    # Adicionar labels das arestas com a afinidade
    labels = {(u, v): f'{d["afinidade"]:.2f}' for u, v, d in grafo.edges(data=True)}  # Arredonda a afinidade para até duas casas decimais
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.title(f"Iteração {len(evolucao_afinidades)}, Caos: {caos:.2f}")
    
    plt.pause(0.001)
    
    # Aguardar um curto período de tempo entre iterações
    time.sleep(0.1)

# Exibir gráfico da evolução do caos
plt.figure()
plt.plot(evolucao_caos)
plt.xlabel("Iteração")
plt.ylabel("Valor do Caos")
plt.title("Evolução do Caos ao Longo do Tempo")
plt.show()
