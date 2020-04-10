#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Futuro
    [ ] Copiar código na Wiki na área de transferência
    [ ] lista posto na posicao i ate a posicao 3 no passo de 2


    Ambiente:
    Windows 10, Ubuntu 19.10, Kali Linux
    Sublime text 3
    color Schema = Dracula
    Theme = Darkmatter
"""

from tkinter.font import nametofont
from threading import Thread
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import DISABLED
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import INSERT
from tkinter import Button
from tkinter import NORMAL
from tkinter import RAISED
from tkinter import SUNKEN
from tkinter import Frame
from tkinter import Label
from tkinter import FLAT
from tkinter import Menu
from tkinter import NSEW
from tkinter import Text
from tkinter import font
from tkinter import END
from tkinter import Tk
from funcoes import *
from time import sleep
from time import time
from json import load
from random import randint
from os import listdir
from os.path import abspath
from os import getcwd
from re import finditer
from re import findall
from interpretador import Run
from colorir import Colorir
from tkinter import N, S, E, W, Entry
import webbrowser

__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'
__project__     = 'Combratec'
__github__      = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__status__      = 'Desenvolvimento'
__date__        = '01/08/2019'
__last_update__ = '10/04/2020'
__version__     = '0.1'

global dic_info_arquivo
global bool_tela_em_fullscreen
global lst_titulos_frames
global fr_ajuda
global altura_widget
global tx_terminal
global tx_codfc
global lb_linhs
global dic_design
global cor_do_comando
global top_janela_terminal
global posCorrente
global posAbsuluta
global instancia

bool_tela_em_fullscreen = False
lst_titulos_frames = []
dic_info_arquivo = {'link': None,'texto': None}
posAbsuluta = 0
posCorrente = 0
path = abspath(getcwd())
dic_comandos, dic_design, cor_do_comando = atualiza_configuracoes_temas()
colorir_codigo = Colorir(cor_do_comando, dic_comandos)

def salvar_arquivo_como_dialog(event = None):
    global dic_info_arquivo

    opt = {"mode":'w',
           "defaultextension":".fyn",
           "title":"Selecione o script",
           "filetypes":(("Meus scripts", "*.fyn"), ("all files", "*.*"))
    }

    arq = filedialog.asksaveasfile(opt)

    lnk_arquivo_salvar = str(arq.name)

    if arq is None:
        return None

    arq.close()

    text2save = str(tx_codfc.get(1.0, END))
    try:
        arq = open(lnk_arquivo_salvar, 'w', encoding='utf8')
        arq.write(text2save[0:-1])
        arq.close()

    except Exception as erro:
        messagebox.showinfo('Erro', 'Erro ao salvar programa, erro: {}'.format(erro))

    else:
        dic_info_arquivo['link'] = arq.name
        dic_info_arquivo['texto'] = text2save

        return arq.name

def salvar_arquivo(event=None):
    """
    Salva um arquivo que já está aberto
    """

    global dic_info_arquivo

    if dic_info_arquivo['link'] == None:
        salvar_arquivo_como_dialog()

    else:
        programaCodigo = tx_codfc.get(1.0, END)

        if dic_info_arquivo['texto'] == programaCodigo:
            Run.log(self, " Programa não sofreu modificações para ser salvo novamente....")

        else:
            try:
                salvar_arquivo(arquivo = dic_info_arquivo['link'], texto = programaCodigo[0:-1])

            except Exception as erro:
                messagebox.showinfo('Erro', 'Não foi possível salvar essa versão do código, erro: {}'.format(erro))

            else:
                dic_info_arquivo['texto'] = programaCodigo

def salvar_arquivo_dialog(event=None):
    global dic_info_arquivo
    global tx_codfc

    arq_tips = [('Scripts fyn', '*.fyn'), ('Todos os arquivos', '*')]
    arq_dial = filedialog.Open(filetypes = arq_tips)
    arq_nome = arq_dial.show()

    if arq_nome == ():
        print(' Nenhum arquivo escolhido')

    else:
        print(' Arquivo "{}" escolhido'.format(arq_nome))
        arq_txts = abrir_arquivo(arq_nome)

        if arq_txts[0] != None:
            tx_codfc.delete(1.0, END)
            tx_codfc.insert(END, arq_txts[0])

        else:
            messagebox.showinfo("ops","Aconteceu um erro ao abrir o arquivo" + arq_txts[1])

        colorir_codigo.coordena_coloracao(None,tx_codfc)

        dic_info_arquivo['link'] = arq_nome
        dic_info_arquivo['texto'] = arq_txts[0]

def abrirArquivo(link):
    global dic_info_arquivo
    global tx_codfc

    print(' Abrindo arquivo "{}" escolhido'.format(link))

    arq = abrir_arquivo(link)

    if arq[0] != None:
        tx_codfc.delete(1.0, END)
        tx_codfc.insert(END, arq[0])

        colorir_codigo.coordena_coloracao(None, tx_codfc)

        dic_info_arquivo['link'] = link
        dic_info_arquivo['texto'] = arq[0]

    else:
        if "\'utf-8' codec can\'t decode byte" in arq[1]:
            messagebox.showinfo("Erro de codificação", "Por favor, converta seu arquivo para a codificação UTF-8. Não foi possível abrir o arquivo: \"{}\", erro: \"{}\"".format(link, arq[1]))
        else:
            messagebox.showinfo('Erro', 'Aconteceu um erro ao tentar abrir o script: {}, erro: {}'.format(link, arq[1]))

        print('Arquivo não selecionado')

def inicializa_orquestrador(event = None):
    print("\n Orquestrador iniciado")
    global tx_codfc
    global instancia
    global tx_terminal

    inicio = time()
    try:
        print(instancia.numero_threads)
    except:
        pass
    else:
        messagebox.showinfo('Problemas',"Já existe um programa sendo executado!")
        return 0

    inicializador_terminal()
    
    tx_terminal.delete('1.0', END)

    linhas = tx_codfc.get('1.0', END)
    nova_linha = ''

    lista = linhas.split('\n')
    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])
    
    linhas = nova_linha

    instancia = Run(tx_terminal, tx_codfc, True)
    t = Thread(target=lambda codigoPrograma = linhas: instancia.orquestrador_interpretador(codigoPrograma))
    t.start()

    while instancia.numero_threads != 0 or not instancia.boo_orquestrador_iniciado:
        tela.update()

    del instancia

    try:
        tx_terminal.insert(END, '\nScript finalizado em {:.3} segundos'.format(time() - inicio))
        tx_terminal.see("end")
 
    except Exception as erro:
        print('Impossível exibir mensagem de finalização, erro: '+ str(erro))

def modoFullScreen(event=None):
    global bool_tela_em_fullscreen

    if bool_tela_em_fullscreen:
        bool_tela_em_fullscreen = False

    else:
        bool_tela_em_fullscreen = True

    tela.attributes("-fullscreen", bool_tela_em_fullscreen)

def ativar_logs(event=None):
    global instancia

    try:
        if instancia.bool_logs:
            instancia.bool_logs = False

        else:
            instancia.bool_logs = True
    except:
        print("Interpretador não iniciado")


def pressionar_enter_terminal(event = None):
    try:
        instancia.pressionou_enter(event)
    except:
        print("Impossivel detectar enter, interpretador finalizado")

def inicializador_terminal():
    global tx_terminal
    global top_janela_terminal
    global instancia

    top_janela_terminal = Toplevel(tela)
    top_janela_terminal.grid_columnconfigure(1, weight=1)
    top_janela_terminal.rowconfigure(1, weight=1)
    top_janela_terminal.geometry("720x450+150+150")

    tx_terminal = Text(top_janela_terminal)
    try:
        # Se ainda não estava carregado
        tx_terminal.configure(dic_design["tx_terminal"])
    except Exception as erro:
        print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

    tx_terminal.bind('<Return>', lambda event:pressionar_enter_terminal(event))
    tx_terminal.focus_force()
    tx_terminal.grid(row=1, column=1, sticky=NSEW)

def atualizarListaDeScripts():
    for file in listdir('scripts/'):
        if len(file) > 5:
            if file[-3:] == 'fyn':
                funcao = lambda link = file: abrirArquivo('scripts/' + str(link))
                mn_arq_casct.add_command(label=file, command = funcao)
 
def atualizarListaTemas():
    for file in listdir('temas/'):
        if len(file) > 11:
            if file[-10:] == 'theme.json':
                funcao = lambda link = file: atualizaInterface('tema', str(link))
                mn_intfc_casct_temas.add_command(label=file, command=funcao)

def atualizarListasintaxe():
    for file in listdir('temas/'):
        if len(file) > 13:
            if file[-12:] == 'sintaxe.json':
                funcao = lambda link = file: atualizaInterface('sintaxe', str(link))
                mn_intfc_casct_sintx.add_command(label=file, command=funcao)

def atualizarListasfontes():
    fontes=list(font.families())
    fontes.sort()

    for fonte in fontes:
        mn_intfc_casct_fonts.add_command(label=fonte)

def arquivoConfiguracao(chave, novo = None):
    if novo == None:
        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)
            retorno = configArquivoJson[chave]

        return retorno

    elif novo != None:
        with open('configuracoes/configuracoes.json') as json_file:
            configArquivoJson = load(json_file)

            configArquivoJson[chave] = novo
            configArquivoJson = str(configArquivoJson).replace('\'','\"')

        file = open('configuracoes/configuracoes.json','w')
        file.write(str(configArquivoJson))
        file.close()

def atualizaInterface(chave, novo):
    global tela
    global tx_codfc
    global dic_design
    global cor_do_comando

    try:
        arquivoConfiguracao(chave, novo)

    except Exception as e:
        return [None,'Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas']

    dic_comandos, dic_design, cor_do_comando = atualiza_configuracoes_temas()

    try:
        atualiza_design_interface()
        colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc)
    except Exception as erro:
        print('ERRO: ', erro)
    else:
        print('Temas atualizados')

    tela.update()
    tx_codfc.update()

def atualiza_design_interface():

    try:
        mn_intfc_casct_sintx.configure(dic_design["cor_menu"])
        mn_intfc_casct_temas.configure(dic_design["cor_menu"])
        mn_intfc_casct_fonts.configure(dic_design["cor_menu"])
        mn_arq_casct.configure(dic_design["cor_menu"])
        mn_ferrm.configure(dic_design["cor_menu"])
        mn_intfc.configure(dic_design["cor_menu"])
        mn_loclz.configure(dic_design["cor_menu"])
        mn_exect.configure(dic_design["cor_menu"])
        mn_arqui.configure(dic_design["cor_menu"])
        mn_edita.configure(dic_design["cor_menu"])
        mn_barra.configure(dic_design["cor_menu"])
        mn_ajuda.configure(dic_design["cor_menu"])
        mn_sobre.configure(dic_design["cor_menu"])
        mn_barra.configure(dic_design["cor_menu"])
        mn_devel.configure(dic_design["cor_menu"])
        lb_linhs.configure(dic_design["lb_linhas"])
        bt_salva.configure(dic_design["dicBtnMenus"])
        bt_ident.configure(dic_design["dicBtnMenus"])
        bt_break.configure(dic_design["dicBtnMenus"])
        bt_playP.configure(dic_design["dicBtnMenus"])
        bt_breaP.configure(dic_design["dicBtnMenus"])
        bt_desfz.configure(dic_design["dicBtnMenus"])
        bt_redsf.configure(dic_design["dicBtnMenus"])
        bt_comme.configure(dic_design["dicBtnMenus"])
        bt_idiom.configure(dic_design["dicBtnMenus"])
        bt_ajuda.configure(dic_design["dicBtnMenus"])
        bt_pesqu.configure(dic_design["dicBtnMenus"])
        bt_atena.configure(dic_design["dicBtnMenus"])
        tx_pesqu.configure(dic_design["tx_pesqu"])
        fr_ajuda.configure(dic_design["fr_ajuda"])
        fr_princ.configure(dic_design["fr_princ"])

        tela.configure(dic_design["tela"])

        tx_codfc.configure(dic_design["tx_codificacao"])
        sb_codfc.configure(dic_design['scrollbar_text'])

        fr_opc_rapidas.configure(dic_design["fr_opcoes_rapidas"])

    except Exception as erro:
        print('Erro ao atualizar o design da interface, erro: ',erro)

def configuracoes(ev):
    print('configuracoes')

    global altura_widget
    global lb_linhs
    global posCorrente
    global posAbsuluta

    if ev != None:
        altura_widget = int( ev.height / 24 )

    qtdLinhas = tx_codfc.get(1.0, 'end').count('\n')
    #print('Quantidade para : ' + str(qtdLinhas))
    #print('Atualizadoo para: ' + str(altura_widget))

    ate = qtdLinhas + 1
    inicio = 1

    add_linha = ''
    for linha in range(inicio, ate):
        add_linha = add_linha +  "  " + str(linha) + '\n'

    lb_linhs.config(state=NORMAL)
    lb_linhs.delete(1.0, END)
    lb_linhs.insert(1.0, add_linha[:-1])

    lb_linhs.config(state=DISABLED)

def obterPosicaoDoCursor(event=None):
    global altura_widget
    global lb_linhs
    global tx_codfc

    numPosicao = str(tx_codfc.index(INSERT))
    posCorrente = int(float(tx_codfc.index(CURRENT)))

    print('linha que o cursor está : ', numPosicao)
    print('posicao do cursor: ', posCorrente)
    print('altura: ', altura_widget)

    if posCorrente - altura_widget <= 0:
        return 0

    add_linha = ''
    for linha in range(posCorrente - altura_widget, posCorrente):
        add_linha = add_linha +  "  " + str(linha) + '\n'

    lb_linhs.config(state=NORMAL)
    lb_linhs.delete(1.0, END)
    lb_linhs.insert(1.0, add_linha[:-1])
    lb_linhs.config(state=DISABLED)

def tela_ajuda(pesquisa):
    global fr_ajuda
    global lst_titulos_frames

    # Remover todos os botões
    for item in lst_titulos_frames:
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()

    lst_titulos_frames = []

    json_ajuda = carregar_json('configuracoes/menu_ajuda.json')

    contador_frames = 2
    for k, v in json_ajuda.items(): # Cria os itens na tela

        descricao = json_ajuda[k]['descricao']
        exemplo = json_ajuda[k]['exemplo']
        titulo = json_ajuda[k]['titulo']
        chave = json_ajuda[k]['chave']
        link = json_ajuda[k]['link']

        if pesquisa in titulo.lower() or pesquisa in chave.lower() == False:
            continue

        # MENU
        fr_ajuda_comando = Frame(fr_ajuda) 
        lb_ajuda_texto_c = Label(fr_ajuda_comando, text=titulo)
        lb_ajuda_descr_c = Label(fr_ajuda_comando, text=exemplo)

        fr_ajuda_comando.configure(dic_design["fr_ajuda_comando"])
        lb_ajuda_texto_c.configure(dic_design["lb_ajuda_texto_c"])
        lb_ajuda_descr_c.configure(dic_design["lb_ajuda_descr_c"])

        fr_ajuda_comando.grid(row=contador_frames, column=1, sticky=NSEW)
        lb_ajuda_texto_c.grid(row=1, column=1, sticky=W)
        lb_ajuda_descr_c.grid(row=2, column=1, sticky=NSEW)

        lst_titulos_frames.append([fr_ajuda_comando, lb_ajuda_texto_c, lb_ajuda_descr_c])

        contador_frames += 1

# tela.attributes('-fullscreen', True)
tela = Tk()
tela.title('Combratec - Linguagem feynman')
tela.rowconfigure(2, weight=1)
tela.geometry("1100x600")
tela.grid_columnconfigure(1, weight=1)

tela.bind('<F11>', lambda event: modoFullScreen(event))
tela.bind('<F5>', lambda event: inicializa_orquestrador(event))
tela.bind('<Control-s>', lambda event: salvar_arquivo(event))
tela.bind('<Control-o>', lambda event: salvar_arquivo_dialog(event))
tela.bind('<Control-S>', lambda event: salvar_arquivo_como_dialog(event))

try:
    imgicon = PhotoImage(file='icone.png')
    tela.call('wm', 'iconphoto', tela._w, imgicon)

except Exception as erro:
    print('Erro ao carregar icone do app:', erro)

mn_barra = Menu(tela, tearoff = False)
tela.config(menu=mn_barra)

mn_ferrm = Menu(mn_barra, tearoff = False)
mn_intfc = Menu(mn_barra, tearoff = False)
mn_loclz = Menu(mn_barra, tearoff = False)
mn_exect = Menu(mn_barra, tearoff = False)
mn_arqui = Menu(mn_barra, tearoff = False)
mn_edita = Menu(mn_barra, tearoff = False)
mn_ajuda = Menu(mn_barra, tearoff = False)
mn_sobre = Menu(mn_barra, tearoff = False)
mn_devel = Menu(mn_barra, tearoff = False)

mn_barra.add_cascade(label='  Arquivo'    , menu=mn_arqui)
mn_barra.add_cascade(label='  Executar'   , menu=mn_exect)
mn_barra.add_cascade(label='  Localizar'  , menu=mn_loclz)
mn_barra.add_cascade(label='  Interface'  , menu=mn_intfc)
mn_barra.add_cascade(label='  Ajuda'      , menu=mn_ajuda)
mn_barra.add_cascade(label='  sobre'      , menu=mn_sobre)
mn_barra.add_cascade(label='  Dev'        , menu=mn_devel)
mn_barra.add_cascade(label='  Ferramentas', menu=mn_ferrm)

mn_arq_casct = Menu(mn_arqui, tearoff = False)
mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command=salvar_arquivo_dialog)
mn_arqui.add_command(label='  Nova Guia (Ctrl-N)')
mn_arqui.add_command(label='  Abrir pasta')
mn_arqui.add_separator()
mn_arqui.add_command(label='  Recentes')
mn_arqui.add_cascade(label='  Exemplos', menu=mn_arq_casct)
atualizarListaDeScripts()

mn_arqui.add_separator()
mn_arqui.add_command(label='  Salvar (Ctrl-S)', command=salvar_arquivo)
mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=salvar_arquivo_como_dialog)
mn_arqui.add_separator()
mn_arqui.add_command(label='  imprimir (Ctrl-P)')
mn_arqui.add_command(label='  Exportar (Ctrl-E)')
mn_arqui.add_command(label='  Enviar por e-mail ')

mn_exect.add_command(label='  Executar Tudo (F5)', command=inicializa_orquestrador)
mn_exect.add_command(label='  Executar linha (F6)')
mn_exect.add_command(label='  Executar até breakpoint (F7)')
mn_exect.add_command(label='  Executar com delay (F8)')
mn_exect.add_command(label='  Parar execução (F9)')
mn_exect.add_command(label='  Inserir breakpoint (F10)')
mn_loclz.add_command(label='  Localizar (CTRL + F)')
mn_loclz.add_command(label='  Substituir (CTRL + R)')
mn_ferrm.add_command(label='  corrigir identação')
mn_ferrm.add_command(label='  Numero de espaços para o tab')

mn_intfc_casct_temas = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  Temas', menu=mn_intfc_casct_temas)

atualizarListaTemas()

mn_intfc_casct_sintx = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  sintaxe', menu=mn_intfc_casct_sintx)

atualizarListasintaxe()

mn_intfc_casct_fonts = Menu(mn_intfc, tearoff = False)
mn_intfc.add_cascade(label='  fontes', menu=mn_intfc_casct_fonts)

atualizarListasfontes()

mn_ajuda.add_command(label='  Ajuda (F1)', command = lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comandos Disponíveis', command = lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comunidade', command = lambda event:webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html"))
mn_sobre.add_command(label='  Projeto', command= lambda event:webbrowser.open("http://feynmancode.blogspot.com/"))

mn_devel.add_command(label='  Logs', command= lambda event = None: ativar_logs())

fr_opc_rapidas = Frame(tela)
fr_opc_rapidas.grid(row = 1, column =1, sticky=NSEW, columnspan=2)

ic_salva = PhotoImage(file='imagens/ic_salvar.png')
ic_ident = PhotoImage(file='imagens/ic_arrumar.png')
ic_break = PhotoImage(file='imagens/ic_parar.png')
ic_playP = PhotoImage(file='imagens/ic_play.png')
ic_breaP = PhotoImage(file='imagens/ic_play_breakpoint.png')
ic_desfz = PhotoImage(file='imagens/left.png')
ic_redsf = PhotoImage(file='imagens/right.png')
ic_comme = PhotoImage(file='imagens/ic_comentario.png')
ic_idiom = PhotoImage(file='imagens/ic_idioma.png')
ic_ajuda = PhotoImage(file='imagens/ic_duvida.png')
ic_pesqu = PhotoImage(file='imagens/ic_pesquisa.png')
ic_atena = PhotoImage(file='imagens/ic_atena.png')

ic_salva = ic_salva.subsample(4,4)
ic_ident = ic_ident.subsample(4,4)
ic_break = ic_break.subsample(4,4)
ic_playP = ic_playP.subsample(4,4)
ic_breaP = ic_breaP.subsample(4,4)
ic_desfz = ic_desfz.subsample(4,4)
ic_redsf = ic_redsf.subsample(4,4)
ic_comme = ic_comme.subsample(4,4)
ic_idiom = ic_idiom.subsample(4,4)
ic_ajuda = ic_ajuda.subsample(4,4)
ic_pesqu = ic_pesqu.subsample(4,4)
ic_atena = ic_atena.subsample(4,4)

bt_salva = Button(fr_opc_rapidas, image=ic_salva, relief = RAISED)
bt_ident = Button(fr_opc_rapidas, image=ic_ident, relief = RAISED)
bt_break = Button(fr_opc_rapidas, image=ic_break, relief = RAISED)
bt_playP = Button(fr_opc_rapidas, image=ic_playP, relief = RAISED, command = inicializa_orquestrador)
bt_breaP = Button(fr_opc_rapidas, image=ic_breaP, relief = RAISED, command = inicializa_orquestrador)
bt_desfz = Button(fr_opc_rapidas, image=ic_desfz, relief = RAISED)
bt_redsf = Button(fr_opc_rapidas, image=ic_redsf, relief = RAISED)
bt_comme = Button(fr_opc_rapidas, image=ic_comme, relief = RAISED)
bt_idiom = Button(fr_opc_rapidas, image=ic_idiom, relief = RAISED)
bt_ajuda = Button(fr_opc_rapidas, image=ic_ajuda, relief = RAISED)
bt_pesqu = Button(fr_opc_rapidas, image=ic_pesqu, relief = RAISED)
bt_atena = Button(fr_opc_rapidas, image=ic_atena, relief = RAISED)

fr_princ = Frame(tela)
fr_princ.grid_columnconfigure(2, weight=1)
fr_princ.rowconfigure(1, weight=1)

lb_linhs = Text(fr_princ)

tx_codfc = Text(fr_princ)
sb_codfc = Scrollbar(fr_princ, relief = FLAT)
fr_ajuda = Frame(fr_princ)
tx_pesqu = Entry(fr_ajuda)

tx_codfc.focus_force()
lb_linhs.config(state = DISABLED)
tx_codfc['yscrollcommand'] = sb_codfc.set
sb_codfc.config(command = tx_codfc.yview)

tx_codfc.bind('<Configure>', configuracoes )
tx_codfc.bind('<Button>', obterPosicaoDoCursor)
tx_codfc.bind('<KeyRelease>', lambda event = None: colorir_codigo.coordena_coloracao(event, tx_codfc=tx_codfc))

bt_salva.grid(row=1,column=1)
bt_ident.grid(row=1,column=2)
bt_break.grid(row=1,column=3)
bt_playP.grid(row=1,column=4)
bt_breaP.grid(row=1,column=5)
bt_desfz.grid(row=1,column=6)
bt_redsf.grid(row=1, column=7)
bt_comme.grid(row=1, column=8)
bt_idiom.grid(row=1, column=9)
bt_ajuda.grid(row=1, column=10)
bt_pesqu.grid(row=1, column=11)
bt_atena.grid(row=1, column=12)

fr_princ.grid(row=2, column=1, sticky=NSEW)
tx_codfc.grid(row=1, column=2, sticky=NSEW)
sb_codfc.grid(row=1, column=3, sticky=NSEW)
lb_linhs.grid(row=1, column=1, sticky=NSEW)

fr_ajuda.grid(row=1, column=4, sticky=NSEW)
tx_pesqu.grid(row=0, column=1, sticky=NSEW)

atualiza_design_interface()

tela_ajuda("")
abrirArquivo('programa_teste.fyn')

tela.mainloop()

