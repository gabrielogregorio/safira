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

arquivoAbertoAtualmente = {'link':None,'texto':None}
boolTelaEmFullScreen = False 
aconteceuUmErro = False
repetirAtivado = False
funcaoAtivada = False
contadorThreads = 0
dicFuncoes = {}
variaveis = {}

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

# Tratamento para strings
def sintaxe_linha_string(palavra,cor,frase,linha):
    evento_string = False # houve uma string?
    lstPosicoesEvento = [] 

    for caractere in range(len(frase)): # Ande por todos os caracteres da frase

        # Se aconteceu uma string e elá já estiver sido iniciada
        if (frase[caractere] == '"' or frase[caractere] == "'") and evento_string == True: 

            evento_string = False # Resete o evento string
            lstPosicoesEvento.append(caractere+1) # Salve a posição que finalizou
            colorirUmaPalavra(palavra,linha,lstPosicoesEvento[0],lstPosicoesEvento[1],cor) # Aplique a coloração
            lstPosicoesEvento = [] # Resete a posição

        elif frase[caractere] == '"' or frase[caractere] == "'": # Se vai acontecer um evento string
            evento_string = True # Marque como evento string iniciado
            lstPosicoesEvento.append(caractere) # Salve a posição que começou

    if evento_string == True: # Se está contecendo um evento string
        tx_codificacao.tag_delete(palavra) # Remova as marcações
        colorirUmaPalavra(palavra,linha,lstPosicoesEvento[0],len(frase),cor) # Colore uma palavra

def sintaxe_linha_numerico(palavra,cor,frase,linha):                         # Aplica o tratamento para números
    for caractere in range(len(frase)):                                      # Ande por todos os caracteres da frase
        if frase[caractere].isnumeric():                                     # Verifique se é numérico
            colorirUmaPalavra(str(palavra),linha,caractere,caractere+1,cor)  # Colore uma palavra

def sintaxe_linha_comentario(palavra,cor,frase,linha):                       # Aplica o tratamento para comentários
    for caractere in range(len(frase)):                                      # Ande por todos os caracteres da frase
        if (frase[caractere:caractere+2] == '//') or (frase[caractere:caractere+1] == '#'): # Se tiver um caractere de comentário
            colorirUmaPalavra(palavra,linha,caractere,len(frase),cor)                       # Colore a região do comentário

# Analisa o contexto da palavra, separa número, string, comentário e palavras no geral
def sintaxe(palavra,cor):
    cor = cor['foreground']
    tx_codificacao.tag_delete(palavra) # remove todas as colorações da palavra
    lista = tx_codificacao.get(1.0,END).split('\n') # obtem uma lista com todas as linhas

    for linha in range(len(lista)): # Ande por todas as linhas

        if palavra == '"' or palavra == "'":  # se a palavra for apontada como string
            sintaxe_linha_string(palavra,cor,lista[linha],str(linha+1))

        elif palavra == "numerico": # se a palavra foi apontada como numérico
            sintaxe_linha_numerico(palavra,cor,lista[linha],str(linha+1))        

        elif palavra == "comentario": # Se a palavra foi apontada como comentário
            sintaxe_linha_comentario(palavra,cor,lista[linha],str(linha+1))        

        else: # Se for uma palavra especial
            sintaxe_linha(palavra,cor,lista[linha],str(linha+1))

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
    sintaxe('retorne'                    , Sintaxe.tempo())

    sintaxe('recebe parametros'          , Sintaxe.tempo())
    sintaxe('passando parametros'        , Sintaxe.tempo())
    sintaxe('parametros'                 , Sintaxe.tempo())
    sintaxe('parametro'                  , Sintaxe.tempo())

    sintaxe('espere'                     , Sintaxe.tempo())
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
    global contadorThreads
    global variaveis
    global repetirAtivado
    global funcaoRepita
    global funcaoAtivada
    global aconteceuUmErro

    # Se algum programa já estiver rodando
    if contadorThreads != 0:
        print("Alerta","Um programa está ativo nesse momento, Aguarde o outro programa se finalizado")
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

    aconteceuUmErro = False    
    tx_informacoes.insert(END, '\n [OK] finalizado')
    tx_informacoes.see("end")

