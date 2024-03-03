from simular_perfil import SimuladorPerfil

if __name__ == "__main__":
    simulator = SimuladorPerfil()
    profile1 = simulator.criar_perfil(2)
    profile2 = simulator.criar_perfil_por_tipo('Realista', 1)
    affinity = simulator.calcular_afinidade(profile1, profile2)
    print(f"Affinity between profiles: {affinity}")
    print(f"Affinity probability: {simulator.calcular_probabilidade_afinidade(affinity)}")

