global variaveis
variaveis = {}

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
                ' recebe ',
                ' vale ']

    for caractere in range(len(linha)):
        total_caracteres_restantes = len(linha) - caractere

        for comando in comandos:
            if ((linha[  caractere : caractere + len(comando)  ] == comando) and ( len(comando) < total_caracteres_restantes )):
                if (comando == ' se '):
                    verifica_condicionais( ' '+ linha[caractere + len(comando):] + ' ' )

                if (comando == ' enquanto '):
                    verifica_loop_enquanto( ' '+ linha[caractere + len(comando):] + ' ' )

                    

                elif (comando == ' espere '):
                    verifica_espere( linha[caractere + len(comando):] )

                elif (comando == ' recebe ' or comando == ' vale '):
                    valor_variavel = linha[caractere + len(comando):]
                    variavel = linha[:caractere]
                    definir_variaveis(variavel,valor_variavel)

                elif ((comando == ' mostre ') or (comando == ' exiba ')) :
                    verifica_validacao_de_valores( linha[caractere + len(comando):] )


# Recebe algo e retorna um valor
# recebe o valor pelado, sem espaços na lateral
def abstrai_valor(objeto):
    # é uma string?
    if objeto[0] == '"' and objeto[-1] == '"':
        print('objeto é uma string!')
        return objeto[1,-1]

    # é um número
    elif objeto.isnumeric():
        return [True,objeto]

    # é uma variável
    else:
        resultado = descobrir_valor_variavel(objeto)

    return resultado

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
    try:
        valor = variaveis[variavel]
    except:
        return [False,'[ERRO] A variavel {} não foi definida!'.format(variavel)]
    else:
        return [True,valor]


def definir_variaveis(variavel , valor_variavel):
    global variaveis
    variavel = variavel.strip()
    variaveis[variavel] = valor_variavel
    print('[OK] VARIAVEL {} SETADA para {}> '.format(variavel,valor_variavel),end = '')
    print('')

def verifica_espere(condicao):
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


def verifica_loop_enquanto (condicao):
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
                valor = abstrai_valor((operacao[1:-1].strip()))
                if valor[0] == False:
                    print(' ##ERRO## ',end='')
                else:
                    print('__valor__ ',end='')
    else:
        print('[ERRO] Não foi definida nenhuma condição')
    print('')


































linhas = '''

nome vale 4
espere nome segundos

x recebe 3

enquanto x for igual a 14 ou tpm for menor que 6

'''.split('\n')

for linha in linhas:
    # garanta 1 espaço antes de cada linha
    analisa_comandos(' ' + linha)
