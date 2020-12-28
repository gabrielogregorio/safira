from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import Frame
from subprocess import run as subprocess_run
from subprocess import PIPE as subprocess_PIPE
from copy import deepcopy
from tkinter import CURRENT
from telas.tutorial import Tutorial
from tkinter import INSERT
from tkinter import RAISED
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import NSEW
from tkinter import Text
from tkinter import Menu
from tkinter import FLAT
from tkinter import END
from tkinter import SEL
from tkinter import Tk
from tkinter import N
from tkinter import W
from tkinter.ttk import Treeview
from tkinter.ttk import Style
import tkinter.font as tkFont
from threading import Thread
from os.path import abspath
from os.path import join
from time import sleep
from time import time
from os import getcwd
from os import listdir
from re import compile
from sys import version
from webbrowser import open as webbrowser_open
from util.funcoes import carregar_json
from util.arquivo import Arquivo
import util.funcoes as funcoes
from telas.escolher_idioma import Idioma
from telas.visualizacao import ContadorLinhas
from telas.visualizacao import EditorDeCodigo
from telas.atualizar import Atualizar
from telas.colorir import Colorir
from telas.splash import Splash
from telas.design import Design
from telas.bug import Bug
from logs.log import Log
from re import search as re_search
from re import sub as re_sub
from interpretador.interpretador import Interpretador
from interpretador.Configurar import ConfigurarInterpretador


def carregar_fonte():
    erro = ""
    try:
        # Carregamento da fonte
        from pyglet import resource
        from pyglet import font
        from pyglet import window

        # fonte_terminal = 'fonte/Roboto_Mono/RobotoMono-Regular.ttf'
        fonte_sistema = 'fonte/OpenSans/OpenSans-Regular.ttf'
        fonte_terminal = 'fonte/Consolas/ConsolaMono.ttf'

        fontes =  ['Roboto Mono', 'Open Sans', 'Consola Mono']
        _ = font.load(name = fontes, dpi=400.0, size=14)

        resource.add_font(fonte_terminal)
        resource.add_font(fonte_sistema)

    except ModuleNotFoundError:
        erro = "Você precisa instalar a biblioteca pyglet para que as fontes sejam carregadas"

    except Exception as e:
        erro = e

    if erro != "":
        print("Erro a carregar fonte"+str(erro))

carregar_fonte()


