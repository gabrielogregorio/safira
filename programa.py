from tkinter import filedialog
from tkinter import *          
import os
from funcoes import funcao
from design import design
#from PIL import ImageTk, Image # Icone
#tela.call('wm', 'iconphoto', tela._w, ImageTk.PhotoImage(Image.open('icone.gif')))

global aconteceu   # Caso o print(' para colocar ')
aconteceu = [False,'']

def dialog_salvar_como_arquivo():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".ec",title = "Selecione o arquivo",filetypes = (("Meus projetos","*.ec"),("all files","*.*")))

    if file is None:
        print('Operação salvar como cancelada.')
        return

    # Captura o texto o programa escrito
    text2save = str(txTelaProgramacao.get(1.0, END))
    file.write(text2save)
    file.close()

    print(file.name)

def dialog_abrir_arquivo():
    ftypes = [('Arquivos ec', '*.ec'), ('Todos os arquivos', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    filename = dlg.show()

    if filename != ():
        print('arquivo {} escolhido'.format(filename))        
        arquivo = funcao.abrir_arquivo(filename) 

        if arquivo != None:
            txTelaProgramacao.delete(1.0, END)
            txTelaProgramacao.insert(END,arquivo)
    else:
        print('Nenhum arquivo escolhido')

def sintaxe_linha(palavra,cor,frase,linha):
    conteudo = frase
    if palavra in frase:

        linha1 = str(linha) + str('.') + str(conteudo.find(palavra))
        linha2 = str(linha) + str('.') + str(conteudo.find(palavra) + len(palavra))

        txTelaProgramacao.tag_add(palavra, linha1 , linha2)        
        txTelaProgramacao.tag_config(palavra,foreground = cor)

def sintaxe(palavra,cor,txTelaProgramacao):
    lista = txTelaProgramacao.get(1.0,END).split('\n')
    for linha in range(len(lista)):
        sintaxe_linha(palavra,cor,lista[linha],str(linha+1))

def atualizar_sintaxe():
    sintaxe('vale','orange',txTelaProgramacao)
    sintaxe('recebe','orange',txTelaProgramacao)
    sintaxe('é igual a','orange',txTelaProgramacao)

    sintaxe('enquanto','#fe468a',txTelaProgramacao)
    sintaxe(' e ',     '#f9264a',txTelaProgramacao)
    sintaxe(' ou ',    '#f9264a',txTelaProgramacao)
  
    sintaxe('for diferente de', '#66d9ef',txTelaProgramacao)
    sintaxe('for menor que'   , '#66d9ef',txTelaProgramacao)
    sintaxe('for maior que'   , '#66d9ef',txTelaProgramacao)
    sintaxe('for igual a'     , '#66d9ef',txTelaProgramacao)

    sintaxe('exiba nessa linha',  '#22ee22',txTelaProgramacao)
    sintaxe('exiba',              '#22ee22',txTelaProgramacao)
    sintaxe('mostre nessa linha ','#22ee22',txTelaProgramacao)
    sintaxe('mostre',             '#22ee22',txTelaProgramacao)

    sintaxe('senao','#e2d872',txTelaProgramacao)
    sintaxe('se','#e2d872',txTelaProgramacao)
    sintaxe('digitado','#e2d872',txTelaProgramacao)

    sintaxe('espere','#fc00ff',txTelaProgramacao)
    sintaxe('segundos','#fc00ff',txTelaProgramacao)

tela = Tk()
tela.title('Linguagem ec beta 0.2')
tela.configure(bg='#343434')

tela.grid_columnconfigure(1,weight=1)
tela.rowconfigure(1,weight=1)

menubar = Menu(tela,design.cor_menu())
tela.config(menu=menubar)

menu_arquivo     = Menu(menubar,design.cor_menu())
menu_executar    = Menu(menubar,design.cor_menu())
menu_localizar   = Menu(menubar,design.cor_menu())
menu_editar      = Menu(menubar,design.cor_menu())
menu_ferramentas = Menu(menubar,design.cor_menu())
menu_interface   = Menu(menubar,design.cor_menu())
menu_ajuda       = Menu(menubar,design.cor_menu())
menu_sobre       = Menu(menubar,design.cor_menu())

menubar.add_cascade(label='Arquivo'   , menu=menu_arquivo)
menubar.add_cascade(label='Executar'  , menu=menu_executar)
menubar.add_cascade(label='Localizar' , menu=menu_localizar)
menubar.add_cascade(label='Editar'    , menu=menu_editar)
menubar.add_cascade(label='Interface' , menu=menu_interface)
menubar.add_cascade(label='Ajuda'     , menu=menu_ajuda)
menubar.add_cascade(label='sobre'     , menu=menu_sobre)

############################### ARQUIVO #######################################
menu_arquivo.add_command(label='Abrir arquivo (Ctrl+O)',command=dialog_abrir_arquivo)
menu_arquivo.add_command(label='Nova Guia (Ctrl-N)')
menu_arquivo.add_command(label='Abrir pasta')
menu_arquivo.add_command(label='Recentes')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Salvar (Ctrl-S)',)
menu_arquivo.add_command(label='Salvar Como (Ctrl-Shift-S)',command=dialog_salvar_como_arquivo)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='imprimir (Ctrl-P)')
menu_arquivo.add_command(label='Exportar (Ctrl-E)')
menu_arquivo.add_command(label='Enviar por e-mail ')
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair (Alt-F4)')

############################### EXECUTAR #######################################
menu_executar.add_command(label='Executar Tudo (F5)')
menu_executar.add_command(label='Executar linha (F6)')
menu_executar.add_command(label='Executar até breakpoint (F7)')
menu_executar.add_command(label='Executar com delay (F8)')
menu_executar.add_command(label='Parar execução (F9)')
menu_executar.add_command(label='Inserir breakpoint (F10)')

############################### LOCALIZAR #######################################
menu_localizar.add_command(label='Localizar (CTRL + F)')
menu_localizar.add_command(label='Substituir (CTRL + R)')

############################### EDITAR #######################################
menu_editar.add_command(label='copiar (CTRL + C)')
menu_editar.add_command(label='cortar (CTRL + X)')
menu_editar.add_command(label='colar (CTRL + V)')
menu_editar.add_command(label='desfazer (CTRL + Z)')
menu_editar.add_command(label='refazer (CTRL + Y)')
menu_editar.add_command(label='selecionar tudo (CTRL + A)')
    
############################### FERRAMENTAS #######################################
menu_ferramentas.add_command(label='corrigir identação')
menu_ferramentas.add_command(label='Numero de espaços para o tab')

############################### INTERFACE #######################################
menu_interface.add_command(label='temas')
menu_interface.add_command(label='fonte')

############################### Ajuda #######################################
menu_ajuda.add_command(label='Ajuda (F1)')
menu_ajuda.add_command(label='Comandos Disponíveis')
menu_ajuda.add_command(label='Comunidade')

############################### Sobre #######################################
menu_sobre.add_command(label='Projeto')
menu_sobre.add_command(label='Desenvolvedores',command=lambda:trocar_de_tela(frTelaPrincipal,frConfig))

def trocar_de_tela(fechar,carregar):
    fechar.grid_forget()
    carregar.grid(row=1,column=1,sticky=NSEW)

# INTERFACE GERAL
frTelaPrincipal = Frame(tela)
frTelaPrincipal.grid_columnconfigure((0,1),weight=2)
frTelaPrincipal.rowconfigure(1,weight=1)

# TELA DE LOGS
txTelaLogs = Text(frTelaPrincipal,width=40,bg='#343434',fg='#ffffff',font=('',15))

# TELA DE CODIFICAÇÃO
txTelaProgramacao = Text(frTelaPrincipal,bg='#343434',fg='#ffffff',font=('',15))
txTelaProgramacao.bind("<Key>",lambda txTelaProgramacao:atualizar_sintaxe())
txTelaProgramacao.delete(1.0, END)

txTelaLogs.grid(row=1,column=0,sticky=NSEW)


#SOBRE>DESENVOLVEDORES
frConfig = Frame(tela)
frConfig.rowconfigure(1,weight=15)
frConfig.rowconfigure((2,3),weight=1)
frConfig.grid_columnconfigure(1,weight=2)

titulo = Label(frConfig,text=" combratec ",font=("Arial",70,"bold"),height=5,bg='#343434',fg='#ffffff')
autores= Label(frConfig,text="Gabriel Gregório da Silva",font=("Arial",15),bg='#343434',fg='#ffffff')
ano    = Label(frConfig,text="2019",font=("Arial",10),bg='#343434',fg='#ffffff')

txTelaProgramacao.grid(row=1,column=1,sticky=NSEW)
frTelaPrincipal.grid(row=1,column=1,sticky=NSEW)
titulo.grid(row=1,column=1,sticky=NSEW)
autores.grid(row=2,column=1,sticky=NSEW)
ano.grid(row=3,column=1,sticky=NSEW)

tela.mainloop()
