#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import webbrowser
from threading import Thread
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import INSERT
from tkinter import Button
from tkinter import RAISED
from tkinter import Frame
from tkinter import Label
from tkinter import FLAT
from tkinter import Menu
from tkinter import NSEW, Canvas
from tkinter import Text
from tkinter import font
from tkinter import END
from tkinter import N, S, E, W, Entry
from tkinter import Tk
import funcoes
from time import time
from json import load
from os import listdir
from os import getcwd
from os.path import abspath
from Arquivo import Arquivo
from Colorir import Colorir
from interpretador import Run


__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__project__ = 'Combratec'
__github__ = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__status__ = 'Desenvolvimento'
__date__ = '01/08/2019'
__last_update__ = '10/04/2020'
__version__ = '0.1'

global dic_info_arquivo
global bool_tela_em_fullscreen
global lst_titulos_frames
global fr_ajuda
global tx_terminal
global tx_codfc
global misterio_linhas
global dic_design
global cor_do_comando
global top_janela_terminal
global posCorrente
global posAbsuluta
global instancia
global linha_para_break_point
global dic_abas
global lst_abas
global fr_abas
global aba_focada
global controle_arquivos

dic_comandos, dic_design, cor_do_comando = funcoes.atualiza_configuracoes_temas()
colorir_codigo = Colorir(cor_do_comando, dic_comandos)
bool_tela_em_fullscreen = False
linha_para_break_point = 0
lst_titulos_frames = []
path = abspath(getcwd())
controle_arquivos = None
posAbsuluta = 0
posCorrente = 0
aba_focada = 1
lst_abas = []

dic_abas = {
    1:{
        "nome":"",
        "foco":True,
        "lst_breakpoints":[],
        "arquivoSalvo":{'link': "",'texto': ""},
        "arquivoAtual":{'texto': ""}
    }
}

def funcoes_arquivos_configurar(event, comando, link=None):
    global controle_arquivos
    global dic_abas
    global aba_focada
    global tx_codfc

    if controle_arquivos == None:
        return 0

    controle_arquivos.atualiza_infos(dic_abas, aba_focada, tx_codfc)

    if comando == "abrirArquivo":
        controle_arquivos.abrirArquivo(link)

    elif comando == "salvar_arquivo_dialog":
        controle_arquivos.salvar_arquivo_dialog(event)

    elif comando == "salvar_arquivo":
        controle_arquivos.salvar_arquivo(event)

    elif comando == "salvar_arquivo_como_dialog":
        controle_arquivos.salvar_arquivo_como_dialog(event)

    aba_focada = controle_arquivos.aba_focada
    dic_abas = controle_arquivos.dic_abas

    colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc)
    renderizar_aba(dic_abas)

def inicializa_orquestrador(event = None, libera_break_point_executa = False):
    print("\n Orquestrador iniciado")
 
    global tx_codfc
    global instancia
    global tx_terminal
    global dic_abas
    global aba_focada

    # Se for executar até o breakpoint
    if libera_break_point_executa:
        bool_ignorar_todos_breakpoints = False
        try:
            instancia.bool_break_point_liberado = True
            instancia.bool_ignorar_todos_breakpoints = False
        except:
            print("Iniciando programa até breakpoint")
        else:
            print("Liberando programa.")
            return 0
    else:
        bool_ignorar_todos_breakpoints = True

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

    linhas = tx_codfc.get('1.0', END)[0:-1]
    nova_linha = ''

    lista = linhas.split('\n')
    for linha in range(len(lista)):
        nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])

    linhas = nova_linha

    instancia = Run(tx_terminal, tx_codfc, True, dic_abas[aba_focada]["lst_breakpoints"], bool_ignorar_todos_breakpoints)
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
                funcao = lambda link = file:  funcoes_arquivos_configurar(None, "abrirArquivo" , 'scripts/' + str(link))
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

    dic_comandos, dic_design, cor_do_comando = funcoes.atualiza_configuracoes_temas()

    try:
        colorir_codigo.alterar_cor_comando(cor_do_comando)

        colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc).update()
        atualiza_design_interface()

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
        bt_brk_p.configure(dic_design["dicBtnMenus"])
        tx_pesqu.configure(dic_design["tx_pesqu"])
        fr_ajuda.configure(dic_design["fr_ajuda"])
        fr_princ.configure(dic_design["fr_princ"])
        tela.configure(dic_design["tela"])
        misterio_linhas.configure(dic_design["lb_linhas"])
        tx_codfc.configure(dic_design["tx_codificacao"])
        sb_codfc.configure(dic_design['scrollbar_text'])
        fr_opc_rapidas.configure(dic_design["fr_opcoes_rapidas"])

    except Exception as erro:
        print('Erro ao atualizar o design da interface, erro: ',erro)

