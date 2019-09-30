# modificação, testando o git com o terminal
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
    ignorar = False
    for caractere in range(len(linha)):
        if ignorar == True:
            ignorar = False
            break
        total_caracteres_restantes = len(linha) - caractere

        for comando in comandos:
            if ignorar == True:
                break

            if ((linha[  caractere : caractere + len(comando)  ] == comando) and ( len(comando) < total_caracteres_restantes )):
                eventos = True
                if (comando == ' se '):
                    verifica_condicionais(' '+ linha[caractere + len(comando):] + ' ',num_linha )

                elif (comando == ' enquanto '):
                    verifica_loop_enquanto( ' '+ linha[caractere + len(comando):] + ' ',num_linha )

                elif (comando == ' espere '):
                    verifica_espere( linha[caractere + len(comando):] , num_linha)

                elif (comando == ' recebe ' or comando == ' vale '):
                    valor_variavel = linha[caractere + len(comando):]
                    variavel = linha[:caractere]
                    print('\n\n>>',variavel)
                    print(num_linha,'LLL',valor_variavel,'LLL')

                    definir_variaveis(variavel,valor_variavel,num_linha)
                    ignorar = True

                elif ((comando == ' mostre ') or (comando == ' exiba ') or (comando == ' exiba nessa linha') or (comando == ' mostre nessa linha ')):
                    verifica_mostre( linha[caractere + len(comando):],num_linha )
                    ignorar = True

    # NÃO TEM NADA NA LINHA
    if linha == '' or linha.isspace():
        pass 

    # NENHUM EVENTO FOI FINALIZADO
    elif eventos == False:
        print('>> [*] POR FAVOR, SEJA MAIS CLARO NA LINHA {}'.format(num_linha))

def abstrai_valor(objeto):
    objeto = objeto.strip()

    # Nada declarado
    if len(objeto) == 0:
        print(123)
        return [False, '>> NENHUM VALOR FOI DEFINIDO']

    # é uma string?
    elif objeto[0] == '"' and objeto[-1] == '"':
        return [True , objeto[1:-1]]

    # Não é string e tem espaço
    elif ' ' in objeto:
        return [False, ">> O VALOR NÃO PODE CONTÉR ESPAÇOS!"]

    # é um número
    elif objeto.isnumeric():
        return [True,objeto]

    # é uma variável
    else:
        return descobrir_valor_variavel(objeto)

def verifica_condicionais(condicao,num_linha):
    print('[{}] <condicional> '.format(num_linha),end = '')
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
                    print(' ##{}## '.format(valor[1]),end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('>> [ERRO] Não foi definida nenhuma condição')
    print('')

def descobrir_valor_variavel(variavel):
    global variaveis
    variavel = variavel.strip()

    try:
        valor = variaveis[variavel]
    except:
        return [False,'>> [ERRO] A variavel {} não foi definida!'.format(variavel)]
    else:
        return [True,valor]


def definir_variaveis(variavel , valor_variavel , num_linha):
    global variaveis
    valor = valor_variavel.strip()
    variavel = variavel.strip()
    print(valor,variavel)

    # Usa palavras reservadas?
    if (("recebe" == variavel) or ("vale" == variavel)):
        print('>> [{}] ({}) É UMA PALAVRA RESERVADA, VOCÊ NÃO PODE USAR ELA COMO VARIAVEL.'.format(num_linha,variavel))

    # Tem Espaço?
    elif ' ' in variavel:
        print('>> [{}] IMPOSIVEL DEFINIR VARIAVEL {}, PORQUE A VARIAVEL CONTÉM ESPAÇOS!'.format(num_linha,variavel,valor))

    elif variavel == "":
        print('>> [{}] DEFINA UMA VARIAVEL PARA RECEBER ESSE VALOR!'.format(num_linha,variavel,valor))

    elif '"' in variavel:
        print('>> [{}] POR FAVOR, NÃO USE " PARA NO NOME DE UMA VARIÁVEL'.format(num_linha,variavel,valor))

    elif valor.isspace():
        print('>> [{}] IMPOSIVEL DEFINIR A VARIAVEL {}, PORQUE ELA NÃO TEM UM VALOR DEFINIDO'.format(num_linha,variavel,valor))

    # Tem Espaço?
    elif (',' in valor) or ('//' in valor) or ('#' in valor):
        print('>> [{}] IMPOSIVEL DEFINIR A VARIAVEL {}, PORQUE OS VALORES CONTÉM CARACTERES INVÁLIDOS'.format(num_linha,variavel))

    elif (  abstrai_valor(valor)[0]  ) == False:

        if abstrai_valor(valor)[1] == ">> O VALOR NÃO PODE CONTÉR ESPAÇOS!":
            print ('>> [{}] IMPOSIVEL DEFINIR A VARIAVEL ({}), PORQUE ({}) NÃO É VÁLIDO POR CONTÉR ESPAÇOS.'.format(num_linha,variavel,valor))
        else:
            print('>> [{}] IMPOSIVEL DEFINIR VARIAVEL {}, PORQUE A VARIAVEL {} NÃO FOI DEFINIDA ANTERIORMENTE'.format(num_linha,variavel,valor))

    else:
        variaveis[variavel] = valor
        print('[{}] VARIAVEL {} FOI SETADA PARA {}> '.format(num_linha,variavel,valor),end = '')
    print('')

def verifica_espere(condicao,num_linha):
    print('[{}] <ESPERE> '.format(num_linha),end = '')
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
                    print(' ##{}## '.format(valor[1]),end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('>> [ERRO] Não foi definida nenhuma condição')
    print('')


def verifica_loop_enquanto (condicao,num_linha):
    print('[{}] <enquanto> '.format(num_linha),end = '')
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
        print('>> [ERRO] Não foi definida nenhuma condição')
    print('')

def verifica_mostre(condicao,num_linha):
    print('[{}] <mostre> '.format(num_linha),end = '')
    condicao = ' ' + condicao + ' '

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
                print(' A variável {} não foi definida!'.format(operacao),end='')
            else:
                print('__{}__ '.format(valor[1]),end='')
    print('')

linhas = '''
x vale 10
y recebe 3
abc vale 15
y vale y

mostre x
mostre y

'''.split('\n')

for num_linha in range(len(linhas)):
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linhas[num_linha],num_linha)
