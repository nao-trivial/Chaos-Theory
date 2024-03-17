class EspacoProximo:
    def __init__(self, conjunto_X, relacao_proxima):
        """
        Cria um espaço próximo com um conjunto X e uma relação próxima.

        Args:
            conjunto_X (set): Conjunto X.
            relacao_proxima (callable): Função que representa a relação próxima.
        """
        self.X = conjunto_X
        self.relacao_proxima = relacao_proxima

    def propriedade_1(self, x, A):
        """
        Verifica a Propriedade 1: x v A implica A difere do conjunto vazio.

        Args:
            x: Elemento de X.
            A (set): Subconjunto de X.

        Returns:
            bool: True se a propriedade for satisfeita, False caso contrário.
        """
        return x in self.X and not self.relacao_proxima(x, A)

    def propriedade_2(self, x, A):
        """
        Verifica a Propriedade 2: x pertence a A implica x v A.

        Args:
            x: Elemento de X.
            A (set): Subconjunto de X.

        Returns:
            bool: True se a propriedade for satisfeita, False caso contrário.
        """
        return x in A and self.relacao_proxima(x, A)

    def propriedade_3(self, x, A, B):
        """
        Verifica a Propriedade 3: x v (A união B) implica x v A ou x v B.

        Args:
            x: Elemento de X.
            A (set): Subconjunto de X.
            B (set): Subconjunto de X.

        Returns:
            bool: True se a propriedade for satisfeita, False caso contrário.
        """
        return self.relacao_proxima(x, A.union(B)) and (self.relacao_proxima(x, A) or self.relacao_proxima(x, B))

    def propriedade_4(self, x, A, B):
        """
        Verifica a Propriedade 4: x v A e A é subconjunto de B implica x v B.

        Args:
            x: Elemento de X.
            A (set): Subconjunto de X.
            B (set): Subconjunto de X.

        Returns:
            bool: True se a propriedade for satisfeita, False caso contrário.
        """
        return self.relacao_proxima(x, A) and A.issubset(B) and self.relacao_proxima(x, B)

    def imprimir_informacoes(self):
        """
        Imprime informações sobre o espaço próximo.
        """
        print(f"Conjunto X: {self.X}")
        print("Relação Próxima:")
        for elemento in self.X:
            conjunto_relacionado = {y for y in self.X if self.relacao_proxima(elemento, {y})}
            print(f"{elemento} v {conjunto_relacionado}")

    def verificar_continuidade(self, f, x):
        """
        Verifica se a função f é contínua em x, de acordo com a definição de continuidade.

        :param f: Função f: X -> Y
        :param x: Ponto x em X
        :return: True se f é contínua em x, False caso contrário
        """
        for conjunto_aberto_A in self.abertos_em_Y():
            if f(x) in conjunto_aberto_A:
                for conjunto_aberto_B in self.abertos_em_X():
                    if x in conjunto_aberto_B and set(f(conjunto_aberto_B)).issubset(conjunto_aberto_A):
                        return True
        return False

    def verificar_continuidade_global(self, f):
        """
        Verifica se a função f é contínua em todos os pontos de X.

        :param f: Função f: X -> Y
        :return: True se f é contínua globalmente, False caso contrário
        """
        for ponto_x in self.X:
            if not self.verificar_continuidade(f, ponto_x):
                return False
        return True

    # (código existente...)

    def abertos_em_Y(self):
        """
        Retorna uma lista de conjuntos abertos em Y.

        :return: Lista de conjuntos abertos em Y
        """
        # Implemente a lógica para obter conjuntos abertos em Y
        pass

    def abertos_em_X(self):
        """
        Retorna uma lista de conjuntos abertos em X.

        :return: Lista de conjuntos abertos em X
        """
        # Implemente a lógica para obter conjuntos abertos em X
        pass

# Exemplo de uso
conjunto_X = {1, 2, 3, 4, 5}
relacao_proxima = lambda x, A: x in A  # Exemplo simples de relação próxima

espaco_proximo = EspacoProximo(conjunto_X, relacao_proxima)

# Verificando as propriedades
x = 1
A = {1, 2, 3}
B = {3, 4, 5}

print("Propriedade 1:", espaco_proximo.propriedade_1(x, A))
print("Propriedade 2:", espaco_proximo.propriedade_2(x, A))
print("Propriedade 3:", espaco_proximo.propriedade_3(x, A, B))
print("Propriedade 4:", espaco_proximo.propriedade_4(x, A, B))

# Imprimindo informações sobre o espaço próximo
espaco_proximo.imprimir_informacoes()
