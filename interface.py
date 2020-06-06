# -*- coding: utf-8 -*-

from libs.visualizacao     import ContadorLinhas
from libs.visualizacao     import EditorDeCodigo
from tkinter.ttk           import Treeview
from tkinter.ttk           import Style
from libs.colorir          import Colorir
from libs.arquivo          import Arquivo
from threading             import Thread
from libs.aba              import Aba
from libs.run              import Run
from tkinter               import SEL
from tkinter               import Toplevel
from tkinter               import PhotoImage
from tkinter               import messagebox
from tkinter               import Scrollbar
from tkinter               import CURRENT
from tkinter               import INSERT
from tkinter               import Button
from tkinter               import RAISED
from tkinter               import Frame
from tkinter               import Label
from tkinter               import Entry
from tkinter               import NSEW
from tkinter               import Text
from tkinter               import FLAT 
from tkinter               import Menu
from os.path               import abspath
from tkinter               import END
from update                import Atualizar
from time                  import sleep
from time                  import time
from json                  import load
from bugs                  import Bug
from os                    import getcwd
from os                    import listdir

import libs.funcoes as funcoes
import tkinter.font as tkFont
import webbrowser
import re


class Splash():
    def __init__(self, tela, dic_design):
        self.frame_splash       = None
        self.fr_splash       = None
        self.l1_splash       = None
        self.l2_splash       = None
        self.tela            = tela
        self.dic_design      = dic_design

    def splash_inicio(self):
        self.frame_splash = Frame(self.tela)

        self.frame_splash.configure(background = self.dic_design["cor_intro"]["background"])
        self.frame_splash.rowconfigure(1, weight=1)
        self.frame_splash.grid_columnconfigure(0, weight=1)

        self.fr_splash = Frame(self.frame_splash)
        self.l1_splash = Label(self.frame_splash, self.dic_design["cor_intro"])
        self.l2_splash = Label(self.frame_splash, self.dic_design["cor_intro"])

        self.fr_splash.configure(background = self.dic_design["cor_intro"]["background"])
        self.l1_splash.configure(text=" COMBRATEC ", font=( "Lucida Sans", 90), bd=80)
        self.l2_splash.configure(text="Safira IDE beta 0.2", font=("Lucida Sans", 12))

        self.frame_splash.grid(row=1, column=1, sticky=NSEW)
        self.fr_splash.grid(row=0, column=1, sticky=NSEW)
        self.l1_splash.grid(row=1, column=1, sticky=NSEW)
        self.l2_splash.grid(row=2, column=1, sticky=NSEW)
        self.frame_splash.update()

        self.tela.update()
        self.tela.withdraw()

        j_width  = self.tela.winfo_reqwidth()
        j_height = self.tela.winfo_reqheight()

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tela.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))

        self.tela.deiconify()
        self.tela.update()
    def splash_fim(self):
        self.fr_splash.grid_forget()
        self.l1_splash.grid_forget()
        self.l2_splash.grid_forget()

        self.frame_splash.grid_forget()