def orquestradorDoInterpretador(linhas):
    global contadorThreads
    global repetirAtivado
    global funcaoRepita
    global aconteceuUmErro
    global funcaoAtivada
    global dicFuncoes
    global funcaoQueEstaSendoAnalisada

    contadorThreads += 1  # Aumenta o número de vezes que o interpretador foi chamado
    linhaComando = ''     # Reseta a linha de comando (enquanto >>x for menor que 6<<)

    contador = 0            # contador para andar por todos os caracteres
    registradorLinhas = ''  # Armazena blocos de código {}
    blocoDeCodigo = False   # Tem um bloco de código sendo armazenado?
    penetracao = 0          # Penetracao dos {{{{}}}} de forma recursiva
    lerBloco = [False,None] # Ler um bloco de código (Condição verdadeira)

    while contador < len(linhas) and not aconteceuUmErro:

        # Se começar um bloco e não tiver começado nenhum anteriormente
        if linhas[contador] == '{' and blocoDeCodigo == False:
            penetracao +=1

            if not registradorLinhas.isspace() and  registradorLinhas != '':
                lerBloco = interpretador(registradorLinhas.strip())

                if lerBloco[0] == False:
                    aconteceuUmErro = True
                    break

                if lerBloco[1] != None and "<class 'bool'>" not in str(type(lerBloco[1])):

                    # Insere no menu lateral
                    if len(str(lerBloco[1])) > len(":nessaLinha:"):

                        if str(lerBloco[1])[:len(":nessaLinha:")] == ":nessaLinha:":
                            tx_informacoes.insert(END, str(lerBloco[1][len(":nessaLinha:"):]))
                        else:
                            tx_informacoes.insert(END, str(lerBloco[1])+'\n')
                    else:
                        tx_informacoes.insert(END, str(lerBloco[1])+'\n')

                    tx_informacoes.see("end")

            # Recomeçar o registrador
            registradorLinhas = '' 
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

            if lerBloco[0] == False:
                aconteceuUmErro = True
                break

            # Se a confição chamadora do bloco for verdadeira
            if lerBloco[1] == True:

                # Se tinha um loop programado
                if repetirAtivado:
                    
                    # Enquanto a condição for verdadeira
                    while boolLinhaDeComando[1]:

                        # Envia um bloco completo para ser novamente executado
                        orquestradorDoInterpretador(registradorLinhas)

                        # Testa novamente a condição do loop
                        boolLinhaDeComando = interpretador(linhaComando)

                        if lerBloco[0] == False:
                            break

                elif funcaoRepita != 0:
                    # Se for maior que zero, aconteceu um repit
                    print(funcaoRepita,'>>>>>..')
                    for valor in range(0,funcaoRepita):
                        print("LOOOP")
                        orquestradorDoInterpretador(registradorLinhas)
                    funcaoRepita = 0
                    boolLinhaDeComando = [True,False]

                elif funcaoAtivada:
                    dicFuncoes[funcaoQueEstaSendoAnalisada] = [dicFuncoes[funcaoQueEstaSendoAnalisada][0],registradorLinhas]
                    funcaoAtivada = False

                else:
                    # Envia um bloco completo para ser executado
                    orquestradorDoInterpretador(registradorLinhas)

            registradorLinhas = ''
            contador += 1
            blocoDeCodigo = False

        # Se chegar no final do código, ou tiver um \n e um bloco não estiver sendo armazenaod
        if (((contador == len(linhas)) or (linhas[contador] == '\n')) ) and not blocoDeCodigo:

            if not registradorLinhas.isspace() and  registradorLinhas != '':

                # Inicie o interpretador da linha
                lerBloco = interpretador(registradorLinhas.strip())

                # Salva o resultado da ultima linha executada
                boolLinhaDeComando = lerBloco

                # Salva a linha que foi testada
                linhaComando = registradorLinhas.strip()

                if lerBloco[0] == False:
                    aconteceuUmErro = True
                    break

                if lerBloco[0] != False and (lerBloco[1] != None and "<class 'bool'>" not in str(type(lerBloco[1])) ):
                    # Insere no menu lateral
                    if len(str(lerBloco[1])) > len(":nessaLinha:"):

                        if str(lerBloco[1])[:len(":nessaLinha:")] == ":nessaLinha:":
                            tx_informacoes.insert(END, str(lerBloco[1][len(":nessaLinha:"):]))
                        else:
                            tx_informacoes.insert(END, str(lerBloco[1])+'\n')
                    else:
                        tx_informacoes.insert(END, str(lerBloco[1])+'\n')

                    tx_informacoes.see("end")
            registradorLinhas = ''
            contador += 1
            continue

        # Armazena o código de uma linha
        registradorLinhas += linhas[contador]
        contador += 1

    # Libera uma unidade no contador de Threads
    contadorThreads -= 1

