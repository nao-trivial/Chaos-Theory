import numpy as np
from typing import List, Union

class CadeiaDeMarkov:
    """
    Classe para simular uma Cadeia de Markov discreta com base em uma matriz de transição e estados definidos.
    
    Atributos:
        matriz_transicao (np.ndarray): Matriz de transição de estados (deve ser quadrada e estocástica).
        estados (List[str]): Lista de nomes dos estados possíveis.
        dicionario_indices (dict): Mapeia cada estado para seu índice correspondente na matriz.
        dicionario_estados (dict): Mapeia cada índice para seu estado correspondente.
    """
    
    def __init__(self, matriz_transicao: Union[List[List[float]], np.ndarray], estados: List[str]):
        """
        Inicializa a Cadeia de Markov com a matriz de transição e estados fornecidos.

        Args:
            matriz_transicao (Union[List[List[float]], np.ndarray]): Matriz de transição entre estados.
            estados (List[str]): Lista de nomes dos estados.

        Raises:
            ValueError: Se a matriz não for quadrada, as linhas não somarem ~1 ou o número de estados for incompatível.
        """
        self.matriz_transicao = np.atleast_2d(matriz_transicao)
        self.estados = estados
        
        # Validações
        if self.matriz_transicao.shape[0] != self.matriz_transicao.shape[1]:
            raise ValueError("A matriz de transição deve ser quadrada.")
        
        if len(self.estados) != self.matriz_transicao.shape[0]:
            raise ValueError("O número de estados deve corresponder ao tamanho da matriz de transição.")
        
        # Verifica se cada linha da matriz soma aproximadamente 1
        for i, linha in enumerate(self.matriz_transicao):
            if not np.isclose(np.sum(linha), 1.0, atol=0.001):
                raise ValueError(f"A linha {i} da matriz de transição soma {np.sum(linha)} (deve ser 1).")
        
        # Cria dicionários para mapeamento entre estados e índices
        self.dicionario_indices = {estado: indice for indice, estado in enumerate(self.estados)}
        self.dicionario_estados = {indice: estado for indice, estado in enumerate(self.estados)}
    
    def proximo_estado(self, estado_atual: str) -> str:
        """
        Retorna o próximo estado com base nas probabilidades da matriz de transição.

        Args:
            estado_atual (str): Estado atual da cadeia.

        Returns:
            str: Próximo estado.

        Raises:
            KeyError: Se o estado atual não existir na lista de estados.
        """
        if estado_atual not in self.dicionario_indices:
            raise KeyError(f"Estado '{estado_atual}' não encontrado. Estados válidos: {self.estados}")
        
        indice = self.dicionario_indices[estado_atual]
        return np.random.choice(self.estados, p=self.matriz_transicao[indice, :])
    
    def gerar_estados(self, estado_atual: str, passos: int = 10) -> List[str]:
        """
        Gera uma sequência de estados futuros a partir do estado atual.

        Args:
            estado_atual (str): Estado inicial da sequência.
            passos (int, opcional): Número de passos/transições a serem simulados. Padrão: 10.

        Returns:
            List[str]: Lista contendo a sequência de estados gerados.
        """
        if estado_atual not in self.dicionario_indices:
            raise KeyError(f"Estado inicial '{estado_atual}' não encontrado. Estados válidos: {self.estados}")
        
        estados_gerados = []
        estado = estado_atual
        for _ in range(passos):
            estado = self.proximo_estado(estado)
            estados_gerados.append(estado)
        return estados_gerados

# Exemplo de uso
if __name__ == "__main__":
    matriz_transicao = [[0.8, 0.2], [0.2, 0.8]]
    estados = ['Chuva', 'Sol']
    
    try:
        cadeia = CadeiaDeMarkov(matriz_transicao, estados)
        sequencia = cadeia.gerar_estados('Chuva', passos=5)
        print("Sequência gerada:", sequencia)
    except Exception as e:
        print(f"Erro: {e}")