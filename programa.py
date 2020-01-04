from tkinter import filedialog
from tkinter import *          
from funcoes import funcao
from design  import design
from design  import Sintaxe
from tkinter import messagebox
from threading import Thread

import tkinter.messagebox as tkmessagebox
import time

# impede que o programa seja iniciado enquanto outro está sendo executado
global contadorThreads

# Se um comando de repetição tiver sido ativado 
global repetirAtivado

# Se a função repita for ativada
global funcaoRepita

# Se um comendo de funcao tiver sido ativado
global funcaoAtivada

# Variáveis usadas durante a interpretação do programa
global variaveis

# Contém o link e o texto do arquivo
global arquivoAbertoAtualmente

# Exibe as informações do interpretador em tempo real
global tx_informacoes

# Local onde o programa é codificado
global tx_codificacao

# Contador de linhas do programa
global lb_linhas

# Dicionario com todas as funcoes
global dicFuncoes

# funcao que está sendo analisada
global funcaoQueEstaSendoAnalisada

# Aconteceu algum erro durante a execução do programa
global aconteceuUmErro

# A tela está em full screen
global boolTelaEmFullScreen

# Botões das guias
global btnsGuias

arquivoAbertoAtualmente = {'link':None,'texto':None}
boolTelaEmFullScreen = False 
aconteceuUmErro = False
repetirAtivado = False
funcaoAtivada = False
contadorThreads = 0
dicFuncoes = {}
variaveis = {}
btnsGuias = []

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

    ftypes = [('Arquivos fyn', '*.fyn'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        print('arquivo {} escolhido'.format(filename))        
        arquivo = funcao.abrir_arquivo(filename) 

        if arquivo != None:
            tx_codificacao.delete(1.0, END)
            tx_codificacao.insert(END,arquivo)

        sintaxeDasPalavras() # atualizar a sintaxe
        arquivoAbertoAtualmente['link'] = filename
        arquivoAbertoAtualmente['texto'] = arquivo
    else:
        print('Nenhum arquivo escolhido')

def colorirUmaPalavra(palavra,linha,valor1,valor2,cor):

    linha1 = '{}.{}'.format(linha , valor1) # linha.coluna(revisar)
    linha2 = '{}.{}'.format(linha , valor2) # linha.coluna(revisar)

    tx_codificacao.tag_add(palavra, linha1 , linha2) 
    tx_codificacao.tag_config(palavra, foreground = cor)

def colorirUmErro(palavra,linha,valor1,valor2,cor='red'):
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
                if caractere > 0: # Se não estiver no primeiro caractere
                    if frase[caractere-1 : caractere+len(palavra)] == ' '+palavra: # Analise o contexto da palavra
                        validacao += 1 
                else:
                        validacao += 1

                if caractere + len(palavra) < quantidade_de_caracteres: # Se não estourar os caracteres
                    if frase[caractere:caractere+1+len(palavra)] == palavra+' ':   # Analise o contexto da palavra
                        validacao += 1 
                else:
                        validacao += 1

                if validacao == 2: # Se tiver sido validado
                    # colora a palavra
                    colorirUmaPalavra(palavra,linha,caractere,caractere + len(palavra),cor)

def sintaxe(palavra,cor):
    cor = cor['foreground']
    tx_codificacao.tag_delete(palavra)
    lista = tx_codificacao.get(1.0,END).split('\n')

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
            # Remoção de bugs no regex
            palavra = palavra.replace('+','\\+')
            palavra = palavra.replace('/','\\/')
            palavra = palavra.replace('*','\\*')

            for valor in re.finditer('(^|\\s){}(\\s|$)'.format(palavra),lista[linha]):
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

    threadContadorLinhas = Thread(target=contadorDeLinhas())
    threadContadorLinhas.start()

    # ATRIBUIÇÃO
    sintaxe('vale'                       , Sintaxe.atribuicao())
    sintaxe('recebe'                     , Sintaxe.atribuicao())
    sintaxe('='                          , Sintaxe.atribuicao())

    # LOOPS  
    sintaxe('enquanto'                   , Sintaxe.lista())
    sintaxe('while'                      , Sintaxe.lista())

    sintaxe('repita'                     , Sintaxe.lista())
    sintaxe('repeat'                     , Sintaxe.lista())
    sintaxe('vezes'                      , Sintaxe.lista())
    sintaxe('vez'                        , Sintaxe.lista())

    # ENTRADA
    sintaxe('oque o for digitado'        , Sintaxe.entrada())

    # LÓGICO
    sintaxe('ou'                         , Sintaxe.logico())
    sintaxe('e'                          , Sintaxe.logico())
 
    sintaxe('for maior que'              , Sintaxe.logico())    
    sintaxe('>'                          , Sintaxe.logico())    
 
    sintaxe('for menor que'              , Sintaxe.logico())    
    sintaxe('<'                          , Sintaxe.logico())    
 
    sintaxe('for igual a'                , Sintaxe.logico())    
    sintaxe('=='                         , Sintaxe.logico())    
 
    sintaxe('for maior ou igual a'       , Sintaxe.logico())    
    sintaxe('>='                         , Sintaxe.logico())    

    sintaxe('for menor ou igual a'       , Sintaxe.logico())    
    sintaxe('<='                         , Sintaxe.logico())    

    sintaxe('for diferente de'           , Sintaxe.logico())    
    sintaxe('!='                         , Sintaxe.logico())    

    sintaxe('se'                         , Sintaxe.condicionais())
    sintaxe('if'                         , Sintaxe.condicionais())
    sintaxe('senao'                      , Sintaxe.condicionais())

    sintaxe('+'                          , Sintaxe.contas())
    sintaxe('mais'                       , Sintaxe.contas())

    sintaxe('/'                          , Sintaxe.contas())
    sintaxe('divide'                     , Sintaxe.contas())
    sintaxe('dividido por'               , Sintaxe.contas())

    sintaxe('**'                         , Sintaxe.contas())
    sintaxe('elevado'                    , Sintaxe.contas())
    sintaxe('elevado por'                , Sintaxe.contas())
    sintaxe('elevado a'                , Sintaxe.contas())

    sintaxe('*'                          , Sintaxe.contas())
    sintaxe('multiplique'                , Sintaxe.contas())
    sintaxe('multiplicado por'           , Sintaxe.contas())

    sintaxe('-'                          , Sintaxe.contas())
    sintaxe('menos'                      , Sintaxe.contas())

    sintaxe('%'                          , Sintaxe.contas())

    sintaxe('exiba'                      , Sintaxe.exibicao())
    sintaxe('mostre'                     , Sintaxe.exibicao())
    sintaxe('escreva'                    , Sintaxe.exibicao())
    sintaxe('escreva na tela'            , Sintaxe.exibicao())
    sintaxe('print'                      , Sintaxe.exibicao())
    sintaxe('imprima'                    , Sintaxe.exibicao())
    sintaxe('display'                    , Sintaxe.exibicao())
    sintaxe('mostre nessa linha'         , Sintaxe.exibicao())
    sintaxe('exiba nessa linha'          , Sintaxe.exibicao())
    sintaxe('escreva nessa linha'        , Sintaxe.exibicao())
    sintaxe('imprima nessa linha'        , Sintaxe.exibicao())

    sintaxe('funcao'                     , Sintaxe.tempo())
    sintaxe('function'                    , Sintaxe.tempo())
    sintaxe('retorne'                    , Sintaxe.tempo())

    sintaxe('recebe parametros'          , Sintaxe.tempo())
    sintaxe('passando parametros'        , Sintaxe.tempo())
    sintaxe('passando parametro'        , Sintaxe.tempo())

    sintaxe('parametros'                 , Sintaxe.tempo())
    sintaxe('parametro'                  , Sintaxe.tempo())
    sintaxe('passando'                  , Sintaxe.tempo())

    sintaxe('espere'                     , Sintaxe.tempo())
    sintaxe('aguarde'                     , Sintaxe.tempo())
    sintaxe('segundos'                   , Sintaxe.tempo())
    sintaxe('segundo'                    , Sintaxe.tempo())
    sintaxe('milisegundos'               , Sintaxe.tempo())
    sintaxe('ms'                         , Sintaxe.tempo())
    sintaxe('milisegundo'                , Sintaxe.tempo())
    sintaxe('s'                          , Sintaxe.tempo())

    sintaxe('número aleatório entre'     , Sintaxe.tempo())
    sintaxe('número aleatorio entre'     , Sintaxe.tempo())
    sintaxe('numero aleatório entre'     , Sintaxe.tempo())
    sintaxe('numero aleatorio entre'     , Sintaxe.tempo())

    sintaxe('numerico'                   , Sintaxe.numerico())

    sintaxe('"'                          , Sintaxe.string())
    sintaxe("'"                          , Sintaxe.string())

    sintaxe('comentario'                 , Sintaxe.comentario())

# inicia o interpretador
def iniciarOrquestradorDoInterpretador(event = None):
    inicio = time.time() # Marca o inicio do programa

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

    tx_informacoes.insert(END, '\n<script finalizado em {:.3} segundos>'.format(time.time() - inicio))
    tx_informacoes.see("end")

def orquestradorDoInterpretador(linhas):
    global contadorThreads
    global repetirAtivado
    global funcaoRepita
    global aconteceuUmErro
    global funcaoAtivada
    global dicFuncoes
    global funcaoQueEstaSendoAnalisada

    contadorThreads += 1    # Aumenta o número de vezes que o interpretador foi chamado
    linhaComCodigoQueFoiExecutado = ''       # Reseta a linha de comando (enquanto >>x for menor que 6<<)
    contador = 0            # contador para andar por todos os caracteres
    blocoComOsComando = ''  # Armazena blocos de código {}
    blocoDeCodigo = False   # Tem um bloco de código sendo armazenado?
    penetracao = 0          # Penetracao dos {{{{}}}} de forma recursiva
    estadoDaCondicional = [False,None] # Ler um bloco de código (Condição verdadeira)

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
                    colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                    return [False,'']

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
                colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                return [False,'']

            # Se a confição chamadora do bloco for verdadeira
            if estadoDaCondicional[1] == True:

                # Se acontecer um loop
                if repetirAtivado:
                    
                    # Enquanto a condição for verdadeira
                    while linhaComOResultadoDaExecucao[1]:

                        # Envia um bloco completo para ser novamente executado
                        resultadoExecucao = orquestradorDoInterpretador(blocoComOsComando)

                        # Se der erro na exeução do bloco
                        if resultadoExecucao[0] == False:
                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(resultadoExecucao[1]))
                            colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(resultadoExecucao[1]))+1,cor='#dd4444')
                            return [False,'']

                        # Testa novamente a condição do loop
                        linhaComOResultadoDaExecucao = interpretador(linhaComCodigoQueFoiExecutado)

                        # Se der erro na exeução do teste
                        if linhaComOResultadoDaExecucao[0] == False:
                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(linhaComOResultadoDaExecucao[1]))
                            colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(linhaComOResultadoDaExecucao[1]))+1,cor='#dd4444')
                            return [False,'']

                    if aconteceuUmErro:
                        break

                elif funcaoRepita != 0:

                    # Se for maior que zero, aconteceu um repit
                    for valor in range(0,funcaoRepita):
                        # Envia um bloco completo para ser novamente executado
                        resultadoOrquestrador = orquestradorDoInterpretador(blocoComOsComando)

                        # Se acontecer um erro
                        if resultadoOrquestrador[0] == False:
                            aconteceuUmErro = True
                            tx_informacoes.insert(END,str(resultadoOrquestrador[1]))
                            colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(resultadoOrquestrador[1]))+1,cor='#dd4444')
                            return [False,'']

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
                        colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(resultadoOrquestrador[1]))+1,cor='#dd4444')
                        return [False,'']

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
                    colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(str(estadoDaCondicional[1]))+1,cor='#dd4444')
                    return [False,'']

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

    # Libera uma unidade no contador de Threads
    contadorThreads -= 1

    if penetracao > 0:
        aconteceuUmErro = True
        if penetracao == 1:
            vezesEsquecidas = '1 vez'
        else:
            vezesEsquecidas = '{} vezes'.format(penetracao)

        msgErro = """Você abriu uma chave'{' e esqueceu de fecha-la '}' """ + str(vezesEsquecidas) + """, por favor, analise o código navamente e corrija"""

        tx_informacoes.insert(END,msgErro)
        colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(msgErro)+1,cor='#dd4444')
        return [False,'']

    elif penetracao < 0:
        aconteceuUmErro = True
        if penetracao == -1:
            vezesEsquecidas = 'uma vez'
        else:
            vezesEsquecidas = '{} vezes'.format(penetracao*-1)

        msgErro = """Você abriu uma chave '{' e fechou ela '}' """ + str(vezesEsquecidas) + """, por favor, analise o código navamente e corrija"""

        tx_informacoes.insert(END,msgErro)
        colorirUmErro('codigoErro',linha=1,valor1=0,valor2=len(msgErro)+1,cor='#dd4444')
        return [False,'']

    return [True,"Não acontecera erros durante a execução do interpretador"]