class Interface:
    def __init__(self, master, icon):
        """ Classe da interface principal"""

        # Oculta a contrução da interface
        self.master = master
        self.master.withdraw()
        self.icon = icon

        self.historico_coloracao = []

        # Design da interface
        self.design = Design()
        self.design.update_design_dic()

        # Splash Screen
        self.splash = Splash(self.design)

        # Botões de erro que podem aparecer
        self.tx_erro_aviso_texto_erro = None
        self.fr_erro_aviso_texto_erro = None
        self.bt_erro_aviso_exemplo = None
        self.bt_erro_aviso_fechar = None
        self.fr_erro_aviso = None

        self.esperar_pressionar_enter = False
        self.interpretador_finalizado = True
        self.bool_full_screen = False
        self.bool_debug_temas = False
        self.libera_bkp = False
        self.bool_logs = False

        self.lst_historico_abas_focadas = [0]
        self.lista_terminal_destruir = []
        self.lista_breakponts = []

        self.num_coloracao_acionados = 0
        self.num_aba_focada = 0
        self.linha_analise = 0
        self.num_lin_bkp = 0

        self.interpretador_status = 'parado'
        self.regex_interpretador = compile(r"^\:(.*?)\:(.*?)\:(.*?)\:(.*)")

        try:
            self.style_terminal = self.carregar_estilos_terminal()
        except Exception as e:
            print(e)
            self.style_terminal = Style()
            self.style_terminal.theme_use("clam")


        self.dic_imgs = {"pt-br": "ic_pt_br.png", "en-us": "ic_en_us.png", "es": "ic_es.png"}

        # Dicionário de configurações da Safira
        self.arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

        # Dicionário de Scripts de aprendizado
        self.arquivo_scripts = funcoes.carregar_json("configuracoes/scripts.json")

        # Dicionario de modelo padrão de Aba
        self.dic_abas = {0: funcoes.carregar_json("configuracoes/guia.json")}

        # Idioma Atual
        self.idioma = self.arquivo_configuracoes['idioma']

        # Textos em cada Idioma
        self.interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

        # Dicionário de comandos disponíveis
        self.dic_comandos, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

        # Carrega os dicionários em uma variável para novo tipo de coloração
        self.dic_coloracao = {}
        for k, self.dic_comando in self.dic_comandos.items():
            for comando in self.dic_comando['comando']:
                com, cor = comando[0], self.cor_do_comando[self.dic_comando['cor']]['foreground']
                if not com.strip() == "":
                    self.dic_coloracao[com] = cor
        #print(self.dic_coloracao)

        # Classes
        # Registro de logs
        self.log = Log()

        # Verificações de bugs
        self.bug = Bug(self.master, self.design, self.idioma, self.interface_idioma, self.icon)

        # Verificações de versões diponíveis para atualizar
        self.atualizar = Atualizar(self.master, self.design, self.idioma, self.interface_idioma, self.icon)

        # Coloração de código
        self.colorir_codigo = Colorir(self.cor_do_comando, self.dic_comandos)

        # Escolha do idioma
        self.escolher_idioma = Idioma(self.master,  self.design, self.idioma, self.interface_idioma, self.icon)

        # Inserção de log
        self.log.adicionar_novo_acesso('logs/registros.json', 'acessos')

        # Caminho atual
        self.path = abspath(getcwd())

        # Instância do interpretador 
        self.instancia = None


        configurar_interpretador = ConfigurarInterpretador()
        self.dicLetras = configurar_interpretador.carregar_dicionario_letra(self.dic_comandos)
        self.dic_regex_compilado, self.re_comandos = configurar_interpretador.gerar_regex_compilado_interpretador(self.dicLetras, self.dic_comandos, self.idioma)
        del configurar_interpretador

        # Interface do sistema
        # Tela Principal
        self.fr_tela = Frame(master)
        self.fr_tela.grid(row=1, column=1, sticky=NSEW)
        self.fr_tela.update()
        self.fr_tela.rowconfigure(2, weight=1)
        self.fr_tela.grid_columnconfigure(1, weight=1)

        # COMANDOS
        cm_abrir_arquivo = lambda event=None: self.manipular_arquivos(None, "abrir_arquivo_dialog")
        cm_salvar_arquivo_como = lambda event=None: self.manipular_arquivos(None, "salvar_arquivo_como_dialog")
        cm_acao_salva_arquivo = lambda event=None: self.manipular_arquivos(None, "salvar_arquivo")
        cm_inserir_bkp = lambda event=None: self.adicionar_remover_breakpoint(event)
        cm_executar_bkp = lambda event=None: self.liberar_breakpoint_ou_inicicar(tipo_execucao='debug')
        cm_parar_execucao = lambda event=None: self.inicializar_interpretador(tipo_execucao='parar')
        cm_executar_programa = lambda event=None: self.inicializar_interpretador(tipo_execucao='continua')
        cm_limpa_breakpoints = lambda event=None: self.limpar_breakpoints()
        cm_abrir_abrir_nova_aba = lambda event=None: self.abrir_nova_aba(event)
        cm_ativar_fullscreen = lambda event: self.ativar_desativar_full_screen(event)
        cm_abrir_disponiv = lambda: webbrowser_open(self.path + "/tutorial/comando.html")
        cm_abrir_comunida = lambda: webbrowser_open("https://safiraide.blogspot.com/p/comunidade.html")
        cm_abrirl_projeto = lambda: webbrowser_open("http://safiraide.blogspot.com/")
        cm_ativaropc_logs = lambda: self.ativar_logs()
        cm_ativarop_debug = lambda: self.ativar_modo_debug_temas()
        cm_atualizar_idioma = lambda: self.atualizar_idioma()
        cm_aumentar_fonte = lambda: self.aumentar_diminuir_fonte("+")
        cm_diminuir_fonte = lambda: self.aumentar_diminuir_fonte("-")
        cm_copiar = lambda: self.copiar_selecao()
        cm_colar = lambda: self.colar_selecao()

        # TECLAS DE ATALHOS
        self.master.bind('<Control-n>', cm_abrir_abrir_nova_aba)
        self.master.bind('<Control-s>', cm_acao_salva_arquivo)
        self.master.bind('<Control-o>', cm_abrir_arquivo)
        self.master.bind('<Control-S>', cm_salvar_arquivo_como)
        self.master.bind('<F5>', cm_executar_programa)
        self.master.bind('<F7>', cm_executar_bkp)
        self.master.bind('<F10>', cm_inserir_bkp)
        self.master.bind('<F11>', cm_ativar_fullscreen)

        # Menu Superior
        self.mn_barra = Menu(self.fr_tela)

        master.config(menu=self.mn_barra)

        # MENU OPCOES
        self.mn_interface = Menu(self.mn_barra)
        self.mn_executar = Menu(self.mn_barra)
        self.mn_exemplos = Menu(self.mn_barra)
        self.mn_arquivo = Menu(self.mn_barra)
        self.mn_editar = Menu(self.mn_barra)
        self.mn_ajuda = Menu(self.mn_barra)
        self.mn_dev = Menu(self.mn_barra)

        # ADICAO DOS MENUS NA INTERFACE
        self.mn_barra.add_cascade(label=self.interface_idioma["label_arquivo"][self.idioma], menu=self.mn_arquivo)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_executar"][self.idioma], menu=self.mn_executar)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_exemplos"][self.idioma], menu=self.mn_exemplos)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_interface"][self.idioma], menu=self.mn_interface)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_ajuda"][self.idioma], menu=self.mn_ajuda)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_dev"][self.idioma], menu=self.mn_dev)

        # MENU ARQUIVOS
        self.mn_arquivo.add_command(label=self.interface_idioma["label_abrir_arquivo"][self.idioma], command=cm_abrir_arquivo)
        self.mn_arquivo.add_command(label=self.interface_idioma["label_nova_aba"][self.idioma], command=cm_abrir_abrir_nova_aba)
        self.mn_arquivo.add_command(label=self.interface_idioma["label_salvar"][self.idioma], command=cm_acao_salva_arquivo)
        self.mn_arquivo.add_command(label=self.interface_idioma["label_salvar_como"][self.idioma], command=cm_salvar_arquivo_como)
        self.mn_arquivo.bind('<Button-1>', lambda x: 'break')

        # MENU EXECUTAR
        self.mn_executar.add_command(label=self.interface_idioma["label_executar_tudo"][self.idioma], command=cm_executar_programa)
        self.mn_executar.add_command(label=self.interface_idioma["label_ate_breakpoint"][self.idioma], command=cm_executar_bkp)
        self.mn_executar.add_command(label=self.interface_idioma["label_parar_execucao"][self.idioma], command=cm_parar_execucao)
        self.mn_executar.add_command(label=self.interface_idioma["label_inserir_breakpoint"][self.idioma], command=cm_inserir_bkp)

        # MENU INTERFACE
        self.carregar_cascata_scripts()
        self.carregar_cascata_temas()
        self.carregar_cascata_sintaxe()

        # MENU DE AJUSTES
        self.mn_interface.add_command(label=self.interface_idioma["label_mais"][self.idioma], command=cm_aumentar_fonte)
        self.mn_interface.add_command(label=self.interface_idioma["label_menos"][self.idioma], command=cm_diminuir_fonte)

        # MENU AJUDA
        #self.mn_ajuda.add_command(label=self.interface_idioma["label_comandos_disponiveis"][self.idioma], command=cm_abrir_disponiv)
        self.mn_ajuda.add_command(label="  Tutorial", command=lambda event=None: self.abrir_aba_tutorial())
        self.mn_ajuda.add_command(label=self.interface_idioma["label_reportar_bug"][self.idioma], command=lambda event=None: self.bug.interface())
        self.mn_ajuda.add_command(label=self.interface_idioma["label_verificar_atualizacao"][self.idioma], command=lambda event=None: self.buscar_atualização())

        # MENU DESENVOLVIMENTO
        self.mn_dev.add_command(label=self.interface_idioma["label_logs"][self.idioma], command=cm_ativaropc_logs)
        self.mn_dev.add_command(label='  Debug', command=cm_ativarop_debug)

        # IMAGENS PARA O MENU DE ACESSO RÁPIDO
        self.ic_redesfazer = PhotoImage(file='imagens/left.png')
        self.ic_desfazer = PhotoImage(file='imagens/right.png')
        self.ic_salvar = PhotoImage(file='imagens/ic_salvar.png')
        self.ic_iniciar_parar = PhotoImage(file='imagens/ic_play.png')
        self.ic_parar = PhotoImage(file='imagens/ic_parar.png')
        self.ic_exec_ate_bkp = PhotoImage(file='imagens/ic_play_breakpoint.png')
        self.ic_inserir_bkp = PhotoImage(file='imagens/breakPoint.png')
        self.ic_ajuda = PhotoImage(file='imagens/ic_duvida.png')
        self.ic_pesquisa = PhotoImage(file='imagens/ic_pesquisa.png')
        self.ic_nao_salvo = PhotoImage(file="imagens/nao_salvo.png")
        self.ic_marcar_bkp = PhotoImage(file="imagens/limpar_bkp.png")
        self.ic_idioma = PhotoImage(file="imagens/{}".format(self.dic_imgs[self.idioma]))
        self.ic_aviso = PhotoImage(file="imagens/aviso.png")

        # AJUSTES NO TAMANHO
        self.ic_salvar = self.ic_salvar.subsample(4, 4)
        self.ic_iniciar_parar = self.ic_iniciar_parar.subsample(4, 4)
        self.ic_parar = self.ic_parar.subsample(4, 4)
        self.ic_exec_ate_bkp = self.ic_exec_ate_bkp.subsample(4, 4)
        self.ic_inserir_bkp = self.ic_inserir_bkp.subsample(4, 4)
        self.ic_ajuda = self.ic_ajuda.subsample(4, 4)
        self.ic_pesquisa = self.ic_pesquisa.subsample(4, 4)
        self.ic_nao_salvo = self.ic_nao_salvo.subsample(2, 2)
        self.ic_marcar_bkp = self.ic_marcar_bkp.subsample(4, 4)
        self.ic_idioma = self.ic_idioma.subsample(4, 4)
        self.ic_redesfazer = self.ic_redesfazer.subsample(4, 4)
        self.ic_desfazer = self.ic_desfazer.subsample(4, 4)
        self.ic_aviso = self.ic_aviso.subsample(1, 1)

        # CRIANDO AS OPÇÔES RÁPIDAS
        self.fr_opcoes = Frame(self.fr_tela)

        # CARREGANDO AS OPÇÔES
        self.bt_salvar = Button(self.fr_opcoes, image=self.ic_salvar, command=cm_acao_salva_arquivo)
        self.bt_executar = Button(self.fr_opcoes, image=self.ic_iniciar_parar, command=cm_executar_programa)
        self.bt_executar_bkp = Button(self.fr_opcoes, image=self.ic_exec_ate_bkp, command=cm_executar_bkp)
        self.bt_inserir_bkp = Button(self.fr_opcoes, image=self.ic_inserir_bkp, command=cm_inserir_bkp)
        self.bt_limpar_bkp = Button(self.fr_opcoes, image=self.ic_marcar_bkp, command=cm_limpa_breakpoints)
        self.bt_ajuda = Button(self.fr_opcoes, image=self.ic_ajuda, command=lambda event=None: self.abrir_aba_tutorial())
        #self.bt_pesquisar = Button(self.fr_opcoes, image=self.ic_pesquisa)
        self.bt_idioma = Button(self.fr_opcoes, image=self.ic_idioma, command=cm_atualizar_idioma)
        self.bt_redesfazer = Button(self.fr_opcoes, image=self.ic_redesfazer)
        self.bt_desfazer = Button(self.fr_opcoes, image=self.ic_desfazer)

        self.bt_copiar = Button(self.fr_opcoes, text=self.interface_idioma["copiar"][self.idioma], command=cm_copiar)
        self.bt_colar = Button(self.fr_opcoes, text=self.interface_idioma["colar"][self.idioma], command=cm_colar)
        self.fr_aviso = Frame(self.fr_opcoes)
        self.lb_aviso = Label(self.fr_aviso)
        self.bt_aviso = Button(self.fr_aviso)

        self.lb_aviso.grid(row=1, column=1)
        self.bt_aviso.grid(row=1, column=2, sticky=NSEW)

        self.fr_princ = Frame(self.fr_tela)
        self.fr_princ.grid_columnconfigure(2, weight=1)
        self.fr_princ.rowconfigure(1, weight=1)

        self.fr_abas = Frame(self.fr_princ, height=20)
        self.fr_abas.rowconfigure(1, weight=1)
        self.fr_abas.grid(row=0, column=0, columnspan=4, sticky=NSEW)

        self.fr_espaco = Label(self.fr_abas, width=11)
        self.fr_espaco.grid(row=1, column=0, sticky=NSEW)


        self.carregar_abas_inicio()

        # ************ Tela de desenvolvimento do código ****************** #
        self.tx_editor = EditorDeCodigo(self.fr_princ, undo=True, autoseparators=True, maxundo=50, tabs=4)
        self.tx_editor.focus_force()

        self.tx_editor.bind('<Control-c>', lambda event=None: self.copiar_selecao())
        self.tx_editor.bind("<<Paste>>", lambda event=None: self.colar_selecao())
        self.tx_editor.bind('<Control-a>', lambda event=None: self.selecionar_tudo())
        self.tx_editor.bind("<<Change>>", lambda event: self.desenhar_atualizar_linhas(event))
        self.tx_editor.bind('<Button>', lambda event:  self.obter_posicao_do_cursor(event))
        self.tx_editor.bind('<KeyRelease>', lambda event: self.ativar_coordernar_coloracao(event))

        # Para Windows e Mac
        self.tx_editor.bind('<Control-MouseWheel>', lambda event: self.aumentar_diminuir_fonte("+") if int(event.delta) > 0 else self.aumentar_diminuir_fonte("-"))

        # Para linux
        self.tx_editor.bind('<Control-Button-4>', lambda event: self.aumentar_diminuir_fonte("+"))
        self.tx_editor.bind('<Control-Button-5>', lambda event: self.aumentar_diminuir_fonte("-"))

        self.sb_codfc = Scrollbar(self.fr_princ, orient="vertical", command=self.tx_editor.yview, relief=FLAT)
        self.tx_editor.configure(yscrollcommand=self.sb_codfc.set)

        self.tx_editor.bind("<Tab>", lambda event=None: self.txt_editor_tab())

        self.cont_lin = ContadorLinhas(self.fr_princ, self.design, bool_tem_linha = True)
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas
        self.cont_lin.atribuir(self.tx_editor)

        self.cont_lin1 = ContadorLinhas(self.fr_princ, self.design, bool_tem_linha = False)
        self.cont_lin1.aba_focada2 = self.num_aba_focada
        self.cont_lin1.dic_abas2 = self.dic_abas
        self.cont_lin1.atribuir(self.tx_editor)

        self.fr_opcoes.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        self.bt_salvar.grid(row=1, column=1)
        self.bt_executar.grid(row=1, column=4)
        self.bt_executar_bkp.grid(row=1, column=5)
        self.bt_inserir_bkp.grid(row=1, column=6)
        self.bt_limpar_bkp.grid(row=1, column=8)
        self.bt_ajuda.grid(row=1, column=11)
        #self.bt_pesquisar.grid(row=1, column=12)
        self.bt_idioma.grid(row=1, column=13)
        self.bt_copiar.grid(row=1, column=14)
        self.bt_colar.grid(row=1, column=15)
        self.fr_aviso.grid(row=1, column=16)
        self.fr_princ.grid(row=2, column=1, sticky=NSEW)

        self.cont_lin1.grid(row=1, column=0, sticky=NSEW)
        self.cont_lin.grid(row=1, column=1, sticky=NSEW)


        # ******** Manipulação dos arquivos **************** #
        self.controle_arquivos = Arquivo(
            self.dic_abas, 
            self.num_aba_focada,
            self.tx_editor)

        #self.buscar_atualização()
        self.splash.splash_fim()
        self.master.withdraw()

        self.tutorial = Tutorial(self.fr_princ,  self.design, self.idioma, self.interface_idioma, self.icon)
        self.atualizar_design_interface()

        self.trocar_interface(troca='codigo')

        try:
            master.state('zoomed')
        except Exception as erro1:
            print(erro1)
            try:
                master.wm_attributes('-zoomed', 1)
            except Exception as erro2:
                print(erro2)


        # Atualizar a interface graficaa
        master.deiconify()
        master.update()

        self.avisos()


        #self.manipular_arquivos(None, "abrirArquivo", 'natal.safira')
    def trocar_interface(self, troca):
        if troca == 'tutorial':
            self.tx_editor.grid_remove()
            #self.cont_lin1.grid_remove()
            #self.cont_lin.grid_remove()
            self.sb_codfc.grid_remove()

            self.tutorial.barra_superior.grid(row=0, column=1, sticky=NSEW)
            self.tutorial.fr_texto.grid(row=1, column=2, columnspan=2, sticky= NSEW)
            self.tutorial.fr_botoes.grid(row=2, column=2, columnspan=2, sticky=NSEW)
            


        elif troca == 'codigo':

            self.tutorial.fr_botoes.grid_remove()
            self.tutorial.barra_superior.grid_remove()
            self.tutorial.fr_texto.grid_remove()

            self.tx_editor.grid(row=1, column=2, sticky=NSEW)
            self.sb_codfc.grid(row=1, column=3, sticky=NSEW)

    def abrir_aba_tutorial(self):
        self.abrir_nova_aba(tutorial=True)
        self.dic_abas[self.num_aba_focada]["tipo"] = 'tutorial'
        self.trocar_interface(troca='tutorial')
        self.atualizar_codigo_editor(self.num_aba_focada)



    def avisos(self):
        t_width  = int(self.master.winfo_screenwidth())
        t_heigth = int(self.master.winfo_screenheight())

        if t_width < 1366 or t_heigth < 768:
            self.fr_aviso.configure(highlightthickness=1)
            self.lb_aviso.configure(image=self.ic_aviso)
            self.bt_aviso.configure(text=self.interface_idioma["aviso_resolucao_alta"][self.idioma])

        elif t_width > 1366 or t_heigth > 768:
            self.fr_aviso.configure(highlightthickness=1)
            self.lb_aviso.configure(image=self.ic_aviso)
            self.bt_aviso.configure(text=self.interface_idioma["aviso_resolucao_baixa"][self.idioma])


    def liberar_breakpoint_ou_inicicar(self, tipo_execucao):

        if self.interpretador_status == 'parado':
            Interface.inicializar_interpretador(self, tipo_execucao='debug')
        else:
            self.libera_bkp = True

    def colocar_linhas_codigo(self, linhas: str) -> str:
        """Adiciona [[numero_linha] no inicio de todas as linhas]
        Args:
            linhas (str): [O código qualquer ]
        Returns:
            str: [O código com o [numero_linha] em todas as linhas]
        """

        nova_linha = ''
        lista = linhas.split('\n')
        for linha in range(len(lista)):
            nova_linha += '[{}]{}\n'.format(str(linha + 1), lista[linha])

        return nova_linha

    def inicializar_interpretador(self, tipo_execucao: str):
        """inicia uma instância do interpretador informando um código
        Args:
        tipo_execucao = "debug", "parar", "direto"
        Returns:
            None:
        """
        print("Inicializador do orquestrador iniciado")

        if self.interpretador_status == 'iniciado' or tipo_execucao == 'parar':
            # Para o interpretador
            try:
                self.instancia.aconteceu_erro = True

                if self.interpretador_finalizado:
                    # Finalização completa
                    # Delete a instância
                    del self.instancia

                    # Insere mensagem de finalização
                    self.cont_lin1.linha_analise = 0
                    self.cont_lin1.desenhar_linhas()

                    self.bt_executar.configure(image=self.ic_iniciar_parar)
                    self.interpretador_status = 'parado'

            except Exception as erro:
                print("Instância inexistente")

            return 0

        elif self.interpretador_status == 'parado':
            self.interpretador_status = 'iniciado'
            self.interpretador_finalizado = False

            # Configura o icone de parar
            self.bt_executar.configure(image=self.ic_parar)
            self.bt_executar.update()

            # Carregar o console
            if tipo_execucao == 'debug':
                Interface.iniciar_terminal_debug(self)
                bool_ignorar_todos_breakpoints = False
            else:
                Interface.iniciar_terminal_direto(self)

                # A principio, ignore todos os breakpoint
                bool_ignorar_todos_breakpoints = True

            # Limpar o terminal
            self.tx_terminal.delete('1.0', END)
            self.tx_terminal.update()

            # Atualizar os elementos da interface
            self.master.update()
            self.tx_editor.update()
            self.tx_terminal.update()

            # Linha que o interpretador está executando
            self.linha_analise = None

            # Obter o código
            linhas = self.tx_editor.get('1.0', END)[0:-1]

            # Adicionar marcação do número da linha
            linhas = self.colocar_linhas_codigo(linhas)

            # Obter o diretório base
            diretorio_base = self.dic_abas[self.num_aba_focada]["arquivoSalvo"]["link"]

            # Obter apenas o diretório
            diretorio_base = re_sub('([^\\/]{1,})$', '', diretorio_base)
 
            # Criar uma instância do interpretador
            self.instancia = Interpretador(
                self.bool_logs,
                self.dic_abas[self.num_aba_focada]["lst_breakpoints"],
                bool_ignorar_todos_breakpoints,
                diretorio_base,
                self.dicLetras,
                self.dic_comandos,
                self.idioma,
                dic_regex_compilado=None, re_comandos=self.re_comandos)

            # Remover os comentárioos
            linhas = self.instancia.cortar_comentarios(linhas)

            # Marcar o inicio do interpretador
            inicio = time()

            # iniciar um thread do interpretador
            t = Thread(target=lambda codigoPrograma=linhas: self.instancia.orquestrador_interpretador_(codigoPrograma))
            t.start()

            # Referenciar o terminal
            tx_terminal = self.tx_terminal
            valor_antigo = 0
            p_cor_num = 0

            # Enquanto o interpretador não iniciar
            while self.instancia.numero_threads_ativos != 0 or not self.instancia.boo_orquestrador_iniciado:

                try:
                    # Atualize a interface
                    self.master.update()
                    self.tx_editor.update()
                    self.tx_terminal.update()
                except:

                    # Se alguma coisa foi fechada, finalize o interpretador
                    self.instancia.aconteceu_erro = True
                    break

                if tipo_execucao == 'debug':
                    # Marca que chegou até a linha
                    linha_analise = int(self.instancia.num_linha)
                    self.cont_lin1.linha_analise = linha_analise
                    self.cont_lin1.desenhar_linhas()

                    self.tx_editor.update()
                    self.master.update()

                acao = ""
                # Obtem uma instrução do interpretador
                acao = self.instancia.controle_interpretador

                # Se existe uma ação
                if acao != "":
                    valores = None
                    valores = re_search(self.regex_interpretador, acao)

                    # Se a instrução é de exibição na tela
                    if valores is not None:

                        # Obter instrução
                        # Numero da

                        instrucao = valores.group(1)
                        linha = valores.group(4)
                        cor = valores.group(3)

                        if instrucao == 'nessaLinha':
                            self.instancia.controle_interpretador = ""

                            try:

                                # Insere o texto e libera o interpretador
                                inicio_cor = float(self.tx_terminal.index("end-1line lineend"))
                                self.tx_terminal.insert(END, linha)

                                # Se era para exibir com alguma cor especial
                                if cor != "":
                                    # Adiciona a cor
                                    fim_cor = float(self.tx_terminal.index("end-1line lineend"))
                                    self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                                    self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)

                                    # Marca onde a cor foi inserida
                                    p_cor_num += 1
                                self.tx_terminal.see('end')

                            except Exception as e:
                                self.instancia.aconteceu_erro = True
                                break
                        elif instrucao == 'mostreLinha':
                            self.instancia.controle_interpretador = ""

                            try:
                                # Insere  texto
                                inicio_cor = float(self.tx_terminal.index("end-1line lineend"))
                                self.tx_terminal.insert(END, linha + '\n')

                                # Se era para exibir em uma cor
                                if cor != "":

                                    # Exibe nesta cor
                                    fim_cor = float(self.tx_terminal.index("end-1line lineend"))
                                    self.tx_terminal.tag_add("palavra"+str(p_cor_num), inicio_cor, fim_cor)
                                    self.tx_terminal.tag_config("palavra"+str(p_cor_num), foreground=cor)
                                    p_cor_num += 1

                                self.tx_terminal.see('end')

                            except:
                                self.instancia.aconteceu_erro = True
                                break

                    elif acao == ':input:':
                        # Obtem como está o código agora
                        textoOriginal = len(self.tx_terminal.get(1.0, END))

                        # Espera o usuário pressionar enter
                        self.esperar_pressionar_enter = True
                        while self.esperar_pressionar_enter:

                            try:
                                self.master.update()
                                self.tx_editor.update()
                                self.tx_terminal.update()
                                self.tx_terminal.get(1.0, END)
                            except:
                                self.instancia.aconteceu_erro = True
                                break

                        if self.instancia.aconteceu_erro:
                            continue

                        # Marca que já foi pressionado enter
                        self.esperar_pressionar_enter = False

                        # Obtem o novo texto com o que o usuário digitou
                        digitado = self.tx_terminal.get(1.0, END)
                        digitado = digitado[textoOriginal - 1:-2]

                        # Atribui o texto
                        self.instancia.texto_digitado = digitado.replace("\n", "")

                        # Libera o interpretador
                        self.instancia.controle_interpretador = ""

                    elif acao == 'limpar_tela':

                        # Limpa o terminal
                        try:
                            self.tx_terminal.delete('1.0', END)

                            # Atualiza o interpretador para continuar
                            self.instancia.controle_interpretador = ""
                        except Exception as erro:
                            self.instancia.aconteceu_erro = True
                            break

                        self.instancia.controle_interpretador = ""

                    elif acao == 'aguardando_breakpoint':
                            # Aguarda o breakpoint ser liberado

                            try:
                                # Marca que chegou até a linha
                                linha_analise = int(self.instancia.num_linha)

                                self.cont_lin1.linha_analise = linha_analise
                                self.cont_lin1.desenhar_linhas()

                                self.tx_editor.update()
                                self.master.update()

                                # Enquanto o breakpoint estiver preso
                                self.libera_bkp = False

                                # Enquanto o breakpoint não for liberado
                                while not self.libera_bkp:

                                    # Atualiza a tela
                                    self.tx_terminal.update()
                                    self.tx_editor.update()
                                    self.master.update()

                                    sleep(0.0001)

                                    if self.instancia.aconteceu_erro:
                                        break

                                # Libera o interpretador
                                self.instancia.controle_interpretador = ""

                                # Deixa breakpoint liberado
                                self.libera_bkp = False

                            except Exception as erro:
                                self.instancia.aconteceu_erro = True
                                break
                    else:
                        print("Instrução do Interpretador não é reconhecida => '{}'".format(acao))
            mensagem_erro = ""
            if self.instancia.aconteceu_erro:
                # Se o erro foi avisado
                if self.instancia.erro_alertado is True:

                    # Se não foi interrompido
                    if self.instancia.mensagem_erro != "Interrompido":

                        # Se não foi erro ao iniciar
                        if self.instancia.mensagem_erro != "Erro ao iniciar o Interpretador":

                            # Mostre uma mensagem complementar na tela
                            mensagem_erro = self.instancia.mensagem_erro
                            Interface.mostrar_mensagem_de_erro(self, self.instancia.mensagem_erro, self.instancia.dir_script_aju_erro, self.instancia.linha_que_deu_erro)

            try:

                if not mensagem_erro:
                    self.tx_terminal.insert(END, self.interface_idioma["script_finalizado"][self.idioma].format(
                        round(time() - inicio, 4)))

                else:
                    self.tx_terminal.tag_add('erro_terminal', END)
                    self.tx_terminal.tag_configure('erro_terminal', foreground='#ff80a2')

                    self.tx_terminal.insert(END, '\n\n{}\n\n'.format(mensagem_erro), 'erro_terminal')
                    self.tx_terminal.insert(END, 'Finalizado em {} s'.format(
                        round(time() - inicio, 4)))

                self.tx_terminal.see("end")

            except Exception as erro:
                print('Impossível exibir mensagem de finalização, erro: '+str(erro))

            self.interpretador_finalizado = True

            # Em modo que não seja debug, finalize o interpretador
            # if tipo_execucao == 'continua' or not self.instancia.aconteceu_erro:
            tipo_execucao = 'parar'
            Interface.inicializar_interpretador(self, tipo_execucao)

            return 0

    def carregar_estilos_terminal(self):

        relief_titulo = self.design.get("titulo_terminal")["relief"]

        background_titulo = self.design.get("titulo_terminal")["background"]
        foreground_titulo = self.design.get("titulo_terminal")["foreground"]

        active_foreground_titulo = self.design.get("titulo_terminal")["active_foreground"]
        active_background_titulo = self.design.get("titulo_terminal")["active_background"]

        pressed_foreground_titulo = self.design.get("titulo_terminal")["pressed_foreground"]
        pressed_background_titulo = self.design.get("titulo_terminal")["pressed_background"]

        background_linha = self.design.get("linha_terminal")["background"]
        foreground_linha = self.design.get("linha_terminal")["foreground"]
        fieldbackground_linha = self.design.get("linha_terminal")["fieldbackground"]

        self.style_terminal = Style()
        self.style_terminal.theme_use("clam")

        self.style_terminal.element_create("Custom.Treeheading.border", "from", "default")

        self.style_terminal.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
                    ("Custom.Treeheading.text", {'sticky':'we'})
                ]})
            ]}),
        ])

        # Titulo das colunas
        self.style_terminal.configure("Custom.Treeview.Heading",
                background=self.design.get("titulo_terminal")["background"],
                foreground=self.design.get("titulo_terminal")["foreground"],
                relief=relief_titulo)

        # Titulo das colunas
        self.style_terminal.configure("Custom.Treeview",
            background=self.design.get("linha_terminal")["background"],
            foreground=self.design.get("linha_terminal")["foreground"],
            fieldbackground=self.design.get("linha_terminal")["fieldbackground"])

        # Linhas
        self.style_terminal.configure(style="Custom.Treeview",
            background=background_linha,
            foreground=foreground_linha,
            fieldbackground=fieldbackground_linha)

        # Mapeamento especial dos titulos
        self.style_terminal.map("Custom.Treeview.Heading",
            relief=[('active', relief_titulo), ('pressed', relief_titulo)],

            foreground=[
                ('pressed', '!disabled', pressed_foreground_titulo),
                ('active', '!disabled', active_foreground_titulo)],
            background=[
                ('pressed', '!disabled', pressed_background_titulo),
                ('active', '!disabled', active_background_titulo)])

        return self.style_terminal

    def txt_editor_tab(self):
        self.tx_editor.insert(INSERT, " " * 4)
        return 'break'

    def buscar_atualização(self, primeira_vez=False):
        t = Thread(target=lambda primeira_vez=primeira_vez: self.atualizar.verificar_versao(primeira_vez))
        t.start()
        

    def carregar_cascata_temas(self):
        self.mn_interface_cascate_temas = Menu(self.mn_interface, tearoff=False)
        self.mn_interface.add_cascade(label=self.interface_idioma["label_cascate_temas"][self.idioma], menu=self.mn_interface_cascate_temas)

        for file in listdir('temas/interface/'):
            arquivo = " " + file
            if self.arquivo_configuracoes["tema"] == file:
                arquivo = "*" + file

            funcao = lambda link = file: self.atualizar_tema_sintaxe_da_interface('tema', str(link))
            self.mn_interface_cascate_temas.add_command(label=arquivo, command=funcao)

    def carregar_cascata_sintaxe(self):
        self.mn_interface_cascata_sintaxe = Menu(self.mn_interface, tearoff=False)
        self.mn_interface.add_cascade(label=self.interface_idioma["label_cascate_sintaxe"][self.idioma], menu=self.mn_interface_cascata_sintaxe)

        for file in listdir('temas/sintaxe/'):
            arquivo = " " + file
            if self.arquivo_configuracoes["sintaxe"] == file:
                arquivo = "*" + file

            funcao = lambda link = file: self.atualizar_tema_sintaxe_da_interface('sintaxe', str(link))
            self.mn_interface_cascata_sintaxe.add_command(label=arquivo, command=funcao)

    def carregar_cascata_scripts(self):
        scripts = listdir('scripts/' + self.idioma)
        scripts.sort()

        for file in scripts:
            if file.endswith("safira"):
                funcao = lambda link = file:  self.abrir_um_script(link)
                self.mn_exemplos.add_command(label="  " + file + "  ", command=funcao)

    def abrir_um_script(self, link:str):
        if self.dic_abas[self.num_aba_focada]["arquivoAtual"]["texto"].strip() != "":
            self.abrir_nova_aba(None)

        self.manipular_arquivos(None, "abrirArquivo",
            'scripts/'+ self.idioma + '/' + str(link))


    def manipular_arquivos(self, event, comando:str, link=None):
        if self.controle_arquivos is None: return 0
        retorno_salvar_como = None

        self.controle_arquivos.atualiza_infos(self.dic_abas, self.num_aba_focada, self.tx_editor)

        if comando == "abrirArquivo":
            print("abrirArquivo")
            self.controle_arquivos.abrirArquivo(link)

        elif comando == "abrir_arquivo_dialog":
            print("abrir_arquivo_dialog")
            self.controle_arquivos.abrir_arquivo_dialog(event)

        elif comando == "salvar_arquivo":
            print("salvar_arquivo")
            retorno_salvar_como = self.controle_arquivos.salvar_arquivo(event)

        elif comando == "salvar_arquivo_como_dialog":
            print("salvar_arquivo_como_dialog")
            self.controle_arquivos.salvar_arquivo_como_dialog(event)

        self.num_aba_focada = self.controle_arquivos.aba_focada
        self.dic_abas = self.controle_arquivos.dic_abas

        if comando in ["abrirArquivo", "salvar_arquivo_como_dialog", "abrir_arquivo_dialog"] or retorno_salvar_como == "salvar_arquivo_como_dialog":
            self.atualizar_codigo_editor(self.num_aba_focada)
        return 0

    def aumentar_diminuir_fonte(self, acao:str):
        print("aumentar_diminuir_fonte")

        if acao == "+": adicao = 1
        else: adicao = -1

        self.design.get("cor_menu")["font"][1] = int(self.design.get("cor_menu")["font"][1]) + adicao
        self.design.get("lb_sobDeTitulo")["font"][1] = int(self.design.get("lb_sobDeTitulo")["font"][1]) + adicao
        self.design.get("dicBtnMenus")["font"][1] = int(self.design.get("dicBtnMenus")["font"][1]) + adicao
        self.design.get("tx_terminal")["font"][1] = int(self.design.get("tx_terminal")["font"][1]) + adicao
        self.design.get("tx_codificacao")["font"][1] = int(self.design.get("tx_codificacao")["font"][1]) + adicao
        self.design.get("fonte_ct_linha")["font"][1] = int(self.design.get("fonte_ct_linha")["font"][1]) + adicao
        self.design.get("fonte_ct_linha")["width"] = int(self.design.get("fonte_ct_linha")["width"]) + adicao

        self.tx_editor.configure(self.design.get("tx_codificacao"))
        self.cont_lin.desenhar_linhas()
        self.cont_lin1.desenhar_linhas()

        self.fr_tela.update()
    def ativar_coordernar_coloracao(self, event=None):
        # Coordena a atualização de uma aba
        self.fechar_mensagem_de_erro()
        self.atualizar_coloracao_codigo_aba(True, event)

        if self.dic_abas != {}:
            self.dic_abas[self.num_aba_focada ]["arquivoAtual"]['texto'] = self.tx_editor.get(1.0, END)
            if self.dic_abas[self.num_aba_focada ]["arquivoAtual"]['texto'] != self.dic_abas[ self.num_aba_focada ]["arquivoSalvo"]['texto']:

                if self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] is False:
                    self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = True

                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()
                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()

                    self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(image=self.ic_nao_salvo, width=largura_original)

            else:
                self.dic_abas[self.num_aba_focada]["listaAbas"][3].config(image='', width=0)
                self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = False

            self.dic_abas[self.num_aba_focada]["listaAbas"][3].update()

        if hasattr(event, "keysym"):
            self.obter_posicao_do_cursor(event)

    def configurar_cor_aba(self, dic_cor_abas, bg_padrao, dic_cor_botao, dic_cor_marcador):
        print('configurar_cor_aba', dic_cor_abas, bg_padrao, dic_cor_botao, dic_cor_marcador, self.num_aba_focada)
        self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(dic_cor_botao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground=bg_padrao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][1].configure(dic_cor_marcador)
        self.dic_abas[self.num_aba_focada]["listaAbas"][0].configure(background=bg_padrao)

    def carregar_abas_inicio(self):
        """
            Usado apenas no inicio do programa *****1 VEZ*****
        """

        print('carregar_abas_inicio')
        for num_aba, dados_aba in self.dic_abas.items():
            # Coloração da aba
            if dados_aba["foco"]:
                self.num_aba_focada = num_aba
                dic_cor_marcador = self.design.get("dic_cor_marcador_focado")
                dic_cor_finao = self.design.get("dic_cor_abas_focada")
                dic_cor_botao = self.design.get("abas_botao_fechar_focado")
            else:
                dic_cor_marcador = self.design.get("dic_cor_marcador_nao_focado")
                dic_cor_finao = self.design.get("dic_cor_abas_nao_focada")
                dic_cor_botao = self.design.get("abas_botao_fechar_desfocado")
            

            fr_uma_aba = Frame(self.fr_abas)
            fr_uma_aba.rowconfigure(1, weight=1)

            nome_arquivo = str(dados_aba["arquivoSalvo"]["link"]).split("/")
            nome_arquivo = str(nome_arquivo[-1])

            try:
                fr_uma_aba.configure(backgroun=dic_cor_finao["background"])
            except Exception as erro:
                print(erro)

            txt_btn = "x "

            if nome_arquivo.strip() == "":
                nome_arquivo = "            "
            else:
                nome_arquivo = " " + nome_arquivo

            fr_marcador = Frame(fr_uma_aba, dic_cor_marcador, padx=100, bd=10)
            lb_aba = Button(fr_uma_aba, dic_cor_finao, text=nome_arquivo, border=0, highlightthickness=0)
            bt_fechar = Button(fr_uma_aba, dic_cor_botao, text=txt_btn, relief='groove', border=0, highlightthickness=0)

            try:
                padrao = dic_cor_botao["foreground"]
            except Exception as erro:
                print(erro)
                padrao = "white"

            bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: self.realcar_cor_botao_fechar_aba(bt_fechar))
            bt_fechar.bind("<Leave>", lambda event=None, padrao=padrao, bt_fechar=bt_fechar: self.voltar_cor_botao_fechar_aba(padrao, bt_fechar))

            lb_aba.bind('<ButtonPress>', lambda event=None, num_aba=num_aba: self.focar_aba(num_aba))
            bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: self.fechar_uma_aba(bt_fechar))


            fr_uma_aba.grid(row=1, column=num_aba+2, sticky=N)
            fr_marcador.grid(row=0, column=1, columnspan=2, sticky=NSEW)
            lb_aba.grid(row=1, column=1, sticky=NSEW)
            bt_fechar.grid(row=1, column=2)

            fr_uma_aba.update()
            fr_marcador.update()
            lb_aba.update()
            bt_fechar.update()
            
            self.dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
            self.dic_abas[num_aba]["listaAbas"].append(fr_marcador)
            self.dic_abas[num_aba]["listaAbas"].append(lb_aba)
            self.dic_abas[num_aba]["listaAbas"].append(bt_fechar)




    def abrir_nova_aba(self, event=None, tutorial=False):
        sleep(0.1)
        print('abrir_nova_aba', event)
        # Adicionar na posição 0
        posicao_adicionar = 0

        # Se tem mais de uma aba
        if len(self.dic_abas) != 0:
            # Cores
            dic_cor_finao = self.design.get("dic_cor_abas_nao_focada")
            dic_cor_botao = self.design.get("abas_botao_fechar_desfocado")
            dic_cor_marcador = self.design.get("dic_cor_marcador_nao_focado")

            # Remover o foco da aba focada
            self.configurar_cor_aba(dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)

            # Obter posição final
            posicao_adicionar = max(self.dic_abas.keys())+1

        # Adicionar nova Aba
        self.dic_abas[posicao_adicionar] = funcoes.carregar_json("configuracoes/guia.json")

        # Cores
        dic_cor_finao = self.design.get("dic_cor_abas_focada")
        dic_cor_botao = self.design.get("abas_botao_fechar_focado")
        dic_cor_marcador = self.design.get("dic_cor_marcador_focado")

        # Criando uma Aba
        fr_uma_aba = Frame(self.fr_abas, background=dic_cor_finao["background"])
        fr_marcador = Frame(fr_uma_aba, dic_cor_marcador)
        lb_aba = Button(fr_uma_aba, dic_cor_finao, text=" "*14)

        bt_fechar = Button(fr_uma_aba, dic_cor_botao, text='x ', relief='groove', border=0, highlightthickness=0)

        # Eventos
        lb_aba.bind('<ButtonPress>', lambda event=None, num_aba=posicao_adicionar: self.focar_aba(num_aba))
        bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: self.fechar_uma_aba(bt_fechar))
        bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: self.realcar_cor_botao_fechar_aba(bt_fechar))
        bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: self.voltar_cor_botao_fechar_aba(padrao, bt_fechar))

        # Layout
        fr_uma_aba.rowconfigure(1, weight=1)
        fr_uma_aba.grid(row=1, column=posicao_adicionar+2, sticky=N)
        fr_marcador.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        # Configuração de Aba
        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_marcador)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

        # Atualizar Aba focada
        self.num_aba_focada = posicao_adicionar
        self.lst_historico_abas_focadas.append(posicao_adicionar)

        # Focar nova aba
        self.atualizar_codigo_editor(self.num_aba_focada)
        self.trocar_interface(troca='codigo')


    def fechar_uma_aba(self, bt_fechar):
        bool_era_focado = False
        dic_cor_abas = self.design.get("dic_cor_abas")

        for chave, valor in self.dic_abas.items():

            # Se for a aba para focar
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:

                # Se a aba não estava salva
                if self.dic_abas[chave]["ja_foi_marcado_nao_salvo"]:

                    # Focar a aba que erapara fechar
                    self.focar_aba(chave)

                    # Deseja salvar seu código nesta aba?
                    resposta = messagebox.askyesnocancel(
                        self    .interface_idioma["tit_fechar_aba_safira"][self.idioma],
                        self.interface_idioma["msg_fechar_aba_safira"][self.idioma],
                        icon='warning')

                    if resposta is True:  # yes
                        self.manipular_arquivos(None, "salvar_arquivo")

                    elif resposta is False: # No
                        pass
                    elif resposta is None: # Cancel
                        return 0
                    else:
                        print("Mensagem: {}".format(resposta))
                        return 0

                # Remover a chave do histórico de abas focadas
                while chave in self.lst_historico_abas_focadas:
                    self.lst_historico_abas_focadas.remove(chave)


                # Se tinha só uma Aba
                # Limpar os dados e atualizar o texto
                if len(self.dic_abas) == 1:
                    self.dic_abas[chave]["nome"] =""
                    self.dic_abas[chave]["lst_breakpoints"] = []
                    self.dic_abas[chave]["arquivoSalvo"] = {"link": "", "texto": ""}
                    self.dic_abas[chave]["arquivoAtual"] = {"texto": ""}

                    self.atualizar_codigo_editor(chave)
                    # Adicionando novamente a chave
                    self.lst_historico_abas_focadas.append(chave)
                    return 0

                else:
                    # Tem mais de uma aba

                    # Destrua ela
                    self.dic_abas[chave]["listaAbas"][0].update()
                    self.dic_abas[chave]["listaAbas"][0].grid_forget()

                    # Se esta aba estava focada
                    if self.dic_abas[chave]["foco"] is True:
                        bool_era_focado = True

                    # Deletar o registro
                    del self.dic_abas[chave]
                    break

        # Aba fechada era a aba que estava focada
        if bool_era_focado:
            print('bool_era_focado', self.lst_historico_abas_focadas)

            # Obter a penultima aba focada
            chave = self.lst_historico_abas_focadas[-1]

            # Obter cores para uma nova aba
            dic_cor_finao = self.design.get("dic_cor_abas_focada")
            dic_cor_botao = self.design.get("abas_botao_fechar_focado")
            dic_cor_marcador = self.design.get("dic_cor_marcador_focado")

            # Atualizar a aba focada
            self.num_aba_focada = chave

            # Informar que a aba será focada
            self.dic_abas[chave]["foco"] = True

            # Atualizar cor da aba focada
            self.configurar_cor_aba(dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)

            # Atualizar código no editor
            self.atualizar_codigo_editor(chave)

            # Adicionar no histórico
            self.lst_historico_abas_focadas.append(chave)

            # Atualizar Aba
            self.atualizar_coloracao_codigo_aba()


        if self.dic_abas[self.num_aba_focada]['tipo'] == 'tutorial':
            self.trocar_interface(troca='tutorial')
        else:
            self.trocar_interface(troca='codigo')




    def atualizar_cor_abas(self):
        print('atualizar_cor_abas')

        for num_aba, _ in self.dic_abas.items():

            # Coloração da aba
            if num_aba == self.num_aba_focada:
                dic_cor_marcador = self.design.get("dic_cor_marcador_focado")
                dic_cor_finao = self.design.get("dic_cor_abas_focada")
                dic_cor_botao = self.design.get("abas_botao_fechar_focado")
            else:
                dic_cor_marcador = self.design.get("dic_cor_marcador_nao_focado")
                dic_cor_finao = self.design.get("dic_cor_abas_nao_focada")
                dic_cor_botao = self.design.get("abas_botao_fechar_desfocado")

            fr_uma_aba = self.dic_abas[num_aba]["listaAbas"][0]
            fr_marcador = self.dic_abas[num_aba]["listaAbas"][1]
            lb_aba = self.dic_abas[num_aba]["listaAbas"][2]
            bt_fechar = self.dic_abas[num_aba]["listaAbas"][3]

            try:
                fr_uma_aba.configure(backgroun=dic_cor_finao["background"])
            except Exception as erro:
                print(erro)

            fr_marcador.configure(dic_cor_marcador)
            lb_aba.configure(dic_cor_finao)
            bt_fechar.configure(dic_cor_botao)


    def focar_aba(self, num_aba):
        print('focar_aba', num_aba)
        if num_aba == self.num_aba_focada:
            return 0

        dic_cor_finao = self.design.get("dic_cor_abas_nao_focada")
        dic_cor_botao = self.design.get("abas_botao_fechar_desfocado")
        dic_cor_marcador = self.design.get("dic_cor_marcador_nao_focado")
        self.configurar_cor_aba(dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)

        self.dic_abas[self.num_aba_focada]["foco"] = False

        dic_cor_finao = self.design.get("dic_cor_abas_focada")
        dic_cor_botao = self.design.get("abas_botao_fechar_focado")
        dic_cor_marcador = self.design.get("dic_cor_marcador_focado")

        self.num_aba_focada = num_aba
        self.dic_abas[num_aba]["foco"] = True

        self.lst_historico_abas_focadas.append(num_aba)

        self.configurar_cor_aba(dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
        self.atualizar_codigo_editor(num_aba)

        self.atualizar_coloracao_codigo_aba()

        if self.dic_abas[self.num_aba_focada]['tipo'] == 'tutorial':
            self.trocar_interface(troca='tutorial')
        else:
            self.trocar_interface(troca='codigo')


    def atualizar_coloracao_codigo_aba(self, limpar=False, event=None):
        # num_modulos_acionados => 0

        if event is not None:
            if event.keysym in ('Down', 'Up', 'Left', 'Right', 'Return', 'BackSpace'):
                return 0

        self.num_coloracao_acionados += 1

        if self.num_coloracao_acionados > 3:
            return 0

        if self.num_coloracao_acionados == 2:
            while self.num_coloracao_acionados != 0:
                self.fr_tela.update()
            self.num_coloracao_acionados += 1

        if limpar:
            self.colorir_codigo.historico_coloracao = []
        self.colorir_codigo.coordena_coloracao(None, tx_editor_codigo=self.tx_editor)

        self.num_coloracao_acionados = 0

    def atualizar_coloracao_codigo_aba_th(self, limpar=False, event=None):
        inicio = time()

        # num_coloracao_acionados => 0
        if self.num_coloracao_acionados > 1:
            return 0

        if self.num_coloracao_acionados == 1:
            while self.num_coloracao_acionados != 0:
                pass

        if event is not None:
            if event.keysym in ('Down', 'Up', 'Left', 'Right', 'Return', 'BackSpace'):
                return 0

        self.num_coloracao_acionados += 1

        if limpar:
            self.colorir_codigo.historico_coloracao = []
        self.colorir_codigo.coordena_coloracao(None, tx_editor_codigo=self.tx_editor)

        self.num_coloracao_acionados -= 0

        print('\n\ntempo processamento ', time()-inicio)


    def atualizar_codigo_editor(self, num_aba):
        if self.dic_abas[num_aba]['tipo'] == 'tutorial': 
            self.dic_abas[num_aba]["listaAbas"][2].configure(text='Tutorial Safira')

            for x in range(0, 3):
                self.dic_abas[num_aba]["listaAbas"][x].update()

            return 0

        self.tx_editor.delete(1.0, END)
        self.tx_editor.insert(END, str(self.dic_abas[num_aba]["arquivoAtual"]["texto"])[0:-1])

        nome_arquivo = self.dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if nome_arquivo.strip() == "":
            nome_arquivo = " " * 14

        self.dic_abas[num_aba]["listaAbas"][2].configure(text=nome_arquivo)

        for x in range(0, 3):
            self.dic_abas[num_aba]["listaAbas"][x].update()
        self.atualizar_coloracao_codigo_aba(True)

    def realcar_cor_botao_fechar_aba(self, bt_fechar):
   
        for chave, _ in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                if self.dic_abas[chave]['foco']:
                    dict_cores = self.design.get("abas_botao_fechar_focado")
                else:
                    dict_cores = self.design.get("abas_botao_fechar_desfocado")

                activeforeground = dict_cores["foreground"]
                foreground = dict_cores["activeforeground"]

                self.dic_abas[chave]["listaAbas"][3].configure(activeforeground=activeforeground, foreground=foreground)
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def voltar_cor_botao_fechar_aba(self, padrao, bt_fechar):


        for chave, _ in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:

                if self.dic_abas[chave]['foco']:
                    dict_cores = self.design.get("abas_botao_fechar_focado")
                else:
                    dict_cores = self.design.get("abas_botao_fechar_desfocado")


                activeforeground = dict_cores["activeforeground"]
                foreground = dict_cores["foreground"]

                self.dic_abas[chave]["listaAbas"][3].configure(activeforeground=activeforeground, foreground=foreground)
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    # ************************************************************************* #
    #                      TERMINAL COM A EXECUÇÂO                              #
    # ************************************************************************* #
    def destruir_instancia_terminal(self):
        try:
            self.lista_terminal_destruir[0].withdraw()
        except Exception as erro:
            print('destruir_instancia_terminal', erro)

        for widget in self.lista_terminal_destruir:
            try:

                widget.destroy()
                self.tx_terminal = None
            except Exception as e:
                pass

            try:
                widget.grid_forget()
                self.tx_terminal = None
            except Exception as e:
                pass

        try:
            self.instancia.aconteceu_erro = True
            self.libera_bkp = True

        except AttributeError:
            pass

    def iniciar_terminal_direto(self):
        self.destruir_instancia_terminal()

        self.top_janela_terminal = Toplevel(self.fr_tela)
        self.top_janela_terminal.tk.call('wm', 'iconphoto', self.top_janela_terminal._w, self.icon)

        self.top_janela_terminal.protocol("WM_DELETE_WINDOW", lambda event=None: self.destruir_instancia_terminal())


        self.top_janela_terminal.grid_columnconfigure(1, weight=1)
        self.top_janela_terminal.rowconfigure(1, weight=1)
        # Ocultar tkinter
        self.top_janela_terminal.withdraw()

        t_width  = self.master.winfo_screenwidth()
        t_heigth = self.master.winfo_screenheight()

        self.top_janela_terminal.geometry("720x450+{}+{}".format(int(t_width/2-(720/2)), int(t_heigth/2-(450/2))))
        self.top_janela_terminal.deiconify()
        self.fr_tela.update()
        self.tx_terminal = Text(self.top_janela_terminal)

        try:
            self.tx_terminal.configure(self.design.get("tx_terminal"))
        except Exception as erro:
            print("Erro 2 ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: self.alterar_status_pressionou_enter(event))
        #self.tx_terminal.bind("<KeyRelease>", lambda event: self.capturar_tecla_terminal(event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)
        self.tx_terminal.update()
        self.tx_terminal.get(1.0, END)
        self.lista_terminal_destruir = [self.top_janela_terminal, self.tx_terminal]

    def iniciar_terminal_debug(self):
        self.destruir_instancia_terminal()

        coluna_identificadores = (
            self.interface_idioma["debug_variavel"][self.idioma],
            self.interface_idioma["debug_tipo"][self.idioma],
            self.interface_idioma["debug_valor"][self.idioma])

        fr_terminal_e_grid = Frame(self.fr_princ, self.design.get("tx_terminal_debug_fr1"))
        fr_terminal_e_grid.grid(row=1, column=4, rowspan=2, sticky=NSEW)
        fr_terminal_e_grid.grid_columnconfigure(1, weight=1)
        fr_terminal_e_grid.rowconfigure(1, weight=1)

        fr_fechar_menu = Frame(fr_terminal_e_grid, self.design.get("tx_terminal_debug_fr2"))
        fr_fechar_menu.grid_columnconfigure(1, weight=1)
        fr_fechar_menu.grid(row=0, column=1, sticky=NSEW)

        bt_fechar = Button(fr_fechar_menu, self.design.get("tx_terminal_debug_bt1"))
        bt_fechar['command'] = lambda: self.destruir_instancia_terminal()
        bt_fechar.grid(row=0, column=1, sticky="E")

        self.tx_terminal = Text(fr_terminal_e_grid)

        try:
            self.tx_terminal.configure(self.design.get("tx_terminal"))
        except Exception as erro:
            print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: self.alterar_status_pressionou_enter())
        # self.tx_terminal.bind("<KeyRelease>", lambda event: self.capturar_tecla_terminal(event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)

        fr_grid_variaveis = Frame(fr_terminal_e_grid, self.design.get("cor_grid_variaveis"))
        fr_grid_variaveis.grid(row=2, column=1, sticky=NSEW)

        fr_grid_variaveis.grid_columnconfigure(1, weight=1)
        fr_grid_variaveis.rowconfigure(2, weight=1)

        self.tx_busca = Label(fr_grid_variaveis, self.design.get("cor_grid_variaveis_texto_busca"), text=self.interface_idioma["debug_faca_busca"][self.idioma])
        self.et_campo_busca = Entry(fr_grid_variaveis, self.design.get("cor_grid_variaveis_campo_busca"))
        self.et_campo_busca.bind("<KeyRelease>", lambda event: self.retornar_variaveis())

        self.arvores_grid = Treeview(
            fr_grid_variaveis,
            columns=coluna_identificadores,
            show="headings",
            style="Custom.Treeview")

        self.arvores_grid.tag_configure('RED_TAG',
            foreground=self.design.get("cor_grid_treeview_red_tag")['foreground'],
            font=self.design.get("cor_grid_treeview_red_tag")['font'])

        #vsroolb = Scrollbar(fr_grid_variaveis,
        # self.design.get("cor_grid_variaveis_scrollbar"), relief=FLAT,
        # orient="vertical", command=self.arvores_grid.yview)
        #hsroolb = Scrollbar(fr_grid_variaveis,
        # self.design.get("cor_grid_variaveis_scrollbar"), relief=FLAT,
        # orient="horizontal", command=self.arvores_grid.xview)

        #self.arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)


        for coluna in coluna_identificadores:
            # parametro a se analisar = selectmode="#f1a533")
            self.arvores_grid.heading(coluna, text=coluna.title())#

            # selectmode="orange")
            self.arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title())+20)

        self.tx_busca.grid(row=0, column=1, sticky=NSEW)
        self.et_campo_busca.grid(row=1, column=1, sticky=NSEW)
        self.arvores_grid.grid(row=2, column=1, sticky=NSEW)

        #vsroolb.grid(row=2, column=2, sticky='ns')
        #hsroolb.grid(row=3, column=1,  sticky='ew')

        self.retornar_variaveis()
        self.lista_terminal_destruir = [
            fr_terminal_e_grid,
            fr_grid_variaveis,
            self.arvores_grid,
            self.tx_terminal,
            self.tx_busca,
            self.et_campo_busca,
            fr_fechar_menu,
            bt_fechar]

    # ************************************************************************* #
    #                           TRATAMENTO DE ERROS                             #
    # ************************************************************************* #

    def destruir_widget_mensagem_erro(self, objeto):
        try:
            if objeto is not None:
                objeto.grid_forget()
        except Exception as e:
            print("Erro ao destruir widget de erro", e)

    def abrir_dica_script_erro(self, dir_script):
        self.abrir_nova_aba()
        self.manipular_arquivos(None, "abrirArquivo", 'scripts/'+dir_script)

    def fechar_mensagem_de_erro(self, remover_marcacao=True):

        self.destruir_widget_mensagem_erro(self.bt_erro_aviso_fechar)
        self.destruir_widget_mensagem_erro(self.bt_erro_aviso_exemplo)
        self.destruir_widget_mensagem_erro(self.tx_erro_aviso_texto_erro)
        self.destruir_widget_mensagem_erro(self.fr_erro_aviso_texto_erro)
        self.destruir_widget_mensagem_erro(self.fr_erro_aviso)

        if remover_marcacao:
            try:
                self.tx_editor.tag_delete("codigoErro")
            except Exception as erro:
                print("Erro ao fechar possível mensagem de erro '{}'".format(erro))

    def realizar_coloração_erro(self, linha_que_deu_erro):
        lista = self.tx_editor .get(1.0, END)

        if linha_que_deu_erro is not None:
            lista = self.tx_editor.get(1.0, END).split("\n")

            palavra = "codigoErro"

            linha1 = str(linha_que_deu_erro) + ".0"
            linha2 = str(linha_que_deu_erro) + "." + str(len(lista[int(linha_que_deu_erro) - 1]))

            self.tx_editor.tag_add(palavra, linha1, linha2)
            self.tx_editor.tag_config(palavra, background="#572929")

    def mostrar_mensagem_de_erro(self, msg_erro, dir_script, linha_que_deu_erro):
        self.realizar_coloração_erro(linha_que_deu_erro)

        try:
            self.fechar_mensagem_de_erro(remover_marcacao=False)
        except Exception as e:
            print("Não foi possível abrir uma possível mensagem de erro", e)

        self.fr_erro_aviso = Frame(self.fr_princ, self.design.get('msg_erro_fr1'))
        self.fr_erro_aviso.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso.grid(row=2, column=2, sticky=NSEW)

        self.fr_erro_aviso_texto_erro = Frame(self.fr_erro_aviso, self.design.get('msg_erro_fr2'))
        self.fr_erro_aviso_texto_erro.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        self.tx_erro_aviso_texto_erro = Text(self.fr_erro_aviso_texto_erro, self.design.get('msg_erro_tx1'), relief=FLAT)
        self.tx_erro_aviso_texto_erro.insert(1.0, msg_erro)
        self.tx_erro_aviso_texto_erro.configure(self.design.get('msg_erro_tx1_disable'))
        self.tx_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        if dir_script != "":

            self.bt_erro_aviso_exemplo = Button(self.fr_erro_aviso,
                    self.design.get('msg_erro_bt1'),
                    text=self.interface_idioma["erro_ver_exemplo"][self.idioma],
                    command=lambda: self.abrir_dica_script_erro(self.arquivo_scripts[dir_script][self.idioma]))

            self.bt_erro_aviso_exemplo.grid(row=1, column=2)

        self.bt_erro_aviso_fechar = Button(self.fr_erro_aviso, self.design.get('msg_erro_bt2'), text="x", command=lambda event=None: self.fechar_mensagem_de_erro())
        self.bt_erro_aviso_fechar.grid(row=1, column=3)

    def adicionar_remover_breakpoint(self, event=None):
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

        self.desenhar_atualizar_linhas(event=None)

    def limpar_breakpoints(self):
        # Marcar um breakpoint
        if self.dic_abas[self.num_aba_focada]["lst_breakpoints"] == []:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = [int(x) for x in range(1, len(self.tx_editor.get(1.0, END).split("\n")))]

        else:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = []

        # Atualizar Breakpont no interpretador
        try:
            self.instancia.lst_breakpoints = self.dic_abas[self.num_aba_focada]["lst_breakpoints"]
        except Exception as e:
            print("Programa não está em execução, bkp ignorados", e)

        self.desenhar_atualizar_linhas(event=None)

    def liberar_um_breakpoint(self):
        self.libera_bkp = True

    def retornar_variaveis(self):
        try:
            dic_variaveis = self.instancia.dic_variaveis

            # IDS como argumentos
            self.arvores_grid.delete(*self.arvores_grid.get_children())

            palavra = self.et_campo_busca.get()

            for k, v in dic_variaveis.items():
                if palavra in k:
                    self.arvores_grid.insert('', END, values=(k, self.instancia.verificar_tipo(v), v))


        except Exception as e:
            print("instancia de variáveos não pronta ", e)


    # *********************************** #
    #          USOS DIVERSOS              #
    # *********************************** #

    def alterar_status_pressionou_enter(self, event=None):
        self.esperar_pressionar_enter = False

    def ativar_logs(self, event=None):
        self.bool_logs = False if self.bool_logs else True

    def atualizar_idioma(self):
        self.escolher_idioma.selecionar_idioma(self.dic_imgs)

    def ativar_modo_debug_temas(self):
        """
            Inicia o modo para atualizar os temas ou a sintaxe constantemente para
            a criação de novos temas
        """
        if self.bool_debug_temas:
            self.bool_debug_temas = False
        else:
            self.bool_debug_temas = True

    def desenhar_atualizar_linhas(self, event):
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas
        self.cont_lin.desenhar_linhas()

        self.cont_lin1.aba_focada2 = self.num_aba_focada
        self.cont_lin1.dic_abas2 = self.dic_abas
        self.cont_lin1.desenhar_linhas()
        self.fr_tela.update()

    def ativar_desativar_full_screen(self, event=None):
        self.bool_full_screen = False if self.bool_full_screen else True

        self.master.attributes("-fullscreen", self.bool_full_screen)
        self.fr_tela.update()

    def copiar_selecao(self):
        print("Copiado: ", self.tx_editor.event_generate("<<Copy>>"))

    def colar_selecao(self):
        try:
            self.tx_editor.delete("sel.first", "sel.last")
        except:
            pass

        texto_colar = self.tx_editor.clipboard_get()

        if "text doesn't contain any characters tagged with \"sel\"" != texto_colar:
            self.tx_editor.insert("insert", self.tx_editor.clipboard_get())
        return "break"

    def selecionar_tudo(self):
        self.tx_editor.tag_add(SEL, "1.0", END)
        self.tx_editor.mark_set(INSERT, "1.0")
        self.tx_editor.see(INSERT)
        return 'break'

    def atualizar_design_objeto(self, objeto, menu):
        try:
            objeto.configure(self.design.get(menu))
            objeto.update()

        except Exception as erro:
            print("Erro atualizar interface config = " + str(erro))

    def atualizar_design_interface(self):
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas

        self.cont_lin1.aba_focada2 = self.num_aba_focada
        self.cont_lin1.dic_abas2 = self.dic_abas

        self.atualizar_design_objeto(self.mn_interface_cascata_sintaxe, "cor_menu")
        self.atualizar_design_objeto(self.mn_interface_cascate_temas, "cor_menu")
        self.atualizar_design_objeto(self.mn_interface, "cor_menu")
        self.atualizar_design_objeto(self.mn_executar, "cor_menu")
        self.atualizar_design_objeto(self.mn_arquivo, "cor_menu")
        self.atualizar_design_objeto(self.mn_editar, "cor_menu")
        self.atualizar_design_objeto(self.mn_exemplos, "cor_menu")
        self.atualizar_design_objeto(self.mn_barra, "cor_menu")
        self.atualizar_design_objeto(self.mn_ajuda, "cor_menu")
        self.atualizar_design_objeto(self.mn_dev, "cor_menu")
        self.atualizar_design_objeto(self.bt_salvar, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_executar, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_executar_bkp, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_ajuda, "dicBtnMenus")
        self.atualizar_design_objeto(self.lb_aviso, "dicBtnMenus")
        self.atualizar_design_objeto(self.fr_aviso, "fr_dict_aviso")
        #self.atualizar_design_objeto(self.bt_pesquisar, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_copiar, "dicBtnCopiarColar")
        self.atualizar_design_objeto(self.bt_colar, "dicBtnCopiarColar")
        self.atualizar_design_objeto(self.bt_aviso, "dicBtnAviso")
        self.atualizar_design_objeto(self.bt_idioma, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_inserir_bkp, "dicBtnMenus")
        self.atualizar_design_objeto(self.bt_limpar_bkp, "dicBtnMenus")
        self.atualizar_design_objeto(self.fr_princ, "fr_princ")
        self.atualizar_design_objeto(self.fr_tela, "tela")
        self.atualizar_design_objeto(self.tx_editor, "tx_codificacao")
        self.atualizar_design_objeto(self.sb_codfc, "scrollbar_text")
        self.atualizar_design_objeto(self.fr_opcoes, "fr_opcoes_rapidas")
        self.atualizar_design_objeto(self.cont_lin, "lb_linhas")
        self.atualizar_design_objeto(self.cont_lin1, "lb_linhas")
        self.atualizar_design_objeto(self.fr_abas, "dic_cor_abas_frame")
        self.atualizar_design_objeto(self.fr_espaco, "dic_cor_abas_frame")
        self.atualizar_cor_abas()

    def obter_posicao_do_cursor(self, event=None):
        self.tx_editor.update()

        try:
            numPosicao = str(self.tx_editor.index(INSERT))
            posCorrente = int(float(self.tx_editor.index(CURRENT)))

        except Exception as erro:
            print("Erro ao obter a posição o cursor =", erro)

        else:
            p1, p2 = str(numPosicao).split('.')

            if event.keysym == "braceleft" or event.keysym == "{":
                texto_linha = self.tx_editor.get('current linestart', 'current lineend')

                num = len(texto_linha) - len(texto_linha.lstrip())

                texto_inserir = '\n    \n' + ' '*num + '} '

                self.tx_editor.insert('{}.{}'.format(p1, int(p2)), texto_inserir)
                self.tx_editor.mark_set("insert", "{}.{}".format(int(p1)+1, int(p2)+4))
            self.num_lin_bkp = posCorrente

    def atualizar_tema_sintaxe_da_interface(self, chave, novo):
        while True:
            try:
                funcoes.arquivo_de_configuracoes_interface(chave, novo)
            except Exception as e:
                print('''Erro ao atualizar o arquivo 
                    \'configuracoes/configuracoes.json\'. Sem esse arquivo, não
                    é possível atualizar os temas: '''+ str(e))
                return 0

            self.dic_comandos, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()
            self.design.update_design_dic()

            try:
                self.colorir_codigo.alterar_cor_comando(self.cor_do_comando)

                self.atualizar_design_interface()
                self.cont_lin.aba_focada2 = self.num_aba_focada
                self.cont_lin.dic_abas2 = self.dic_abas

                self.cont_lin1.aba_focada2 = self.num_aba_focada
                self.cont_lin1.dic_abas2 = self.dic_abas
                self.atualizar_coloracao_codigo_aba()

            except Exception as erro:
                print('ERRO: ', erro)
            else:
                print('Temas atualizados')

            self.fr_tela.update()
            self.tx_editor.update()

            if not self.bool_debug_temas:
                break

    def fechar_janela(self, inst):
        resposta = messagebox.askquestion(
            self.interface_idioma["tit_fechar_safira"][self.idioma],
            self.interface_idioma["msg_fechar_safira"][self.idioma],
            icon='warning')

        if resposta == 'yes':
            # Ocultar tkinter
            inst.withdraw()
            inst.destroy()
