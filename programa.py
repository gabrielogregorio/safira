from tkinter import filedialog
from tkinter import *          
from funcoes import funcao
from design import design
from design import Sintaxe
import tkinter.messagebox as tkmessagebox

pressed_f4 = False
def EXIT():
	result = tkmessagebox.askquestion('Deseja sair?')
	if result == 'yes':
		tela.destroy()
		exit()

def alt_f4():
	global pressed_f4
	pressed_f4 = True		

def dialog_salvar():
    arquivo = filedialog.asksaveasfile(mode='w', defaultextension=".ec",title = "Selecione o arquivo",filetypes = (("Meus projetos","*.ec"),("all files","*.*")))

    if arquivo is None:
        print('Operação salvar como cancelada.')
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
    sintaxe('é igual a'                 , Sintaxe.atribuicao() ,tx_codificacao)
    sintaxe('='                         , Sintaxe.atribuicao() ,tx_codificacao)
    sintaxe('<-'                        , Sintaxe.atribuicao() ,tx_codificacao)

    # LOOPS  
    sintaxe('lista'                     , Sintaxe.lista() ,tx_codificacao)
    sintaxe('a lista'                   , Sintaxe.lista() ,tx_codificacao)

    sintaxe('vetor'                     , Sintaxe.lista() ,tx_codificacao)
    sintaxe('o vetor'                   , Sintaxe.lista() ,tx_codificacao)

    sintaxe('o array'                   , Sintaxe.lista() ,tx_codificacao)
    sintaxe('array'                     , Sintaxe.lista() ,tx_codificacao)

    # VETORES
    sintaxe('recebe uma lista'          , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('recebe um vetor'           , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('com os intens'             , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('com os valores'            , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('* '                        , Sintaxe.vetor() ,tx_codificacao)
    sintaxe('- '                        , Sintaxe.vetor() ,tx_codificacao)

    # ENTRADA
    sintaxe('oque o usuario digitar'    , Sintaxe.entrada() ,tx_codificacao)
    sintaxe('oque a pessoa digitar'     , Sintaxe.entrada() ,tx_codificacao) 
    sintaxe('oque o for digitado'       , Sintaxe.entrada() ,tx_codificacao)
    sintaxe('numero digitado'           , Sintaxe.entrada() ,tx_codificacao)
    sintaxe('string digitada'           , Sintaxe.entrada() ,tx_codificacao)
    sintaxe('caracter digitado'         , Sintaxe.entrada() ,tx_codificacao)

    # CONTAS
    sintaxe('por'                       , Sintaxe.contas() ,tx_codificacao)

    sintaxe('+'                         , Sintaxe.contas() ,tx_codificacao)
    sintaxe('mais'                      , Sintaxe.contas() ,tx_codificacao)

    sintaxe('-'                         , Sintaxe.contas() ,tx_codificacao)
    sintaxe('menos'                     , Sintaxe.contas() ,tx_codificacao)

    sintaxe('/'                         , Sintaxe.contas() ,tx_codificacao)
    sintaxe('dividido por'              , Sintaxe.contas() ,tx_codificacao)

    sintaxe('//'                        , Sintaxe.contas() ,tx_codificacao)
    sintaxe('resto de'                  , Sintaxe.contas() ,tx_codificacao)

    sintaxe('*'                         , Sintaxe.contas() ,tx_codificacao)
    sintaxe('multiplicado por'          , Sintaxe.contas() ,tx_codificacao)

    sintaxe('**'                        , Sintaxe.contas() ,tx_codificacao)
    sintaxe('elevado a'                 , Sintaxe.contas() ,tx_codificacao)

    sintaxe('mean'                      , Sintaxe.contas() ,tx_codificacao)
    sintaxe('média de'                  , Sintaxe.contas() ,tx_codificacao)
    sintaxe('a média de'                , Sintaxe.contas() ,tx_codificacao)
    sintaxe('média ponderada de'        , Sintaxe.contas() ,tx_codificacao)
    sintaxe('a média ponderada de'      , Sintaxe.contas() ,tx_codificacao)

    sintaxe('max'                       , Sintaxe.contas() ,tx_codificacao)
    sintaxe('maior elemento'            , Sintaxe.contas() ,tx_codificacao)
    sintaxe('maior valor'               , Sintaxe.contas() ,tx_codificacao)

    sintaxe('min'                       , Sintaxe.contas() ,tx_codificacao)
    sintaxe('menor elemento'            , Sintaxe.contas() ,tx_codificacao)
    sintaxe('menor valor'               , Sintaxe.contas() ,tx_codificacao)

    # LÓGICO
    sintaxe('||'                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('or'                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('ou'                        , Sintaxe.logico() ,tx_codificacao)

    sintaxe('&&'                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('and'                       , Sintaxe.logico() ,tx_codificacao)
    sintaxe('e'                         , Sintaxe.logico() ,tx_codificacao)

    sintaxe('!='                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for diferente de'          , Sintaxe.logico() ,tx_codificacao)

    sintaxe('<'                         , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for menor que'             , Sintaxe.logico() ,tx_codificacao)

    sintaxe('>'                         , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for maior que'             , Sintaxe.logico() ,tx_codificacao)

    sintaxe('=='                        , Sintaxe.logico() ,tx_codificacao)
    sintaxe('for igual a'               , Sintaxe.logico() ,tx_codificacao)

    # CONDICIONAIS
    sintaxe('se'                        , Sintaxe.condicionais() ,tx_codificacao)
    sintaxe('if'                        , Sintaxe.condicionais() ,tx_codificacao)

    sintaxe('senao'                     , Sintaxe.condicionais() ,tx_codificacao)
    sintaxe('else'                      , Sintaxe.condicionais() ,tx_codificacao)

    # MÉTODOS
    sintaxe('método'                    , Sintaxe.metodo() ,tx_codificacao)
    sintaxe('function'                  , Sintaxe.metodo() ,tx_codificacao)
    sintaxe('def'                       , Sintaxe.metodo() ,tx_codificacao)

    sintaxe('recebe parametro'          , Sintaxe.parametro() ,tx_codificacao)
    sintaxe('recebe parametros'         , Sintaxe.parametro() ,tx_codificacao)

    # EXIBIÇÃO
    sintaxe('exiba nessa linha'         , Sintaxe.exibicao() ,tx_codificacao)
    sintaxe('exiba'                     , Sintaxe.exibicao() ,tx_codificacao)
    sintaxe('mostre nessa linha'        , Sintaxe.exibicao() ,tx_codificacao)
    sintaxe('mostre'                    , Sintaxe.exibicao() ,tx_codificacao)

    # ENTRADA DE DADOS
    sintaxe('digitado'                  , Sintaxe.condicionais() ,tx_codificacao)
    sintaxe('tiver'                     , Sintaxe.condicionais() ,tx_codificacao)
    sintaxe('em'                        , Sintaxe.condicionais() ,tx_codificacao)
 
    # DELAY
    sintaxe('espere'                    , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('segundos'                  , Sintaxe.tempo() ,tx_codificacao)
    sintaxe('s'                         , Sintaxe.tempo() ,tx_codificacao)
    
    # ALEATÓRIO
    sintaxe('número aleatório entre'    , Sintaxe.aleatorio() ,tx_codificacao)

    # COLORAÇÃO
    sintaxe('na cor'                    , Sintaxe.atribuicao() ,tx_codificacao)
    sintaxe('azul'                      , Sintaxe.azul()  ,tx_codificacao)
    sintaxe('roxo'                      , Sintaxe.roxo()  ,tx_codificacao)
    sintaxe('verde'                     , Sintaxe.verde() ,tx_codificacao)
    
    # STRINGS
    sintaxe('"'                         , Sintaxe.string() ,tx_codificacao)

    # COMENTÁRIO
    sintaxe('comentario'                , Sintaxe.comentario() ,tx_codificacao)

tela = Tk()
tela.title('Linguagem ec beta 0.3')
tela.configure(bg='#343434')
tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)
tela.config(menu=menu_barra)

menu_barra = Menu(tela,design.cor_menu())

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
menu_arquivo.add_command(label='Sair (Alt-F4)',command=EXIT)

# =================================== EXECUTAR =================================== #
menu_executar.add_command(label='Executar Tudo (F5)')
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

lb_sobDeTitulo = Label(fr_sobDesenvol, design.lb_sobDeTitulo() ,text=" COMBRATEC ")
lb_sobDAutores = Label(fr_sobDesenvol, design.lb_sobDAutores() ,text="Gabriel Gregório da Silva")
lb_sobDesenAno = Label(fr_sobDesenvol, design.lb_sobDesenAno() ,text="2019")

tx_informacoes.grid(row=1,column=0,sticky=NSEW)
tx_codificacao.grid(row=1,column=1,sticky=NSEW)
fr_InPrincipal.grid(row=1,column=1,sticky=NSEW)
lb_sobDeTitulo.grid(row=1,column=1,sticky=NSEW)
lb_sobDAutores.grid(row=2,column=1,sticky=NSEW)
lb_sobDesenAno.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
