import numpy as np

class ModelosEstocasticos:
    def cadeia_markov(self, estado_inicial, matriz_transicao, n):
        """
        Simula uma Cadeia de Markov.
        
        Parâmetros:
        estado_inicial : int : estado inicial (índice do estado)
        matriz_transicao : np.ndarray : matriz de transição de estados
        n : int : número de iterações
        """
        estados = [estado_inicial]
        for _ in range(n - 1):
            estado_atual = estados[-1]
            estado_proximo = np.random.choice(len(matriz_transicao), p=matriz_transicao[estado_atual])
            estados.append(estado_proximo)
        return estados
