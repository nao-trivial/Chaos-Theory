from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

class PerfilClusterizer:
    def __init__(self, perfis):
        self.perfis = perfis
        self.caos_levels = []
        self.cluster_centers = None
        self.kmeans = None

    def calcular_caos(self):
        # Calcula o nível de caos como a média das diferenças entre os valores dos perfis
        diffs = np.diff(self.perfis, axis=0)
        self.caos_levels = np.mean(np.abs(diffs), axis=0)

    def clusterizar(self, n_clusters):
        # Padronize os perfis
        scaler = StandardScaler()
        perfis_padronizados = scaler.fit_transform(self.perfis)

        # Execute o algoritmo KMeans
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.kmeans.fit(perfis_padronizados)

        # Obtenha os centros dos clusters
        self.cluster_centers = self.kmeans.cluster_centers_

    def obter_setor(self, perfil):
        # Obtenha o setor (cluster) ao qual o perfil pertence
        return self.kmeans.predict([perfil])[0]

# Exemplo de uso
if __name__ == "__main__":
    # Suponha que você já tenha uma lista de perfis
    perfis = [
        (10, 5, 3, 7),
        (8, 6, 4, 6),
        # ... outros perfis ...
    ]

    clusterizer = PerfilClusterizer(perfis)
    clusterizer.calcular_caos()
    clusterizer.clusterizar(n_clusters=3)

    # Exemplo: obter o setor de um perfil específico
    perfil_teste = (9, 4, 2, 8)
    setor = clusterizer.obter_setor(perfil_teste)
    print(f"O perfil pertence ao setor {setor}")
