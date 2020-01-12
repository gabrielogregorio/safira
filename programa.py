from tkinter.font import nametofont
from threading    import Thread
from tkinter      import filedialog
from tkinter      import INSERT
from funcoes      import funcao
from tkinter      import *
from design       import Sintaxe
from design       import design
from random       import randint
from time         import sleep, time
from os           import listdir

global funcaoQueEstaSendoAnalisada # funcao que está sendo analisada
global arquivoAbertoAtualmente     # Contém o link e o texto do arquivo
global boolTelaEmFullScreen        # A tela está em full screen
global aconteceuUmErro             # Aconteceu algum erro durante a execução do programa
global contadorThreads             # impede que o programa seja iniciado enquanto outro está sendo executado
global alturaDoWidget              # Altura da janela em linhas
global repetirAtivado              # Se um comando de repetição tiver sido ativado 
global tx_informacoes              # Exibe as informações do interpretador em tempo real
global tx_codificacao              # Local onde o programa é codificado
global dicSubComandos              # Comandos internos a cada função
global funcaoAtivada               # Se um comendo de funcao tiver sido ativado
global funcaoRepita                # Se a função repita for ativada
global dicComandos                 # Dicionário com toodos os comandos disponíveis
global numeroDoLog                 # Posição do log registrado
global dicFuncoes                  # Dicionario com todas as funcoes
global variaveis                   # Variáveis usadas durante a interpretação do programa
global lb_linhas                   # Contador de linhas do programa
global btnsGuias                   # Botões das guias

arquivoAbertoAtualmente = {'link':None,'texto':None}
boolTelaEmFullScreen = False 
aconteceuUmErro = False
repetirAtivado = False
funcaoAtivada = False
contadorThreads = 0
numeroDoLog = 1
dicFuncoes = {}
variaveis = {}
btnsGuias = []

dicComandos = {
    'pare':
        [
            'interrompa',
            'break',
            'stop',
            'pare',
        ],        
    'listas':
        [
            'lista de ',
            'vetor de ',
            'lista ',
            'vetor ',
        ],        
    'aleatorio':
        [
            'um número aleatório entre',
            'um número aleatorio entre',
            'um numero aleatório entre',
            'um numero aleatorio entre',
            'número aleatório entre',
            'número aleatorio entre',
            'numero aleatório entre',
            'numero aleatorio entre'
        ],
    'mostreNessa':
        [
            'mostre nessa linha ',
            'exiba nessa linha ',
            'escreva nessa linha ',
            'imprima nessa linha '
        ],
    'mostre':
        [
            'escreva na tela ',
            'mostre ',
            'exiba ',
            'print ',
            'imprima ',
            'display ',
            'escreva '
        ],
    'declaraVariaveis':
        [
            ' vale ',
            ' recebe ',
            ' = '
        ],
    'funcoes':
        [
            'funcao ',
            'function '
        ],
    'loopsss':
        [
            'enquanto ',
            'while '
        ],
    'aguarde':
        [
            'espere ',
            'aguarde '
        ],
    'repita':
        [
            'repita ',
            'repeat ',
            'repetir ',
            'repitir '
        ],
    'se':
        [
            'se ',
            'quando ',
            'if '
        ],
    'limpatela':
        [
            'limpar a tela',
            'limpatela',
            'clear'
        ],
    'digitado':
        [
            'o numero que for digitado',
            'o numero que o usuario digitar',
            'numero digitado',
            'entrada',
            'input',
            'o que for digitado',
            'o que o usuario digitar',
            'digitado',
            'entrada',
            'input'
        ]
    }

# Corrigindo bugs
dicSubComandos = {
    'repitaVezes':
        [
            'vezes',
            'vez'
        ],
    'logico':
        [
            'and',
            '&&',
            'e',
            'ou',
            'or',
            '||',
            'for maior que',
            '>',
            'for menor que',
            '<',
            'for igual a',
            '==',
            'for maior ou igual a',
            '>=',
            'for menor ou igual a',
            '<=',
            'for diferente de',
            '!='
        ],
    'matematica':
        [
            'multiplicado por',
            'dividido por',
            'multiplique',
            'elevado por',
            'elevado a',
            'elevado',
            'divide',
            'menos',
            'mais',
            '**',
            '-',
            '*',
            '%',
            '/',
            '+'
        ],
    'esperaEm':
        [
            ' milisegundos',
            ' milisegundo',
            ' segundos',
            ' segundo',
            ' ms',
            ' s'
        ],
    'passandoParametros':
        [
            'passando parametros',
            'passando parametro',
            'parametros',
            'parametro',
            'passando'
        ],
    'recebeParametros':
        [
            'recebe parametros'
        ]
    }

def salvarArquivoComoDialog(event = None):
    global arquivoAbertoAtualmente

    # Escolha um local
    arquivo = filedialog.asksaveasfile(mode='w', 
        defaultextension=".fyn",
        title = "Selecione o script",
        filetypes = (("Meus scripts","*.fyn"),("all files","*.*")))

    # Se não for feito nenhuma escolha
    if arquivo is None:
        return None

    # Busque o conteudo da tela principal
    text2save = str(tx_codificacao.get(1.0, END))

    # Salve no arquivo escolhido
    arquivo.write(text2save)
    arquivo.close()

    # Atuaize os dados globais do arquivo aberto atualmente
    arquivoAbertoAtualmente['link'] = arquivo.name
    arquivoAbertoAtualmente['texto'] = text2save

    return arquivo.name

def salvarArquivo(event=None):
    global arquivoAbertoAtualmente

    # Se nenhum arquivo foi salvo
    if arquivoAbertoAtualmente['link'] == None:
        salvarArquivoComoDialog()

    else: # Se o arquivo já estava aberto
        programaCodigo = tx_codificacao.get(1.0, END)

        # Vamos salvar o arquivo por que o texto está diferente
        if arquivoAbertoAtualmente['texto'] != programaCodigo:
            arquivo = open(arquivoAbertoAtualmente['link'],'w')
            arquivo.write(programaCodigo)
            arquivo.close()

            arquivoAbertoAtualmente['texto'] = programaCodigo

