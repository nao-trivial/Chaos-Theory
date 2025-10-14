# Script de Aula: Modelando Dinâmicas Sociais com Teoria do Caos

## 📋 Visão Geral do Código

Este código demonstra como sistemas caóticos (atrator de Lorenz) podem influenciar a formação de redes sociais, criando um modelo interativo de conexões entre indivíduos com perfis variáveis.

## 🎯 Objetivos de Aprendizado

· Conceitos de Caos: Atrator de Lorenz, sensibilidade às condições iniciais
· Modelagem de Redes: Grafos, formação de conexões, medidas de similaridade
· Programação: Simulações iterativas, visualização em tempo real

## 🔧 Código Principal

```python
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
    return round(afinidade, 2)

# Parâmetros da equação de Lorenz
sigma = 10
rho = 28
beta = 8/3
dt = 0.01

# Condições iniciais
x, y, z = 0.1, 0.1, 0.1

# Criar grafo vazio
grafo = nx.Graph()

# Listas para armazenar a evolução das afinidades e do caos
evolucao_afinidades = []
evolucao_caos = []

# Função para calcular a probabilidade de formação de aresta
def calcular_probabilidade_afinidade(afinidade):
    return max(0, 1 - afinidade / 50)

# Loop principal de simulação
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
    evolucao_caos.append(caos)
    
    # Criar novo indivíduo e adicionar ao grafo
    novo_individuo = criar_perfil(caos)
    grafo.add_node(novo_individuo)
    
    # Encontrar indivíduo mais próximo
    menor_afinidade = float('inf')
    individuo_mais_proximo = None
    for individuo in grafo.nodes():
        if individuo != novo_individuo:
            afinidade = calcular_afinidade(novo_individuo, individuo)
            if afinidade < menor_afinidade:
                menor_afinidade = afinidade
                individuo_mais_proximo = individuo
    
    # Decidir se forma conexão baseado na probabilidade
    probabilidade = calcular_probabilidade_afinidade(menor_afinidade)
    
    if random.random() < probabilidade:
        grafo.add_edge(novo_individuo, individuo_mais_proximo, afinidade=menor_afinidade)
    
    # Armazenar dados para análise
    afinidades_iteracao = [calcular_afinidade(novo_individuo, individuo) for individuo in grafo.nodes()]
    evolucao_afinidades.append(afinidades_iteracao)
    
    # Interface interativa
    if input("Deseja ver a evolução do sistema? (sim/não): ").lower() != "sim":
        break
    
    # Visualização do grafo
    plt.clf()
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=False, node_size=50)
    labels = {(u, v): f'{d["afinidade"]:.2f}' for u, v, d in grafo.edges(data=True)}
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.title(f"Iteração {len(evolucao_afinidades)}, Caos: {caos:.2f}")
    plt.pause(0.001)
    time.sleep(0.1)

# Visualizações finais
plt.figure()
plt.plot(evolucao_caos)
plt.xlabel("Iteração")
plt.ylabel("Valor do Caos")
plt.title("Evolução do Caos ao Longo do Tempo")
plt.show()

plt.figure(figsize=(10, 6))
plt.imshow(evolucao_afinidades, cmap='viridis', aspect='auto', interpolation='nearest')
plt.colorbar(label="Afinidade")
plt.xlabel("Indivíduo")
plt.ylabel("Iteração")
plt.title("Evolução das Afinidades ao Longo do Tempo")
plt.show()
```

## 🧩 Explicação dos Componentes

### 1. Sistema Caótico (Lorenz)

```python
# Equações diferenciais que geram comportamento caótico
dx = sigma * (y - x) * dt
dy = (x * (rho - z) - y) * dt
dz = (x * y - beta * z) * dt
```

· sigma, rho, beta: Parâmetros do sistema
· dt: Passo de tempo para integração numérica

### 2. Modelagem de Perfis

