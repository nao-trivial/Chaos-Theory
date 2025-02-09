# Definição da função de iteração
def f(x):
    return -x / 2 + 3

# Configuração da iteração
x0 = 5  # Valor inicial
num_iter = 10  # Número de iterações

# Impressão da sequência iterativa
print("Iteração da função f(x) = -x/2 + 3")
print(f"Passo 0: x = {x0}")

x = x0
for i in range(1, num_iter + 1):
    x = f(x)
    print(f"Passo {i}: x = {x}")
