import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Configuração geral para todos os gráficos
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

# 1. COMPORTAMENTOS BÁSICOS DA EQUAÇÃO DISCRETA
def logistic_map(x, r):
    return r * x * (1 - x)

def plot_basic_behaviors():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    r_values = [0.8, 2.5, 3.2, 3.9]
    titles = ['Extinção (r < 1)', 'Estabilização (1 < r < 3)', 
              'Oscilação de Período 2 (r ≈ 3.2)', 'Comportamento Caótico (r > 3.57)']
    
    for i, (r, title) in enumerate(zip(r_values, titles)):
        ax = axes[i//2, i%2]
        x = np.zeros(100)
        x[0] = 0.1  # Condição inicial
        
        for n in range(1, 100):
            x[n] = logistic_map(x[n-1], r)
        
        ax.plot(x, 'b-', linewidth=1.5)
        ax.set_title(title)
        ax.set_xlabel('Iteração (n)')
        ax.set_ylabel('População (xₙ)')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('comportamentos_basicos.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. DIAGRAMA DE BIFURCAÇÃO
def plot_bifurcation_diagram():
    # Parâmetros
    r_min, r_max = 2.5, 4.0
    r_points = 1000
    iterations = 1000
    last = 100
    
    # Inicialização
    r_values = np.linspace(r_min, r_max, r_points)
    x = 1e-5 * np.ones(r_points)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Simulação
    for i in range(iterations):
        x = logistic_map(x, r_values)
        # Plotamos apenas as últimas iterações
        if i >= (iterations - last):
            ax.plot(r_values, x, ',k', alpha=0.25, markersize=0.1)
    
    ax.set_xlabel('Taxa de crescimento (r)')
    ax.set_ylabel('População (x)')
    ax.set_title('Diagrama de Bifurcação da Equação Logística')
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    
    # Adicionando anotações para pontos críticos
    critical_points = [3, 3.45, 3.57]
    for cp in critical_points:
        ax.axvline(x=cp, color='red', linestyle='--', alpha=0.7)
        ax.text(cp, 0.95, f'r = {cp}', rotation=90, verticalalignment='top')
    
    plt.savefig('diagrama_bifurcacao.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. SOLUÇÃO DA EQUAÇÃO DIFERENCIAL LOGÍSTICA
def logistic_ode(P, t, r, K):
    return r * P * (1 - P/K)

def plot_logistic_ode():
    # Parâmetros
    r = 0.5  # Taxa de crescimento
    K = 1000  # Capacidade de suporte
    P0 = 10   # População inicial
    
    # Tempo
    t = np.linspace(0, 50, 500)
    
    # Solução da EDO
    solution = odeint(logistic_ode, P0, t, args=(r, K))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, solution, 'b-', linewidth=2, label=f'P(t), r={r}, K={K}')
    ax.axhline(y=K, color='red', linestyle='--', label=f'Capacidade de suporte (K={K})')
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('População P(t)')
    ax.set_title('Solução da Equação Diferencial Logística')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig('equacao_diferencial.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. SENSIBILIDADE ÀS CONDIÇÕES INICIAIS
def plot_sensitivity():
    r = 3.9  # Valor que gera comportamento caótico
    x0_1 = 0.1
    x0_2 = 0.1001  # Condição inicial ligeiramente diferente
    
    iterations = 100
    
    # Simulação para duas condições iniciais
    x1 = np.zeros(iterations)
    x2 = np.zeros(iterations)
    
    x1[0] = x0_1
    x2[0] = x0_2
    
    for n in range(1, iterations):
        x1[n] = logistic_map(x1[n-1], r)
        x2[n] = logistic_map(x2[n-1], r)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Trajetórias individuais
    ax1.plot(x1, 'b-', linewidth=1.5, label=f'x₀ = {x0_1}')
    ax1.plot(x2, 'r-', linewidth=1.5, label=f'x₀ = {x0_2}')
    ax1.set_xlabel('Iteração (n)')
    ax1.set_ylabel('População (xₙ)')
    ax1.set_title('Sensibilidade às Condições Iniciais (Trajetórias)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Diferença entre as trajetórias
    ax2.plot(np.abs(x1 - x2), 'g-', linewidth=1.5)
    ax2.set_xlabel('Iteração (n)')
    ax2.set_ylabel('|x₁ - x₂|')
    ax2.set_title('Divergência entre Trajetórias')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sensibilidade_condicoes_iniciais.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. COMPARAÇÃO ENTRE FORMA DISCRETA E CONTÍNUA
def plot_comparison():
    # Parâmetros
    r_disc = 2.8  # Para a forma discreta
    r_cont = 0.7  # Para a forma contínua (valor menor para comparação justa)
    K = 1         # Capacidade de suporte normalizada
    
    # Forma discreta
    iterations = 50
    x_disc = np.zeros(iterations)
    x_disc[0] = 0.1
    
    for n in range(1, iterations):
        x_disc[n] = logistic_map(x_disc[n-1], r_disc)
    
    # Forma contínua
    t = np.linspace(0, 25, 250)
    P0 = 0.1
    solution = odeint(logistic_ode, P0, t, args=(r_cont, K))
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plotando ambas as soluções
    ax.plot(range(iterations), x_disc, 'bo-', linewidth=1.5, markersize=4, 
            label=f'Forma Discreta (r={r_disc})')
    ax.plot(t, solution, 'r-', linewidth=2, 
            label=f'Forma Contínua (r={r_cont}, K={K})')
    
    ax.set_xlabel('Tempo / Iterações')
    ax.set_ylabel('População')
    ax.set_title('Comparação entre as Formas Discreta e Contínua da Equação Logística')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig('comparacao_formas.png', dpi=300, bbox_inches='tight')
    plt.close()

# Executar todas as funções para gerar as imagens
if __name__ == "__main__":
    plot_basic_behaviors()
    plot_bifurcation_diagram()
    plot_logistic_ode()
    plot_sensitivity()
    plot_comparison()
    print("Todas as imagens foram geradas com sucesso!")