def tela_ajuda(pesquisa):
    global fr_ajuda
    global lst_titulos_frames

    # Remover todos os botões
    for item in lst_titulos_frames:
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()

    lst_titulos_frames = []

    json_ajuda = funcoes.carregar_json('configuracoes/menu_ajuda.json')

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

class ContadorLinhas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        global dic_abas
        global aba_focada
        self.textwidget = None

    def atribuir(self, text_widget):
        self.textwidget = text_widget

    def desenhar_linhas(self, *args):
        # Deletar tudo
        self.delete("all")

        # Obter indice
        i = self.textwidget.index("@0,0")
        while True :

            # Desenhar
            dline= self.textwidget.dlineinfo(i)

            if dline is None:
                break

            y = dline[1]
            linenum = str(i).split(".")[0]

            cor_padrao = "#777777"
            if int(linenum) in dic_abas[aba_focada]["lst_breakpoints"]:
                linenum = linenum + " * "
                cor_padrao = "red"

            self.create_text(2,y,anchor="nw", text=linenum, font=("monospace regular", 12),  fill=cor_padrao)
            i = self.textwidget.index("%s+1line" % i)

class EditorDeCodigo(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        if (args[0] in ("insert", "replace", "delete") or args[0:3] == ("mark", "set", "insert") or args[0:2] == ("xview", "moveto") or args[0:2] == ("xview", "scroll") or args[0:2] == ("yview", "moveto") or args[0:2] == ("yview", "scroll")):
            self.event_generate("<<Change>>", when="tail")

        return result        

def atualizacao_linhas(event):
    misterio_linhas.desenhar_linhas()

def obterPosicaoDoCursor(event=None):
    global misterio_linhas
    global tx_codfc
    global linha_para_break_point

    numPosicao = str(tx_codfc.index(INSERT))
    posCorrente = int(float(tx_codfc.index(CURRENT)))

    print('linha que o cursor está : ', numPosicao)
    print('posicao do cursor: ', posCorrente)
    linha_para_break_point = posCorrente

def atualiza_texto_tela(num_aba):
    global tx_codfc
    global dic_abas

    tx_codfc.delete(1.0, END)
    tx_codfc.insert(END, str(dic_abas[num_aba]["arquivoAtual"]["texto"]))
    colorir_codigo.coordena_coloracao(None, tx_codfc = tx_codfc)

def adiciona_remove_breakpoint(event = None):
    global misterio_linhas
    global linha_para_break_point
    global dic_abas
    global aba_focada

    if int(linha_para_break_point) in dic_abas[aba_focada]["lst_breakpoints"]:
        dic_abas[aba_focada]["lst_breakpoints"].remove(int(linha_para_break_point))
    else:
        dic_abas[aba_focada]["lst_breakpoints"].append(int(linha_para_break_point))

    print(dic_abas[aba_focada]["lst_breakpoints"])
    atualizacao_linhas(event = None)

def atualiza_aba(lb_aba = None, numero=0):
    global lst_abas
    global dic_abas
    global tx_codfc

    if lb_aba != None:
        for itens in lst_abas:
            if itens[2] == lb_aba:
                dic_abas[itens[0]]["foco"] = True
                atualiza_texto_tela(itens[0])
            else:
                dic_abas[itens[0]]["foco"] = False
    else:
        for itens in lst_abas:
            if itens[0] == numero:
                dic_abas[itens[0]]["foco"] = True
                atualiza_texto_tela(itens[0])
            else:
                dic_abas[itens[0]]["foco"] = False
    
    renderizar_aba(dic_abas)
    atualizacao_linhas(event = None)

def fecha_aba(bt_fechar):
    global dic_abas
    global aba_focada
    global lst_abas

    focou_nova_aba = False
    item_para_deletar = 0

    print("Removendo: ", lst_abas, "<")
    print("Removendo2: ", dic_abas, "<")
    posicao_remover = 1
    posicoes_analisadas = 1

  
    for itens in lst_abas:

        if itens[3] == bt_fechar:
            posicao_remover = posicoes_analisadas
            item_para_deletar = itens[0]

        elif not focou_nova_aba:
            focou_nova_aba = True
            dic_abas[itens[0]]["foco"] = True
            aba_focada = itens[0]
            atualiza_texto_tela(itens[0])

        else:
            dic_abas[itens[0]]["foco"] = False

        posicoes_analisadas += 1

    if len(lst_abas) == 1:
        dic_abas = {1:{
            "nome":"",
            "foco":True,
            "lst_breakpoints":[],
            "arquivoSalvo":{'link': "",'texto': ""},
            "arquivoAtual":{'texto': ""}
            }
        }
        atualiza_texto_tela(1)

    else:
        # removendo o frame
        lst_abas[posicao_remover -1][1].grid_forget()
        lst_abas[posicao_remover -1][2].grid_forget()
        lst_abas[posicao_remover -1 ][3].grid_forget()

        # deletando os respectivos valores
        del dic_abas[item_para_deletar]
        del lst_abas[posicao_remover -1]
    
    dic_copia = {}
    inicio = 1

    for k, v in dic_abas.items():
        dic_copia[inicio] = dic_abas[k]
        inicio += 1
    dic_abas = dic_copia
    renderizar_aba(dic_abas)

def renderizar_aba(dic_abas):
    global lst_abas
    global fr_abas
    global aba_focada

    inicio = 2
    dic_cor_abas = {"background":"#c5d4fc", "foreground":"#565656"}

    # Destruindo as abas anteriores
    if lst_abas != []:
        for item in lst_abas:
            item[1].grid_forget()
            item[2].grid_forget()
            item[3].grid_forget()
        lst_abas = []

    for k, v in dic_abas.items():
        if v["foco"] == True:
            aba_focada = k
            dic_cor_abas["background"] = "#e6edff"
            bg_padrao = "#e6edff"
        else:
            dic_cor_abas["background"] = "#c5d4fc"
            bg_padrao = "#c5d4fc"

        fr_uma_aba = Frame(fr_abas, height=20, background='#adc4ff')
        fr_uma_aba.rowconfigure(1, weight=1)
        nome_arquivo = str(v["arquivoSalvo"]["link"]).split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if v["arquivoSalvo"]["texto"] != v["arquivoAtual"]["texto"]:
            txt_btn = "*"
        else:
            txt_btn = "x"

        lb_aba = Button(fr_uma_aba, dic_cor_abas, text=nome_arquivo, border=0, highlightthickness=0, padx=8, activebackground=bg_padrao)
        bt_fechar = Button(fr_uma_aba, dic_cor_abas, text=txt_btn, relief=FLAT, border=0, activebackground=bg_padrao, highlightthickness=0)
 
        fr_uma_aba.grid(row=1, column=inicio, sticky=N)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        lst_abas.append([inicio -1, fr_uma_aba, lb_aba, bt_fechar])
        lb_aba['command'] = lambda lb_aba=lb_aba: atualiza_aba(lb_aba)
        bt_fechar['command'] = lambda bt_fechar=bt_fechar: fecha_aba(bt_fechar)

        inicio += 1

def ativar_coordernar_coloracao():
    global tx_codfc
    global dic_abas
    global aba_focada

    renderizar_aba(dic_abas)
    dic_abas[aba_focada]["arquivoAtual"]['texto'] = tx_codfc.get(1.0, END)
    colorir_codigo.coordena_coloracao(None, tx_codfc=tx_codfc)

def nova_aba(event=None):
    global dic_abas
    global aba_focada

    posicao_final_maior = 0

    for k, v in dic_abas.items():
        if k > posicao_final_maior:
            posicao_final_maior = k

        dic_abas[k]["foco"] = False

    dic_abas[posicao_final_maior + 1] = {"nome":"",
                                   "foco":True,
                                   "lst_breakpoints":[],
                                   "arquivoSalvo":{'link': "",'texto': ""},
                                   "arquivoAtual":{'texto': ""}}

    aba_focada= posicao_final_maior + 1
    renderizar_aba(dic_abas)
    atualiza_aba(numero = posicao_final_maior + 1)

# tela.attributes('-fullscreen', True)
tela = Tk()
tela.title('Combratec - Linguagem feynman')
tela.rowconfigure(2, weight=1)
tela.geometry("1100x600")
tela.grid_columnconfigure(1, weight=1)

tela.bind('<F11>', lambda event: modoFullScreen(event))
tela.bind('<F5>', lambda event: inicializa_orquestrador(event))
tela.bind('<Control-s>', lambda event:funcoes_arquivos_configurar(None, "salvar_arquivo"))
tela.bind('<Control-o>', lambda event: funcoes_arquivos_configurar(None, "salvar_arquivo_dialog"))
tela.bind('<Control-S>', lambda event: funcoes_arquivos_configurar(None, "salvar_arquivo_como_dialog"))
tela.bind('<F7>', lambda event: inicializa_orquestrador(libera_break_point_executa = True))
tela.bind('<F10>', lambda event: adiciona_remove_breakpoint())
tela.bind('<Control-n>', nova_aba)

try:
    imgicon = PhotoImage(file='icone.png')
    tela.call('wm', 'iconphoto', tela._w, imgicon)

except Exception as erro:
    print('Erro ao carregar icone do app:', erro)

mn_barra = Menu(tela, tearoff=False)
tela.config(menu=mn_barra)

mn_ferrm = Menu(mn_barra, tearoff=False)
mn_intfc = Menu(mn_barra, tearoff=False)
mn_loclz = Menu(mn_barra, tearoff=False)
mn_exect = Menu(mn_barra, tearoff=False)
mn_arqui = Menu(mn_barra, tearoff=False)
mn_edita = Menu(mn_barra, tearoff=False)
mn_ajuda = Menu(mn_barra, tearoff=False)
mn_sobre = Menu(mn_barra, tearoff=False)
mn_devel = Menu(mn_barra, tearoff=False)

mn_barra.add_cascade(label='  Arquivo'    , menu=mn_arqui)
mn_barra.add_cascade(label='  Executar'   , menu=mn_exect)
mn_barra.add_cascade(label='  Localizar'  , menu=mn_loclz)
mn_barra.add_cascade(label='  Interface'  , menu=mn_intfc)
mn_barra.add_cascade(label='  Ajuda'      , menu=mn_ajuda)
mn_barra.add_cascade(label='  sobre'      , menu=mn_sobre)
mn_barra.add_cascade(label='  Dev'        , menu=mn_devel)
mn_barra.add_cascade(label='  Ferramentas', menu=mn_ferrm)

mn_arq_casct = Menu(mn_arqui, tearoff = False)
mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command= lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo_dialog"))
mn_arqui.add_command(label='  Nova Aba (Ctrl-N)', command = nova_aba)
mn_arqui.add_command(label='  Abrir pasta')
mn_arqui.add_separator()
mn_arqui.add_command(label='  Recentes')
mn_arqui.add_cascade(label='  Exemplos', menu=mn_arq_casct)
atualizarListaDeScripts()

mn_arqui.add_separator()
mn_arqui.add_command(label='  Salvar (Ctrl-S)', command= lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo"))
mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=lambda event=None: funcoes_arquivos_configurar(None, "salvar_arquivo_como_dialog"))
mn_arqui.add_separator()
mn_arqui.add_command(label='  imprimir (Ctrl-P)')
mn_arqui.add_command(label='  Exportar (Ctrl-E)')
mn_arqui.add_command(label='  Enviar por e-mail ')

mn_exect.add_command(label='  Executar Tudo (F5)', command=lambda event=None: inicializa_orquestrador(libera_break_point_executa=False))
mn_exect.add_command(label='  Executar linha (F6)')
mn_exect.add_command(label='  Executar até breakpoint (F7)', command=lambda event=None: inicializa_orquestrador(libera_break_point_executa = True))
mn_exect.add_command(label='  Executar com delay (F8)')
mn_exect.add_command(label='  Parar execução (F9)')
mn_exect.add_command(label='  Inserir breakpoint (F10)', command = adiciona_remove_breakpoint)
mn_loclz.add_command(label='  Localizar (CTRL + F)')
mn_loclz.add_command(label='  Substituir (CTRL + R)')
mn_ferrm.add_command(label='  corrigir identação')
mn_ferrm.add_command(label='  Numero de espaços para o tab')

mn_intfc_casct_temas = Menu(mn_intfc, tearoff=False)
mn_intfc.add_cascade(label='  Temas', menu=mn_intfc_casct_temas)
atualizarListaTemas()

mn_intfc_casct_sintx = Menu(mn_intfc, tearoff=False)
mn_intfc.add_cascade(label='  sintaxe', menu=mn_intfc_casct_sintx)
atualizarListasintaxe()

mn_intfc_casct_fonts = Menu(mn_intfc, tearoff=False)
mn_intfc.add_cascade(label='  fontes', menu=mn_intfc_casct_fonts)
atualizarListasfontes()

mn_ajuda.add_command(label='  Ajuda (F1)', command=lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comandos Disponíveis', command=lambda event:webbrowser.open(path + "/tutorial/index.html"))
mn_ajuda.add_command(label='  Comunidade', command=lambda event:webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html"))
mn_sobre.add_command(label='  Projeto', command=lambda event:webbrowser.open("http://feynmancode.blogspot.com/"))

mn_devel.add_command(label='  Logs', command= lambda event=None: ativar_logs())

# ========================================************===========================================
ic_salva = PhotoImage(file='imagens/ic_salvar.png')
ic_ident = PhotoImage(file='imagens/ic_arrumar.png')
ic_break = PhotoImage(file='imagens/ic_parar.png')
ic_playP = PhotoImage(file='imagens/ic_play.png')
ic_breaP = PhotoImage(file='imagens/ic_play_breakpoint.png')
ic_brk_p = PhotoImage(file='imagens/breakPoint.png')
ic_desfz = PhotoImage(file='imagens/left.png')
ic_redsf = PhotoImage(file='imagens/right.png')
ic_comme = PhotoImage(file='imagens/ic_comentario.png')
ic_idiom = PhotoImage(file='imagens/ic_idioma.png')
ic_ajuda = PhotoImage(file='imagens/ic_duvida.png')
ic_pesqu = PhotoImage(file='imagens/ic_pesquisa.png')
ic_atena = PhotoImage(file='imagens/ic_atena.png')

ic_salva = ic_salva.subsample(4, 4)
ic_ident = ic_ident.subsample(4, 4)
ic_break = ic_break.subsample(4, 4)
ic_playP = ic_playP.subsample(4, 4)
ic_breaP = ic_breaP.subsample(4, 4)
ic_brk_p = ic_brk_p.subsample(4, 4)
ic_desfz = ic_desfz.subsample(4, 4)
ic_redsf = ic_redsf.subsample(4, 4)
ic_comme = ic_comme.subsample(4, 4)
ic_idiom = ic_idiom.subsample(4, 4)
ic_ajuda = ic_ajuda.subsample(4, 4)
ic_pesqu = ic_pesqu.subsample(4, 4)
ic_atena = ic_atena.subsample(4, 4)
# ========================================************===========================================

fr_opc_rapidas = Frame(tela)

bt_salva = Button(fr_opc_rapidas, image=ic_salva, relief=RAISED)
bt_ident = Button(fr_opc_rapidas, image=ic_ident, relief=RAISED)
bt_break = Button(fr_opc_rapidas, image=ic_break, relief=RAISED)
bt_playP = Button(fr_opc_rapidas, image=ic_playP, relief=RAISED, command = inicializa_orquestrador)
bt_breaP = Button(fr_opc_rapidas, image=ic_breaP, relief=RAISED, command = lambda event=None: inicializa_orquestrador(libera_break_point_executa = True))
bt_brk_p = Button(fr_opc_rapidas, image=ic_brk_p, relief=RAISED, command = adiciona_remove_breakpoint)
bt_desfz = Button(fr_opc_rapidas, image=ic_desfz, relief=RAISED)
bt_redsf = Button(fr_opc_rapidas, image=ic_redsf, relief=RAISED)
bt_comme = Button(fr_opc_rapidas, image=ic_comme, relief=RAISED)
bt_idiom = Button(fr_opc_rapidas, image=ic_idiom, relief=RAISED)
bt_ajuda = Button(fr_opc_rapidas, image=ic_ajuda, relief=RAISED)
bt_pesqu = Button(fr_opc_rapidas, image=ic_pesqu, relief=RAISED)
bt_atena = Button(fr_opc_rapidas, image=ic_atena, relief=RAISED)

fr_princ = Frame(tela)
fr_princ.grid_columnconfigure(2, weight=1)
fr_princ.rowconfigure(1, weight=1)

fr_abas = Frame(fr_princ, height=20, background='#adc4ff')
fr_abas.rowconfigure(1, weight=1)
fr_espaco = Label(fr_abas, width=4, background='#adc4ff')

renderizar_aba(dic_abas = dic_abas)

fr_espaco.grid(row=1, column=0, sticky=NSEW)

tx_codfc = EditorDeCodigo(fr_princ)
tx_codfc.bind("<<Change>>", atualizacao_linhas)
tx_codfc.bind("<Configure>", atualizacao_linhas)
tx_codfc.bind('<Button>', obterPosicaoDoCursor)
tx_codfc.bind('<KeyRelease>', lambda event = None: ativar_coordernar_coloracao())
tx_codfc.focus_force()
 
sb_codfc = Scrollbar(fr_princ, orient="vertical", command=tx_codfc.yview, relief=FLAT)
tx_codfc.configure(yscrollcommand=sb_codfc.set)
misterio_linhas = ContadorLinhas(fr_princ)
misterio_linhas.atribuir(tx_codfc)

fr_ajuda = Frame(fr_princ)
tx_pesqu = Entry(fr_ajuda)

fr_opc_rapidas.grid(row=1, column=1, sticky=NSEW, columnspan=2)
bt_salva.grid(row=1, column=1)
bt_ident.grid(row=1, column=2)
bt_break.grid(row=1, column=3)
bt_playP.grid(row=1, column=4)
bt_breaP.grid(row=1, column=5)
bt_brk_p.grid(row=1, column=6)
bt_desfz.grid(row=1, column=7)
bt_redsf.grid(row=1, column=8)
bt_idiom.grid(row=1, column=9)
bt_ajuda.grid(row=1, column=10)
bt_pesqu.grid(row=1, column=11)
bt_atena.grid(row=1, column=12)
bt_comme.grid(row=1, column=13)

fr_princ.grid(row=2, column=1, sticky=NSEW)
fr_abas.grid(row=0, column=1, columnspan=3, sticky=NSEW)
misterio_linhas.grid(row=1, column=1, sticky=NSEW)
tx_codfc.grid(row=1, column=2, sticky=NSEW)
sb_codfc.grid(row=1, column=3, sticky=NSEW)

#fr_ajuda.grid(row=1, column=4, sticky=NSEW)
#tx_pesqu.grid(row=0, column=1, sticky=NSEW)

atualiza_design_interface()
tela_ajuda("")

controle_arquivos = Arquivo(dic_abas, aba_focada, tx_codfc)
#funcoes_arquivos_configurar(None, "abrirArquivo", 'bkp.fyn')

tela.mainloop()
