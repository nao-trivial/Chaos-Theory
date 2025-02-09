# Importando a classe EspacoProximo do arquivo topology_engine.py
from topology_engine import EspacoProximo

def teste_propriedades(espaco):
    """
    Função para testar as propriedades de um espaço próximo.
    """
    x = 1
    A = {1, 2, 3}
    B = {3, 4, 5}

    # Testando as propriedades
    print("Teste da Propriedade 1:", "Passou" if espaco.propriedade_1(x, A) else "Falhou")
    print("Teste da Propriedade 2:", "Passou" if espaco.propriedade_2(x, A) else "Falhou")
    print("Teste da Propriedade 3:", "Passou" if espaco.propriedade_3(x, A, B) else "Falhou")
    print("Teste da Propriedade 4:", "Passou" if espaco.propriedade_4(x, A, B) else "Falhou")

def main():
    # Definindo um conjunto e uma relação próxima simples para o teste
    conjunto_X = {1, 2, 3, 4, 5}
    relacao_proxima = lambda x, A: x in A  # Exemplo de relação próxima

    # Criando uma instância de EspacoProximo
    espaco_proximo = EspacoProximo(conjunto_X, relacao_proxima)

    # Executando os testes das propriedades
    teste_propriedades(espaco_proximo)

    # Imprimindo informações sobre o espaço próximo
    espaco_proximo.imprimir_informacoes()

if __name__ == "__main__":
    main()
