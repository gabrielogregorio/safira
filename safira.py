# -*- coding: utf-8 -*-

from libs.aba import Aba
from libs.interpretador import Run
from libs.colorir import Colorir
from libs.visualizacao import ContadorLinhas
from libs.visualizacao import EditorDeCodigo
from libs.arquivo import Arquivo
import libs.funcoes as funcoes

import webbrowser
from time import time, sleep
from threading import Thread
from os.path import abspath
from os import listdir
from json import load
from os import getcwd
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import INSERT
from tkinter import Button
from tkinter import RAISED
from tkinter import NORMAL
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import NSEW
from tkinter import Text
from tkinter import FLAT
from tkinter import Menu
from tkinter import END
from tkinter import N
from tkinter import S
from tkinter import E
from tkinter import W
from tkinter import Tk

__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__project__ = 'Combratec'
__github__ = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__status__ = 'Desenvolvimento'
__date__ = '01/08/2019'
__last_update__ = '02/05/2020'
__version__ = '0.1'

class Safira(Aba):
    def __init__(self):
        self.dic_comandos, self.dic_design, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()
        self.colorir_codigo = Colorir(self.cor_do_comando, self.dic_comandos)
        self.bool_tela_em_fullscreen = False
        self.top_janela_terminal = None
        self.controle_arquivos = None
        self.path = abspath(getcwd())
        self.lista_terminal_destruir = []
        self.bool_debug_temas = False
        self.linhas_laterais = None
        self.tx_terminal = None
        self.instancia = None
        self.tx_codfc = None
        self.linha_p_brk_p = 0
        self.posAbsuluta = 0
        self.posCorrente = 0
        self.aba_focada = 0
        self.lst_abas = []
        self.bt_play = None
        self.frame_tela = None
        self.tela = None
        self.fr_splash = None    # splash
        self.l1_splash = None    # splash
        self.l2_splash = None    # splash
        self.frame_splash = None # splash
        self.fr_opc_rapidas = None
        self.ic_salva = None
        self.ic_playP = None
        self.ic_PStop = None
        self.ic_breaP = None
        self.ic_brk_p = None
        self.ic_desfz = None
        self.ic_redsf = None
        self.ic_ajuda = None
        self.ic_pesqu = None
        self.bt_salva = None
        self.bt_playP = None
        self.bt_breaP = None
        self.bt_brk_p = None
        self.bt_desfz = None
        self.bt_redsf = None
        self.bt_ajuda = None
        self.bt_pesqu = None
        self.dic_abas = { 0:funcoes.carregar_json("configuracoes/guia.json")}
        self.bool_interpretador_iniciado = False
        self.lst_historico_abas_focadas = []

    def main(self):
        Safira.splashScreen1(self)
        sleep(1)
        Safira.inicioScreen(self)

    def splashScreen1(self):
        self.tela = Tk()

        self.tela.rowconfigure(1, weight=1)
        self.tela.grid_columnconfigure(1, weight=1)
        self.tela.withdraw() # Remove visibilidade
        self.tela.overrideredirect(1) # Remove barra de titulos

        self.frame_splash = Frame(self.tela)

        self.frame_splash.configure(self.dic_design["cor_intro"])
        self.frame_splash.rowconfigure(1, weight=1)
        self.frame_splash.grid_columnconfigure(0, weight=1)

        self.fr_splash = Frame(self.frame_splash, self.dic_design["cor_intro"])
        self.l1_splash = Label(self.frame_splash, self.dic_design["cor_intro"], text=" COMBRATEC ", fg="#404040", font=( "Lucida Sans", 90), bd=80)
        self.l2_splash = Label(self.frame_splash, self.dic_design["cor_intro"], text="Safira ILE", fg="#404040", font=("Lucida Sans", 12))

        self.frame_splash.grid(row=1, column=1, sticky=NSEW)
        self.fr_splash.grid(row=0, column=1, sticky=NSEW)
        self.l1_splash.grid(row=1, column=1, sticky=NSEW)
        self.l2_splash.grid(row=2, column=1, sticky=NSEW)
        self.frame_splash.update()

        Safira.centraliza_tela(self)

    def inicioScreen(self):
        self.fr_splash.grid_forget()
        self.l1_splash.grid_forget()
        self.l2_splash.grid_forget()
        self.frame_splash.grid_forget()

        self.tela.update()

        self.tela.overrideredirect(0) # Traz barra de titulo
        self.tela.update()
        self.tela.withdraw() # Ocultar tkinter

        self.frame_tela = Frame(self.tela)
        self.frame_tela.grid(row=1, column=1, sticky=NSEW)
        self.frame_tela.update()

        # Configurações de self.telas
        self.tela.bind('<F11>', lambda event: Safira.modoFullScreen(self, event))
        self.tela.bind('<F5>', lambda event: Safira.inicializa_orquestrador(self, event))
        self.tela.bind('<Control-s>', lambda event: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo"))
        self.tela.bind('<Control-o>', lambda event: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo_dialog"))
        self.tela.bind('<Control-S>', lambda event: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo_como_dialog"))
        self.tela.bind('<F7>', lambda event: Safira.inicializa_orquestrador(self, libera_break_point_executa = True))

        self.tela.bind('<F10>', lambda event: Safira.adiciona_remove_breakpoint(self))
        #self.tela.bind('<F9>', lambda event: Safira.inicializa_orquestrador(self))
        self.tela.bind('<Control-n>', lambda event: Safira.nova_aba(self, event))
        self.tela.title('Combratec -  Safira ILE')
        # self.tela.attributes('-fullscreen', True)
        self.frame_tela.rowconfigure(2, weight=1)
        self.frame_tela.grid_columnconfigure(1, weight=1)

        try:
            imgicon = PhotoImage(file='icone.png')
            self.tela.call('wm', 'iconphoto', self.tela._w, imgicon)
        except Exception as erro:
            print('>>> Erro ao carregar icone do app:', erro)

        self.mn_barra = Menu(self.tela, tearoff=False, font = ("Lucida Sans", 13))
        self.tela.config(menu=self.mn_barra)

        dic_config_menu = {"tearoff":False, "font" : ("Lucida Sans", 13) }

        self.mn_ferrm = Menu( self.mn_barra, dic_config_menu )
        self.mn_intfc = Menu( self.mn_barra, dic_config_menu )
        self.mn_exect = Menu( self.mn_barra, dic_config_menu )
        self.mn_loclz = Menu( self.mn_barra, dic_config_menu )
        self.mn_exemp = Menu( self.mn_barra, dic_config_menu )
        self.mn_arqui = Menu( self.mn_barra, dic_config_menu )
        self.mn_edita = Menu( self.mn_barra, dic_config_menu )
        self.mn_ajuda = Menu( self.mn_barra, dic_config_menu )
        self.mn_sobre = Menu( self.mn_barra, dic_config_menu )
        self.mn_devel = Menu( self.mn_barra, dic_config_menu )

        self.mn_barra.add_cascade(label='  Arquivo'    , menu=self.mn_arqui, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Executar'   , menu=self.mn_exect, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Localizar'  , menu=self.mn_loclz, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Exemplos'  , menu=self.mn_exemp, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Interface'  , menu=self.mn_intfc, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Ajuda'      , menu=self.mn_ajuda, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  sobre'      , menu=self.mn_sobre, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Dev'        , menu=self.mn_devel, font = ("Lucida Sans", 13))
        self.mn_barra.add_cascade(label='  Ferramentas', menu=self.mn_ferrm, font = ("Lucida Sans", 13))

        self.mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command= lambda event=None: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo_dialog"))
        self.mn_arqui.add_command(label='  Nova Aba (Ctrl-N)', command = lambda event=None: Safira.nova_aba(self, event))
        self.mn_arqui.add_command(label='  Abrir pasta')
        self.mn_arqui.add_separator()
        self.mn_arqui.add_command(label='  Recentes')
        self.mn_arqui.add_separator()
        self.mn_arqui.add_command(label='  Salvar (Ctrl-S)', command= lambda event=None: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo"))
        self.mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=lambda event=None: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo_como_dialog"))
        self.mn_arqui.add_separator()
        self.mn_arqui.add_command(label='  imprimir (Ctrl-P)')
        self.mn_arqui.add_command(label='  Exportar (Ctrl-E)')
        self.mn_arqui.add_command(label='  Enviar por e-mail ')

        self.mn_exect.add_command(label='  Executar Tudo (F5)', command=lambda event=None: Safira.inicializa_orquestrador(self, libera_break_point_executa=False))
        self.mn_exect.add_command(label='  Executar linha (F6)')
        self.mn_exect.add_command(label='  Executar até breakpoint (F7)', command=lambda event=None: Safira.inicializa_orquestrador(self, libera_break_point_executa = True))
        self.mn_exect.add_command(label='  Parar execução (F9)', command = lambda event: Safira.inicializa_orquestrador(self, event))
        self.mn_exect.add_command(label='  Inserir breakpoint (F10)', command = lambda event: Safira.adiciona_remove_breakpoint(self, event))
        self.mn_loclz.add_command(label='  Localizar (CTRL + F)')
        self.mn_loclz.add_command(label='  Substituir (CTRL + R)')

        mn_arq_exemplo_casc = Menu(self.mn_exemp, tearoff = False)
        for file in listdir('scripts/'):
            if len(file) > 5:
                if file[-3:] == 'fyn':
                    funcao = lambda link = file:  Safira.funcoes_arquivos_configurar(self, None, "abrirArquivo" , 'scripts/' + str(link))
                    self.mn_exemp.add_command(label="  " + file + "  ", command = funcao)

        self.mn_intfc_casct_temas = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  Temas', menu=self.mn_intfc_casct_temas)
        for file in listdir('temas/'):
            if len(file) > 11:
                if file[-10:] == 'theme.json':
                    funcao = lambda link = file: Safira.atualizaInterface(self, 'tema', str(link))
                    self.mn_intfc_casct_temas.add_command(label=file, command=funcao)

        self.mn_intfc_casct_sintx = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  sintaxe', menu=self.mn_intfc_casct_sintx)
        for file in listdir('temas/'):
            if len(file) > 13:
                if file[-12:] == 'sintaxe.json':
                    funcao = lambda link = file: Safira.atualizaInterface(self, 'sintaxe', str(link))
                    self.mn_intfc_casct_sintx.add_command(label=file, command=funcao)

        self.mn_ajuda.add_command( label='  Ajuda (F1)', command= lambda:webbrowser.open(self.path + "/tutorial/index.html") )
        self.mn_ajuda.add_command( label='  Comandos Disponíveis', command =lambda: webbrowser.open(self.path + "/tutorial/index.html") )
        self.mn_ajuda.add_command( label='  Comunidade', command=lambda: webbrowser.open("https://feynmancode.blogspot.com/p/comunidade.html") )
        self.mn_sobre.add_command( label='  Projeto', command=lambda: webbrowser.open("http://feynmancode.blogspot.com/") )
        self.mn_devel.add_command( label='  Logs', command=lambda:  Safira.ativar_logs(self) )
        self.mn_devel.add_command( label='  Debug', command=lambda:  Safira.debug(self) )

        self.ic_salva = PhotoImage( file='imagens/ic_salvar.png' )
        self.ic_playP = PhotoImage( file='imagens/ic_play.png' )
        self.ic_PStop = PhotoImage( file='imagens/ic_parar.png' )
        self.ic_breaP = PhotoImage( file='imagens/ic_play_breakpoint.png' )
        self.ic_brk_p = PhotoImage( file='imagens/breakPoint.png' )
        self.ic_desfz = PhotoImage( file='imagens/left.png' )
        self.ic_redsf = PhotoImage( file='imagens/right.png' )
        self.ic_ajuda = PhotoImage( file='imagens/ic_duvida.png' )
        self.ic_pesqu = PhotoImage( file='imagens/ic_pesquisa.png' )

        self.ic_salva = self.ic_salva.subsample(4, 4)
        self.ic_playP = self.ic_playP.subsample(4, 4)
        self.ic_PStop = self.ic_PStop.subsample(4, 4)
        self.ic_breaP = self.ic_breaP.subsample(4, 4)
        self.ic_brk_p = self.ic_brk_p.subsample(4, 4)
        self.ic_desfz = self.ic_desfz.subsample(4, 4)
        self.ic_redsf = self.ic_redsf.subsample(4, 4)
        self.ic_ajuda = self.ic_ajuda.subsample(4, 4)
        self.ic_pesqu = self.ic_pesqu.subsample(4, 4)

        self.fr_opc_rapidas = Frame(self.frame_tela)

        self.bt_salva = Button( self.fr_opc_rapidas, image=self.ic_salva, relief=RAISED, command= lambda event=None: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo") )
        self.bt_playP = Button( self.fr_opc_rapidas, image=self.ic_playP, relief=RAISED, command =lambda event=None: Safira.inicializa_orquestrador(self, event) )
        self.bt_breaP = Button( self.fr_opc_rapidas, image=self.ic_breaP, relief=RAISED, command = lambda event=None: Safira.inicializa_orquestrador(self, libera_break_point_executa = True) )
        self.bt_brk_p = Button( self.fr_opc_rapidas, image=self.ic_brk_p, relief=RAISED, command = lambda event=None: Safira.adiciona_remove_breakpoint(self, event) )
        self.bt_desfz = Button( self.fr_opc_rapidas, image=self.ic_desfz, relief=RAISED )
        self.bt_redsf = Button( self.fr_opc_rapidas, image=self.ic_redsf, relief=RAISED )
        self.bt_ajuda = Button( self.fr_opc_rapidas, image=self.ic_ajuda, relief=RAISED )
        self.bt_pesqu = Button( self.fr_opc_rapidas, image=self.ic_pesqu, relief=RAISED )

        self.fr_princ = Frame(self.frame_tela, bg='red')
        self.fr_princ.grid_columnconfigure(2, weight=1)
        self.fr_princ.rowconfigure(1, weight=1)

        self.fr_abas = Frame(self.fr_princ, height=20)
        self.fr_abas.rowconfigure(1, weight=1)
        self.fr_espaco = Label(self.fr_abas, width=7)

        Safira.renderizar_abas_inicio(self)

        self.fr_espaco.grid(row=1, column=0, sticky=NSEW)
        self.tx_codfc = EditorDeCodigo(self.fr_princ)
        self.tx_codfc.bind("<<Change>>", lambda event: Safira.atualizacao_linhas(self, event))
        self.tx_codfc.bind("<Configure>", lambda event: Safira.atualizacao_linhas(self, event))
        self.tx_codfc.bind('<Button>', lambda event:  Safira.obterPosicaoDoCursor(self, event))
        self.tx_codfc.bind('<KeyRelease>', lambda event = None: Safira.ativar_coordernar_coloracao(self, event))
        self.tx_codfc.focus_force()

        ### self.tela.bind('<Control-S>', lambda event: Safira.funcoes_arquivos_configurar(self, None, "salvar_arquivo_como_dialog"))
        self.tx_codfc.bind('<Control-MouseWheel>', lambda event: Safira.mudar_fonte(self, "+") if int(event.delta) > 0 else Safira.mudar_fonte(self, "-"))

        self.sb_codfc = Scrollbar(self.fr_princ, orient="vertical", command=self.tx_codfc.yview, relief=FLAT)
        self.tx_codfc.configure(yscrollcommand=self.sb_codfc.set)

        self.linhas_laterais = ContadorLinhas(self.fr_princ, self.dic_design)

        self.linhas_laterais.aba_focada2 = self.aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas
        self.linhas_laterais.atribuir(self.tx_codfc)

        self.fr_opc_rapidas.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        self.bt_salva.grid(row=1, column=1)
        self.bt_playP.grid(row=1, column=4)
        self.bt_breaP.grid(row=1, column=5)
        self.bt_brk_p.grid(row=1, column=6)
        self.bt_desfz.grid(row=1, column=7)
        self.bt_redsf.grid(row=1, column=8)
        self.bt_ajuda.grid(row=1, column=10)
        self.bt_pesqu.grid(row=1, column=11)
        self.fr_princ.grid(row=2, column=1, sticky=NSEW)
        self.fr_abas.grid(row=0, column=1, columnspan=4, sticky=NSEW)
        self.linhas_laterais.grid(row=1, column=1, sticky=NSEW)
        self.tx_codfc.grid(row=1, column=2, sticky=NSEW)
        self.sb_codfc.grid(row=1, column=3, sticky=NSEW)

        self.controle_arquivos = Arquivo(self.dic_abas, self.aba_focada, self.tx_codfc)
        Safira.atualiza_design_interface(self)
        self.tela.update()

        self.tela.withdraw() # Ocultar tkinter
        t_width    = self.tela.winfo_screenwidth()
        t_heigth   = self.tela.winfo_screenheight()
        self.tela.geometry("{}x{}+0+0".format(t_width, t_heigth))
        self.tela.deiconify()

        self.tela.update()
        #Safira.funcoes_arquivos_configurar(None, "abrirArquivo", 'game.fyn')
        Safira.funcoes_arquivos_configurar(self, None, "abrirArquivo", 'scripts/teste.fyn')

        self.tela.mainloop()

    def mudar_fonte(self, acao):

        if acao == "+":
            adicao = 1
            print("+++")
        else:
            adicao = -1
            print("---")

        self.dic_design["cor_menu"]["font"][1] = int(self.dic_design["cor_menu"]["font"][1]) + adicao
        #self.dic_design["lb_sobDeTitulo"]["font"][1] = int(self.dic_design["lb_sobDeTitulo"]["font"][1]) + adicao
        #self.dic_design["dicBtnMenus"]["font"][1] = int(self.dic_design["dicBtnMenus"]["font"][1]) + adicao
        #self.dic_design["tx_terminal"]["font"][1] = int(self.dic_design["tx_terminal"]["font"][1]) + adicao
        self.dic_design["tx_codificacao"]["font"][1] = int(self.dic_design["tx_codificacao"]["font"][1]) + adicao
        self.dic_design["fonte_ct_linha"]["font"][1] = int(self.dic_design["fonte_ct_linha"]["font"][1]) + adicao
        self.dic_design["fonte_ct_linha"]["width"] = int(self.dic_design["fonte_ct_linha"]["width"]) + adicao

        self.tx_codfc.configure(self.dic_design["tx_codificacao"])
        self.linhas_laterais.desenhar_linhas()

    def inicializa_orquestrador(self, event = None, libera_break_point_executa = False):
        print("\n Orquestrador iniciado")

        self.bt_playP.configure(image=self.ic_PStop)
        self.bt_playP.update()

        # Se o interpretador já foi iniciado e o breakpoint for falso
        try:
            print(self.instancia.numero_threads)
        except:
            print("Thread Parou")
        else:
            if self.bool_interpretador_iniciado and libera_break_point_executa == False:
                self.instancia.aconteceu_erro = True
                return 0

        # Se for executar até o breakpoint
        if libera_break_point_executa:

            bool_ignorar_todos_breakpoints = False
            try:
                self.instancia.bool_break_point_liberado = True
                self.instancia.bool_ignorar_todos_breakpoints = False
            except:
                print("Iniciando programa até breakpoint")
            else:
                print("Liberando programa.")
                return 0
        else:
            bool_ignorar_todos_breakpoints = True

        inicio = time()

        self.bool_interpretador_iniciado = True
        if libera_break_point_executa:
            Safira.inicializador_terminal_debug(self)

        else:
            Safira.inicializador_terminal_producao(self)

        self.tx_terminal.delete('1.0', END)
        self.linha_analise = 0

        linhas = self.tx_codfc.get('1.0', END)[0:-1]
        nova_linha = ''

        lista = linhas.split('\n')
        for linha in range(len(lista)):
            nova_linha += '[{}]{}\n'.format( str(linha + 1), lista[linha] )

        linhas = nova_linha

        self.instancia = Run( self.tx_terminal,
                              self.tx_codfc,
                              False,
                              self.dic_abas[self.aba_focada]["lst_breakpoints"],
                              bool_ignorar_todos_breakpoints)

        t = Thread(target=lambda codigoPrograma = linhas: self.instancia.orquestrador_interpretador(codigoPrograma))
        t.start()

        valor_antigo = 0

        while self.instancia.numero_threads != 0 or not self.instancia.boo_orquestrador_iniciado:
            self.tela.update()

            try:
                self.linha_analise = int(self.instancia.num_linha)
                if self.linha_analise != valor_antigo:
                    valor_antigo = self.linha_analise
                    self.linhas_laterais.linha_analise = self.linha_analise
                    self.linhas_laterais.desenhar_linhas()
            except Exception as erro:
                print("Erro update", erro)

        del self.instancia

        try:
            self.tx_terminal.config(state=NORMAL)
            self.tx_terminal.insert(END, '\nScript finalizado em {:.3} segundos'.format(time() - inicio))
            self.tx_terminal.see("end")

        except Exception as erro:
            print('Impossível exibir mensagem de finalização, erro: '+ str(erro))
        
        self.linhas_laterais.linha_analise = 0
        self.linhas_laterais.desenhar_linhas()

        self.bt_playP.configure(image=self.ic_playP)
        self.bool_interpretador_iniciado = False



    def inicializador_terminal_debug(self):
        Safira.destruir_instancia_terminal(self)

        frame_terminal_e_grid = Frame(self.fr_princ)
        frame_terminal_e_grid.grid(row=1, column=4, sticky=NSEW)

        frame_terminal_e_grid.grid_columnconfigure(1, weight=1)
        frame_terminal_e_grid.rowconfigure(1, weight=1)

        # Terminal
        self.tx_terminal = Text(frame_terminal_e_grid)

        try:
            self.tx_terminal.configure(self.dic_design["tx_terminal"])
        except Exception as erro:
            print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Safira.pressionar_enter_terminal(self, event))
        self.tx_terminal.bind("<KeyRelease>", lambda event: Safira.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)

        # Debug
        coluna_identificadores = ('Variavel', 'Tipo','Valor')
        fram_grid_variaveis = Frame(frame_terminal_e_grid)
        fram_grid_variaveis.grid(row=2, column=1, sticky = NSEW)

        fram_grid_variaveis.grid_columnconfigure(1, weight=1)
        fram_grid_variaveis.rowconfigure(2, weight=1)

        self.campo_busca = Entry(fram_grid_variaveis, font=("", 13))
        self.campo_busca.bind("<KeyRelease>",  lambda event: Safira.retornar_variaveis_correspondentes(self))

        self.arvores_grid = ttk.Treeview(fram_grid_variaveis, columns=coluna_identificadores, show="headings")
        vsroolb = Scrollbar(fram_grid_variaveis, orient="vertical", command=self.arvores_grid.yview)
        hsroolb = Scrollbar(fram_grid_variaveis, orient="horizontal", command=self.arvores_grid.xview)
        self.arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)

        for coluna in coluna_identificadores:
            self.arvores_grid.heading(coluna, text=coluna.title() )
            self.arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title()) + 20)

        self.campo_busca.grid(row=1, column=1, sticky=NSEW)
        self.arvores_grid.grid(row=2,column=1,  sticky=NSEW)
        vsroolb.grid(row=2,column=2, sticky='ns')
        hsroolb.grid(row=3,column=1,  sticky='ew')

        Safira.retornar_variaveis_correspondentes(self)

        self.lista_terminal_destruir = [hsroolb, self.arvores_grid, self.campo_busca, fram_grid_variaveis, frame_terminal_e_grid]

    def inicializador_terminal_producao(self):
        Safira.destruir_instancia_terminal(self)

        self.top_janela_terminal = Toplevel(self.tela)
        self.top_janela_terminal.grid_columnconfigure(1, weight=1)
        self.top_janela_terminal.rowconfigure(1, weight=1)

        self.top_janela_terminal.withdraw() # Ocultar tkinter

        t_width  = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.top_janela_terminal.geometry("720x450+{}+{}".format( int(t_width / 2 - 720 / 2), int(t_heigth / 2 - 450 / 2) ))
        self.top_janela_terminal.deiconify()

        self.tela.update()

        self.tx_terminal = Text(self.top_janela_terminal)

        try:
            self.tx_terminal.configure(self.dic_design["tx_terminal"])
        except Exception as erro:
            print("Erro 2 ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Safira.pressionar_enter_terminal(self, event))
        self.tx_terminal.bind("<KeyRelease>", lambda event: Safira.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)

    def atualiza_interface_config(self, objeto, menu):
        try:
            objeto.configure(self.dic_design[menu])
        except Exception as erro:
            print("Interface" + str(erro))

    def atualiza_design_interface(self):

        Safira.atualiza_interface_config(self, self.mn_intfc_casct_sintx, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_intfc_casct_temas, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_ferrm, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_intfc, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_loclz, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_exect, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_arqui, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_edita, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_exemp, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_barra, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_ajuda, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_sobre, "cor_menu")
        Safira.atualiza_interface_config(self, self.mn_devel, "cor_menu")
        Safira.atualiza_interface_config(self, self.bt_salva, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_playP, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_breaP, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_desfz, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_redsf, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_ajuda, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_pesqu, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.bt_brk_p, "dicBtnMenus")
        Safira.atualiza_interface_config(self, self.fr_princ, "self.fr_princ")
        Safira.atualiza_interface_config(self, self.tela, "self.tela")
        Safira.atualiza_interface_config(self, self.tx_codfc, "tx_codificacao")
        Safira.atualiza_interface_config(self, self.sb_codfc, "scrollbar_text")
        Safira.atualiza_interface_config(self, self.fr_opc_rapidas, "fr_opcoes_rapidas")

        self.linhas_laterais.aba_focada2 = self.aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas
        Safira.atualiza_interface_config(self, self.linhas_laterais, "lb_linhas")

        Safira.atualiza_interface_config(self, self.fr_abas, "dic_cor_abas_frame")
        Safira.atualiza_interface_config(self, self.fr_espaco, "dic_cor_abas_frame")

    def ativar_coordernar_coloracao(self, event = None):
        if self.dic_abas != {}:
            self.dic_abas[ self.aba_focada ]["arquivoAtual"]['texto'] = self.tx_codfc.get(1.0, END)

        self.colorir_codigo.coordena_coloracao(event, tx_codfc=self.tx_codfc)

        if event is not None:
            Safira.obterPosicaoDoCursor(self, event)

    def obterPosicaoDoCursor(self, event=None):
        try:
            numPosicao = str(self.tx_codfc.index(INSERT))
            posCorrente = int(float(self.tx_codfc.index(CURRENT)))
        except Exception as erro:
            print("Erro ao obter a posição o cursor =", erro)
        else:

            p1, p2 = str(numPosicao).split('.')
            try:
                palavra = self.tx_codfc.get('{}.{}'.format(p1, int(p2)-1), '{}.{}'.format(p1,int(p2))  )
                print("Palavra = ", palavra)
            except Exception as erro:
                print("Erro", erro)

            else:
                if event.keysym == "braceleft":
                    self.tx_codfc.insert('{}.{}'.format(p1,int(p2)), '\n    \n}' )
                    self.tx_codfc.mark_set("insert", "{}.{}".format( int(p1)+1, int(p2)+4 ))

            self.linha_p_brk_p = posCorrente

    def atualizaInterface(self, chave, novo):
        while True:
            try:
                Safira.arquivoConfiguracao(self, chave, novo)
            except Exception as e:
                print('Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas')
                return 0

            dic_comandos, self.dic_design, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

            try:
                self.colorir_codigo.alterar_cor_comando(self.cor_do_comando)
                self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc).update()
                Safira.atualiza_design_interface(self)
            except Exception as erro:
                print('ERRO: ', erro)
            else:
                print('Temas atualizados')

            self.tela.update()
            self.tx_codfc.update()

            if not self.bool_debug_temas:
                break

    def debug(self):
        messagebox.showinfo("Aviso","Debug iniciado para todos os casos")

        if self.bool_debug_temas: self.bool_debug_temas = False
        else: self.bool_debug_temas = True

    def funcoes_arquivos_configurar(self, event, comando, link=None):
        if self.controle_arquivos is None: return 0

        self.controle_arquivos.atualiza_infos(self.dic_abas, self.aba_focada, self.tx_codfc)

        if comando == "abrirArquivo":
            self.controle_arquivos.abrirArquivo(link)

        elif comando == "salvar_arquivo_dialog":
            self.controle_arquivos.salvar_arquivo_dialog(event)

        elif comando == "salvar_arquivo":
            self.controle_arquivos.salvar_arquivo(event)

        elif comando == "salvar_arquivo_como_dialog":
            self.controle_arquivos.salvar_arquivo_como_dialog(event)

        self.aba_focada = self.controle_arquivos.aba_focada
        self.dic_abas = self.controle_arquivos.dic_abas

        self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc)
        Safira.atualiza_texto_tela(self, self.aba_focada)

    def pressionar_enter_terminal(self, event = None):
        try:
            self.instancia.pressionou_enter(event)
        except Exception as erro:
            print("Impossivel detectar enter:", erro)

    def capturar_tecla_terminal(self, event):
        try:
            self.instancia.capturar_tecla( event.keysym )
        except Exception as erro:
            print("Erro ao capturar a tela", erro)

    def destruir_instancia_terminal(self):
        for widget in self.lista_terminal_destruir:
            try:
                widget.destroy()
            except Exception as e:
                print("Impossivel destruir instância: ", e)

    def retornar_variaveis_correspondentes(self):
        try:
            self.dic_variaveis = self.instancia.dic_variaveis
        except Exception as e:
            print("instancia não pronta ", e)
        else:
            self.arvores_grid.delete(*self.arvores_grid.get_children()) # IDS como argumentos

            palavra = self.campo_busca.get()
            for k, v in self.dic_variaveis.items():
                if palavra in k:
                    self.arvores_grid.insert('', END, values=(k, v[1], v[0]))

    def arquivoConfiguracao(self, chave, novo = None):
        if novo is None:
            with open('configuracoes/configuracoes.json') as json_file:
                configArquivoJson = load(json_file)
                retorno = configArquivoJson[chave]

            return retorno

        elif novo is not None:
            with open('configuracoes/configuracoes.json') as json_file:
                configArquivoJson = load(json_file)

                configArquivoJson[chave] = novo
                configArquivoJson = str(configArquivoJson).replace('\'','\"')

            file = open('configuracoes/configuracoes.json','w')
            file.write(str(configArquivoJson))
            file.close()

    def atualizacao_linhas(self, event):
        self.linhas_laterais.aba_focada2 = self.aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas
        self.linhas_laterais.desenhar_linhas()

    def modoFullScreen(self, event=None):
        if self.bool_tela_em_fullscreen: self.bool_tela_em_fullscreen = False
        else: self.bool_tela_em_fullscreen = True

        self.tela.attributes("-fullscreen", self.bool_tela_em_fullscreen)

    def ativar_logs(self, event=None):
        try:
            if self.instancia.bool_logs: self.instancia.bool_logs = False
            else: self.instancia.bool_logs = True
        except:
            print("Interpretador não iniciado")

    def adiciona_remove_breakpoint(self, event = None):
        if int(self.linha_p_brk_p) in self.dic_abas[self.aba_focada]["lst_breakpoints"]:
            self.dic_abas[self.aba_focada]["lst_breakpoints"].remove(int(self.linha_p_brk_p))
        else:
            self.dic_abas[self.aba_focada]["lst_breakpoints"].append(int(self.linha_p_brk_p))
        Safira.atualizacao_linhas(self, event = None)

    def centraliza_tela(self):
        self.tela.update()
        self.tela.withdraw() # Ocultar tkinter
        j_width  = self.tela.winfo_reqwidth()
        j_height = self.tela.winfo_reqheight()

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tela.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))
        self.tela.deiconify()
        self.tela.update()

if __name__ == "__main__":
    Safira().main()