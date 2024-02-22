import numpy as np

# Definição da classe CadeiaDeMarkov
class CadeiaDeMarkov(object):
    # Inicializa a classe CadeiaDeMarkov
    def __init__(self, matriz_transicao, estados):
        # Transforma a matriz de transiçao em um array 2D
        self.matriz_transicao = np.atleast_2d(matriz_transicao)

        # Lista dos estados possiveis
        self.estados = estados

        # Dicionario para mapear cada estado ao seu indice na matriz de transição
        self.dicionario_indices = {self.estados[indice]: indice for indice in range(len(self.estados))}

        # Dicionario para mapear cada indice ao seu estado correspondente
        self.dicionario_estados = {indice: self.estados[indice] for indice in range(len(self.estados))}

    # Retorna o espaço do proximo passo dado o estado atual
    def proximo_estado(self, estado_atual):
        # Escolhe o proximo estado de acordo com as probabilidades da matriz de transiçao
        return np.random.choice(self.estados, p=self.matriz_transicao[self.dicionario_indices[estado_atual], :])
    
    # Gera a proxima sequencia de estados futuros
    def gerar_estados(self, estado_atual, numero=10):
        # Lista para armazenar a sequencia de estados futuros
        estados_futuros = []
        for i in range(numero):
            # Calcula o proximo estado
            proximo_estado = self.proximo_estado(estado_atual)
            
            # Adiciona o proximo estado a lista
            estados_futuros.append(proximo_estado)

            # Atualiza o estado atual
            estado_atual = proximo_estado

        # Estados futuros
        return estados_futuros

# Exemplo de uso

# Matriz de transiçao
matriz_transicao = [[0.8, 0.2], [0.2, 0.8]]

# Cria uma instancia da classe CadeiaDeMarkov
cadeia_de_markov = CadeiaDeMarkov(matriz_transicao = matriz_transicao, 
                                  estados = ['Chuva', 'Sol']) 

# Gera a sequencia de estados
x = cadeia_de_markov.gerar_estados(estado_atual='Chuva', numero=5)

print(x)


