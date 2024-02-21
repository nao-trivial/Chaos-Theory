import numpy as np

class MarkovChain(object):
    # Inicializa a classe MarkovChain
    def __init__(self, transition_matrix, states):
        self.transition_matrix = np.atleast_2d(transition_matrix)
        self.states = states


"""# Importando a biblioteca numpy
import numpy as np

# Definindo a classe MarkovChain
class MarkovChain(object):
    def __init__(self, transition_matrix, states):
        """
       # Inicializa a classe MarkovChain
        """
        # Converte a matriz de transição para um array 2D
        self.transition_matrix = np.atleast_2d(transition_matrix)
        # Lista dos possíveis estados
        self.states = states
        # Dicionário para mapear cada estado para seu índice na matriz de transição
        self.index_dict = {self.states[index]: index for index in range(len(self.states))}
        # Dicionário para mapear cada índice para seu estado correspondente
        self.state_dict = {index: self.states[index] for index in range(len(self.states))}

    def next_state(self, current_state):
        """
        #Retorna o estado do próximo passo dado o estado atual.
        """
        # Escolhe o próximo estado de acordo com as probabilidades da matriz de transição
        return np.random.choice(
         self.states, 
         p=self.transition_matrix[self.index_dict[current_state], :]
        )

    def generate_states(self, current_state, no=10):
        """
        #Gera a próxima sequência de estados
        """
        # Lista para armazenar a sequência de estados futuros
        future_states = []
        for i in range(no):
            # Calcula o próximo estado
            next_state = self.next_state(current_state)
            # Adiciona o próximo estado à lista
            future_states.append(next_state)
            # Atualiza o estado atual
            current_state = next_state
        # Retorna a lista de estados futuros
        return future_states

# Matriz de transição
transition_matrix = [[0.8, 0.2],
                     [0.2, 0.8]]

# Cria uma instância da classe MarkovChain
markov_chain = MarkovChain(transition_matrix=transition_matrix, states=['Chuva', 'Sol'])

# Gera a sequência de estados
markov_chain.generate_states(current_state='Chuva', no=10)
"""