# Interpreta um conjunto de linhas
def interpretador(codigo):
    codigo = codigo.strip()
    
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
        return [True,None]

    else:

        # Obtem todas as linhas 
        linhas = codigo.split('\n')

        aleatorio        = ['número aleatório entre','número aleatorio entre','numero aleatório entre','numero aleatorio entre']
        mostreNessa      = ['mostre nessa linha ','exiba nessa linha ','escreva nessa linha ','imprima nessa linha ']
        mostre           = ['escreva na tela ','mostre ','exiba ','print ','imprima ','display ','escreva ']
        
        declaraVariaveis = [' vale ',' recebe ',' = ']
        funcoes          = ['funcao ','function ']
        loopsss          = ['enquanto ','while ']
        aguarde          = ['espere ','aguarde ']
        repita           = ['repita ','repeat ']
        se               = ['se ','if ']

        #entrada = ['recebe o que o usuario digitar','capture o que o usuario digitar','recebe o que for digitado','leia o que for digitado','input']
        #vetor = ['vetor','crie uma lista chamada','lista']

        for linha in linhas:
            for comando in mostreNessa:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoExibicaoNessaLinha(linha[len(comando):])

        for linha in linhas:
            for comando in mostre:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoExibicao(linha[len(comando):])

            for comando in se:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoCondicional(linha[len(comando):])

            for comando in loopsss:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoLoopsEnquanto(linha[len(comando):])

            for comando in aguarde:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoTempo(linha[len(comando):])

            for comando in funcoes:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoDeclararFuncoes(linha[len(comando):])

            for comando in aleatorio:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoNumeroAleatorio(linha[len(comando):])

            for comando in repita:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoRepitir(linha[len(comando):])

            for comando in declaraVariaveis:
                if comando in linha:
                    return funcaoAtribuicao(linha,comando)

            if linha.isalnum():
                return funcaoExecutaFuncoes(linha)

            return [False,"Um comando desconhecido foi localizado:'{}'".format(linha)]

