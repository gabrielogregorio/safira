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
    # COMANDOS DISPONÍVEIS PARA O SE
    comandos_comparadores = [' for igual a ',' for diferente de ',' for maior que ',' for menor que ',' e ',' ou ']
    operacoes = []
    ignorar_leitura_antes_de = -1
    valor = ''
    analise_valor = False

    for caractere in range(0,len(condicao)):
        # Caso uma condicional seja identificada (pule ela)
        if caractere < ignorar_leitura_antes_de:
            continue

        total_caracteres_restantes = len(condicao) - caractere
        encontrou_comando = False

        # VERIFICAR COMANDO
        for comando in comandos_comparadores:
            # COMANDO ENCONTRADO
            if ((condicao[caractere:caractere + len(comando)] == comando) and ( len(comando) <= total_caracteres_restantes )):
                # O QUE FAZER, DEPENDENDO DO COMANDO
                if (analise_valor == True):
                    analise_valor = False
                    operacoes.append('({})'.format(valor))
                    valor = ''

                if comando == ' for igual a ':
                    operacoes.append('==')
                    [ ignorar_leitura_antes_de , encontrou_comando ] = [caractere + len(comando),True]
                    break

                elif comando == ' for diferente de ':
                    operacoes.append('!=')
                    [ ignorar_leitura_antes_de , encontrou_comando ] = [caractere + len(comando),True]
                    break

                elif comando == ' for menor que ':
                    operacoes.append('<')
                    [ ignorar_leitura_antes_de , encontrou_comando ] = [caractere + len(comando),True]
                    break

                elif comando == ' e ':
                    operacoes.append('e')
                    [ ignorar_leitura_antes_de , encontrou_comando ] = [caractere + len(comando),True]
                    break

                elif comando == ' ou ':
                    operacoes.append('ou')
                    [ ignorar_leitura_antes_de , encontrou_comando ] = [caractere + len(comando),True]
                    break
            
        if encontrou_comando == False:

            if (analise_valor == False):
                analise_valor = True

            if (analise_valor == True):
                valor += condicao[caractere]
                if total_caracteres_restantes == 1:
                    operacoes.append('({})'.format(valor))

        encontrou_comando = False

    if operacoes != []:
        for operacao in operacoes:  
            if operacao == '==':
                print('<IGUALDADE> ',end='')        

            elif operacao == '<':
                print('<MENOR> ',end='')    

            elif operacao == '!=':
                print('<DIFERENCA> ',end='')    

            elif operacao == 'e':
                print('<AND> ',end='')    

            elif operacao == 'ou':
                print('<OR > ',end='')    

            elif '(' in operacao:
                print('__valor__ ',end='')


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

#linhas = '''mundo recebe 'x'
#mostre "mundo"
linhas = '''se numero0 for igual a numero1 ou numero2 for igual a numero3
se numero1 for igual a numero2 e numero3 for diferente de numero4 ou numero5 for menor que numero6
se numero7 for diferente de numero8
espere numero9 segundos'''.split('\n')

for linha in linhas:
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linha)