class Interface(Aba):
    def __init__(self, tela, dic_comandos, dic_design, cor_do_comando):
        super().__init__()

        self.cor_do_comando                  = cor_do_comando
        self.dic_comandos                    = dic_comandos
        self.dic_design                      = dic_design
        self.tela                            = tela

        self.bool_tela_em_fullscreen         = False
        self.bool_debug_temas                = False
        self.bool_logs                       = False

        self.lst_historico_abas_focadas      = []
        self.lista_terminal_destruir         = []
        self.lista_breakponts                = []
        self.lst_abas                        = []

        self.num_lin_bkp            = 0
        self.valor_threads                   = 0
        self.linha_analise                   = 0
        self.posAbsuluta                     = 0
        self.posCorrente                     = 0
        self.num_aba_focada                      = 0

        self.tx_erro_aviso_texto_erro        = None
        self.fr_erro_aviso_texto_erro        = None
        self.bt_erro_aviso_exemplo           = None
        self.bt_erro_aviso_fechar            = None
        self.controle_arquivos               = None
        self.linhas_laterais                 = None
        self.fr_opc_rapidas                  = None
        self.fr_erro_aviso                   = None
        self.frame_tela                      = None
        self.fr_princ                        = None
        self.tx_codfc                        = None
        self.ic_salva                        = None
        self.ic_playP                        = None
        self.bt_brkp1                        = None
        self.bt_lp_bk                        = None
        self.ic_PStop                        = None
        self.ic_breaP                        = None
        self.ic_brk_p                        = None
        self.ic_desfz                        = None
        self.ic_redsf                        = None
        self.ic_ajuda                        = None
        self.ic_pesqu                        = None
        self.bt_salva                        = None
        self.bt_playP                        = None
        self.bt_breaP                        = None
        self.bt_brk_p                        = None
        self.bt_desfz                        = None
        self.bt_redsf                        = None
        self.bt_ajuda                        = None
        self.bt_pesqu                        = None
        self.fr_abas                         = None
        self.bt_play                         = None

        self.arquivo_configuracoes           = funcoes.carregar_json("configuracoes/configuracoes.json")
        self.colorir_codigo                  = Colorir(self.cor_do_comando, self.dic_comandos)
        self.path                            = abspath(getcwd())

        self.bug                             = Bug(self.tela)
        self.dic_abas                        = { 0:funcoes.carregar_json("configuracoes/guia.json") }
        self.atualizar                       = Atualizar(self.tela)

    def ativar_logs(self, event=None):
        self.bool_logs = True

        if self.bool_logs:
            self.bool_logs = False

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

    def retornar_variaveis_correspondentes(self):
        try:
            dic_variaveis = self.instancia.dic_variaveis

        except Exception as e:
            print("instancia de variáveos não pronta ", e)

        else:
            self.arvores_grid.delete(*self.arvores_grid.get_children()) # IDS como argumentos

            palavra = self.campo_busca.get()

            for k, v in dic_variaveis.items():
                if palavra in k:
                    caracteres = ""
                    for x in v[0]:
                        if caracteres == "":
                            caracteres += '"' + str(x[0]) + '"'
                        else:
                            caracteres += ', "' + str(x[0]) + '"'

                    self.arvores_grid.insert('', END, values=(k, v[1], caracteres))

    def adiciona_remove_breakpoint(self, event = None):
        # Marcar um breakpoint
        if int(self.num_lin_bkp) in self.dic_abas[self.num_aba_focada]["lst_breakpoints"]:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"].remove(int(self.num_lin_bkp))

        else:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"].append(int(self.num_lin_bkp))

        # Atualizar Breakpont no interpretador
        try:
            self.instancia.lst_breakpoints = self.dic_abas[self.num_aba_focada]["lst_breakpoints"]
        except Exception as e:
            print("Programa não está em execução, bkp ignorados", e)

        Interface.atualizacao_linhas(self, event = None)

    def limpar_todos_os_breakpoints(self):
        if self.dic_abas[self.num_aba_focada]["lst_breakpoints"] == []:
            Interface.marca_todos_breakpoint(self)

        else:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = []
            Interface.atualizacao_linhas(self, event = None)

        try:
            self.instancia.lst_breakpoints = self.dic_abas[self.num_aba_focada]["lst_breakpoints"]
        except Exception as e:
            print("Programa não está em execução, bkp ignorados", e)

    def inicializa_orquestrador(self, event = None, libera_break_point_executa = False, linha_linha = False):

        print("Inicializador do orquestrador iniciado")

        """
        Inicia o oequestrador do interpretador de comandos

        :param event:
        :param libera_break_point_executa:
        :param linha_linha: Para debug linha a linha
        :return:
        """

        self.bt_playP.configure(image=self.ic_PStop)
        self.bt_playP.update()

        tipo_exec = 'producao'
        if linha_linha == True:
            if len( self.tx_codfc.get(1.0, END).split("\n") ) != len(self.instancia.lst_breakpoints):
                self.instancia.lst_breakpoints = [x for x in range(0, len(   self.tx_codfc.get(1.0, END).split("\n")  ))]
            else:
                self.instancia.bool_break_point_liberado = True

        print("\n Orquestrador iniciado")
 
        # Se o interpretador já foi iniciado e o breakpoint for falso
        try:
            print(self.instancia.numero_threads)
        except:
            print("Thread Parou")
        else:
            # interromper terminal
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
                print("Liberando programa, breakpoint liberado!")
                return 0
        else:
            bool_ignorar_todos_breakpoints = True

        inicio = time()

        self.bool_interpretador_iniciado = True
        if libera_break_point_executa:
            Interface.inicializador_terminal_debug(self)
            tipo_exec = 'debug'

        else:
            Interface.inicializador_terminal_producao(self)
            tipo_exec = 'producao'
   
        self.tx_terminal.delete('1.0', END)
        self.linha_analise = 0

        linhas = self.tx_codfc.get('1.0', END)[0:-1]
        nova_linha = ''

        lista = linhas.split('\n')
        for linha in range(len(lista)):
            nova_linha += '[{}]{}\n'.format( str(linha + 1), lista[linha] )

        # Obter o diretório base
        diretorio_base = self.dic_abas[self.num_aba_focada]["arquivoSalvo"]["link"]

        diretorio_base = re.sub('([^\/]{1,})$','', diretorio_base) # Obter diretório apenas

        linhas = nova_linha
        print("Instância criada")
        self.instancia = Run( self.tx_terminal, self.tx_codfc, self.bool_logs, self.dic_abas[self.num_aba_focada]["lst_breakpoints"], bool_ignorar_todos_breakpoints, diretorio_base)

        t = Thread(target=lambda codigoPrograma = linhas: self.instancia.orquestrador_interpretador(codigoPrograma))
        t.start()

        valor_antigo = 0

        while self.instancia.numero_threads != 0 or not self.instancia.boo_orquestrador_iniciado:
            self.tela.update()
            self.tx_codfc.update()
            self.tx_terminal.update()
            sleep(0.2)

            # Modo debug
            if tipo_exec == 'debug':
                try:

                    self.linha_analise = int(self.instancia.num_linha)
                    if self.linha_analise != valor_antigo:
                        valor_antigo = self.linha_analise
                        self.linhas_laterais.linha_analise = self.linha_analise
                        self.linhas_laterais.desenhar_linhas()
                        self.tela.update()
                        self.tx_codfc.update()
                except Exception as erro:
                    print("Erro update", erro)

        # Se o erro foi avisado
        if self.instancia.erro_alertado == True:
            if self.instancia.txt_ultima_msg_erro != "Interrompido":
                if self.instancia.txt_ultima_msg_erro != "Erro ao iniciar o Interpretador":
                    Interface.mostrar_mensagem_de_erro(self, self.instancia.txt_ultima_msg_erro, self.instancia.dir_script_aju_erro)

        print("Instância deletada")
        del self.instancia

        try:
            #self.tx_terminal.config(state=NORMAL)
            self.tx_terminal.insert(END, '\n\nScript finalizado em {:.5} segundos'.format(time() - inicio))
            self.tx_terminal.see("end")

        except Exception as erro:
            print('Impossível exibir mensagem de finalização, erro: '+ str(erro))
        
        self.linhas_laterais.linha_analise = 0
        self.linhas_laterais.desenhar_linhas()
        self.tela.update()

        self.bt_playP.configure(image=self.ic_playP)
        self.bool_interpretador_iniciado = False

    def destruir_instancia_terminal(self):

        """
        Destroe uma instância qualquer de um terminal

        :return:
        """

        for widget in self.lista_terminal_destruir:
            try:
                widget.destroy()
            except Exception as e:
                pass

            try:
                widget.grid_forget()
            except Exception as e:
                pass

    def inicializador_terminal_debug(self):

        """
        Inicia terminal lateral no modo debug
        :return:
        """

        Interface.destruir_instancia_terminal(self)
        coluna_identificadores = ('Variavel', 'Tipo','Valor')

        frame_terminal_e_grid = Frame(self.fr_princ, bg="#191913")
        frame_terminal_e_grid.grid(row=1, column=4, rowspan=2, sticky=NSEW)
        frame_terminal_e_grid.grid_columnconfigure(1, weight=1)
        frame_terminal_e_grid.rowconfigure(1, weight=1)

        fr_fechar_menu = Frame(frame_terminal_e_grid, height=10, bg="#191913")
        fr_fechar_menu.grid_columnconfigure(1, weight=1)
        fr_fechar_menu.grid(row=0, column=1, sticky=NSEW)

        bt_fechar = Button(fr_fechar_menu, text="x",fg="#f1f1f1", bg="#191913", activebackground="#191913", command = lambda event=None: Interface.destruir_instancia_terminal(self))
        bt_fechar.configure(relief=FLAT, highlightthickness=0, bd=0, font=("",12))
        bt_fechar.grid(row=0, column=1, sticky="E")

        self.tx_terminal = Text(frame_terminal_e_grid)

        try:
            self.tx_terminal.configure(self.dic_design["tx_terminal"])
        except Exception as erro:
            print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Interface.pressionar_enter_terminal(self, event))
        self.tx_terminal.bind("<KeyRelease>", lambda event: Interface.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)

        fram_grid_variaveis = Frame(frame_terminal_e_grid, bg="#222222")
        fram_grid_variaveis.grid(row=2, column=1, sticky = NSEW)

        fram_grid_variaveis.grid_columnconfigure(1, weight=1)
        fram_grid_variaveis.rowconfigure(2, weight=1)

        self.texto_busca = Label(fram_grid_variaveis, text="Faça a busca por variáveis", bg="#222222", fg="white")
        self.campo_busca = Entry(fram_grid_variaveis, font=("", 13), bg="#222222", fg="white", highlightthickness=0, insertbackground="white")
        self.campo_busca.bind("<KeyRelease>",  lambda event: Interface.retornar_variaveis_correspondentes(self))

        style = Style()
        style.theme_use("clam")

        style.configure("Custom.Treeview", background="#222222", fieldbackground="#222222", foreground="white")
        style.map("Custom.Treeview.Heading", relief=[('active','flat'),('pressed','flat')])

        self.arvores_grid = Treeview(fram_grid_variaveis, columns=coluna_identificadores, show="headings", style="Custom.Treeview")
        self.arvores_grid.tag_configure('RED_TAG', foreground='red', font=('arial', 12))

        vsroolb = Scrollbar(fram_grid_variaveis, orient="vertical", command=self.arvores_grid.yview, bg="#222222", bd=0, relief=FLAT, highlightthickness=0, activebackground="#222232")
        hsroolb = Scrollbar(fram_grid_variaveis, orient="horizontal", command=self.arvores_grid.xview, bg="#222222", bd=0, relief=FLAT, highlightthickness=0, activebackground="#222232")

        self.arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)
        
        for coluna in coluna_identificadores:
            self.arvores_grid.heading(coluna, text=coluna.title())#, selectmode="#f1a533")
            self.arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title()) + 20 )#, selectmode="orange")

        self.texto_busca.grid(row=0, column=1, sticky=NSEW)
        self.campo_busca.grid(row=1, column=1, sticky=NSEW)
        self.arvores_grid.grid(row=2,column=1,  sticky=NSEW)

        vsroolb.grid(row=2,column=2, sticky='ns')
        hsroolb.grid(row=3,column=1,  sticky='ew')

        Interface.retornar_variaveis_correspondentes(self)
        self.lista_terminal_destruir = [frame_terminal_e_grid, fram_grid_variaveis, self.arvores_grid, self.tx_terminal, self.texto_busca, self.campo_busca, fr_fechar_menu, bt_fechar, vsroolb, hsroolb]

    def inicializador_terminal_producao(self):

        """
        Inicia o terminal sem o debug e na tela central

        :return:
        """

        Interface.destruir_instancia_terminal(self)

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

        self.tx_terminal.bind('<Return>', lambda event: Interface.pressionar_enter_terminal(self, event))
        self.tx_terminal.bind("<KeyRelease>", lambda event: Interface.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)
        self.lista_terminal_destruir = [self.top_janela_terminal, self.tx_terminal]


    def inicioScreen(self):

        self.tela.overrideredirect(0) # Traz barra de titulo
        self.tela.withdraw() # Ocultar tkinter

        self.frame_tela = Frame(self.tela)
        self.frame_tela.grid(row=1, column=1, sticky=NSEW)
        self.frame_tela.update()

        comando_abriro_arquivo = lambda event = None: Interface.funcoes_arquivos_configurar(self, None, "salvar_arquivo_dialog")
        comando_salvararq_como = lambda event = None: Interface.funcoes_arquivos_configurar(self, None, "salvar_arquivo_como_dialog")
        comando_acao_salvararq = lambda event = None: Interface.funcoes_arquivos_configurar(self, None, "salvar_arquivo")
        comando_executar_brakp = lambda event = None: Interface.inicializa_orquestrador(self, libera_break_point_executa = True)
        comando_inserir_breakp = lambda event = None: Interface.adiciona_remove_breakpoint(self, event)
        comando_parar_execucao = lambda event = None: Interface.inicializa_orquestrador(self, event)
        comando_executar_linha = lambda event = None: Interface.inicia_marca_break_point_geral(self) 
        comando_limpa_breakpon = lambda event = None: Interface.limpar_todos_os_breakpoints(self) 
        comando_executar_progr = lambda event = None: Interface.inicializa_orquestrador(self)
        comando_abrir_nova_aba = lambda event = None: Interface.nova_aba(self, event)
        comando_ativar_fullscr = lambda event: Interface.modoFullScreen(self, event)
        comando_abrir_disponiv = lambda: webbrowser.open(self.path + "/tutorial/comando.html") 
        comando_abrir_comunida = lambda: webbrowser.open("https://safiraide.blogspot.com/p/comunidade.html") 
        comando_abrirl_projeto = lambda: webbrowser.open("http://safiraide.blogspot.com/") 
        comando_abrirlnk_ajuda = lambda: webbrowser.open(self.path + "/tutorial/comando.html") 
        comando_ativaropc_logs = lambda: Interface.ativar_logs(self)
        comando_ativarop_debug = lambda: Interface.debug(self)

        self.tela.bind('<Control-n>', comando_abrir_nova_aba)
        self.tela.bind('<Control-s>', comando_acao_salvararq)
        self.tela.bind('<Control-o>', comando_abriro_arquivo)
        self.tela.bind('<Control-S>', comando_salvararq_como)
        self.tela.bind('<F5>', comando_executar_progr)
        self.tela.bind('<F6>', comando_executar_linha)
        self.tela.bind('<F7>', comando_executar_brakp)
        self.tela.bind('<F10>', comando_inserir_breakp)
        self.tela.bind('<F11>', comando_ativar_fullscr)

        self.tela.title('Combratec -  Safira IDE')
        self.tela.call('wm', 'iconphoto', self.tela._w, PhotoImage(file='imagens/icone.png'))

        self.frame_tela.rowconfigure(2, weight=1)
        self.frame_tela.grid_columnconfigure(1, weight=1)

        # ************************** MENUS ************************** #

        self.mn_barra = Menu(self.tela)
        self.tela.config(menu=self.mn_barra)

        self.mn_intfc = Menu( self.mn_barra)
        self.mn_exect = Menu( self.mn_barra)
        self.mn_exemp = Menu( self.mn_barra)
        self.mn_arqui = Menu( self.mn_barra)
        self.mn_edita = Menu( self.mn_barra)
        self.mn_ajuda = Menu( self.mn_barra)
        self.mn_devel = Menu( self.mn_barra)

        self.mn_barra.add_cascade(label='  Arquivo', menu=self.mn_arqui)
        self.mn_barra.add_cascade(label='  Executar', menu=self.mn_exect)
        self.mn_barra.add_cascade(label='  Exemplos', menu=self.mn_exemp)
        self.mn_barra.add_cascade(label='  Interface', menu=self.mn_intfc)
        self.mn_barra.add_cascade(label='  Ajuda/Sobre', menu=self.mn_ajuda)
        self.mn_barra.add_cascade(label='  Dev', menu=self.mn_devel)

        self.mn_arqui.add_command(label='  Abrir arquivo (Ctrl+O)', command= comando_abriro_arquivo)
        self.mn_arqui.add_command(label='  Nova Aba (Ctrl-N)', command = comando_abrir_nova_aba)
        self.mn_arqui.add_separator()
        self.mn_arqui.add_command(label='  Salvar (Ctrl-S)', command= comando_acao_salvararq)
        self.mn_arqui.add_command(label='  Salvar Como (Ctrl-Shift-S)', command=comando_salvararq_como)

        self.mn_exect.add_command(label='  Executar Tudo (F5)', command=comando_executar_progr)
        self.mn_exect.add_command(label='  Executar linha por linha (F6)', command = comando_executar_linha)
        self.mn_exect.add_command(label='  Executar até breakpoint (F7)', command=comando_executar_brakp)
        self.mn_exect.add_command(label='  Parar execução (F9)', command = comando_parar_execucao)
        self.mn_exect.add_command(label='  Inserir breakpoint (F10)', command = comando_inserir_breakp)

        Interface.cascate_scripts(self)
        Interface.cascate_temas_temas(self)
        Interface.cascate_temas_sintaxe(self)

        self.mn_ajuda.add_command( label='  Ajuda (F1)', command= comando_abrirlnk_ajuda)
        self.mn_ajuda.add_command( label='  Comandos Disponíveis', command=comando_abrir_disponiv)
        self.mn_ajuda.add_separator()
        self.mn_ajuda.add_command( label='  Reportar um Bug', command= lambda event=None: self.bug.interface())
        self.mn_ajuda.add_command( label='  Verificar Atualização', command= lambda event=None: self.atualizar.verificar_versao())

    
        self.mn_devel.add_command( label='  Logs', command= comando_ativaropc_logs )
        #self.mn_devel.add_command( label='  Debug', command= comando_ativarop_debug )

        self.ic_salva = PhotoImage( file='imagens/ic_salvar.png' )
        self.ic_playP = PhotoImage( file='imagens/ic_play.png' )
        self.ic_PStop = PhotoImage( file='imagens/ic_parar.png' )
        self.ic_breaP = PhotoImage( file='imagens/ic_play_breakpoint.png' )
        self.ic_brk_p = PhotoImage( file='imagens/breakPoint.png' )
        self.ic_brkp1 = PhotoImage( file='imagens/ic_play_breakpoint_um.png' )
        self.ic_ajuda = PhotoImage( file='imagens/ic_duvida.png' )
        self.ic_pesqu = PhotoImage( file='imagens/ic_pesquisa.png' )
        self.ic_nsalv = PhotoImage( file="imagens/nao_salvo.png" )
        self.iclp_bkp = PhotoImage( file="imagens/limpar_bkp.png" )

        self.ic_salva = self.ic_salva.subsample(4, 4)
        self.ic_playP = self.ic_playP.subsample(4, 4)
        self.ic_PStop = self.ic_PStop.subsample(4, 4)
        self.ic_breaP = self.ic_breaP.subsample(4, 4)
        self.ic_brk_p = self.ic_brk_p.subsample(4, 4)
        self.ic_ajuda = self.ic_ajuda.subsample(4, 4)
        self.ic_pesqu = self.ic_pesqu.subsample(4, 4)
        self.ic_nsalv = self.ic_nsalv.subsample(2, 2)
        self.ic_brkp1 = self.ic_brkp1.subsample(4, 4)
        self.iclp_bkp = self.iclp_bkp.subsample(4, 4)
        

        # ************ Icones de opções rápidas ************** #

        self.fr_opc_rapidas = Frame(self.frame_tela)

        self.bt_salva = Button( self.fr_opc_rapidas, image=self.ic_salva, command = comando_acao_salvararq )
        self.bt_playP = Button( self.fr_opc_rapidas, image=self.ic_playP, command = comando_executar_progr )
        self.bt_breaP = Button( self.fr_opc_rapidas, image=self.ic_breaP, command = comando_executar_brakp )
        self.bt_brk_p = Button( self.fr_opc_rapidas, image=self.ic_brk_p, command = comando_inserir_breakp )
        self.bt_brkp1 = Button( self.fr_opc_rapidas, image=self.ic_brkp1, command = comando_executar_linha )
        self.bt_lp_bk = Button( self.fr_opc_rapidas, image=self.iclp_bkp, command = comando_limpa_breakpon )
        self.bt_ajuda = Button( self.fr_opc_rapidas, image=self.ic_ajuda)
        self.bt_pesqu = Button( self.fr_opc_rapidas, image=self.ic_pesqu)

        self.fr_princ = Frame(self.frame_tela)
        self.fr_princ.grid_columnconfigure(2, weight=1)
        self.fr_princ.rowconfigure(1, weight=1)

        self.fr_abas = Frame(self.fr_princ, height=20)
        self.fr_abas.rowconfigure(1, weight=1)
        self.fr_espaco = Label(self.fr_abas, width=5)

        Interface.renderizar_abas_inicio(self)

        # ************ Tela de desenvolvimento do código ****************** #

        self.tx_codfc = EditorDeCodigo(self.fr_princ, undo=True, autoseparators=True, maxundo = 50, tabs=4)
        self.tx_codfc.focus_force()

        self.tx_codfc.bind('<Control-c>', lambda event=None:Interface.copiar_selecao(self))
        self.tx_codfc.bind("<<Paste>>", lambda event=None:Interface.colar_selecao(self))
        self.tx_codfc.bind('<Control-a>', lambda event=None:Interface.selecione_tudo(self))

        self.tx_codfc.bind("<<Change>>", lambda event: Interface.atualizacao_linhas(self, event))
        self.tx_codfc.bind("<Configure>", lambda event: Interface.atualizacao_linhas(self, event))
        self.tx_codfc.bind('<Button>', lambda event:  Interface.obterPosicaoDoCursor(self, event))
        self.tx_codfc.bind('<KeyRelease>', lambda event = None: Interface.ativar_coordernar_coloracao(self, event))
        self.tx_codfc.bind('<Control-MouseWheel>', lambda event: Interface.mudar_fonte(self, "+") if int(event.delta) > 0 else Interface.mudar_fonte(self, "-"))

        self.sb_codfc = Scrollbar(self.fr_princ, orient="vertical", command=self.tx_codfc.yview, relief=FLAT)
        self.tx_codfc.configure(yscrollcommand=self.sb_codfc.set)

        self.linhas_laterais = ContadorLinhas(self.fr_princ, self.dic_design)
        self.linhas_laterais.aba_focada2 = self.num_aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas
        self.linhas_laterais.atribuir(self.tx_codfc)

        self.fr_espaco.grid(row=1, column=0, sticky=NSEW)
        self.fr_opc_rapidas.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        self.bt_salva.grid(row=1, column=1)
        self.bt_playP.grid(row=1, column=4)
        self.bt_breaP.grid(row=1, column=5)
        self.bt_brk_p.grid(row=1, column=6)
        self.bt_brkp1.grid(row=1, column=7)
        self.bt_lp_bk.grid(row=1, column=8)
        self.bt_ajuda.grid(row=1, column=10)
        self.bt_pesqu.grid(row=1, column=11)
        self.fr_princ.grid(row=2, column=1, sticky=NSEW)
        self.fr_abas.grid(row=0, column=1, columnspan=4, sticky=NSEW)
        self.linhas_laterais.grid(row=1, column=1, sticky=NSEW)
        self.tx_codfc.grid(row=1, column=2, sticky=NSEW)
        self.sb_codfc.grid(row=1, column=3, sticky=NSEW)

        # ******** Manipulação dos arquivos **************** #
        self.controle_arquivos = Arquivo(self.dic_abas, self.num_aba_focada, self.tx_codfc)
        Interface.atualiza_design_interface(self)

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        Aba.tela = self.tela
        self.tela.geometry("{}x{}+0+0".format(t_width - 1, t_heigth - 1 ))
        self.colorir_codigo.tela = self.tela

        #Interface.funcoes_arquivos_configurar(self, None, "abrirArquivo", 'script.fyn')

        self.tela.deiconify()
        self.tela.update()

        self.atualizar.verificar_versao(primeira_vez=True)

        self.tela.mainloop()

    def cascate_temas_temas(self):

        self.mn_intfc_casct_temas = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  Temas', menu=self.mn_intfc_casct_temas)

        for file in listdir('temas/'):
            if 'theme.json' in file:
                funcao = lambda link = file: Interface.atualiza_dados_interface(self, 'tema', str(link))

                if self.arquivo_configuracoes["tema"] == file: file = "*" + file
                else: file = " " + file

                self.mn_intfc_casct_temas.add_command(label=file, command=funcao)

    def cascate_temas_sintaxe(self):

        self.mn_intfc_casct_sintx = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  sintaxe', menu=self.mn_intfc_casct_sintx)

        for file in listdir('temas/'):
            if 'sintaxe.json' in file:
                funcao = lambda link = file: Interface.atualiza_dados_interface(self, 'sintaxe', str(link))

                if self.arquivo_configuracoes["sintaxe"] == file: file = "*" + file
                else: file = " " + file

                self.mn_intfc_casct_sintx.add_command(label=file, command=funcao)

    def cascate_scripts(self):

        for file in listdir('scripts/'):
            if len(file) > 5:
                if file[-3:] == 'fyn':
                    funcao = lambda link = file:  Interface.abrir_script(self, link)
                    self.mn_exemp.add_command(label="  " + file + "  ", command = funcao)

    def abrir_script(self, link):

        Interface.nova_aba(self, None)
        Interface.funcoes_arquivos_configurar(self, None, "abrirArquivo" , 'scripts/' + str(link) )

    def fechar_um_widget_erro(self, objeto):

        try:
            objeto.grid_forget()
        except Exception as e:
            print("Erro ao destruir widget de erro", e)

    def abrir_script_mensagem_erro(self, dir_script):

        Interface.nova_aba(self)
        Interface.funcoes_arquivos_configurar(self, None, "abrirArquivo" , 'scripts/'+dir_script)

    def fechar_mensagem_de_erro(self, remover_marcacao = True):

        Interface.fechar_um_widget_erro(self, self.bt_erro_aviso_fechar )
        Interface.fechar_um_widget_erro(self, self.bt_erro_aviso_exemplo )
        Interface.fechar_um_widget_erro(self, self.tx_erro_aviso_texto_erro )
        Interface.fechar_um_widget_erro(self, self.fr_erro_aviso_texto_erro )
        Interface.fechar_um_widget_erro(self, self.fr_erro_aviso )

        if remover_marcacao:
            self.tx_codfc.tag_delete("codigoErro")

    def debug(self):

        if self.bool_debug_temas:
            messagebox.showinfo("Aviso","Debug de temas finalizado")
            self.bool_debug_temas = False
        else:
            messagebox.showinfo("Aviso","Debug de temas Iniciado")
            self.bool_debug_temas = True

    def atualizacao_linhas(self, event):

        self.linhas_laterais.aba_focada2 = self.num_aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas
        self.linhas_laterais.desenhar_linhas()
        self.tela.update()

    def modoFullScreen(self, event=None):

        if self.bool_tela_em_fullscreen: self.bool_tela_em_fullscreen = False
        else: self.bool_tela_em_fullscreen = True

        self.tela.attributes("-fullscreen", self.bool_tela_em_fullscreen)
        self.tela.update()

    # **************** AÇÕES DIRETAS DO TEXT **********************#
    def copiar_selecao(self):

        print('copy')
        self.tx_codfc.event_generate("<<Copy>>")

    def colar_selecao(self):

        try:
            self.tx_codfc.delete("sel.first", "sel.last")
        except:
            pass
        self.tx_codfc.insert("insert", self.tx_codfc.clipboard_get())
        return "break"

    def selecione_tudo(self):

        self.tx_codfc.tag_add(SEL, "1.0", END)
        self.tx_codfc.mark_set(INSERT, "1.0")
        self.tx_codfc.see(INSERT)
        return 'break'

    def marca_todos_breakpoint(self):
        self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = [ x for x in range(len(self.tx_codfc.get(1.0, END)))]
        Interface.atualizacao_linhas(self, event = None)

    def inicia_marca_break_point_geral(self):

        """
        Configura um breakpoint em todo os código focado

        :return:
        """

        Interface.marca_todos_breakpoint(self)
        self.tx_codfc.update()

        Interface.inicializa_orquestrador(self, libera_break_point_executa = True)

    def mostrar_mensagem_de_erro(self, msg_erro, dir_script):

        try:
            Interface.fechar_mensagem_de_erro(self, remover_marcacao = False)
        except Exception as e:
            print("Não foi possível abrir uma possível mensagem de erro", e)

        self.fr_erro_aviso = Frame(self.fr_princ, height=50, bg="#111121", bd=10, highlightthickness=10, highlightbackground="#222232", highlightcolor="#222232")
        self.fr_erro_aviso.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso.grid(row = 2, column = 2, sticky = NSEW)

        self.fr_erro_aviso_texto_erro = Frame(self.fr_erro_aviso, bg="#111121")
        self.fr_erro_aviso_texto_erro.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        self.tx_erro_aviso_texto_erro = Text(self.fr_erro_aviso_texto_erro, bg="#111121", fg="#ff9696", height=2, highlightthickness=0, relief=FLAT)
        self.tx_erro_aviso_texto_erro.insert(1.0, msg_erro)
        self.tx_erro_aviso_texto_erro.configure(state="disable", selectbackground = "#222232")
        self.tx_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        if dir_script != "":
            self.bt_erro_aviso_exemplo = Button(self.fr_erro_aviso, text="Ver um exemplo ", relief="flat", fg="green",activeforeground="green", bg="#111121", activebackground="#111121", font=("", 13), command=lambda abc = self: Interface.abrir_script_mensagem_erro(abc, dir_script))
            self.bt_erro_aviso_exemplo.grid(row=1, column=2)

        self.bt_erro_aviso_fechar = Button(self.fr_erro_aviso, text="x", relief="sunken", fg="#ff9696",activeforeground="#ff9696", bg="#111121", activebackground="#111121", font=("", 13), highlightthickness=0, bd=0, command=lambda abc = self: Interface.fechar_mensagem_de_erro(abc))
        self.bt_erro_aviso_fechar.grid(row=1, column=3)

    def mudar_fonte(self, acao):

        print("mmudar a fonte")

        if acao == "+": adicao = 1
        else: adicao = -1

        self.dic_design["cor_menu"]["font"][1] = int(self.dic_design["cor_menu"]["font"][1]) + adicao
        self.dic_design["lb_sobDeTitulo"]["font"][1] = int(self.dic_design["lb_sobDeTitulo"]["font"][1]) + adicao
        self.dic_design["dicBtnMenus"]["font"][1] = int(self.dic_design["dicBtnMenus"]["font"][1]) + adicao
        self.dic_design["tx_terminal"]["font"][1] = int(self.dic_design["tx_terminal"]["font"][1]) + adicao
        self.dic_design["tx_codificacao"]["font"][1] = int(self.dic_design["tx_codificacao"]["font"][1]) + adicao
        self.dic_design["fonte_ct_linha"]["font"][1] = int(self.dic_design["fonte_ct_linha"]["font"][1]) + adicao
        self.dic_design["fonte_ct_linha"]["width"] = int(self.dic_design["fonte_ct_linha"]["width"]) + adicao

        self.tx_codfc.configure(self.dic_design["tx_codificacao"])
        self.linhas_laterais.desenhar_linhas()
        self.tela.update()


    def atualiza_interface_config(self, objeto, menu):

        """
        Atualiza de forma individual um tema, se baseando no objeto e na chave do docionário de design

        :param objeto: Objeto para atualizar
        :param menu: Chave das configurações
        :return:
        """
        try:
            objeto.configure(self.dic_design[menu])
            objeto.update()

        except Exception as erro:
            print("Erro Atualiza interface config = " + str(erro))

    def atualiza_design_interface(self):

        """
        Atualiza a cor das interfaces do programa

        :return:
        """

        Interface.atualiza_interface_config(self, self.mn_intfc_casct_sintx, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_intfc_casct_temas, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_intfc, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_exect, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_arqui, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_edita, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_exemp, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_barra, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_ajuda, "cor_menu")
        Interface.atualiza_interface_config(self, self.mn_devel, "cor_menu")
        Interface.atualiza_interface_config(self, self.bt_salva, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_playP, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_breaP, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_desfz, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_redsf, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_ajuda, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_pesqu, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_brk_p, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_brkp1, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.bt_lp_bk, "dicBtnMenus")
        Interface.atualiza_interface_config(self, self.fr_princ, "fr_princ")
        Interface.atualiza_interface_config(self, self.tela, "tela")
        Interface.atualiza_interface_config(self, self.tx_codfc, "tx_codificacao")
        Interface.atualiza_interface_config(self, self.sb_codfc, "scrollbar_text")
        Interface.atualiza_interface_config(self, self.fr_opc_rapidas, "fr_opcoes_rapidas")

        self.linhas_laterais.aba_focada2 = self.num_aba_focada
        self.linhas_laterais.dic_abas2 = self.dic_abas

        Interface.atualiza_interface_config(self, self.linhas_laterais, "lb_linhas")

        Interface.atualiza_interface_config(self, self.fr_abas, "dic_cor_abas_frame")
        Interface.atualiza_interface_config(self, self.fr_espaco, "dic_cor_abas_frame")

    def atualiza_dados_interface(self, chave, novo):

        """
        Coordena a atualização do arquivo de coloração e coordena a atualização de cores

        :param chave: chave de acesso do arquivo de configurações
        :param novo: Novo valor para o arquivo de configurações
        :return:
        """
        while True:
            try:
                Interface.arquivoConfiguracao(self, chave, novo)
            except Exception as e:
                print('Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas')
                return 0

            dic_comandos, self.dic_design, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

            try:
                self.colorir_codigo.aba_focada = self.num_aba_focada
                self.colorir_codigo.alterar_cor_comando(self.cor_do_comando)
                #self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc, primeira_vez=True).update()

                Interface.atualiza_design_interface(self)
                self.linhas_laterais.aba_focada2 = self.num_aba_focada
                self.linhas_laterais.dic_abas2 = self.dic_abas

            except Exception as erro:
                print('ERRO: ', erro)
            else:
                print('Temas atualizados')

            self.tela.update()
            self.tx_codfc.update()

            if not self.bool_debug_temas:
                break
    
    def ativar_coordernar_coloracao(self, event = None):

        """
        Recebe um evento do de uma tecla pressionado ou apenas uma chamada e realiza procedimentos de acordo com
        cada caractere digitado

        :param event: Evento do tipo clique ou None
        :return:
        """

        self.colorir_codigo.aba_focada = self.num_aba_focada
        self.colorir_codigo.coordena_coloracao(event, tx_codfc=self.tx_codfc)
        #Thread(target= lambda event=event: Interface.th_confirm(self, event)).start()

        if self.dic_abas != {}:
            self.dic_abas[ self.num_aba_focada ]["arquivoAtual"]['texto'] = self.tx_codfc.get(1.0, END)

            if self.dic_abas[ self.num_aba_focada ]["arquivoAtual"]['texto'] != self.dic_abas[ self.num_aba_focada ]["arquivoSalvo"]['texto']:

                if self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] == False:
                    self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = True

                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()

                    # Mantendo o tamnho
                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()
                    self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(image=self.ic_nsalv, width=largura_original)

            else:
                self.dic_abas[self.num_aba_focada]["listaAbas"][3].config(image='', width=0)
                self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = False

            self.dic_abas[self.num_aba_focada]["listaAbas"][3].update()

        if hasattr(event, "keysym"):
            Interface.obterPosicaoDoCursor(self, event)
        
    def obterPosicaoDoCursor(self, event=None):

        """
        Salva a posição clicada com o mouse e análisa o caractere que foi digitado, para aplicar efeitos como {}
        :param event: Evento
        :return:
        """
        try:
            numPosicao = str(self.tx_codfc.index(INSERT))
            posCorrente = int(float(self.tx_codfc.index(CURRENT)))

        except Exception as erro:
            print("Erro ao obter a posição o cursor =", erro)

        else:
            p1, p2 = str(numPosicao).split('.')
            if event.keysym == "braceleft" or event.keysym == "{":
                self.tx_codfc.insert('{}.{}'.format(p1,int(p2)), '\n    \n}' )
                self.tx_codfc.mark_set("insert", "{}.{}".format( int(p1)+1, int(p2)+4 ))

            self.num_lin_bkp = posCorrente

    def funcoes_arquivos_configurar(self, event, comando, link=None):

        if self.controle_arquivos is None: return 0
        retorno_salvar_como = None

        self.controle_arquivos.atualiza_infos(self.dic_abas, self.num_aba_focada, self.tx_codfc)

        if comando == "abrirArquivo": self.controle_arquivos.abrirArquivo(link)
        elif comando == "salvar_arquivo_dialog": self.controle_arquivos.salvar_arquivo_dialog(event)
        elif comando == "salvar_arquivo": retorno_salvar_como = self.controle_arquivos.salvar_arquivo(event)
        elif comando == "salvar_arquivo_como_dialog": self.controle_arquivos.salvar_arquivo_como_dialog(event)

        self.num_aba_focada = self.controle_arquivos.aba_focada
        self.dic_abas = self.controle_arquivos.dic_abas

        if comando in ["abrirArquivo", "salvar_arquivo_como_dialog", "salvar_arquivo_dialog"] or retorno_salvar_como == "salvar_arquivo_como_dialog":
            Interface.atualiza_texto_tela(self, self.num_aba_focada)

    def arquivoConfiguracao(self, chave, novo = None):

        if novo is None:
            with open('configuracoes/configuracoes.json', encoding='utf8') as json_file:
                configArquivoJson = load(json_file)
                retorno = configArquivoJson[chave]
            return retorno

        elif novo is not None:
            with open('configuracoes/configuracoes.json', encoding='utf8') as json_file:
                configArquivoJson = load(json_file)

                configArquivoJson[chave] = novo
                configArquivoJson = str(configArquivoJson).replace('\'','\"')

            file = open('configuracoes/configuracoes.json','w')
            file.write(str(configArquivoJson))
            file.close()
