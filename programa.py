from tkinter import filedialog
from tkinter import *          
from funcoes import funcao
from design import design
from design import Sintaxe
import tkinter.messagebox as tkmessagebox

def dialog_salvar():
    arquivo = filedialog.asksaveasfile(mode='w', defaultextension=".ec",title = "Selecione o arquivo",filetypes = (("Meus projetos","*.ec"),("all files","*.*")))

    if arquivo is None:
        return None

    text2save = str(tx_codificacao.get(1.0, END))
    arquivo.write(text2save)
    arquivo.close()

    return arquivo.name

def dialog_abrir():
    ftypes = [('Arquivos ec', '*.ec'), ('Todos os arquivos', '*')]
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

    linha1 = '{}.{}'.format(linha , valor1)
    linha2 = '{}.{}'.format(linha , valor2)

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

        if frase[caractere] == '"' and evento_string == True:
            evento_string = False
            save_position_evento.append(caractere+1)
            colorir_palavra(palavra,linha,save_position_evento[0],save_position_evento[1],cor)
            save_position_evento = []

        elif frase[caractere] == '"':
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
    sintaxe('percorra '                 , Sintaxe.lista() ,tx_codificacao)
    sintaxe('a lista'                   , Sintaxe.lista() ,tx_codificacao)

    # VETORES
    sintaxe('recebe uma lista'          , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('com os intens'             , Sintaxe.vetor() ,tx_codificacao)

    # ENTRADA
    sintaxe('oque o for digitado'       , Sintaxe.entrada() ,tx_codificacao)

    # CONTAS
    sintaxe('por'                       , Sintaxe.contas() ,tx_codificacao)

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

    sintaxe('recebe parametro'          , Sintaxe.parametro() ,tx_codificacao)
    sintaxe('recebe parametros'         , Sintaxe.parametro() ,tx_codificacao)

    # EXIBIÇÃO
    sintaxe('exiba nessa linha'         , Sintaxe.exibicao() ,tx_codificacao)
    sintaxe('exiba'                     , Sintaxe.exibicao() ,tx_codificacao)
 
    # DELAY
    sintaxe('espere'                    , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('segundos'                  , Sintaxe.tempo() ,tx_codificacao)
    
    # STRINGS
    sintaxe('"'                         , Sintaxe.string() ,tx_codificacao)

    # COMENTÁRIO
    sintaxe('comentario'                , Sintaxe.comentario() ,tx_codificacao)


###########################################################################################################################
global variaveis
variaveis = {}
# variavel : valor. Ambas tem que ser strings

# Define uma variavel
def definirValorVariavel(linha):
    # print(definirValorVariavel('gabriela vale 13'))
    lista = linha.split(' ')

    variavelADefinir = lista[0]
    valor = lista[-1]    
    atribuicao = ' '
    for palavra in lista[1:-1]:
        atribuicao += palavra + ' '

    if (atribuicao == ' vale '):
        global variaveis
        variaveis[variavelADefinir] = valor
        return True

    return [None, "ERRO: Você digitou uma atribuição que não existe:{}:".format(atribuicao)]

# Obter o valor de uma variável
def extrairValorVariavel(string):
    # É um número
    if string.isnumeric():
        return string

    # É uma string
    if ((string[0] == '"') and(string[-1] == '"')):
        return string

    global variaveis
    for k,v in variaveis.items():
        if k == string:
            return extrairValorVariavel(v)

    return [None, "ERRO: A variável: {} Não foi definida".format(string)]

# Testa uma condicional e retorna True ou False
def condicional(linha):
    # condicional('se var1 for diferente de 15')
    lista = linha.split(' ')

    if lista[0] == 'se':
        print(lista,'>>>>>>>')
        valor1 = extrairValorVariavel(lista[1])
        valor2 = extrairValorVariavel(lista[-1])

        if valor1[0] == None:
            return valor1[1]

        if valor2[0] == None:
            return valor2[1]

        condicao = ' '
        for palavra in lista[2:-1]:
            condicao += palavra + ' '

        if condicao == ' for diferente de ':      
            if valor1 != valor2:
                return True
            else:
                return False

        elif condicao == ' for menor que ':
            if valor1 < valor2:
                return True
            else:
                return False

        elif condicao == ' for maior que ':
            if valor1 > valor2:
                return True
            else:
                return False

        elif condicao == ' for igual a ':
            if valor1 == valor2:
                return True
            else:
                return False

        return [None, "ERRO: Você digitou uma condição que não existe:{}:".format(condicao)]
###########################################################################################################################

def iniciarInterpretador(event = None):
    programa = tx_codificacao.get("1.0",END)
    programa = programa.strip()
    lista = programa.split('\n')

    for linha in range(len(lista)):

        lista_linha = lista[linha].split(' ')

        if (len(lista_linha) < 1):
            continue

        if (lista[linha][0:3] == 'se '):
            print(lista[linha])
            tx_informacoes.insert(END, condicional(lista[linha]))

        elif (lista_linha[1] == 'vale'):
            print(lista[linha])
            tx_informacoes.insert(END, definirValorVariavel(lista[linha]))

tela = Tk()
tela.bind('<F5>',lambda event: iniciarInterpretador(event))
tela.title('Linguagem ec beta 0.3')
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