def abrirArquivoDialog(event=None):
    global arquivoAbertoAtualmente

    ftypes = [('Scripts fyn', '*.fyn'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        log(' Arquivo "{}" escolhido'.format(filename))        
        arquivo = funcao.abrir_arquivo(filename) 

        if arquivo != None:
            tx_codificacao.delete(1.0, END)
            tx_codificacao.insert(END,arquivo)

        sintaxeDasPalavras()

        arquivoAbertoAtualmente['link'] = filename
        arquivoAbertoAtualmente['texto'] = arquivo
    else:
        log(' Nenhum arquivo escolhido')

def abrirArquivo(link):
    global arquivoAbertoAtualmente

    log(' Abrindo arquivo "{}" escolhido'.format(link))        

    arquivo = funcao.abrir_arquivo(link) 

    if arquivo != None: 
        tx_codificacao.delete(1.0, END) 
        tx_codificrt(END,arquivo)

        sintaxeDasPalavras()

        arquivoAbertoAtualmente['link'] = link
        arquivoAbertoAtualmente['texto'] = arquivo
    else:
        print('Arquivo não selecionado')

def colorirUmaPalavra(palavra,linha,valor1,valor2,cor):

    linha1 = '{}.{}'.format(linha , valor1) # linha.coluna(revisar)
    linha2 = '{}.{}'.format(linha , valor2) # linha.coluna(revisar)

    tx_codificacao.tag_add(palavra, linha1 , linha2) 
    tx_codificacao.tag_config(palavra, foreground = cor)

def colorirUmErro(palavra,valor1,valor2,cor='red'):
    global tx_informacoes

    linha = tx_informacoes.get(1.0,END)
    linha = len(linha.split('\n'))-1

    linha1 = '{}.{}'.format(linha , valor1) # linha.coluna(revisar)
    linha2 = '{}.{}'.format(linha , valor2) # linha.coluna(revisar)

    tx_informacoes.tag_add(palavra, linha1 , linha2) 
    tx_informacoes.tag_config(palavra, foreground = cor)

# Tratamentos para uma possível palavra especial
def sintaxe_linha(palavra,cor,frase,linha):
    quantidade_de_caracteres = len(frase)

    for caractere in range(len(frase)):
        if caractere+len(palavra) <= quantidade_de_caracteres:                 
            if frase[caractere:caractere+len(palavra)] == palavra:

                # Análisa se a palavra não está em outro contexto
                validacao = 0 

                # Se não estiver no primeiro caractere
                if caractere > 0:
                    if frase[caractere-1 : caractere+len(palavra)] == ' '+palavra:
                        validacao += 1 
                else:
                    validacao += 1

                if caractere + len(palavra) < quantidade_de_caracteres:
                    if frase[caractere:caractere+1+len(palavra)] == palavra+' ':
                        validacao += 1 
                else:
                    validacao += 1

                # Se tiver sido validado
                if validacao == 2:

                    # colora a palavra
                    colorirUmaPalavra(palavra,linha,caractere,caractere + len(palavra),cor)

def sintaxe(palavra,cor):
    cor = cor['foreground']
    tx_codificacao.tag_delete(palavra)
    lista = tx_codificacao.get(1.0,END).split('\n')

    # Remoção de bugs no regex, deixe ele aqui para eviar um \* \\* \\\* \\\\* no loop
    palavra_comando = palavra.replace('+','\\+')
    palavra_comando = palavra_comando.replace('/','\\/')
    palavra_comando = palavra_comando.replace('*','\\*')

    # Ande por todas as linhas do programa
    for linha in range(len(lista)):

        # Se a palavra for apontada como string
        if palavra == '"' or palavra == "'":
            for valor in re.finditer(""""[^"]*"|'[^']*'""",lista[linha]):
                colorirUmaPalavra(str(palavra),str(linha+1),valor.start(),valor.end(),cor)

        # se a palavra foi apontada como numérico
        elif palavra == "numerico":
            for valor in re.finditer('(\\s|^)([0-9\\.\\,\\s]+)(\\s|$)',lista[linha]):
                colorirUmaPalavra(str(palavra),str(linha+1),valor.start(),valor.end(),cor)

        # Se a palavra foi apontada como comentário
        elif palavra == "comentario":
            for valor in re.finditer('(#|\\/\\/).*$',lista[linha]):
                colorirUmaPalavra(str(palavra),str(linha+1),valor.start(),valor.end(),cor)

        # Se for uma palavra especial
        else:
            for valor in re.finditer('(^|\\s){}(\\s|$)'.format(palavra_comando),lista[linha]):
                colorirUmaPalavra(str(palavra),str(linha+1),valor.start(),valor.end(),cor)

def contadorDeLinhas():
    global lb_linhas

    linhas = ''
    linhasContadas = tx_codificacao.get(1.0,END)
    for x in range(1,linhasContadas.count('\n') + 1):
        linhas += ' {}\n'.format(x)

    lb_linhas.config(state=NORMAL)
    lb_linhas.delete(1.0,'end')
    lb_linhas.insert('end',linhas)
    lb_linhas.config(state=DISABLED)

# Cores que as palavras vão assumir
def sintaxeDasPalavras():
    global dicComandos

    threadContadorLinhas = Thread(target=contadorDeLinhas())
    threadContadorLinhas.start()

    # Principais comandos
    for comando in dicComandos['pare']:
        sintaxe(comando.strip(), Sintaxe.pare())

    for comando in dicComandos['declaraVariaveis']:
        sintaxe(comando.strip(), Sintaxe.atribuicao())

    for comando in dicComandos['listas']:
        sintaxe(comando.strip(), Sintaxe.lista())

    for comando in dicComandos['digitado']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicComandos['loopsss']:
        sintaxe(comando.strip(), Sintaxe.lista())

    for comando in dicComandos['repita']:
        sintaxe(comando.strip(), Sintaxe.lista())

    for comando in dicComandos['se']:
        sintaxe(comando.strip(), Sintaxe.condicionais())

    for comando in dicComandos['mostre']:
        sintaxe(comando.strip(), Sintaxe.exibicao())

    for comando in dicComandos['mostreNessa']:
        sintaxe(comando.strip(), Sintaxe.exibicao())

    for comando in dicComandos['funcoes']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicComandos['aguarde']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicComandos['aleatorio']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicComandos['limpatela']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    # Comandos internos a cada função
    for comando in dicSubComandos['passandoParametros']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicSubComandos['recebeParametros']:
        sintaxe(comando.strip(), Sintaxe.tempo())

    for comando in dicSubComandos['esperaEm']:
        sintaxe(comando.strip(), Sintaxe.tempo())
    
    for comando in dicSubComandos['matematica']:
        sintaxe(comando.strip(), Sintaxe.contas())

    for comando in dicSubComandos['repitaVezes']:
        sintaxe(comando.strip(), Sintaxe.lista())

    for comando in dicSubComandos['logico']:
        sintaxe(comando.strip(), Sintaxe.logico())

    # Numero
    sintaxe('numerico'     , Sintaxe.numerico())

    # String
    sintaxe('"'            , Sintaxe.string())
    sintaxe("'"            , Sintaxe.string())

    # Comentários
    sintaxe('comentario'   , Sintaxe.comentario())

# inicia o interpretador
def iniciarOrquestradorDoInterpretador(event = None):
    inicio = time() # Marca o inicio do programa

    global contadorThreads
    global variaveis
    global repetirAtivado
    global funcaoRepita
    global funcaoAtivada
    global aconteceuUmErro

    # Se algum programa já estiver rodando
    if contadorThreads != 0:
        print("Já existe um programa sendo executado!")
        return 0

    variaveis       = {}     # Reinicia as variaveis do interpretador    
    dicFuncoes      = {}     # Reinicia as funcoes do interpretador
    repetirAtivado  = False  # Remove os loops while
    funcaoAtivada   = False  # Função foi ativada
    funcaoRepita    = 0      # Remove a repetição do comando repetir n vezes
    aconteceuUmErro = False  # Não aconteceu nenhum erro
    contadorThreads = 0      # Reinicia o contador de Threads

    create_topExecutando()   # Inicia a tela do programa

    tx_informacoes.delete('1.0',END)        # Limpa o conteudo da tela de execução.
    linhas = tx_codificacao.get('1.0',END)  # Obtem o código do programa

    # Inicia o interpretador em um Thread
    t = Thread(target=lambda valor = linhas: orquestradorDoInterpretador(valor))
    t.start()

    # Enquanto todos os Threads não forem finalizados
    while contadorThreads != 0:
        tela.update()

    tx_informacoes.insert(END, '\nscript finalizado em {:.3} segundos'.format(time() - inicio))
    tx_informacoes.see("end")

def orquestradorDoInterpretador(linhas):
    global contadorThreads
    global repetirAtivado
    global funcaoRepita
    global aconteceuUmErro
    global funcaoAtivada
    global dicFuncoes
    global funcaoQueEstaSendoAnalisada

    contadorThreads += 1                # Aumenta o número de vezes que o interpretador foi chamado
    linhaComCodigoQueFoiExecutado = ''  # Reseta a linha de comando (enquanto >>x for menor que 6<<)
    contador = 0                        # contador para andar por todos os caracteres
    blocoComOsComando = ''              # Armazena blocos de código {}
    blocoDeCodigo = False               # Tem um bloco de código sendo armazenado?
    penetracao = 0                      # Penetracao dos {{{{}}}} de forma recursiva
    estadoDaCondicional = [False,None]  # Ler um bloco de código (Condição verdadeira)

    while contador < len(linhas) and not aconteceuUmErro:

        # Se começar um bloco e não tiver começado nenhum anteriormente
        if linhas[contador] == '{' and blocoDeCodigo == False:
            penetracao +=1

            # Se não for uma linha vazia
            if not blocoComOsComando.isspace() and  blocoComOsComando != '':
                estadoDaCondicional = interpretador(blocoComOsComando.strip())

                # A execucao do bloco foi bem suscedida?
                if estadoDaCondicional[0] == False:
                    aconteceuUmErro = True
                    tx_informacoes.insert(END,str(estadoDaCondicional[1]))
                    colorirUmErro('codigoErro',valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                    break

                if estadoDaCondicional[1] != None and "<class 'bool'>" not in str(type(estadoDaCondicional[1])):

                    # Insere no menu lateral
                    if len(str(estadoDaCondicional[1])) > len(":nessaLinha:"):

                        if str(estadoDaCondicional[1])[:len(":nessaLinha:")] == ":nessaLinha:":
                            tx_informacoes.insert(END, str(estadoDaCondicional[1][len(":nessaLinha:"):]))
                        else:
                            tx_informacoes.insert(END, str(estadoDaCondicional[1])+'\n')
                    else:
                        tx_informacoes.insert(END, str(estadoDaCondicional[1])+'\n')

                    tx_informacoes.see("end")

            # Recomeçar o registrador
            blocoComOsComando = '' 
            contador += 1

            # Começar a salvar o bloco de código
            blocoDeCodigo = True
            continue
 
        # Aumenta a penetração
        if linhas[contador] == '{':
            penetracao +=1

        # Diminui a penetração
        if linhas[contador] == '}':
            penetracao -=1

        # Se o bloco principal finalizar
        if linhas[contador] == '}' and blocoDeCodigo and penetracao == 0:

            if estadoDaCondicional[0] == False:
                aconteceuUmErro = True
                tx_informacoes.insert(END,str(estadoDaCondicional[1]))
                colorirUmErro('codigoErro',valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                break

            # Se a confição chamadora do bloco for verdadeira
            if estadoDaCondicional[1] == True:

                # Se acontecer um loop
                if repetirAtivado:
                    
                    # Enquanto a condição for verdadeira
                    while linhaComOResultadoDaExecucao[1]:
                        if aconteceuUmErro:
                            break

                        # Envia um bloco completo para ser novamente executado
                        resultadoExecucao = orquestradorDoInterpretador(blocoComOsComando)

                        # Comando pare localizado
                        print('>>>>>>>>>>.',resultadoExecucao)

                        # Se der erro na exeução do bloco
                        if resultadoExecucao[0] == False:

                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(resultadoExecucao[1]))
                            colorirUmErro('codigoErro',valor1=0,valor2=len(str(resultadoExecucao[1]))+1,cor='#dd4444')
                            break

                        # Testa novamente a condição do loop
                        linhaComOResultadoDaExecucao = interpretador(linhaComCodigoQueFoiExecutado)

                        # Se der erro na exeução do teste
                        if linhaComOResultadoDaExecucao[0] == False:
                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(linhaComOResultadoDaExecucao[1]))
                            colorirUmErro('codigoErro',valor1=0,valor2=len(str(linhaComOResultadoDaExecucao[1]))+1,cor='#dd4444')
                            break

                    if aconteceuUmErro:
                        break

                elif funcaoRepita != 0:
                    if aconteceuUmErro:
                        break

                    # Se for maior que zero, aconteceu um repit
                    for valor in range(0,funcaoRepita):
                        # Envia um bloco completo para ser novamente executado
                        resultadoOrquestrador = orquestradorDoInterpretador(blocoComOsComando)

                        # Se acontecer um erro
                        if resultadoOrquestrador[0] == False:
                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(resultadoOrquestrador[1]))
                            colorirUmErro('codigoErro',valor1=0,valor2=len(str(resultadoOrquestrador[1]))+1,cor='#dd4444')
                            break

                    if aconteceuUmErro:
                        break

                    funcaoRepita = 0
                    linhaComOResultadoDaExecucao = [True,False]

                # Se uma função foi
                elif funcaoAtivada:
                    # Atualize o dicionário de funções
                    dicFuncoes[funcaoQueEstaSendoAnalisada] = [dicFuncoes[funcaoQueEstaSendoAnalisada][0],blocoComOsComando]
                    funcaoAtivada = False
                # Se for uma condição
                else:
                    # Envia um bloco completo para ser executado
                    resultadoOrquestrador = orquestradorDoInterpretador(blocoComOsComando)

                    # Se acontecer um erro
                    if resultadoOrquestrador[0] == False:
                        aconteceuUmErro = True
                        tx_informacoes.insert(END,str(resultadoOrquestrador[1]))
                        colorirUmErro('codigoErro',valor1=0,valor2=len(str(resultadoOrquestrador[1]))+1,cor='#dd4444')
                        break

            blocoComOsComando = ''
            contador += 1
            blocoDeCodigo = False

        # O que fazer assim que chegar no final do bloco de código
        # Se chegar no final da linha ou do código código e um bloco não estiver sendo armazenado
        if (((contador == len(linhas)) or (linhas[contador] == '\n')) ) and not blocoDeCodigo:

            # Se não for uma linha vazia
            if not blocoComOsComando.isspace() and  blocoComOsComando != '':

                # Inicie o interpretador da linha
                estadoDaCondicional = interpretador(blocoComOsComando.strip())

                    
                if estadoDaCondicional[0] == False:
                    aconteceuUmErro = True
                    tx_informacoes.insert(END,str(estadoDaCondicional[1]))
                    colorirUmErro('codigoErro',valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                    break

                # Salva o resultado da ultima linha executada
                linhaComOResultadoDaExecucao = estadoDaCondicional
                linhaComCodigoQueFoiExecutado = blocoComOsComando.strip()

                if (estadoDaCondicional[1] != None and "<class 'bool'>" not in str(type(estadoDaCondicional[1])) ):

                    # Insere no menu lateral
                    if len(str(estadoDaCondicional[1])) > len(":nessaLinha:"):

                        if str(estadoDaCondicional[1])[:len(":nessaLinha:")] == ":nessaLinha:":
                            tx_informacoes.insert(END, str(estadoDaCondicional[1][len(":nessaLinha:"):]))
                        else:
                            tx_informacoes.insert(END, str(estadoDaCondicional[1])+'\n')
                    else:
                        tx_informacoes.insert(END, str(estadoDaCondicional[1])+'\n')

                    tx_informacoes.see("end")
            # Limpar o bloco de comandos
            blocoComOsComando = ''

            # Avançar para os próximos caracteres
            contador += 1

            # Chegou ao final de uma execução
            continue

        # Armazena o código de uma linha
        blocoComOsComando += linhas[contador]
        contador += 1


    if penetracao > 0:
        aconteceuUmErro = True
        if penetracao == 1:
            vezesEsquecidas = '1 vez'
        else:
            vezesEsquecidas = '{} vezes'.format(penetracao)

        msgErro = """Você abriu uma chave'{' e esqueceu de fecha-la '}' """ + str(vezesEsquecidas) + """, por favor, analise o código navamente e corrija"""

        tx_informacoes.insert(END,msgErro)
        colorirUmErro('codigoErro',valor1=0,valor2=len(msgErro)+1,cor='#dd4444')
        contadorThreads -= 1
        return [False,'']

    elif penetracao < 0:
        aconteceuUmErro = True
        if penetracao == -1:
            vezesEsquecidas = 'uma vez'
        else:
            vezesEsquecidas = '{} vezes'.format(penetracao*-1)

        msgErro = """Você abriu uma chave '{' e fechou ela '}' """ + str(vezesEsquecidas) + """, por favor, analise o código navamente e corrija"""

        tx_informacoes.insert(END,msgErro)
        colorirUmErro('codigoErro',valor1=0,valor2=len(msgErro)+1,cor='#dd4444')
        contadorThreads -= 1
        return [False,'']

    # Libera uma unidade no contador de Threads
    contadorThreads -= 1

    return [True,"Não acontecera erros durante a execução do interpretador"]


# Interpreta um conjunto de linhas
def interpretador(codigo):

    global aconteceuUmErro
    if aconteceuUmErro:
        return [False,'Um erro foi encontrado ao iniciar o interpretador','string']

    log(' > Interpretador acionado!')

    codigo = codigo.strip()
    global dicComandos    
    global repetirAtivado
    global variaveis
    global funcaoRepita

    # Remove o modo repetir
    repetirAtivado = False

    # Limpa o número de repeticoes
    funcaoRepita = 0
    simbolosEspeciais = ['{','}']

    # Se o código estiver vazio
    if (codigo == '' or codigo.isspace()) or codigo in simbolosEspeciais:
        return [True,None,'booleano']

    else:
        # Obtem todas as linhas 
        linhas = codigo.split('\n')

        #vetor = ['vetor','crie uma lista chamada','lista']


        for linha in linhas:
            linha = linha.strip()

            ignoraComentario = linha.find('#')
            if ignoraComentario != -1:
                linha = linha[0:ignoraComentario]

            if linha == '':
                continue


            for comando in dicComandos['mostreNessa']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função exibicao nessa linha: "{}"'.format(codigo))
                       return funcaoExibicaoNessaLinha(linha[len(comando):],logs='> ')

            for comando in dicComandos['pare']:
                if len(comando) <= len(linha):
                    if comando == linha:
                       log(' > Função pare: "{}"'.format(codigo))
                       return funcaoPare(logs='> ')

            for comando in dicComandos['mostre']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função exibicao: "{}"'.format(codigo))
                       return funcaoExibicao(linha[len(comando):],logs='> ')

            for comando in dicComandos['limpatela']:
                if len(comando) <= len(linha):
                    if comando == linha:
                       log(' > Função limpar a tela: "{}"'.format(codigo))
                       return funcaoLimpaTela(logs='> ')

            for comando in dicComandos['se']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função condicional: "{}"'.format(codigo))
                       return funcaoCondicional(linha[len(comando):],logs='> ')

            for comando in dicComandos['loopsss']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função loops enquanto: "{}"'.format(codigo))
                       return funcaoLoopsEnquanto(linha[len(comando):],logs='> ')

            for comando in dicComandos['aguarde']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função tempo: "{}"'.format(codigo))
                       return funcaoTempo(linha[len(comando):],logs='> ')

            for comando in dicComandos['funcoes']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função declarar funções: "{}"'.format(codigo))
                       return funcaoDeclararFuncoes(linha[len(comando):],logs='> ')

            for comando in dicComandos['aleatorio']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função numero aleatório: "{}"'.format(codigo))
                       return funcaoNumeroAleatorio(linha[len(comando):],logs='> ')

            for comando in dicComandos['repita']:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       log(' > Função repetir: "{}"'.format(codigo))
                       return funcaoRepitir(linha[len(comando):],logs='> ')

            for comando in dicComandos['digitado']:
                if len(comando) <= len(linha):
                    if comando == linha:
                       log(' > Função digitado: "{}"'.format(codigo))
                       return funcaoDigitado(linha,logs='> ')

            for comando in dicComandos['declaraVariaveis']:
                if comando in linha:
                    log(' > Função atribuição: "{}"'.format(codigo))
                    return funcaoAtribuicao(linha,comando,logs='> ')

            if linha[0].isalnum():
                log(' > Função executar funções: "{}"'.format(codigo))
                return funcaoExecutaFuncoes(linha,logs='> ')

            log(' > Comando desconhecido: "{}"'.format(codigo))
            return [False,"Um comando desconhecido foi localizado:'{}'".format(linha),'string']

    return [True,None,'booleano']

global estaEsperandoPressionarEnter
estaEsperandoPressionarEnter = False

def log(mensagem):
    global numeroDoLog
    numeroDoLog += 1

    print(str(numeroDoLog) + mensagem)

def aperouEnter(event=None):
    global estaEsperandoPressionarEnter
    if estaEsperandoPressionarEnter:
        estaEsperandoPressionarEnter = False

def funcaoDigitado(linha,logs):
    logs = '  ' + logs

    log(logs + 'Função digitado com a linha "{}"'.format(linha))

    global tx_informacoes
    global estaEsperandoPressionarEnter

    textoOriginal = len(tx_informacoes.get(1.0,END))

    estaEsperandoPressionarEnter = True

    while estaEsperandoPressionarEnter:
        tx_informacoes.update()

    digitado = tx_informacoes.get(1.0,END)
    digitado = digitado[textoOriginal-1:-2]

    if 'numero' in linha:
        try:
            float(digitado)
        except:
            return[False,"Você disse que queria digitar um número, mas digitou um texto '{}'".format(digitado),'string']
        else:
            return [True,float(digitado),'float']
    else:
        return [True,digitado,'string']

def funcaoLimpaTela(logs):
    logs = '  ' + logs
    log(logs + 'Limpatela ativado!')

    global tx_informacoes
    tx_informacoes.delete(1.0,END)
    return [True,None,'booleano']

# repita 10 vezes \n{\nmostre 'oi'\n}
def funcaoRepitir(linha,logs):
    logs = '  ' + logs
    log(logs + 'funcao repetir com a linha: "{}"'.format(linha))
    global funcaoRepita

    # Remoção de lixo
    linha = linha.replace('vezes','')
    linha = linha.replace('vez','')

    # Eliminação de espaços laterais
    linha = linha.strip()

    # Obter o valor da variável
    linha = abstrairValoresDaLinhaInteira(linha,logs)

    # Deu erro?
    if linha[0] == False:
        return linha

    if linha[2] != 'float':
        return[False,'Você precisa passar um número inteiro para usar a função repetir: "{}"'.format(linha),'string']

    # É inteiro
    try:
        int(linha[1])
    except:
        return [False,"Para usar a função repetir, você precisa passar um número inteiro. Você passou '{}'".format(linha[1]),'string']
    else:
        funcaoRepita = int(linha[1])

        if funcaoRepita == 0:
            # Se for zero, não reproduza nenhuma vez
            return [True,False,'booleano']

        # Não houve erros e é para repetir
        return [True,True,'booleano']


# numero aleatório entre 10 e 20
def funcaoPare(logs):

    logs = '  ' + logs
    log(logs + 'funcao pare')

    return [True,'loop interrompido','string']

# numero aleatório entre 10 e 20
def funcaoNumeroAleatorio(linha,logs):
    logs = '  ' + logs
    log(logs + 'funcao aleatório com a linha: {}'.format(linha))

    # Remova os espaços da linha
    linha = linha.strip()

    # Se tiver  e que indica intervalo
    if ' e ' in linha:

        # Obtenção dos dois valores
        num1, num2 = linha.split(' e ')
 
        # Obtendo ambos os valores
        num1 = abstrairValoresDaLinhaInteira(num1,logs)
        num2 = abstrairValoresDaLinhaInteira(num2,logs)

        # Se deu para obter o valor do primeiro
        if num1[0] == False:
            return num1
 
        # Se deu erro para obter o valor do segundo
        if num2[0] == False:
            return num2

        # Se o primeiro for numéricos
        try:
            int(num1[1])
        except:
            return [False,"O valor 1 não é numérico",'string']
 
        # Se o segundo for numéricos
        try:
            int(num2[1])
        except:
            return [False,"O valor 2 não é numérico",'string']

        n1 = int(num1[1])
        n2 = int(num2[1])

        if n1 == n2:
            return [False,"O valor 1 e o valor 2 da função aleatório tem que ser diferentes",'string']
        elif n1 > n2:
            return [False,"O valor 1 é maior que o valor 2, o valor 1 tem que ser maior",'string']

        return [True,randint(n1,n2),'float']

    else:
        return [False,"Erro, você precisa definir o segundo valor, tipo 'entre 2 e 5'!",'string']

# calcMedia passando parametros nota1, nota2
def funcaoExecutaFuncoes(linha,logs):
    logs = '  ' + logs
    log(logs + 'Executar funções com a linha: {}'.format(linha))

    global dicFuncoes

    chamarFuncoes    = ['passando parametros','passando parametro','parametros','parametro','passando']
 
    nomeDaFuncao = None
    parametros = None

    for comando in chamarFuncoes:

        if comando in linha:
            nomeDaFuncao, parametros = linha.split(comando)
            nomeDaFuncao = nomeDaFuncao.strip()
            parametros = parametros.strip()
            break

    if nomeDaFuncao == None:
        nomeDaFuncao = linha

    try:
        dicFuncoes[nomeDaFuncao]
    except:
        return [False,"A função '{}' não existe".format(nomeDaFuncao),'string']
    else:

        # Se tiver multiplos parametros
        if ',' in str(parametros):
            listaDeParametros = parametros.split(',')
            listaFinalDeParametros = []

            for parametro in listaDeParametros:
                listaFinalDeParametros.append(parametro.strip())

            # Se tiver a mesma quantiade de parametros
            if len(dicFuncoes[nomeDaFuncao][0]) == len(listaFinalDeParametros):

                for parametroDeclarar in range(len(dicFuncoes[nomeDaFuncao][0])):
                    resultado = funcaoAtribuicao('{} recebe {} '.format(dicFuncoes[nomeDaFuncao][0][parametroDeclarar],listaFinalDeParametros[parametroDeclarar]),'recebe',logs)

                    if resultado[0] == False:
                        return resultado
            else:
                return [False,"A função '{}' tem {} parametros, mas você passou {} parametros!".format(nomeDaFuncao,len(dicFuncoes[nomeDaFuncao][0]),len(listaFinalDeParametros)),'string']

        # Se tiver só um parametro
        elif parametros != None:
            if len(dicFuncoes[nomeDaFuncao][0]) == 1:
                resultado = funcaoAtribuicao('{} recebe {} '.format(dicFuncoes[nomeDaFuncao][0],parametros),'recebe',logs)

                if resultado[0] == False:
                    return resultado
            else:
                return [False,"A função '{}' tem {} parametros, mas você passou 1 parametro!".format(nomeDaFuncao,len(dicFuncoes[nomeDaFuncao][0])),'string']

        resultadoOrquestrador = orquestradorDoInterpretador(dicFuncoes[nomeDaFuncao][1])
        if resultadoOrquestrador[0] == False:
            return resultadoOrquestrador

        return [True,None,'booleano']

# funcao gabriel recebe paramentros nota1, nota2
def funcaoDeclararFuncoes(linha,logs):
    logs = '  ' + logs
    log(logs + 'Declarar funcoes: {}'.format(linha))

    global funcaoAtivada
    global funcaoQueEstaSendoAnalisada

    recebeParametros = ['recebe parametros','recebe']

    for comando in recebeParametros:
        if comando in linha:
            lista = linha.split(comando)

            nomeDaFuncao = lista[0].strip()
            parametros = lista[1].strip()

            if ',' in parametros: # Se tiver multiplos parametros
                listaDeParametros = parametros.split(',')

                listaFinalDeParametros = []
                for parametro in listaDeParametros:
                    listaFinalDeParametros.append(parametro.strip())

                dicFuncoes[nomeDaFuncao] = [listaFinalDeParametros,'bloco']
            else:
                dicFuncoes[nomeDaFuncao] = [parametros,'bloco']

            funcaoQueEstaSendoAnalisada = nomeDaFuncao
            funcaoAtivada = True
            log(logs + 'Funcoes declaradas: {}'.format(dicFuncoes))
            return [True,True,'booleano']
    
    dicFuncoes[linha.strip()] = ['','bloco']
    funcaoQueEstaSendoAnalisada = linha.strip()
    funcaoAtivada = True

    return [True,True,'booleano']

def funcaoExibicao(linha,logs):
    logs = '  ' + logs
    log(logs + 'funcao exibição: {}'.format(linha))
    codigo = linha.strip()
    return abstrairValoresDaLinhaInteira(codigo,logs)

def funcaoExibicaoNessaLinha(linha,logs):
    logs = '  ' + logs
    log(logs + 'Função exibir nessa linha ativada'.format(linha))
    codigo = linha.strip()
    retorno = abstrairValoresDaLinhaInteira(codigo,logs)

    if retorno[0] == False:
        return retorno

    return [retorno[0],':nessaLinha:'+str(retorno[1]),'string']

def funcaoTempo(codigo,logs):
    logs = '  ' + logs
    log(logs + 'Função tempo: {}'.format(codigo))
    global dicSubComandos
    codigo = codigo.strip()
   
    for comando in  dicSubComandos['esperaEm']:
        log(logs + comando)

        if len(comando) < len(codigo):

            if comando == codigo[len(codigo)-len(comando):]:

                resultado = abstrairValoresDaLinhaInteira(codigo[:len(codigo)-len(comando)],logs)
                if resultado != False:

                    if comando == " segundos" or comando == " s" or comando == " segundo":
                        sleep(resultado[1])
                        return [True,None,'booleano']

                    elif comando == " milisegundos" or comando == " ms" or comando == "milisegundo":
                        sleep(resultado[1]/1000)
                        return [True,None,'booleano']

                else:
                    return [False,'Erro ao obter um valor no tempo','string']

    return [True,None]

# A string deve estar crua
def obterValorDeString(string,logs):    
    logs = '  ' + logs
    log(logs + 'Obter valor de uma string: {}'.format(string))

    valorFinal = ''
    anterior = 0

    for valor in re.finditer(""""[^"]*"|'[^']*'""",string):

        abstrair = abstrairValoresDaLinhaInteira(string[anterior:valor.start()],logs)
        if abstrair[0] == False:
            log(logs + 'Erro ao abstrair um valor da linha inteira: {}'.format(abstrair))
            return abstrair

        log(logs+'Abstrair vale: {}'.format(abstrair))

        valorFinal = valorFinal + str(abstrair[1]) + string[valor.start()+1:valor.end()-1]
        anterior = valor.end()

    # Capturar o resto        
    abstrair = abstrairValoresDaLinhaInteira(string[anterior:],logs)
    if abstrair[0] == False:
        log(logs + 'Erro ao abstrair ultimo valor')
        return abstrair

    valorFinal = valorFinal + str(abstrair[1])

    return [True,valorFinal,'string']

def encontrarETransformarVariaveis(linha,logs):
    logs = '  ' + logs
    log(logs + 'Encontrar e transformar variaveis: {}'.format(linha))
    # Abstração de variáveis
    anterior = 0
    normalizacao = 0
    linha_base = linha
    tipos_obtidos = []

    for valor in re.finditer(' ',linha_base):
        palavra = linha[anterior : valor.start() + normalizacao]

        if palavra.isalnum() and palavra[0].isalpha():

            variavelDessaVez = obterValorDeUmaVariavel(palavra,logs)
            log(logs + 'Variavel da vez: {}'.format(variavelDessaVez))
            if variavelDessaVez[0] == False:
                return variavelDessaVez

            tipos_obtidos.append(variavelDessaVez[2])
            linha = str(linha[:anterior]) + str(variavelDessaVez[1]) + str(linha[valor.start() + normalizacao:]) 
            if len(palavra) < len(str(variavelDessaVez[1])):
                normalizacao += (len(str(variavelDessaVez[1])) - len(palavra))

            elif len(palavra) > len(str(variavelDessaVez[1])):
                normalizacao -= (len(palavra) - len(str(variavelDessaVez[1])))

        anterior = valor.end() + normalizacao

    log(logs + 'Resultado ao localizar variáveis: {}'.format(linha))

    return [True,linha,'string']

# A string deve estar crua
def fazerContas(linha,logs):
    logs = '  ' + logs
    log(logs + 'Fazer contas: {}'.format(linha))

    # Do maior para o menor
    linha = linha.replace(' multiplicado por ',' * ')
    linha = linha.replace(' dividido por ',' / ')
    linha = linha.replace(' multiplique ', ' * ')
    linha = linha.replace(' elevado por ',' ** ')
    linha = linha.replace(' elevado a ',' ** ')    
    linha = linha.replace(' elevado ',' ** ')
    linha = linha.replace(' divide ',' / ')
    linha = linha.replace(' mais ',' + ')
    linha = linha.replace(' menos ', ' - ')

    if "'" in linha or '"' in linha:
        # Não mude esse texto
        log(logs + 'Isso é uma string, não dá para fazer contas com elas')
        return [False, "Isso é uma string",'string']

    # Removendo os espaços laterais
    linha = ' {} '.format(linha)

    simbolosEspeciais = ['+','-','*','/','%','(',')']
    qtdSimbolosEspeciais = 0

    # Deixando todos os itens especiais com espaço em relação aos valores
    for iten in simbolosEspeciais:

        if iten in linha:
            qtdSimbolosEspeciais += 1

        linha = linha.replace(iten,' {} '.format(iten))
    log(logs + 'simbolos especiais removidos: {}'.format(linha))

    # Se não tiver nenhuma operação
    if qtdSimbolosEspeciais == 0:
        log(logs + 'Não tem simbolos especiais de contas, ou seja, não é uma conta!')
        return [False, "Não foi possivel realizar a conta, porque não tem nenhum valor aqui. ",'string']

    # Correção do potenciação
    linha = linha.replace('*  *','**')
    linha = linha.replace('< =','<=')
    linha = linha.replace('> =','>=')
    linha = linha.replace("! =",'!=')
    log(logs + 'Simbolos especiais corrigidos: {}'.format(linha))

    linha = encontrarETransformarVariaveis(linha,logs)
    if linha[0] == False:
        return linha

    for caractere in linha[1]:
        if str(caractere).isalpha():
            return [False, 'não é possível fazer contas com strings',linha[1],'string']

    log(logs + 'A linha vale: {}'.format(linha))
    # Tente fazer uma conta com isso
    try:
        resutadoFinal = eval(linha[1])
    except Exception as erro:
        return [False, "Não foi possivel realizar a conta |{}|".format(linha[1]),'string']
    else:
        return [True, resutadoFinal,'float']

def obterValorDeUmaVariavel(variavel,logs):
    logs = '  ' + logs
    log(logs + 'Obter valor da variável: {}'.format(variavel))

    variavel = variavel.strip()
    global variaveis

    variavel = variavel.replace('\n','')
    log(logs + 'Variaveis disponíveis: {}'.format(variaveis))

    try:
        variaveis[variavel]
    except:
        log(logs + 'Não foi possível obter o valor da variável: {}'.format(variavel))
        return [False,'[erro] - variavel:{} não definida'.format(variavel),'string']
    else:
        log(logs + 'Valor da variável {} obtido com sucesso! como {}'.format(variavel, [ variaveis[variavel][0] , variaveis[variavel][1] ] ))
        return [True,variaveis[variavel][0],variaveis[variavel][1]]

def obterDigitadoOuAleatorio(possivelVariavel,logs):
    logs = '  ' + logs
    log(logs + 'Obter comando digitado ou aleatório: {}'.format(possivelVariavel))

    for comandoDigitado in dicComandos['digitado']:

        if len(comandoDigitado) <= len(possivelVariavel):

            if possivelVariavel == comandoDigitado:
                resultado = funcaoDigitado(comandoDigitado,logs)
                log(logs + 'Resultado obtido da função Digitado: {}'.format(resultado))
                return resultado

    for comandoAleatorio in dicComandos['aleatorio']:

        if len(comandoAleatorio) <= len(possivelVariavel):

            if possivelVariavel[0:len(comandoAleatorio)] == comandoAleatorio:
                resultado = funcaoNumeroAleatorio(possivelVariavel[len(comandoAleatorio):],logs)
                log(logs + 'Resultado obtido da função Aleatorio: {}'.format(resultado))
                return resultado

    # Não é nem um e nem o outro                
    return [False,None,'booleano']

# Os valores aqui ainda estão crus, como: mostre "oi",2 + 2
def abstrairValoresDaLinhaInteira(possivelVariavel,logs):
    logs = '  ' + logs
    log(logs + 'Abstrar valor de uma linha inteira com possivelVariavel: "{}"'.format(possivelVariavel))
    possivelVariavel = possivelVariavel.strip()

    if possivelVariavel == '':
        log(logs + 'Possivel variavel é uma linha vazia')
        return [True,possivelVariavel,'string']

    resultado = obterDigitadoOuAleatorio(possivelVariavel,logs)
    if resultado[0] == True:
        log(logs + 'Resultado obtido do digitado ou aleatorio: {}'.format(resultado))
        return resultado

    # É digitado ou aleatório, porém, deu erro:
    elif resultado != [False,None,'booleano']:
        return resultado

    # Caso existam contas entre strings ( Formatação )
    if possivelVariavel[0] == ',':
        log(logs + 'Foram encontrados virgulas no começo ao abstrair uma variável')
        possivelVariavel = possivelVariavel[1:]

    # Caso existam contas entre strings ( Formatação )
    if len(possivelVariavel) > 1:

        if possivelVariavel[-1] == ',':
            log(logs + 'Foram encontrados virgulas no final ao abstrair uma variável')
            possivelVariavel = possivelVariavel[0:len(possivelVariavel)-1]

    possivelVariavel = possivelVariavel.strip()
    if possivelVariavel == '':
        log(logs + 'Depois dos processos de filtro, não sobrou nada para analisar')
        return [True,possivelVariavel,'string']

    resultado = fazerContas(possivelVariavel,logs)
    if resultado[0] == True:
        log(logs + 'Deu certo para fazer as contas, resultado: {}'.format(resultado))
        return resultado

    if '"' in possivelVariavel or "'" in possivelVariavel:
        log(logs + 'Foi encontrado aspas, obtendo valor de string')
        return obterValorDeString(possivelVariavel,logs)

    try:
        float(possivelVariavel)
    except:
        log(logs + 'Não é um float: {}'.format(possivelVariavel))
        resultado = obterValorDeUmaVariavel(possivelVariavel,logs)
        return resultado
    else:
        log(logs + "  É um Float: {}".format(possivelVariavel))
        return [True,float(possivelVariavel),'float']

def funcaoAtribuicao(linha,comando,logs):
    logs = '  ' + logs
    log(logs + 'Função atribuição: {}'.format(linha))
    global variaveis

    variavel, valor = linha.split(comando)

    variavel = variavel.strip()
    valor    = valor.replace('\n','')
    valor    = valor.strip()

    resultado = abstrairValoresDaLinhaInteira(valor,logs)
    log(logs + 'Resultado do abstrair valores da linha interira: {}'.format(resultado))
    if resultado[0] == True:
        log(logs + 'variavel "{}" declarada como "{}"'.format(variavel,[resultado[1],resultado[2]]) )
        variaveis[variavel] = [resultado[1],resultado[2]]
        return [True,None,'booleano']

    log(logs + 'Erro ao abstrair valor da variável')
    return resultado         

def funcaoLoopsEnquanto(linha,logs):
    logs = '  ' + logs
    log(logs + 'Função loops enquanto: {}'.format(linha))

    global repetirAtivado
    repetirAtivado = True

    return funcaoCondicional(linha,logs)

def funcaoCondicional(linha,logs):
    logs = '  ' + logs
    log(logs + 'Função condicional: {}'.format(linha))
    linha = linha.replace(' for maior ou igual a ',' >= ')
    linha = linha.replace(' for menor ou igual a ',' <= ')
    linha = linha.replace(' for diferente de ',' != ')
    linha = linha.replace(' for maior que ',' > ')
    linha = linha.replace(' for menor que ',' < ')
    linha = linha.replace(' for igual a ',' == ')
    linha = linha.replace(' e ' ,'  and  ')
    linha = linha.replace(' && ','  and  ')
    linha = linha.replace(' ou ','  or  ')
    linha = linha.replace(' || ','  or  ')

    linha = ' {} '.format(linha)

    simbolosEspeciais = ['>=','<=','!=','>','<','==','(',')']
    simbolos = ['and','or']
    qtdSimbolosEspeciais = 0

    # Deixando todos os itens especiais com espaço em relação aos valores
    for item in simbolosEspeciais:
        if item in linha:
            qtdSimbolosEspeciais += 1
        linha = linha.replace(item,' {} '.format(item))
    linha = linha.replace('* *','**')
    linha = linha.replace('> =','>=')
    linha = linha.replace('< =','<=')
    linha = linha.replace('! =','!=')

    # Se não tiver nenhuma operação
    if qtdSimbolosEspeciais == 0:
        return [False, "Não foi possivel realizar a condição por que não tem nenhum simbolo condicional",'string']

    # Abstração de variáveis
    anterior = 0
    linha = linha.strip() + " " # Esse espaço é para analisar o ultimo caractere
    atualizarPosicaoReferencia = 0
    for valor in re.finditer(' ',linha):

        palavra = str(linha[anterior:valor.start()+atualizarPosicaoReferencia])
        palavra = palavra.strip()
        if palavra.isalnum() and palavra[0].isalpha() and palavra not in simbolos and len(palavra) != 0:

            variavelDessaVez = obterValorDeUmaVariavel(palavra,logs)
            if variavelDessaVez[0] == False:
                return variavelDessaVez

            log(logs + 'A variável dessa vez vale: {} '.format(variavelDessaVez))
            if str(variavelDessaVez[2]) == 'string':
                variavelDessaVez[1] = '"'+str(variavelDessaVez[1])+'"'

            linha = str(linha[:anterior]) + str(variavelDessaVez[1]) + str(linha[valor.start() + atualizarPosicaoReferencia:]) 

            # Se a variavel for maior que o valor
            if len(palavra) < len(str(variavelDessaVez[1])):
                atualizarPosicaoReferencia += (len(str(variavelDessaVez[1])) - len(palavra))

            # Se a variavel for menor que a variável
            elif len(palavra) > len(str(variavelDessaVez[1])):
                atualizarPosicaoReferencia -= (len(palavra) - len(str(variavelDessaVez[1])))

        anterior = valor.end() + atualizarPosicaoReferencia

    log(logs+'Linha: '.format(linha))
    # Tente fazer uma conta com isso
    try:
        resutadoFinal = eval(linha)
    except Exception as erro:
        return [False, "Não foi possivel realizar a condicao |{}|".format(linha),'string']
    else:
        return [True, resutadoFinal,'booleano']

def modoFullScreen(event=None):
    global boolTelaEmFullScreen

    if boolTelaEmFullScreen:
        boolTelaEmFullScreen = False
    else:
        boolTelaEmFullScreen = True

    tela.attributes("-fullscreen", boolTelaEmFullScreen)

def trocar_de_tela(fechar,carregar):
    fechar.grid_forget()
    carregar.grid(row=1,column=1,sticky=NSEW)


def create_topExecutando():
    global tx_informacoes

    topExecutando = Toplevel(tela)
    topExecutando.grid_columnconfigure(1,weight=1)
    topExecutando.rowconfigure(1,weight=1)
    topExecutando.geometry("600x300+100+100")

    tx_informacoes = Text(topExecutando,design.tx_informacoes(),relief = FLAT)
    tx_informacoes.bind('<Return>',lambda event:aperouEnter(event))
    tx_informacoes.focus_force()
    tx_informacoes.grid(row=1,column=1,sticky=NSEW)

def atualizaLinhasLaterais(linhas):
    global lb_linhas
    lb_linhas.config(state=NORMAL)
    lb_linhas.delete(1.0,END)
    lb_linhas.insert(END,linhas)
    lb_linhas.config(state=DISABLED)

def configuracoes(ev):
    global alturaDoWidget
    alturaDoWidget = int( ev.height / 24 )
    print("Altura",alturaDoWidget)

def atualizarListaDeScripts():
    for file in listdir('scripts/'):
        if len(file) > 5:       
            if file[-3:] == 'fyn':
                menu_arquivo_cascate.add_command(label=file,command= lambda link = file: abrirArquivo('scripts/' + str(file)))

def obterPosicaoDoCursor(event=None):
    global tx_codificacao

    numPosicao = str(tx_codificacao.index(INSERT)) # Obter posicao
    if '.' not in numPosicao:
        numPosicao = numPosicao + '.0'

    linha, coluna = numPosicao.split('.')

    print(tx_codificacao.get('{}.{}'.format( int(linha),int(coluna)-1 )))


tela = Tk()
tela.attributes('-zoomed', True)
tela.title('Linguagem feynman')
tela.configure(bg='#393944')
tela.rowconfigure(2,weight=1)
tela.grid_columnconfigure(1,weight=1)

tela.bind('<F11>',lambda event: modoFullScreen(event))
tela.bind('<F5>',       lambda event: iniciarOrquestradorDoInterpretador(event))
tela.bind('<Control-s>',lambda event: salvarArquivo(event))
tela.bind('<Control-o>',lambda event: abrirArquivoDialog(event))
tela.bind('<Control-S>',lambda event: salvarArquivoComoDialog(event))

menu_barra = Menu(tela,design.cor_menu(),relief=FLAT)
tela.config(menu=menu_barra)

menu_ferramentas = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_interface   = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_localizar   = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_executar    = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_arquivo     = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_editar      = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_ajuda       = Menu(menu_barra, design.cor_menu(),relief=FLAT)
menu_sobre       = Menu(menu_barra, design.cor_menu(),relief=FLAT)

menu_barra.add_cascade(label='Arquivo'   , menu=menu_arquivo)
menu_barra.add_cascade(label='Executar'  , menu=menu_executar)
menu_barra.add_cascade(label='Localizar' , menu=menu_localizar)
menu_barra.add_cascade(label='Interface' , menu=menu_interface)
menu_barra.add_cascade(label='Ajuda'     , menu=menu_ajuda)
menu_barra.add_cascade(label='sobre'     , menu=menu_sobre)

# =================================== ARQUIVO =================================== #
menu_arquivo_cascate = Menu(menu_arquivo, design.cor_menu(),relief=FLAT)
menu_arquivo.add_command(label='Abrir arquivo (Ctrl+O)',command=abrirArquivoDialog)
menu_arquivo.add_command(label='Nova Guia (Ctrl-N)')
menu_arquivo.add_command(label='Abrir pasta')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Recentes')
menu_arquivo.add_cascade(label='Exemplos', menu=menu_arquivo_cascate)

atualizarListaDeScripts()

menu_arquivo.add_separator()
menu_arquivo.add_command(label='Salvar (Ctrl-S)',command=salvarArquivo)
menu_arquivo.add_command(label='Salvar Como (Ctrl-Shift-S)',command=salvarArquivoComoDialog)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='imprimir (Ctrl-P)')
menu_arquivo.add_command(label='Exportar (Ctrl-E)')
menu_arquivo.add_command(label='Enviar por e-mail ')

# =================================== EXECUTAR =================================== #
menu_executar.add_command(label='Executar Tudo (F5)',command=iniciarOrquestradorDoInterpretador)
menu_executar.add_command(label='Executar linha (F6)')
menu_executar.add_command(label='Executar até breakpoint (F7)')
menu_executar.add_command(label='Executar com delay (F8)')
menu_executar.add_command(label='Parar execução (F9)')
menu_executar.add_command(label='Inserir breakpoint (F10)')

# =================================== LOCALIZAR =================================== #
menu_localizar.add_command(label='Localizar (CTRL + F)')
menu_localizar.add_command(label='Substituir (CTRL + R)')

# =================================== FERRAMENTAS =================================== #
menu_ferramentas.add_command(label='corrigir identação')
menu_ferramentas.add_command(label='Numero de espaços para o tab')

# =================================== INTERFACE =================================== #
menu_interface.add_command(label='temas')
menu_interface.add_command(label='fonte')

# =================================== AJUDA =================================== #
menu_ajuda.add_command(label='Ajuda (F1)')
menu_ajuda.add_command(label='Comandos Disponíveis')
menu_ajuda.add_command(label='Comunidade')

# =================================== SOBRE =================================== #
menu_sobre.add_command(label='Projeto')

fr_opcoesRapidas = Frame(tela,background='#353544')
fr_opcoesRapidas.grid(row=1,column=1,sticky=NSEW)

icone_play      = PhotoImage(file='imagens/icon_play.png')
icone_break     = PhotoImage(file='imagens/icon_break.png')
icone_save      = PhotoImage(file='imagens/icon_save.png')
icone_continue  = PhotoImage(file='imagens/icon_continue.png')
icone_pre_save  = PhotoImage(file='imagens/icon_pre_save.png')
icone_new_file  = PhotoImage(file='imagens/icon_new_file.png')

icone_play      = icone_play.subsample(2,2) 
icone_break     = icone_break.subsample(2,2) 
icone_save      = icone_save.subsample(2,2) 
icone_continue  = icone_continue.subsample(2,2) 
icone_pre_save  = icone_pre_save.subsample(2,2) 
icone_new_file  = icone_new_file.subsample(2,2) 

btn_play = Button(fr_opcoesRapidas,image=icone_play,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_play.grid(row=1,column=1)

btn_break = Button(fr_opcoesRapidas,image=icone_break,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_break.grid(row=1,column=2)

btn_save = Button(fr_opcoesRapidas,image=icone_save,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_save.grid(row=1,column=3)

btn_continue = Button(fr_opcoesRapidas,image=icone_continue,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_continue.grid(row=1,column=4)

btn_pre_save = Button(fr_opcoesRapidas,image=icone_pre_save,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_pre_save.grid(row=1,column=5)

btn_new_file = Button(fr_opcoesRapidas,image=icone_new_file,relief=FLAT,background='#353544',highlightthickness=0,activebackground='#353544')
btn_new_file.grid(row=1,column=6)
# =================================== INTERFACE GERAL =================================== #
fr_InPrincipal = Frame(tela,bg='#393944')
fr_InPrincipal.grid_columnconfigure(2,weight=1)
fr_InPrincipal.rowconfigure(1,weight=1)
fr_InPrincipal.grid(row=2,column=1,sticky=NSEW)

lb_linhas = Text(fr_InPrincipal,design.lb_linhas())
lb_linhas.insert('end',' 1\n 2\n 3\n 4\n 5\n 6\n 7\n 8')
lb_linhas.config(state=DISABLED,relief = FLAT,border= 0, highlightthickness=0)
lb_linhas.grid(row=1,column=1,sticky=NSEW)

# =================================== TELA DE CODIFICAÇÃO =================================== #
tx_codificacao = Text(fr_InPrincipal,design.tx_codificacao(),relief=FLAT)
tx_codificacao.focus_force()
tx_codificacao.grid(row=1,column=2,sticky=NSEW)

#tx_codificacao.bind("<Button-4>",lambda tx_codificacao:scroolUp())
#tx_codificacao.bind("<Button-5>",lambda tx_codificacao:scroolDown())
tx_codificacao.bind('<Configure>',configuracoes)
tx_codificacao.bind("<KeyRelease>",lambda tx_codificacao :sintaxeDasPalavras())
tx_codificacao.bind('<KeyPress>',obterPosicaoDoCursor)
tx_codificacao.delete(1.0, END)


tela.mainloop()
