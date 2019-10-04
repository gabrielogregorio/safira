# OS VALORES DEVEM ESTAR CORRETOS!
# NÃO SÃO SUPORTADOS ERROS NESSE PROGRAMA

# MOSTRA STRING OU NÚMERO
def mostre(conteudo):
    print(conteudo)

# COMPARA VALORES VÁLIDOS E RETORNA TRUE OU FALSE
def condicional(valor1,operacao,valor2):
    operacao = operacao.strip()

    if operacao == "==":
        if valor1 == valor2:
            return True
        else:
            return False

    elif operacao == "<": # menor que 
        if valor1 < valor2:
            return True
        else:
            return False

    elif operacao == ">": # maior que
        if valor1 > valor2:
            return True
        else:
            return False

    elif operacao == "!=":# diferente de
        if valor1 != valor2:
            return True
        else:
            return False

    else:
        return "[Erro] uma operação inválida foi repassada ao interpretador"

# CARACTERES E OPERAÇÕES VÁLIDAS DEVEM SER PASSADAS
def operacoes(valor1,operacoes,valor2):
    if operacoes == "+":
        return (valor1 + valor2)

    elif operacoes == "-":
        return (valor1 - valor2)

    elif operacoes == "/":
        return (valor1 / valor2)

    elif operacoes == "//":
        return (valor1 // valor2)

    elif operacoes == "*":
        return (valor1 * valor2)

    elif operacoes == "**":
        return (valor1 ** valor2)
    else:
        return '[Erro]. Operações inválidas foram repasadas'

# OPERAÇÕES COM FATORIAIS
def operacoes_fatorial(objetivo):
    inicio = 1

    for numero in range(0,objetivo):
        inicio = inicio * (numero+1)

    return inicio

def entrada_de_dados(tipo):
    if tipo == 'numerico':
        digite = int(input())

    else:
        digite = input()

    return digite