# repita 10 vezes \n{\nmostre 'oi'\n}
def funcaoRepitir(linha):
    print('funcao repetir')
    global funcaoRepita

    # Remoção de lixo
    linha = linha.replace('vezes','')
    linha = linha.replace('vez','')

    # Eliminação de espaços laterais
    linha = linha.strip()

    # Obter o valor da variável
    linha = abstrairValoresDaLinhaInteira(linha)

    # Deu erro?
    if linha[0] == False:
        return linha

    # É inteiro
    try:
        int(linha[1])
    except:
        return [False,"O valor precisa ser inteiro!"]
    else:
        funcaoRepita = int(linha[1])

        if funcaoRepita == 0:
            # Se for zero, não reproduza nenhuma vez
            return [True,False]

        # Não houve erros e é para repetir
        return [True,True]

# numero aleatório entre 10 e 20
def funcaoNumeroAleatorio(linha):
    print('funcao aleatório')

    # Remova os espaços da linha
    linha = linha.strip()

    # Se tiver  e que indica intervalo
    if ' e ' in linha:

        # Obtenção dos dois valores
        num1, num2 = linha.split(' e ')
 
        # Obtendo ambos os valores
        num1 = abstrairValoresDaLinhaInteira(num1)
        num2 = abstrairValoresDaLinhaInteira(num2)

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
            return [False,"O valor 1 não é numérico"]
 
        # Se o segundo for numéricos
        try:
            int(num2[1])
        except:
            return [False,"O valor 2 não é numérico"]

        # Retorne um valo aleatório
        import random
        return [True,random.randint(int(num1[1]),int(num2[1]))]

    else:
        return [False,"Erro, você precisa definir o segundo valor, tipo 'entre 2 e 5'!"]