# Interpreta um conjunto de linhas
def interpretador(codigo):
    global repetirAtivado
    global variaveis
    global funcaoRepita

    # Remove o modo repetir
    repetirAtivado = False
    funcaoRepita = 0

    # Se o código estiver vazio
    if (codigo == '' or codigo.isspace()):
        return ''

    else:

        # Obtem todas as linhas 
        linhas = codigo.split('\n')

        aleatorio        = ['número aleatório entre','número aleatorio entre','numero aleatório entre','numero aleatorio entre']
        mostreNessa      = ['mostre nessa linha ','exiba nessa linha ','escreva nessa linha ','imprima nessa linha ']
        mostre           = ['mostre ','exiba ','escreva ','print ','imprima ','escreva na tela ','display ']
        chamarFuncoes    = ['passando parametros ','parametros ','parametro ']
        declaraVariaveis = [' vale ',' recebe ',' = ']
        funcoes          = ['funcao ','function ']
        loopsss          = ['enquanto ','while ']
        aguarde          = ['espere ','aguarde ']
        repita           = ['repita ','repeat ']
        se               = ['se ','if ']

        entrada = ['recebe o que o usuario digitar','capture o que o usuario digitar','recebe o que for digitado','leia o que for digitado','input']
        vetor = ['vetor','crie uma lista chamada','lista']

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

            for comando in chamarFuncoes:
                if comando in linha:
                    print('Executar Função')
                    return funcaoExecutaFuncoes(linha,comando)

            for comando in repita:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return funcaoRepitir(linha[len(comando):])

            for comando in declaraVariaveis:
                if comando in linha:
                    return funcaoAtribuicao(linha,comando)

def funcaoRepitir(linha):
    global funcaoRepita

    linha = linha.replace('vezes','')
    linha = linha.replace('vez','')
    linha = linha.strip()

    linha = abstrairValoresDaLinhaInteira(linha)

    # Deu erro
    if linha[0] == False:
        return linha

    # É inteiro
    try:
        int(linha[1])
    except:
        return [False,"O valor precisa ser inteiro!"]
    else:
        funcaoRepita = int(linha[1])

        # Se for zero, não reproduza nenhuma vez
        if funcaoRepita == 0:
            return [True,False]
        return [True,True]

def funcaoNumeroAleatorio(linha):
    linha = linha.strip()
    if ' e ' in linha:
        num1, num2 = linha.split(' e ')
 
        num1 = abstrairValoresDaLinhaInteira(num1)
        num2 = abstrairValoresDaLinhaInteira(num2)

        # Se deu para obter o valor de ambos
        if num1[0] == False:
            # False e True embutido
            return num1

        if num2[0] == False:
            # False e True embutido
            return num2

        # Se são numéricos
        try:
            float(num1[1])
        except:
            return [False,"O valor 1 não é numérico"]

        try:
            float(num2[1])
        except:
            return [False,"O valor 2 não é numérico"]

        import random
        return [True,random.randint(num1[1],num2[1])]

    else:
        return [False,"Erro, você precisa definir o segundo valor!"]

def funcaoExecutaFuncoes(linha,comando):
    global dicFuncoes
    nomeDaFuncao, parametros = linha.split(comando)
    nomeDaFuncao = nomeDaFuncao.strip()
    parametros = parametros.strip()
    try:
        dicFuncoes[nomeDaFuncao]

    except:
        return [False,"Essa função não existe"]

    else:

        if ',' in parametros: # Se tiver multiplos parametros
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
            if len(dicFuncoes[nomeDaFuncao][0]) == 1:
                resultado = funcaoAtribuicao('{} recebe {} '.format(dicFuncoes[nomeDaFuncao][0],parametros),'recebe')

                if resultado[0] == False:
                    return resultado

        orquestradorDoInterpretador(dicFuncoes[nomeDaFuncao][1])
        return [True,None]

def funcaoDeclararFuncoes(linha):
    global funcaoAtivada
    global funcaoQueEstaSendoAnalisada

    print(linha)
    recebe = ['recebe parametros','recebe']

    for comando in recebe:
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
            return [True,True]

def funcaoExibicao(linha):
    codigo = linha.strip()
    return abstrairValoresDaLinhaInteira(codigo)

