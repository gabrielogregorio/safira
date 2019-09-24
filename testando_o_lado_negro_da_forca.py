# analisa se tem comandos e qual procedimento executar
def analisa_comandos(linha):
    # RECEBE CADA LINHA DO PROGRAMA > ' ' + linha

    comandos = [' se ',
                ' espere ',
                ' mostre ',
                ' exiba ',
                ' repita ',
                ' enquanto ',
                ' pare ',
                ' recebe ']

    for caractere in range(len(linha)):
        total_caracteres_restantes = len(linha) - caractere

        for comando in comandos:
            if ((linha[  caractere : caractere + len(comando)  ] == comando) and ( len(comando) < total_caracteres_restantes )):
                if (comando == ' se '):
                    verifica_condicionais( ' '+ linha[caractere + len(comando):] + ' ' )

                elif (comando == ' espere '):
                    verifica_espere( linha[caractere + len(comando):] )

                elif (comando == ' recebe '):
                    verifica_atribuicoes( linha[caractere + len(comando):] )

                elif ((comando == ' mostre ') or (comando == ' exiba ')) :
                    verifica_validacao_de_valores( linha[caractere + len(comando):] )

def verifica_condicionais(condicao):
    print('<condicional> ',end = '')
    # ************* SO VALE PARA ITEN RELACAO COM ITEN ********************

    # ABSTRAIR COMPARADORES
    ignorar_leitura_antes_de = -1

    # COMANDOS DISPONÍVEIS PARA O SE
    comparadores = [' for igual a ',' for diferente de ',' for maior que ',' for menor que ',' e ',' ou ']
    operacoes = []

    valor1 = ''
    valor2 = ''
    analise1 = False
    analise2 = False

    for caractere in range(0,len(condicao)):
        # Caso uma condicional seja identificada (pule ela)
        if caractere < ignorar_leitura_antes_de:
            continue

        total_caracteres_restantes = len(condicao) - caractere

        # VERIFICAR COMANDO
        for comando in comparadores:
            if ((condicao[caractere:caractere + len(comando)] == comando) and ( len(comando) <= total_caracteres_restantes )):
                if comando == ' for igual a ':
                    if ((analise1 == True) and (analise2 == False)):
                        analibse1 = False
                        analise2 = True
                        operacoes.append('({})'.format(valor1))
                        valor1 = ''

                    elif ((analise1 == False) and (analise2 == True)):
                        operacoes.append('({})'.format(valor2))
                        valor2 = ''
                        analise2 = False

                    operacoes.append('==')
                    break

                elif comando == ' for diferente de ':
                    if ((analise1 == True) and (analise2 == False)):
                        analise1 = False
                        analise2 = True
                        operacoes.append('({})'.format(valor1))
                        valor1 = ''
                    elif ((analise1 == False) and (analise2 == True)):
                        operacoes.append('({})'.format(valor2))
                        valor2 = ''
                        analise2 = False
                    operacoes.append('!=')
                    break

                elif comando == ' for menor que ':
                    if ((analise1 == True) and (analise2 == False)):
                        analise2 = True
                        operacoes.append('({})'.format(valor1))
                        valor1 = ''
                    elif ((analise1 == False) and (analise2 == True)):
                        operacoes.append('({})'.format(valor2))
                        valor2 = ''
                        analise2 = False
                    operacoes.append('<')
                    break

                elif comando == ' e ':
                    if ((analise1 == True) and (analise2 == False)):
                        analise2 = True
                        operacoes.append('({})'.format(valor1))
                        valor1 = ''
                    elif ((analise1 == False) and (analise2 == True)):
                        operacoes.append('({})'.format(valor2))
                        valor1 = ''
                        valor2 = ''
                        analise2 = False
                    operacoes.append('e')
                    break
                elif comando == ' ou ':
                    if ((analise1 == True) and (analise2 == False)):
                        analise1 = False
                        analise2 = True
                        operacoes.append('({})'.format(valor1))
                        valor1 = ''
                    elif ((analise1 == False) and (analise2 == True)):
                        operacoes.append('({})'.format(valor2))
                        valor2 = ''
                        analise2 = False
                    operacoes.append('ou')
                    break

        if ((analise1 == False) and (analise2 == False)):
            analise1 == True

        if ((analise1 == True) and (analise2 == False)):
            valor1 += condicao[caractere]

        elif ((analise1 == False) and (analise2 == True)):
            valor2 += condicao[caractere]


    if operacoes != []:
        for operacao in operacoes:    

            if operacao == '==':
                print('<igualdade> ',end='')        

            elif operacao == '<':
                print('<menor> ',end='')    

            elif operacao == '!=':
                print('<diferença> ',end='')    

            elif operacao == 'e':
                print('<AND> ',end='')    

            elif operacao == 'ou':
                print('<OR> ',end='')    

            elif ('(' in operacao):
                print('({}) '.format(operacao),end='')

    else:
        print('Não foi definida uma condição')
    print('')


def abstrair_valores_de_variaveis(variavel):
    pass

def verifica_validacao_de_valores(finalização):
    print('[OK] valores > ',end = '')
    print('')

    # verifica e resolve conflitos para retornar um único valor

def verifica_atribuicoes(valor):
    print('[OK] Atribuições > ',end = '')
    # objeto recebe VALOR
    # Verifica se o valor é consinstente ou não
    print('')

def verifica_espere(finalização):
    print('[OK] espere > ',end = '')
    print('')
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
se 7 for igual a 4 e 5 for diferente de 6 ou 4 for menor que 8
se 4 for diferente de 3
espere 4 segundos'''.split('\n')

for linha in linhas:
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linha)