```python
def criar_perfil(caos):
    return (
        random.randint(0, 10) + caos,
        # ... mais dimensões
    )
```

· Cada perfil tem 4 características influenciadas pelo valor do caos
· Representa como fatores externos (caos) afetam características individuais

### 3. Métrica de Similaridade

```python
def calcular_afinidade(perfil1, perfil2):
    return sum(abs(p1 - p2) for p1, p2 in zip(perfil1, perfil2))
```

· Distância Manhattan entre perfis
· Quanto menor a afinidade, mais similares são os perfis

## 💡 Pontos de Discussão em Aula

Conceitos de Teoria do Caos

· Atrator de Lorenz: Padrão reconhecível mas não repetitivo
· Dependência sensível: Pequenas mudanças nas condições iniciais geram grandes diferenças
· Não-linearidade: O sistema não pode ser previsto a longo prazo

Aplicações em Ciências Sociais

· Como fatores externos (caos) influenciam formação de grupos
· O papel da similaridade na criação de redes sociais
· Emergência de padrões a partir de regras simples

## 🔬 Experimentos Sugeridos

1. Variando Parâmetros de Lorenz

```python
# Experimente diferentes valores:
sigma = 10    # Número de Prandtl
rho = 28      # Número de Rayleigh  
beta = 8/3    # Razão de aspecto
```

2. Modificando a Função de Afinidade

```python
# Distância Euclidiana
def calcular_afinidade(perfil1, perfil2):
    return np.sqrt(sum((p1 - p2)**2 for p1, p2 in zip(perfil1, perfil2)))

# Similaridade por cosseno  
def calcular_afinidade(perfil1, perfil2):
    dot_product = sum(p1 * p2 for p1, p2 in zip(perfil1, perfil2))
    norm1 = np.sqrt(sum(p**2 for p in perfil1))
    norm2 = np.sqrt(sum(p**2 for p in perfil2))
    return 1 - (dot_product / (norm1 * norm2))
```

3. Diferentes Estratégias de Conexão

```python
# Conectar com múltiplos indivíduos próximos
def encontrar_vizinhos_proximos(grafo, novo_individuo, k=3):
    afinidades = []
    for individuo in grafo.nodes():
        if individuo != novo_individuo:
            afinidade = calcular_afinidade(novo_individuo, individuo)
            afinidades.append((individuo, afinidade))
    # Retorna os k mais próximos
    return sorted(afinidades, key=lambda x: x[1])[:k]
```

## 📊 Análise de Resultados

Métricas para Avaliar

· Densidade da rede: nx.density(grafo)
· Coeficiente de agrupamento: nx.average_clustering(grafo)
· Distância média: nx.average_shortest_path_length(grafo)
· Centralidade: nx.degree_centrality(grafo)

Perguntas para Investigação

1. Como o valor do caos afeta a estrutura da rede?
2. Padrões emergem mesmo com comportamento caótico subjacente?
3. A rede apresenta propriedades de mundo pequeno?
4. Como a distribuição de graus evolui ao longo do tempo?

## 🛠️ Dicas para Implementação

Instalação de Dependências

```bash
pip install networkx matplotlib numpy
```

Otimizações para Aula

· Reduzir número de iterações para demonstrações rápidas
· Salvar figuras intermediárias para discussão
· Preparar diferentes condições iniciais para comparação

Extensões Possíveis

· Adicionar remoção de nós/arestas
· Implementar diferentes sistemas caóticos
· Adicionar análise em tempo real de métricas de rede

## 🎓 Atividades Práticas

1. Mapa de bifurcação: Varie um parâmetro de Lorenz e observe transições
2. Análise de sensibilidade: Teste diferentes condições iniciais
3. Comparação de métricas: Compare diferentes funções de afinidade
4. Visualização criativa: Explore diferentes layouts e cores para o grafo

---

Este material pode ser reutilizado e adaptado para aulas sobre teoria do caos, modelagem de redes e sistemas complexos.