def funcaoExibicaoNessaLinha(linha):
    codigo = linha.strip()
    retorno = abstrairValoresDaLinhaInteira(codigo)
    if retorno[0] == False:
        return retorno
    return [retorno[0],':nessaLinha:'+str(retorno[1])]

def funcaoTempo(codigo):
    codigo = codigo.strip()

    tiposEspera = [' milisegundos',' milisegundo',' segundos',' segundo',' ms',' s']

    for comando in tiposEspera:
        if len(comando) < len(codigo):                                                      # Se o comando não estrapolar o código
            if comando == codigo[len(codigo)-len(comando):]:                                # Se o comando estiver no código
                resultado = abstrairValoresDaLinhaInteira(codigo[:len(codigo)-len(comando)])        # Tente obter o real valor no código
                if resultado != False:                                                      # Se foi possível obter
                    if comando == " segundos" or comando == " s" or comando == " segundo":  # Se está em segunso
                        time.sleep(resultado[1])                                               # Tempo em segundos
                        return [True,None]

                    elif comando == " milisegundos" or comando == " ms" or comando == "milisegundo": # Se está em milisegundos
                        time.sleep(resultado[1]/1000)                                   # Tempo em milisegundos
                        return [True,None]

                else:
                    return [False,'Erro ao obter um valor no tempo']

    return [True,None]

def fazerContas(linha):
    linha = str(linha)
    print("...",linha)
    # Do maior para o menor
    linha = linha.replace(' multiplicado por ',' * ')
    linha = linha.replace(' dividido por ',' / ')
    linha = linha.replace(' multiplique ', ' * ')
    linha = linha.replace(' elevado por ',' ** ')
    linha = linha.replace(' elevado ',' ** ')
    linha = linha.replace(' divide ',' / ')
    linha = linha.replace(' mais ',' + ')
    linha = linha.replace(' menos ', ' - ')

    if "'" in linha or '"' in linha:
        # Não mude esse texto
        print("CERTO")
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

    # Abstração de variáveis
    anterior = 0
    for valor in re.finditer(' ',linha):
        palavra = linha[anterior:valor.start()]
        palavra = palavra.strip()

        if palavra.isalnum() and palavra[0].isalpha():
            variavelDessaVez = obterValorDeUmaVariavel(palavra)
            if variavelDessaVez[0] == False:
                return variavelDessaVez
            linha = str(linha[:anterior]) + str(variavelDessaVez[1]) + str(linha[valor.start():]) 

        anterior = valor.end()

    # Tente fazer uma conta com isso
    try:
        resutadoFinal = eval(linha)
    except Exception as erro:
        return [False, "Não foi possivel realizar a conta |{}|".format(linha)]
    else:
        return [True, resutadoFinal]

def obterValorDeUmaVariavel(variavel):
    global variaveis

    variavel = variavel.replace('\n','')

    try:
        variaveis[variavel]
    except:
        return [False,'[erro] - variavel:{} não definida'.format(variavel)]
    else:
        return [True,variaveis[variavel]]

def abstrairValoresDaLinhaInteira(possivelVariavel):
    possivelVariavel = str(possivelVariavel).replace('\n','')
    possivelVariavel = possivelVariavel.strip()
    
    resultado = fazerContas(possivelVariavel)
    # Se deu erro, mas tem uma mensagem diferente do esperado
    if resultado[0] == False and resultado[1] != "Não foi possivel realizar a conta, porque não tem nenhum valor aqui. " and resultado[1] != "Isso é uma string":
        return resultado
    # Se deu certo
    elif resultado[0] == True:
        return resultado

    if '"' in possivelVariavel or "'" in possivelVariavel:
        return [True,possivelVariavel]

    try:
        float(possivelVariavel)
    except:
        resultado = obterValorDeUmaVariavel(possivelVariavel)
        return resultado # False/True já embutido
    else:
        return [True,float(possivelVariavel)]