# calcMedia passando parametros nota1, nota2
def funcaoExecutaFuncoes(linha):
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
        return [False,"Essa função não existe"]
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
                    resultado = funcaoAtribuicao('{} recebe {} '.format(dicFuncoes[nomeDaFuncao][0][parametroDeclarar],listaFinalDeParametros[parametroDeclarar]),'recebe')

                    if resultado[0] == False:
                        return resultado
            else:
                return [False,"A função '{}' tem {} parametros, mas você passou {} parametros!".format(nomeDaFuncao,len(dicFuncoes[nomeDaFuncao][0]),len(listaFinalDeParametros))]

        # Se tiver só um parametro
        elif parametros != None:
            if len(dicFuncoes[nomeDaFuncao][0]) == 1:
                resultado = funcaoAtribuicao('{} recebe {} '.format(dicFuncoes[nomeDaFuncao][0],parametros),'recebe')

                if resultado[0] == False:
                    return resultado

        resultadoOrquestrador = orquestradorDoInterpretador(dicFuncoes[nomeDaFuncao][1])
        if resultadoOrquestrador[0] == False:
            return resultadoOrquestrador

        return [True,None]

# funcao gabriel recebe paramentros nota1, nota2
def funcaoDeclararFuncoes(linha):
    print('declarar funcoes')
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
            print('funcoes declaradas:',dicFuncoes)
            return [True,True]
    
    dicFuncoes[linha.strip()] = ['','bloco']
    funcaoQueEstaSendoAnalisada = linha.strip()
    funcaoAtivada = True
    print('funcoes declaradas:',dicFuncoes)
    return [True,True]

# parei aqui
def funcaoExibicao(linha):
    print('funcao exibição nessa linha ')
    codigo = linha.strip()
    return abstrairValoresDaLinhaInteira(codigo)

