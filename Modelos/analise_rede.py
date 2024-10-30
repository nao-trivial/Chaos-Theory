import networkx as nx
import pandas as pd

class AnaliseRedeSocial:
    def __init__(self, rede_social):
        self.rede_social = rede_social.grafo

    def calcular_coeficiente_agrupamento(self):
        return nx.average_clustering(self.rede_social)

    def calcular_centralidade(self):
        centralidade_grau = nx.degree_centrality(self.rede_social)
        centralidade_intermediacao = nx.betweenness_centrality(self.rede_social)
        centralidade_proximidade = nx.closeness_centrality(self.rede_social)
        return centralidade_grau, centralidade_intermediacao, centralidade_proximidade

    def calcular_modularidade(self):
        communities = nx.community.greedy_modularity_communities(self.rede_social)
        modularidade = nx.algorithms.community.modularity(self.rede_social, communities)
        return modularidade

    def calcular_distribuicao_afinidade(self):
        pesos = [self.rede_social[u][v]['weight'] for u, v in self.rede_social.edges]
        return {
            "media": round(sum(pesos) / len(pesos), 2),
            "mediana": round(pd.Series(pesos).median(), 2),
            "desvio_padrao": round(pd.Series(pesos).std(), 2)
        }

    def calcular_densidade(self):
        return nx.density(self.rede_social)

    def calcular_diametro(self):
        if nx.is_connected(self.rede_social):
            return nx.diameter(self.rede_social)
        else:
            return "A rede não é conectada."

    def calcular_proporcao_afinidade(self, threshold=0.5):
        afinidade_positiva = sum(1 for _, _, d in self.rede_social.edges(data=True) if d['weight'] > threshold)
        afinidade_negativa = sum(1 for _, _, d in self.rede_social.edges(data=True) if d['weight'] <= threshold)
        total = afinidade_positiva + afinidade_negativa
        return {
            "afinidade_positiva": round(afinidade_positiva / total, 2) if total > 0 else 0,
            "afinidade_negativa": round(afinidade_negativa / total, 2) if total > 0 else 0
        }

    def gerar_tabela_afinidades(self):
        dados = {
            "Nó 1": [u for u, v, d in self.rede_social.edges(data=True)],
            "Nó 2": [v for u, v, d in self.rede_social.edges(data=True)],
            "Afinidade": [d['weight'] for u, v, d in self.rede_social.edges(data=True)]
        }
        return pd.DataFrame(dados)

    def gerar_relatorio(self):
        print("=== Análise da Rede Social ===")
        print(f"Coeficiente de Agrupamento Médio: {self.calcular_coeficiente_agrupamento():.2f}")
        
        centralidade_grau, centralidade_intermediacao, centralidade_proximidade = self.calcular_centralidade()
        print("\nCentralidade de Grau:", centralidade_grau)
        print("\nCentralidade de Intermediação:", centralidade_intermediacao)
        print("\nCentralidade de Proximidade:", centralidade_proximidade)
        
        print(f"\nModularidade da Rede: {self.calcular_modularidade():.2f}")
        
        distribuicao_afinidade = self.calcular_distribuicao_afinidade()
        print(f"\nDistribuição de Afinidade - Média: {distribuicao_afinidade['media']}, "
              f"Mediana: {distribuicao_afinidade['mediana']}, "
              f"Desvio Padrão: {distribuicao_afinidade['desvio_padrao']}")
        
        print(f"\nDensidade da Rede: {self.calcular_densidade():.2f}")
        print(f"\nDiâmetro da Rede: {self.calcular_diametro()}")
        
        proporcao_afinidade = self.calcular_proporcao_afinidade()
        print(f"\nProporção de Afinidade - Positiva: {proporcao_afinidade['afinidade_positiva']}, "
              f"Negativa: {proporcao_afinidade['afinidade_negativa']}")
        
        print("\nTabela de Afinidades:")
        print(self.gerar_tabela_afinidades())