def funcaoAtribuicao(linha,comando):
    print('linha: ',linha, ' comando ',comando)
    global variaveis

    variavel, valor = linha.split(comando)

    variavel = variavel.strip()
    valor    = valor.replace('\n','')
    valor    = valor.strip()
    print('variavel: ',variavel,' valor ',valor)

    resultado = fazerContas(valor)
    if resultado[0] == True:
        variaveis[variavel] = resultado[1]
        return [True,None]

    if resultado[0] == False and resultado[1] != "Não foi possivel realizar a conta, porque não tem nenhum valor aqui. " and resultado[1] != "Isso é uma string":
        print("NAÔ ERRo")
        return resultado

    if '"' in valor or "'" in valor: # é uma string
        variaveis[variavel] = valor
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
    # deix os maiores da esquerda para a direita
    condicoes = ['for maior ou igual a',
                 'for menor ou igual a',
                 'for diferente de',
                 'for maior que',
                 'for menor que',
                 'for igual a',
                 '==',
                 '>=',
                 '!=',
                 '<=',
                 '<',
                 '>']

    for condicao in condicoes:
        if condicao in linha:

            valor1, valor2 = linha.split(condicao)

            valor1 = abstrairValoresDaLinhaInteira(valor1)
            valor2 = abstrairValoresDaLinhaInteira(valor2)

            if valor1[0] == False:
                return valor1

            if valor2[0] == False:
                return valor2

            if condicao == "for maior que" or condicao == '>':
                return [True,valor1[1] > valor2[1]]

            elif condicao == "for menor que" or condicao == '<':
                return [True,valor1[1] < valor2[1]]

            elif condicao == "for igual a" or condicao == '==':
                return [True,valor1[1] == valor2[1]]

            elif condicao == "for maior ou igual a" or condicao == '>=':
                return [True,valor1[1] >= valor2[1]]

            elif condicao == "for menor ou igual a" or condicao == '<=':
                return [True,valor1[1] <= valor2[1]]

            elif condicao == "for diferente de" or comando == "!=":
                return [True,valor1[1] != valor2[1]]

    return [False,"Nenhuma condição foi atendida para: ".format(linha)]

def modoFullScreen(event=None):
    global boolTelaEmFullScreen

    if boolTelaEmFullScreen:
        boolTelaEmFullScreen = False
    else:
        boolTelaEmFullScreen = True

    tela.attributes("-fullscreen", boolTelaEmFullScreen)

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

def trocar_de_tela(fechar,carregar):
    fechar.grid_forget()
    carregar.grid(row=1,column=1,sticky=NSEW)

# =================================== INTERFACE GERAL =================================== #
fr_InPrincipal = Frame(tela,bg='#565656')
fr_InPrincipal.grid_columnconfigure(1,weight=1)
fr_InPrincipal.rowconfigure(1,weight=1)
 
def create_topExecutando():
    global tx_informacoes
    topExecutando = Toplevel(tela)
    topExecutando.grid_columnconfigure(1,weight=1)
    topExecutando.rowconfigure(1,weight=1)
    topExecutando.geometry("600x300+100+100")
    tx_informacoes = Text(topExecutando,design.tx_informacoes())
    #tx_informacoes.bind('<F6>', lambda event: proximaLinha(event))
    tx_informacoes.focus_force()
    tx_informacoes.grid(row=1,column=1,sticky=NSEW)

lb_linhas = Text(fr_InPrincipal,design.lb_linhas())
lb_linhas.insert('end',' 1\n')
lb_linhas.config(state=DISABLED,relief = SUNKEN,border= 0, highlightthickness=0)
# =================================== TELA DE CODIFICAÇÃO =================================== #
tx_codificacao = Text(fr_InPrincipal,design.tx_codificacao())
tx_codificacao.bind("<KeyRelease>",lambda tx_codificacao:sintaxeDasPalavras())
tx_codificacao.delete(1.0, END)

# =================================== SOBRE > DESENVOLVEDORES =================================== #
fr_sobDesenvol = Frame(tela)
fr_sobDesenvol.rowconfigure(1,weight=15)
fr_sobDesenvol.rowconfigure((2,3),weight=1)
fr_sobDesenvol.grid_columnconfigure(1,weight=2)

lb_sobDeTitulo = Label(fr_sobDesenvol, design.lb_sobDeTitulo(), text=" COMBRATEC ")
lb_sobDAutores = Label(fr_sobDesenvol, design.lb_sobDAutores(), text="Gabriel Gregório da Silva")
lb_sobDesenAno = Label(fr_sobDesenvol, design.lb_sobDesenAno(), text="2019")

lb_linhas.grid(row=1,column=0,sticky=NSEW)
tx_codificacao.grid(row=1,column=1,sticky=NSEW)
fr_InPrincipal.grid(row=1,column=1,sticky=NSEW)
lb_sobDeTitulo.grid(row=1,column=1,sticky=NSEW)
lb_sobDAutores.grid(row=2,column=1,sticky=NSEW)
lb_sobDesenAno.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