def funcaoExibicaoNessaLinha(linha):
    print('funcao exibir nessa linha')
    codigo = linha.strip()
    retorno = abstrairValoresDaLinhaInteira(codigo)

    if retorno[0] == False:
        return retorno
    return [retorno[0],':nessaLinha:'+str(retorno[1])]

def funcaoTempo(codigo):
    print('funcao tempo')
    codigo = codigo.strip()

    tiposEspera = [' milisegundos',' milisegundo',' segundos',' segundo',' ms',' s']

    for comando in tiposEspera:
        if len(comando) < len(codigo):                                                         # Se o comando não estrapolar o código
            if comando == codigo[len(codigo)-len(comando):]:                                   # Se o comando estiver no código
                resultado = abstrairValoresDaLinhaInteira(codigo[:len(codigo)-len(comando)])   # Tente obter o real valor no código
                if resultado != False:                                                         # Se foi possível obter
                    if comando == " segundos" or comando == " s" or comando == " segundo":     # Se está em segunso
                        time.sleep(resultado[1])                                               # Tempo em segundos
                        return [True,None]

                    elif comando == " milisegundos" or comando == " ms" or comando == "milisegundo": # Se está em milisegundos
                        time.sleep(resultado[1]/1000)                                   # Tempo em milisegundos
                        return [True,None]

                else:
                    return [False,'Erro ao obter um valor no tempo']

    return [True,None]

def obterValorDeString(string):
    print(">>>",string)
    valorFinal = ''
    anterior = 0

    for valor in re.finditer(""""[^"]*"|'[^']*'""",string):
        print(valor.group())
        print(string[anterior:valor.start()],'>>>>>>>>>>>...')
        abstrair = abstrairValoresDaLinhaInteira(string[anterior:valor.start()])
        if abstrair[0] == False:
            print("EROOOOOO")
            return abstrair

        valorFinal = valorFinal + str(abstrair[1]) + string[valor.start():valor.end()]
        anterior = valor.end()

    # Capturar o resto        
    abstrair = abstrairValoresDaLinhaInteira(string[anterior:])
    if abstrair[0] == False:
        print("EROOOOOO2")
        return abstrair

    valorFinal = valorFinal + str(abstrair[1])

    return [True,valorFinal]

def fazerContas(linha):
    print('Fazer contas')
    linha = str(linha)

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
        return [False, "Isso é uma string"]

    # Removendo os espaços laterais
    linha = ' {} '.format(linha)

    simbolosEspeciais = ['+','-','*','/','%','(',')']
    qtdSimbolosEspeciais = 0

    # Deixando todos os itens especiais com espaço em relação aos valores
    for iten in simbolosEspeciais:
        if iten in linha:
            qtdSimbolosEspeciais += 1
        linha = linha.replace(iten,' {} '.format(iten))

    # Se não tiver nenhuma operação
    if qtdSimbolosEspeciais == 0:
        return [False, "Não foi possivel realizar a conta, porque não tem nenhum valor aqui. "]

    # Correção do potenciação
    linha = linha.replace('*  *','**')
    linha = linha.replace('< =','<=')
    linha = linha.replace('> =','>=')
    linha = linha.replace("! =",'!=')

    # Abstração de variáveis
    anterior = 0
    normalizacao = 0
    linha_base = linha
    for valor in re.finditer(' ',linha_base):
        palavra = linha[anterior : valor.start() + normalizacao]

        if palavra.isalnum() and palavra[0].isalpha():
            variavelDessaVez = obterValorDeUmaVariavel(palavra)
            linha = str(linha[:anterior]) + str(variavelDessaVez[1]) + str(linha[valor.start() + normalizacao:]) 

            if len(palavra) < len(str(variavelDessaVez[1])):
                normalizacao += (len(str(variavelDessaVez[1])) - len(palavra))

            elif len(palavra) > len(str(variavelDessaVez[1])):
                normalizacao -= (len(palavra) - len(str(variavelDessaVez[1])))

        anterior = valor.end() + normalizacao

    # Tente fazer uma conta com isso
    try:
        resutadoFinal = eval(linha)
    except Exception as erro:
        return [False, "Não foi possivel realizar a conta |{}|".format(linha)]
    else:
        return [True, resutadoFinal]

def obterValorDeUmaVariavel(variavel):
    print('obterValorDeUmaVariavel')
    global variaveis

    variavel = variavel.replace('\n','')

    try:
        variaveis[variavel]
    except:
        return [False,'[erro] - variavel:{} não definida'.format(variavel)]
    else:
        return [True,variaveis[variavel]]

