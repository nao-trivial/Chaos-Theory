# main.py

from perfil_analyzer import PerfilClusterizer
from simular_perfil import SimuladorPerfil

def main():
    # Inicialize o simulador de perfil
    simulador = SimuladorPerfil()
    perfis = simulador.simular()
    

    clusterizer = PerfilClusterizer(perfis)
    clusterizer.calcular_caos()  # Implemente essa função
    clusterizer.clusterizar(n_clusters=3)

    # Exemplo: obter o setor de um perfil específico
    perfil_teste = (9, 4, 2, 8)
    setor = clusterizer.obter_setor(perfil_teste)
    print(f"O perfil pertence ao setor {setor}")

if __name__ == "__main__":
    main()
