global variaveis
variaveis = {}

# analisa se tem comandos e qual procedimento executar
def analisa_comandos(linha,num_linha):

    comandos = [' se ',
                ' espere ',
                ' mostre ',
                ' exiba ',
                ' repita ',
                ' enquanto ',
                ' pare ',
                ' recebe ',
                ' vale ']

    eventos = False
    for caractere in range(len(linha)):
        total_caracteres_restantes = len(linha) - caractere

        for comando in comandos:
            if ((linha[  caractere : caractere + len(comando)  ] == comando) and ( len(comando) < total_caracteres_restantes )):
                eventos = True
                if (comando == ' se '):
                    verifica_condicionais(' '+ linha[caractere + len(comando):] + ' ',num_linha )

                if (comando == ' enquanto '):
                    verifica_loop_enquanto( ' '+ linha[caractere + len(comando):] + ' ',num_linha )

                elif (comando == ' espere '):
                    verifica_espere( linha[caractere + len(comando):] , num_linha)

                elif (comando == ' recebe ' or comando == ' vale '):
                    valor_variavel = linha[caractere + len(comando):]
                    variavel = linha[:caractere]

                    definir_variaveis(variavel,valor_variavel,num_linha)

                elif ((comando == ' mostre ') or (comando == ' exiba ') or (comando == ' exiba nessa linha') or (comando == ' mostre nessa linha ')):
                    verifica_mostre( linha[caractere + len(comando):],num_linha )

    if linha == '' or linha.isspace():
        pass
    elif eventos == False:
        print('[{}] O INTERPRETADOR NÂO ENTEDEU O QUE VOCÊ QUIZ DIZER'.format(num_linha))

def abstrai_valor(objeto):
    # é uma string?
    if objeto[0] == '"' and objeto[-1] == '"':
        return [True , objeto[1:-1]]

    # é um número
    elif objeto.isnumeric():
        return [True,objeto]

    # é uma variável
    else:
        return descobrir_valor_variavel(objeto)

def verifica_condicionais(condicao,num_linha):
    print('<condicional> ',end = '')
    comandos_comparadores = [' for igual a ',' for diferente de ',' for maior que ',' for menor que ',' e ',' ou ']
    operacoes = []
    ignorar_leitura_antes_de = -1
    valor = ''
    analise_valor = False

    for caractere in range(0,len(condicao)):
        # CONDIÇÃO IDENTIFICADA, PULE ELA
        if caractere < ignorar_leitura_antes_de:
            continue

        total_caracteres_restantes = len(condicao) - caractere
        encontrou_comando = False

        for comando in comandos_comparadores:
            if ((condicao[caractere:caractere + len(comando)] == comando) and ( len(comando) <= total_caracteres_restantes )):
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
                valor = abstrai_valor((operacao[1:-1].strip()))
                if valor[0] == False:
                    print(' ##ERRO## ',end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('[ERRO] Não foi definida nenhuma condição')
    print('')

def descobrir_valor_variavel(variavel):
    global variaveis
    variavel = variavel.strip()
    try:
        valor = variaveis[variavel]
    except:
        return [False,'[ERRO] A variavel {} não foi definida!'.format(variavel)]
    else:
        return [True,valor]


def definir_variaveis(variavel , valor_variavel , num_linha):
    global variaveis
    valor = valor_variavel.strip()
    variavel = variavel.strip()

    if (abstrai_valor(valor)[0]) == False:
        print('[{}] IMPOSIVEL DEFINIR VARIAVEL {}, PORQUE A VARIAVEL {} NÃO FOI DEFINIDA ANTERIORMENTE'.format(num_linha,variavel,valor_variavel))
    else:
        variaveis[variavel] = valor
        print('[{}] VARIAVEL {} SETADA para {}> '.format(num_linha,variavel,valor_variavel),end = '')
    print('')

def verifica_espere(condicao,num_linha):
    print('<ESPERE> ',end = '')
    condicao = ' ' + condicao.strip() + ' '

    # COMANDOS DISPONÍVEIS PARA O SE
    comandos_comparadores = [' segundos ',' segundo ',' s ']
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

                if ((comando == ' segundo ') or (comando == ' segundos ') or (comando == ' s ')) :
                    operacoes.append('segundos')
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
            if operacao == 'segundos':
                print('<UNIDADE> ',end='')        
            elif '(' in operacao:
                valor = abstrai_valor((operacao[1:-1].strip()))
                if valor[0] == False:
                    print(' ##ERRO## ',end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('[ERRO] Não foi definida nenhuma condição')
    print('')


def verifica_loop_enquanto (condicao,num_linha):
    print('<enquanto> ',end = '')
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

                valor = abstrai_valor((operacao[0:].strip()))
                if valor[0] == False:
                    print(' ##ERRO## ',end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('[ERRO] Não foi definida nenhuma condição')
    print('')

def verifica_mostre(condicao,num_linha):
    print('[{}] <mostre> '.format(num_linha),end = '')

    operacoes = []
    valor = ''

    marcador = False
    indicador_outro = False

    for caractere in range(0,len(condicao)):
        if  ((condicao[caractere] == '"' or caractere + 1 == len(condicao) ) and marcador == True)  and indicador_outro == False:
            marcador = False
            operacoes.append('"{}"'.format(valor))
            valor = ''

        elif marcador == True and indicador_outro == False:
            valor += condicao[caractere]

        elif  condicao[caractere] == '"' and marcador == False and indicador_outro == False:
            marcador = True

        elif indicador_outro == False:
            valor += condicao[caractere]
            indicador_outro = True

        elif (condicao[caractere] == ' ' or caractere+1 == len(condicao))  and indicador_outro == True:
            indicador_outro = False
            valor += condicao[caractere]
            operacoes.append('{}'.format(valor))
            valor = ''

        elif indicador_outro == True:
            valor += condicao[caractere]

    valor = []
    if operacoes != []:
        for operacao in operacoes:
            valor = abstrai_valor((operacao.strip()))
            if valor[0] == False:
                print(' ##ERRO## ',end='')
            else:
                print('__valor__ ',end='')
    print('')

linhas = '''

gabriel vale "1234"



gregorio receb gabriel
nasa vale gregorio
gregorio"gregorio" vale 13

mostre gabriel gregorio"gregorio" nasa
 
'''.split('\n')

for num_linha in range(len(linhas)):
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linhas[num_linha],num_linha)