def abstrairValoresDaLinhaInteira(possivelVariavel):
    print('abstrairValoresDaLinhaInteira')
    print(possivelVariavel)
    possivelVariavel = str(possivelVariavel)
    possivelVariavel = possivelVariavel.replace('\n','')
    possivelVariavel = possivelVariavel.strip()
    if possivelVariavel == '':
        return [True,possivelVariavel]

    print(possivelVariavel,'::')
    # caso existam contas entre strings
    if possivelVariavel[0] == ',':
        possivelVariavel = possivelVariavel[1:]
        print("Nova",possivelVariavel)

    if len(possivelVariavel) > 1:
        if possivelVariavel[-1] == ',':
            possivelVariavel = possivelVariavel[0:len(possivelVariavel)-1]

    print(possivelVariavel,'nova2')

    possivelVariavel = possivelVariavel.strip()
    if possivelVariavel == '':
        return [True,possivelVariavel]

    resultado = fazerContas(possivelVariavel)

    # Se deu certo
    if resultado[0] == True:
        return resultado

    if '"' in possivelVariavel or "'" in possivelVariavel:
        return obterValorDeString(possivelVariavel)

    try:
        float(possivelVariavel)
    except:
        resultado = obterValorDeUmaVariavel(possivelVariavel)
        return resultado
    else:
        return [True,float(possivelVariavel)]

def funcaoAtribuicao(linha,comando):
    global variaveis

    variavel, valor = linha.split(comando)

    variavel = variavel.strip()
    valor    = valor.replace('\n','')
    valor    = valor.strip()

    resultado = fazerContas(valor)

    if resultado[0] == True:
        variaveis[variavel] = resultado[1]
        return [True,None]

    if '"' in valor or "'" in valor: # é uma string
        valor = obterValorDeString(valor)
        if valor[0] == False:
            return valor

        variaveis[variavel] = valor[1]
        return [True,None]

    try:
        float(valor)
    except:
        resultado = obterValorDeUmaVariavel(valor)
        if resultado[0] == False:
            return resultado # True e False embutidos            

        variaveis[variavel] = resultado[1]
        return [True,None]

    else:
        variaveis[variavel] = float(valor)
        return [True,None]

def funcaoLoopsEnquanto(linha):
    global repetirAtivado
    repetirAtivado = True

    return funcaoCondicional(linha)

def funcaoCondicional(linha):
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
        return [False, "Não foi possivel realizar a condição por que não tem nenhum simbolo condicional"]

    print("\n\npalavras")
    # Abstração de variáveis
    anterior = 0
    linha = linha.strip() + " " # Esse espaço é para analisar o ultimo caractere
    atualizarPosicaoReferencia = 0
    for valor in re.finditer('\\s',linha):
        print(linha[anterior: valor.start()])
        palavra = linha[anterior:valor.start()+atualizarPosicaoReferencia]
        palavra = palavra.strip()
        print("PALAVRAS",palavra)
        if palavra.isalnum() and palavra[0].isalpha() and len(palavra) != 0 and palavra not in simbolos:
            variavelDessaVez = obterValorDeUmaVariavel(palavra)
            print(palavra,variavelDessaVez)
            if variavelDessaVez[0] == False:
                return variavelDessaVez

            linha = str(linha[:anterior]) + str(variavelDessaVez[1]) + str(linha[valor.start() + atualizarPosicaoReferencia:]) 

            # Se a variavel for maior que o valor
            if len(palavra) < len(variavelDessaVez):
                atualizarPosicaoReferencia += (len(str(variavelDessaVez[1])) - len(palavra))

            # Se a variavel for menor que a variável
            elif len(palavra) > len(variavelDessaVez):
                atualizarPosicaoReferencia -= (len(palavra) - len(str(variavelDessaVez[1])))

        anterior = valor.end() + atualizarPosicaoReferencia

    # Tente fazer uma conta com isso
    print(linha,'>>>>>>.')
    try:
        resutadoFinal = eval(linha)
        print(resutadoFinal)
    except Exception as erro:
        print("EROOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        return [False, "Não foi possivel realizar a condicao |{}|".format(linha)]
    else:
        return [True, resutadoFinal]

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

tela = Tk()
tela.title('Linguagem feynman beta 0.4')
tela.configure(bg='#565656')
tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)

tela.bind('<F11>',lambda event: modoFullScreen(event))
tela.bind('<F5>',       lambda event: iniciarOrquestradorDoInterpretador(event))
tela.bind('<Control-s>',lambda event: salvarArquivo(event))
tela.bind('<Control-o>',lambda event: abrirArquivoDialog(event))
tela.bind('<Control-S>',lambda event: salvarArquivoComoDialog(event))

menu_barra = Menu(tela,design.cor_menu())
tela.config(menu=menu_barra)

menu_arquivo     = Menu(menu_barra, design.cor_menu())
menu_executar    = Menu(menu_barra, design.cor_menu())
menu_localizar   = Menu(menu_barra, design.cor_menu())
menu_editar      = Menu(menu_barra, design.cor_menu())
menu_ferramentas = Menu(menu_barra, design.cor_menu())
menu_interface   = Menu(menu_barra, design.cor_menu())
menu_ajuda       = Menu(menu_barra, design.cor_menu())
menu_sobre       = Menu(menu_barra, design.cor_menu())

