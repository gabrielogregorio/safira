def analisa_comandos(linha):
    # analisa se tem comandos e qual procedimento executar

    comandos_disponiveis = [' se ',' espere ',' mostre ',' repita ',' enquanto ',' pare ',' recebe ']
    for caractere in range(len(linha)):
        caracteres_restante = len(linha) - caractere

        for comando in comandos_disponiveis:
            if ((linha[  caractere : caractere + len(comando)  ] == comando) and ( len(comando) < caracteres_restante )):
                if comando == ' se ':
                    verifica_condicionais( ' '+ linha[caractere + len(comando):] + ' ' )

                elif comando == ' espere ':
                    verifica_espere( linha[caractere + len(comando):] )

                elif comando == ' recebe ':
                    verifica_atribuicoes( linha[caractere + len(comando):] )

                elif comando == ' mostre ':
                    verifica_validacao_de_valores( linha[caractere + len(comando):] )


        #*frases especiais
        # pense em um número aleatório de
    pass

def verifica_condicionais(string_condicional):
    print('verifica_condicionais | {}'.format(string_condicional))
    # ************* SO VALE PARA ITEN RELACAO COM ITEN ********************

    # ABSTRAIR COMPARADORES
    ignorar_leitura_antes_de = -1
    comparadores = [' for igual a ',' for diferente de ']
    operacao = None
    valor1 = None
    valor2 = None
    string = ''

    for caractere in range(len(string_condicional)):
        # Caso uma condicional seja identificada
        if caractere < ignorar_leitura_antes_de:
            continue

        caracteres_restante = len(string_condicional) - caractere

        # VERIFICAR COMANDO
        for comando in comparadores:
            if ((string_condicional[caractere:caractere + len(comando)] == comando) and ( len(comando) <= caracteres_restante )):
                if comando == ' for igual a ':
                    operacao = '=='
                    break

                elif comando == ' for diferente de ':
                    operacao = '!='
                    break

    if operacao != None:
        print(operacao)
    else:
        print('Não foi definida uma condição')

    # se        >>CONDICAO<<
    # enquanto  >>CONDICAO<<
    # verifica se os valores são condicionais
    # se não forem, retorna a linha do erro

def abstrair_valores_de_variaveis(variavel):
    pass

def verifica_validacao_de_valores(finalização):
    print('verifica e valida finalização | {}'.format(finalização))
    # verifica e resolve conflitos para retornar um único valor

def verifica_atribuicoes(valor):
    print('verifica atribuicoes | {}'.format(valor))
    # objeto recebe VALOR
    # Verifica se o valor é consinstente ou não

def verifica_espere(finalização):
    print('verifique o espere | {}'.format(finalização))
    #espere 2 SEGUNDOS
    # analisa se o valor é válido e se o o que vem depois também

def verifica_loop_especial ():
    # repita 20 VEZES
    # verifica o valor e o VEZES
    pass

def verifica_aleatorio():
    #verifica se os valores são válidos, pode ser string, de 'a' a 'b'
    #pense em um número aleatório de 2 a 20
    pass

linhas = '''mundo recebe 'x'
mostre "mundo"
se for igual a 4
se 4 for diferente de 3
espere 4 segundos'''.split('\n')

for linha in linhas:
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linha)
