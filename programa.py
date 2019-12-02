from tkinter import filedialog
from tkinter import *          
from funcoes import funcao
from design  import design
from design  import Sintaxe
from tkinter import messagebox
from threading import Thread

import tkinter.messagebox as tkmessagebox
import time

global contadorThreads                       # impede que o programa seja iniciado enquanto outro está sendo executado
global repetirAtivado                        # Se um comando de repetição tiver sido ativado 
global variaveis                             # Variáveis usadas durante a interpretação do programa

contadorThreads = 0                          # Conta quantas vezes o interpretador foi iniciado, e decrementa quando ele é finalizado
repetirAtivado = False                       # Define como falso
variaveis = {}                               # Variáveis usadas durante a interpretação do programa

def dialog_salvar():
    arquivo = filedialog.asksaveasfile(mode='w', defaultextension=".fyn",title = "Selecione o arquivo",filetypes = (("Meus projetos","*.fyn"),("all files","*.*")))

    if arquivo is None:
        return None

    text2save = str(tx_codificacao.get(1.0, END))
    arquivo.write(text2save)
    arquivo.close()

    return arquivo.name

def dialog_abrir():
    ftypes = [('Arquivos fyn', '*.fyn'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        print('arquivo {} escolhido'.format(filename))        
        arquivo = funcao.abrir_arquivo(filename) 

        if arquivo != None:
            tx_codificacao.delete(1.0, END)
            tx_codificacao.insert(END,arquivo)
    else:
        print('Nenhum arquivo escolhido')

def colorir_palavra(palavra,linha,valor1,valor2,cor):

    linha1 = '{}.{}'.format(linha , valor1) # linha.coluna(revisar)
    linha2 = '{}.{}'.format(linha , valor2) # linha.coluna(revisar)

    tx_codificacao.tag_add(palavra, linha1 , linha2) 
    tx_codificacao.tag_config(palavra, foreground = cor)

def sintaxe_linha(palavra,cor,frase,linha):
    quantidade_de_caracteres = len(frase)
    for caractere in range(len(frase)):
        if caractere+len(palavra) <= quantidade_de_caracteres:                 
            if frase[caractere:caractere+len(palavra)] == palavra:

                # Análisa se a palavra não está em outro contexto
                validacao = 0
                if caractere > 0:
                    if frase[caractere-1:caractere+len(palavra)] == ' '+palavra:
                        validacao += 1 
                else:
                        validacao += 1

                if caractere + len(palavra) < quantidade_de_caracteres:     
                    if frase[caractere:caractere+1+len(palavra)] == palavra+' ':
                        validacao += 1 
                else:
                        validacao += 1

                if validacao == 2:
                    colorir_palavra(palavra,linha,caractere,caractere + len(palavra),cor)

def sintaxe_linha_string(palavra,cor,frase,linha):
    evento_string = False
    save_position_evento = []        
    for caractere in range(len(frase)):

        if (frase[caractere] == '"' or frase[caractere] == "'") and evento_string == True:
            evento_string = False
            save_position_evento.append(caractere+1)
            colorir_palavra(palavra,linha,save_position_evento[0],save_position_evento[1],cor)
            save_position_evento = []

        elif frase[caractere] == '"' or frase[caractere] == "'":
            evento_string = True
            save_position_evento.append(caractere)

    if evento_string == True:
        tx_codificacao.tag_delete(palavra)
        colorir_palavra(palavra,linha,save_position_evento[0],len(frase),cor)

def sintaxe_linha_numerico(palavra,cor,frase,linha):
    for caractere in range(len(frase)):
        if frase[caractere].isnumeric():
            colorir_palavra(str(palavra),linha,caractere,caractere+1,cor)

def sintaxe_linha_comentario(palavra,cor,frase,linha):
    for caractere in range(len(frase)):
        if (frase[caractere:caractere+2] == '//') or (frase[caractere:caractere+1] == '#'):
            colorir_palavra(palavra,linha,caractere,len(frase),cor)

def sintaxe(palavra,cor,tx_codificacao):
    cor = cor['foreground']
    tx_codificacao.tag_delete(palavra)
    lista = tx_codificacao.get(1.0,END).split('\n')

    for linha in range(len(lista)):

        if palavra == '"':
            sintaxe_linha_string(palavra,cor,lista[linha],str(linha+1))

        elif palavra == "numerico":
            sintaxe_linha_numerico(palavra,cor,lista[linha],str(linha+1))        

        elif palavra == "comentario":
            sintaxe_linha_comentario(palavra,cor,lista[linha],str(linha+1))        

        else:
            sintaxe_linha(palavra,cor,lista[linha],str(linha+1))

def atualizar_sintaxe():
    sintaxe('numerico'                  , Sintaxe.numerico() ,tx_codificacao)

    # ATRIBUIÇÃO
    sintaxe('vale'                      , Sintaxe.atribuicao() ,tx_codificacao)
    sintaxe('recebe'                    , Sintaxe.atribuicao() ,tx_codificacao)

    # LOOPS  
    sintaxe('enquanto'                  , Sintaxe.lista() ,tx_codificacao)
    sintaxe('repita'                    , Sintaxe.lista() ,tx_codificacao)

    # ENTRADA
    sintaxe('oque o for digitado'       , Sintaxe.entrada() ,tx_codificacao)

    # LÓGICO
    sintaxe('ou'                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('e'                         , Sintaxe.logico() ,tx_codificacao)

    sintaxe('for diferente de'          , Sintaxe.logico() ,tx_codificacao)    
    sintaxe('for menor que'             , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for maior que'             , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for igual a'               , Sintaxe.logico() ,tx_codificacao)

    # CONDICIONAIS
    sintaxe('se'                        , Sintaxe.condicionais() ,tx_codificacao)
    sintaxe('senao'                     , Sintaxe.condicionais() ,tx_codificacao)

    # EXIBIÇÃO
    sintaxe('exiba'                     , Sintaxe.exibicao() ,tx_codificacao)
    sintaxe('mostre'                    , Sintaxe.exibicao() ,tx_codificacao)
    
    # STRINGS
    sintaxe('"'                         , Sintaxe.string() ,tx_codificacao)

    # COMENTÁRIO
    sintaxe('comentario'                , Sintaxe.comentario() ,tx_codificacao)

    # DELAY
    sintaxe('espere'                    , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('segundos'                  , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('milisegundos'              , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('s'                         , Sintaxe.tempo() ,tx_codificacao)


###########################################################################################################################

def iniciarInterpretador(event = None):
    global contadorThreads
    if contadorThreads != 0:                                   # Se algum programa já estiver rodando
        messagebox.showinfo("Alerta","Um programa está ativo nesse momento, Aguarde o outro programa se finalizado")
        return 0 # Não continue

    global variaveis 
    variaveis = {}                                             # Reinicia as variaveis do interpretador

    contadorThreads = 0                                        # Reinicia o contador de Threads

    tx_informacoes.delete('1.0',END)                           # Limpa o conteudo da tela lateral
    linhas = tx_codificacao.get('1.0',END)                     # Obtem o código do programa

    t = Thread(target=lambda valor = linhas: inter(valor))     # Define um Thread para iniciar o interpretadort
    t.start()                                                  # Inicia o interpretador em um Thread

    while  contadorThreads != 0:                               # Enquanto todos os Threads não forem finalizados
        tela.update()                                          # Atualize a tela

    tx_informacoes.insert(END, '\n [OK] finalizado')           # Informe que o programa foi finalizado


def inter(linhas):
    global contadorThreads
    global repetirAtivado

    contadorThreads += 1             # Aumenta para +1
    linhaComando = ''                # Reseta a linha de comando (enquanto x for menor que 6)

    contador = 0                     # contador para andar por todos os caracteres
    registradorLinhas = ''           # Armazena blocos de código
    blocoDeCodigo = False            # Bloco de código entre chaves
    penetracao = 0                   # Penetracao dos {
    lerBloco = False                 # Ler um bloco de código

    while contador < len(linhas):                                               # Andar por todo o código
        if linhas[contador] == '{' and blocoDeCodigo == False:                  # Se começar um bloco e não tiver começado nenhum
            penetracao +=1                                                      # penetração de chaves aumentada {{{}}}
            if not registradorLinhas.isspace() and  registradorLinhas != '':    # Se não tiver espaço e nem for vazio
                lerBloco = interpretar(registradorLinhas.strip())               # Inicie o interpretador da linha

                if str(type(lerBloco))!= "<class 'bool'>":                      # se for diferente de verdadeiro ou false
                    tx_informacoes.insert(END, str(lerBloco)+'\n')              # Insere no menu lateral

            registradorLinhas = ''                                              # Recomeçar o registrador
            contador += 1                                                       # Incrementar o contador
            blocoDeCodigo = True                                                # Começar a salvar o bloco de código
            continue                                                            # Ir para o próximo loop
 
        if linhas[contador] == '{':                                             # Se encontrar mais um nível de profundidade de blobo
            penetracao +=1                                                      # Penetração de chaves aumentada {{{}}}

        if linhas[contador] == '}':                                             # Se um bloco ser finalizado
            penetracao -=1                                                      # Penetração de chaves diminuida {{{}}}

        if linhas[contador] == '}' and blocoDeCodigo and penetracao == 0:       # Se o bloco principal finalizar

            if lerBloco == True:                                                # Se a condição for verdadeira
                print(linhaComando,registradorLinhas,repetirAtivado) 
                if repetirAtivado:                                              # Se o modo de repetição estiver ativo
                    
                    while boolLinhaDeComando:                                   # Enquanto a condição for verdadeira
                        inter(registradorLinhas)                                # Envia um bloco completo de forma recursiva {comandos1 comando2}
                        boolLinhaDeComando = interpretar(linhaComando)          # Testa a condição novamente
                else:
                        inter(registradorLinhas)                                # Envia um bloco completo de forma recursiva {comandos1 comando2}
 
            registradorLinhas = ''                                              # Armazena cada caractere em análise 
            contador += 1                                                       # Aumenta o contador
            blocoDeCodigo = False                                               # Não estamos buscando um bloco de código

        if (((contador == len(linhas)) or (linhas[contador] == '\n')) ) and not blocoDeCodigo:
            if not registradorLinhas.isspace() and  registradorLinhas != '':    # Se não tiver espaço e nem for vazio
                lerBloco = interpretar(registradorLinhas.strip())               # Inicie o interpretador da linha
                boolLinhaDeComando = lerBloco
                linhaComando = registradorLinhas.strip()                        # Salva a linha que foi testada

                if str(type(lerBloco))!= "<class 'bool'>" and lerBloco != None: # Se for diferente de verdadeiro ou false
                    tx_informacoes.insert(END, str(lerBloco)+'\n' )             # Insere no menu lateral 2
            registradorLinhas = ''                                              # Armazena cada caractere em análise 
            contador += 1                                                       # Aumenta o contador
            continue                                                            # Volta ao loop para a próxima posição

        registradorLinhas += linhas[contador]                                   # Armazena cada caractere em análise 
        contador += 1                                                           # Aumenta o contador

    contadorThreads -= 1                                                        # Libera uma unidade no contador de Threads

# Interpreta um conjunto de linhas
def interpretar(codigo):
    global repetirAtivado
    global variaveis

    repetirAtivado = False                          # Remove o modo repetir

    if (codigo == '' or codigo.isspace()):          # Se o código estiver vazio
        return ''

    else:
        linhas = codigo.split('\n')                 # Obtem todas as linhas 

        mostre = ['mostre','exiba']  
        for linha in linhas:
            for comando in mostre:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return exibicao(linha[len(comando):])

        se = ['se']
        for linha in linhas:
            for comando in se:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return condicional(linha[len(comando):])

        loopsss = ['enquanto']
        for linha in linhas:
            for comando in loopsss:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return loopsFunction(linha[len(comando):])

        declaraVariaveis = [' vale ',' recebe ']
        for linha in linhas:
            for comando in declaraVariaveis:
                if comando in linha:
                    return atribuicao(linha,comando)

        aguarde = ['espere','aguarde']
        for linha in linhas:
            for comando in aguarde:
                if len(comando) < len(linha):
                    if comando == linha[0:len(comando)]:
                       return tempo(linha[len(comando):])

def tempo(codigo):
    codigo = codigo.strip()

    # Como segundos está incluido dento de milisegundos, use o maior primeiro
    tiposEspera = [' milisegundos',' segundos']
    for comando in tiposEspera:
        if len(comando) < len(codigo):                                               # Se o comando não estrapolar o código
            if comando == codigo[len(codigo)-len(comando):]:                         # Se o comando estiver no código
                resultado = abstrairValorVariavel(codigo[:len(codigo)-len(comando)]) # Tente obter o real valor no código
                if resultado != False:                                               # Se foi possível obter
                    if comando == " segundos":                                       # Se está em segunso
                        time.sleep(resultado)                                        # Tempo em segundos

                    elif comando == " milisegundos":                                 # Se está em milisegundos
                        time.sleep(resultado/1000)                                   # Tempo em milisegundos
                else:
                    print('Erro ao obter um valor no tempo')
                    return False

    return True

def obterValor(variavel):                                  # obter o valor de uma variável
    global variaveis

    variavel = variavel.replace('\n','')

    print(variavel,'><',variaveis)

    try:
        variaveis[variavel]
    except:
        return '[erro] - variavel não definida'
    else:
        return variaveis[variavel]

def abstrairValorVariavel(possivelVariavel):
    possivelVariavel = str(possivelVariavel)
    possivelVariavel = possivelVariavel.replace('\n','')
    possivelVariavel = possivelVariavel.strip()

    contas = [' mais ',' menos ']
    for conta in contas:
        if conta in possivelVariavel:
            valor1,valor2 = possivelVariavel.split(comando)
            valor1 = abstrairValorVariavel(valor1)
            valor2 = abstrairValorVariavel(valor2)

            if conta == ' mais ':
                return (float(valor1)+float(valor2))

            elif conta == ' menos ':
                return (float(valor1)-float(valor2))


    if '"' in possivelVariavel or "'" in possivelVariavel: # é uma string
        return possivelVariavel

    elif possivelVariavel.isnumeric():
        return float(possivelVariavel)

    else:
        resultado = obterValor(possivelVariavel)
        print(resultado)

        if '[erro]' in str(resultado):
            print('Erro de variavel')
            return False

        return resultado

def atribuicao(linha,comando):
    global variaveis

    variavel, valor = linha.split(comando)
    print(linha,comando,variaveis)

    valor = valor.replace('\n','')
    variavel = variavel.strip()
    valor = valor.strip()

    contas = [' mais ',' menos ']
    for conta in contas:
        if conta in valor:
            valor1 , valor2 = valor.split(conta)
            valor1 = abstrairValorVariavel(str(valor1))
            valor2 = abstrairValorVariavel(str(valor2))

            if conta == ' mais ':
                variaveis[variavel] = float(valor1)+float(valor2)

            elif conta == ' menos ':
                variaveis[variavel] =  float(valor1)-float(valor2)
            else:
                return False
            return True

    if '"' in valor or "'" in valor: # é uma string
        variaveis[variavel] = valor

    elif valor.isnumeric():
        variaveis[variavel] = float(valor)

    else: # é uma variavel
        resultado = obterValor(valor)
        if '[erro]' in str(resultado): # Se encontrar um erro
            print('Erro ao declaraVariaveis')
            return False

        variaveis[variavel] = resultado
    print("variavel declaradas ", variaveis)
    return True

def exibicao(linha):
    codigo = linha.strip()
    resultado = abstrairValorVariavel(codigo)
    return resultado

def loopsFunction(linha):
    global repetirAtivado
    repetirAtivado = True

    condicoes = ['for maior que','for menor que','for igual a','for diferente de']
    for condicao in condicoes:
        if condicao in linha:

            valo1, valo2 = linha.split(condicao)

            valo1 = abstrairValorVariavel(valo1)
            valo2 = abstrairValorVariavel(valo2)

            if condicao == "for maior que":
                return valo1 > valo2

            elif condicao == "for menor que":
                return valo1 < valo2

            elif condicao == "for igual a":
                return valo1 == valo2

            elif condicao == "for diferente de":
                return valo1 != valo2
            else:
                print('Erro nas condicoes')

def condicional(linha):
    condicoes = ['for maior que','for menor que','for igual a','for diferente de']
    for condicao in condicoes:
        if condicao in linha:

            valo1, valo2 = linha.split(condicao)

            valo1 = abstrairValorVariavel(valo1)
            valo2 = abstrairValorVariavel(valo2)

            if condicao == "for maior que":
                return valo1 > valo2

            elif condicao == "for menor que":
                return valo1 < valo2

            elif condicao == "for igual a":
                return valo1 == valo2

            elif condicao == "for diferente de":
                return valo1 != valo2
            else:
                print('Erro nas condicoes')

tela = Tk()
tela.bind('<F5>',lambda event: iniciarInterpretador(event))
tela.title('Linguagem feynman beta 0.4')
tela.configure(bg='#343434')
tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)

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
menu_arquivo.add_command(label='Abrir arquivo (Ctrl+O)',command=dialog_abrir)
menu_arquivo.add_command(label='Nova Guia (Ctrl-N)')
menu_arquivo.add_command(label='Abrir pasta')
menu_arquivo.add_command(label='Recentes')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Salvar (Ctrl-S)',)
menu_arquivo.add_command(label='Salvar Como (Ctrl-Shift-S)',command=dialog_salvar)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='imprimir (Ctrl-P)')
menu_arquivo.add_command(label='Exportar (Ctrl-E)')
menu_arquivo.add_command(label='Enviar por e-mail ')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair (Alt-F4)')

# =================================== EXECUTAR =================================== #
menu_executar.add_command(label='Executar Tudo (F5)',command=iniciarInterpretador)
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
fr_InPrincipal = Frame(tela)
fr_InPrincipal.grid_columnconfigure((0,1),weight=2)
fr_InPrincipal.grid_columnconfigure(1,weight=2)
fr_InPrincipal.rowconfigure(1,weight=1)

# =================================== TELA DE LOGS =================================== #
tx_informacoes = Text(fr_InPrincipal,design.tx_informacoes())

# =================================== TELA DE CODIFICAÇÃO =================================== #
tx_codificacao = Text(fr_InPrincipal,design.tx_codificacao())

tx_codificacao.bind("<KeyRelease>",lambda tx_codificacao:atualizar_sintaxe())
tx_codificacao.delete(1.0, END)

# =================================== SOBRE > DESENVOLVEDORES =================================== #
fr_sobDesenvol = Frame(tela)
fr_sobDesenvol.rowconfigure(1,weight=15)
fr_sobDesenvol.rowconfigure((2,3),weight=1)
fr_sobDesenvol.grid_columnconfigure(1,weight=2)

lb_sobDeTitulo = Label(fr_sobDesenvol, design.lb_sobDeTitulo(), text=" COMBRATEC ")
lb_sobDAutores = Label(fr_sobDesenvol, design.lb_sobDAutores(), text="Gabriel Gregório da Silva")
lb_sobDesenAno = Label(fr_sobDesenvol, design.lb_sobDesenAno(), text="2019")

tx_informacoes.grid(row=1,column=0,sticky=NSEW)
tx_codificacao.grid(row=1,column=1,sticky=NSEW)
fr_InPrincipal.grid(row=1,column=1,sticky=NSEW)
lb_sobDeTitulo.grid(row=1,column=1,sticky=NSEW)
lb_sobDAutores.grid(row=2,column=1,sticky=NSEW)
lb_sobDesenAno.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