menu_barra.add_cascade(label='Arquivo'   , menu=menu_arquivo)
menu_barra.add_cascade(label='Executar'  , menu=menu_executar)
menu_barra.add_cascade(label='Localizar' , menu=menu_localizar)
menu_barra.add_cascade(label='Editar'    , menu=menu_editar)
menu_barra.add_cascade(label='Interface' , menu=menu_interface)
menu_barra.add_cascade(label='Ajuda'     , menu=menu_ajuda)
menu_barra.add_cascade(label='sobre'     , menu=menu_sobre)

# =================================== ARQUIVO =================================== #
menu_arquivo.add_command(label='Abrir arquivo (Ctrl+O)',command=abrirArquivoDialog)
menu_arquivo.add_command(label='Nova Guia (Ctrl-N)')
menu_arquivo.add_command(label='Abrir pasta')
menu_arquivo.add_command(label='Recentes')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Salvar (Ctrl-S)',command=salvarArquivo)
menu_arquivo.add_command(label='Salvar Como (Ctrl-Shift-S)',command=salvarArquivoComoDialog)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='imprimir (Ctrl-P)')
menu_arquivo.add_command(label='Exportar (Ctrl-E)')
menu_arquivo.add_command(label='Enviar por e-mail ')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair (Alt-F4)')

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

# =================================== EDITAR =================================== #
menu_editar.add_command(label='copiar (CTRL + C)')
menu_editar.add_command(label='cortar (CTRL + X)')
menu_editar.add_command(label='colar (CTRL + V)')
menu_editar.add_command(label='desfazer (CTRL + Z)')
menu_editar.add_command(label='refazer (CTRL + Y)')
menu_editar.add_command(label='selecionar tudo (CTRL + A)')

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
menu_sobre.add_command(label='Desenvolvedores',command=lambda:trocar_de_tela(fr_InPrincipal,fr_sobDesenvol))

# =================================== INTERFACE GERAL =================================== #
fr_InPrincipal = Frame(tela,bg='#565656')
fr_InPrincipal.grid_columnconfigure(1,weight=1)
fr_InPrincipal.rowconfigure(2,weight=1)

def atualizaCor(btn):
    global arquivoAbertoAtualmente
    global btnsGuias

    for frame,titulo,botao in btnsGuias:
        if botao == btn:
            frame.configure(bg='#565656')
            titulo['text'] = str(arquivoAbertoAtualmente['link'])
            titulo.configure(bg='#565656',activebackground='#565656',activeforeground='#dddddd')
            botao.configure(bg='#565656',activebackground='#565656',activeforeground='#dddddd')
        else:
            frame.configure(bg='#343434')
            titulo.configure(bg='#343434',activebackground='#343434',activeforeground='#343434')
            botao.configure(bg='#343434',activebackground='#343434',activeforeground='#343434')

fr_guias = Frame(fr_InPrincipal,bg='#232323')
for x in range(1,5):
    if x == 1:
        cor = '#565656'
    else:
        cor = '#343434'

    FrGuia = Frame(fr_guias,bg=cor)
    lblGuiaTitulo = Label(FrGuia,bg=cor,fg='#dddddd',text='arquivo.fyn')
    btnGuiaFechar = Button(FrGuia,bg=cor,fg=cor,text='x',relief=SUNKEN,activebackground=cor,activeforeground='white',highlightthickness=0,bd=0,justify='center')
    btnGuiaFechar['command'] = lambda botao = btnGuiaFechar : atualizaCor(botao)

    btnsGuias.append([FrGuia,lblGuiaTitulo,btnGuiaFechar])

    FrGuia.grid(row=1,column=x+1,sticky=NSEW)
    lblGuiaTitulo.grid(row=1,column=x+1,sticky=NSEW)
    btnGuiaFechar.grid(row=1,column=x+2,sticky=NSEW)

fr_guias.grid(row=1,column=0,columnspan=2,sticky=NSEW)


def create_topExecutando():
    global tx_informacoes

    topExecutando = Toplevel(tela)
    topExecutando.grid_columnconfigure(1,weight=1)
    topExecutando.rowconfigure(1,weight=1)
    topExecutando.geometry("600x300+100+100")

    tx_informacoes = Text(topExecutando,design.tx_informacoes())
    tx_informacoes.focus_force()
    tx_informacoes.grid(row=1,column=1,sticky=NSEW)

from tkinter.font import nametofont
global alturaDoWidget

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

def scroolUp(event = None):
    return 0
    global lb_linhas
    global tx_codificacao
    global alturaDoWidget

    lstLinhasContadas  = str(lb_linhas.get(1.0,END)).strip()
    lstLinhasContadas = lstLinhasContadas.split('\n')
    if lstLinhasContadas == ['']:
        lstLinhasContadas = ['1']

    lstLinhasPrograma = str(tx_codificacao.get(1.0,END))
    lstLinhasPrograma = lstLinhasPrograma.strip()
    lstLinhasPrograma = lstLinhasPrograma.split('\n')
    print(lstLinhasPrograma)
    if len(lstLinhasPrograma) == 0:
        print('teste33333')
        lstLinhasPrograma = ['1']

    # Se estiver na linha 2
    if int(lstLinhasContadas[0]) == 2:
        print('teste4644')
        linhaInicial = int(lstLinhasContadas[0]) - 1
        linhaFinal = int(lstLinhasContadas[0]) + alturaDoWidget -1
    # Se estiver no limite
    elif int(lstLinhasContadas[0]) == 1:
        print('teste553')
        linhaInicial = int(lstLinhasContadas[0])
        linhaFinal = int(lstLinhasContadas[0]) + alturaDoWidget 

    # Subida normal
    else:
        print('teste22')
        linhaInicial = int(lstLinhasContadas[0]) - 2
        linhaFinal = int(lstLinhasContadas[0]) + alturaDoWidget - 2

    if linhaFinal > len(lstLinhasPrograma):

        linhaFinal = len(lstLinhasPrograma)+1


    linhas = ''
    for numLinha in range(linhaInicial,linhaFinal):
        linhas = linhas + '{}\n'.format(numLinha)

    print(len(lstLinhasPrograma))
    atualizaLinhasLaterais(linhas)

def scroolDown(event = None):
    return 0
    global lb_linhas
    global tx_codificacao
    global alturaDoWidget

    lstLinhasContadas  = str(lb_linhas.get(1.0,END)).strip()
    lstLinhasContadas = lstLinhasContadas.split('\n')
    if len(lstLinhasContadas) == 0:
        lstLinhasContadas = ['1']

    lstLinhasPrograma = str(tx_codificacao.get(1.0,END))
    lstLinhasPrograma = lstLinhasPrograma.strip()
    lstLinhasPrograma = lstLinhasPrograma.split('\n')
    if len(lstLinhasPrograma) == 0:
        lstLinhasPrograma = ['1']

    linhaInicial = int(lstLinhasContadas[0]) + 2
    linhaFinal = int(lstLinhasContadas[0]) + alturaDoWidget + 2

    linhas = ''
    for numLinha in range(linhaInicial,linhaFinal):
        linhas = linhas + '{}\n'.format(numLinha)

    # Eliminar o ultimo \n
    #atualizaLinhasLaterais(linhas)

lb_linhas = Text(fr_InPrincipal,design.lb_linhas())
lb_linhas.insert('end','1\n2\n3\n4\n5\n6\n7\n8')
lb_linhas.config(state=DISABLED,relief = SUNKEN,border= 0, highlightthickness=0)
# =================================== TELA DE CODIFICAÇÃO =================================== #
tx_codificacao = Text(fr_InPrincipal,design.tx_codificacao())
tx_codificacao.bind("<KeyRelease>",lambda tx_codificacao:sintaxeDasPalavras())
tx_codificacao.bind("<Button-4>",lambda tx_codificacao:scroolUp())
tx_codificacao.bind("<Button-5>",lambda tx_codificacao:scroolDown())
tx_codificacao.bind('<Configure>',configuracoes)
tx_codificacao.delete(1.0, END)

# =================================== SOBRE > DESENVOLVEDORES =================================== #
fr_sobDesenvol = Frame(tela)
fr_sobDesenvol.rowconfigure(2,weight=15)
fr_sobDesenvol.rowconfigure((3,4),weight=1)
fr_sobDesenvol.grid_columnconfigure(1,weight=2)

lb_sobDeTitulo = Label(fr_sobDesenvol, design.lb_sobDeTitulo(), text=" COMBRATEC ")
lb_sobDAutores = Label(fr_sobDesenvol, design.lb_sobDAutores(), text="Gabriel Gregório da Silva")
lb_sobDesenAno = Label(fr_sobDesenvol, design.lb_sobDesenAno(), text="2019")

fr_InPrincipal.grid(row=1,column=1,sticky=NSEW)
tx_codificacao.grid(row=2,column=1,sticky=NSEW)
lb_linhas.grid(row=2,column=0,sticky=NSEW)
lb_sobDeTitulo.grid(row=1,column=1,sticky=NSEW)
lb_sobDAutores.grid(row=2,column=1,sticky=NSEW)
lb_sobDesenAno.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
