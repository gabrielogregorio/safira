# -*- coding: utf-8 -*-

from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import CURRENT
from tkinter import Message
from tkinter import Button
from tkinter import INSERT
from tkinter import RAISED
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
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
from time import sleep
from time import time
from json import load
from os import getcwd
from os import listdir
from re import compile
from sys import version

import webbrowser
import requests
import re

from libs.interpretador import Interpretador
from libs.funcoes import carregar_json
from libs.arquivo import Arquivo
import libs.funcoes as funcoes
from visualizacao import ContadorLinhas
from visualizacao import EditorDeCodigo
from atualizar import Atualizar
from colorir import Colorir
from splash import Splash
from design import Design
from bug import Bug
from log import Log


# Theme One Dark
# sudo apt install python3-distutils
# sudo apt install python3-tk
# sudo apt-get install python3-pip
# sudo apt-get install python3-tk tk-dev

__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__github__ = 'https://github.com/Combratec/safira'
__description__ = 'Linguagem de programação focada em lógica'
__version__ = '0.3'
__project__ = 'Combratec'
__status__ = 'Desenvolvimento'
__date__ = '01/08/2019'


class Safira():
    """Classe que carrega o programa"""

    def __init__(self):
        self.dic_comandos, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

        self.design = Design()
        self.design.update_design_dic()

        # Obter o design configurado atualmente
        self.dic_design = self.design.get_design_dic()
        self.interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

        # Instância de tela principal
        self.tela = Tk()
        self.tela.withdraw()
        self.tela.rowconfigure(1, weight=1)
        self.tela.overrideredirect(1)
        self.tela.grid_columnconfigure(1, weight=1)
        self.splash = None

    def main(self):

        # Carregarmento do splash e da interface
        self.splash = Splash(self.design)
        interf = Interface(self.tela, self.dic_comandos, self.design, self.cor_do_comando, self.interface_idioma, self.splash)

        self.splash.splash_inicio()
        sleep(1)

        interf.carregar_tela_principal()


class Interface():
    def __init__(self, tela, dic_comandos, design, cor_do_comando, interface_idioma, splash):
        """ Classe da interface principal"""

        self.interface_idioma = interface_idioma
        self.cor_do_comando = cor_do_comando
        self.dic_comandos = dic_comandos
        self.splash = splash
        self.design = design
        self.tela = tela

        self.arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")
        self.arquivo_scripts = funcoes.carregar_json("configuracoes/scripts.json")
        self.dic_abas = {0: funcoes.carregar_json("configuracoes/guia.json")}

        self.idioma = self.arquivo_configuracoes['idioma']

        self.log = Log()
        self.bug = Bug(self.tela, design, self.idioma, self.interface_idioma)
        self.atualizar = Atualizar(self.tela, self.design, self.idioma, self.interface_idioma)
        self.colorir_codigo = Colorir(self.cor_do_comando, self.dic_comandos)

        self.log.adicionar_novo_acesso('logs/registros.json', 'acessos')
        self.path = abspath(getcwd())

        self.esperar_pressionar_enter = False
        self.bool_tela_em_fullscreen = False
        self.libera_breakpoint = False
        self.bool_debug_temas = False
        self.bool_logs = False

        self.lst_historico_abas_focadas = []
        self.lista_terminal_destruir = []
        self.lista_breakponts = []
        self.lista_botoes = []
        self.lst_abas = []
        self.imgs = []

        self.num_modulos_acionados = 0
        self.num_aba_focada = 0
        self.valor_threads = 0
        self.linha_analise = 0
        self.num_lin_bkp = 0
        self.posAbsuluta = 0
        self.posCorrente = 0

        self.dic_imgs = {"pt-br": "ic_pt_br.png", "en-us": "ic_en_us.png"}
        self.idioma = "pt-br"
        self.base = "imagens/"

        self.tx_erro_aviso_texto_erro = None
        self.fr_erro_aviso_texto_erro = None
        self.bt_erro_aviso_exemplo = None
        self.bt_erro_aviso_fechar = None
        self.tp_interface_idioma = None
        self.controle_arquivos = None
        self.tx_editor_codigo = None
        self.icone_breakpoint = None
        self.botao_pesquisar = None
        self.icone_play_stop = None
        self.icone_pesquisa = None
        self.fr_top_idioma = None
        self.fr_erro_aviso = None
        self.botao_salvar = None
        self.icone_salvar = None
        self.botao_copiar = None
        self.botao_idioma = None
        self.botao_colar = None
        self.icone_ajuda = None
        self.botao_ajuda = None
        self.icone_stop = None
        self.fr_idionas = None
        self.cont_lin = None
        self.cont_lin1 = None
        self.ic_brk_p = None
        self.fr_opcoe = None
        self.fr_princ = None
        self.bt_lp_bk = None
        self.bt_playP = None
        self.bt_breaP = None
        self.bt_brk_p = None
        self.fr__abas = None
        self.bt_play = None
        self.fr_tela = None
        self.bt_bt = None
        self.bt_bt = None
        self.fr_bt = None
        self.lb_bt = None
        self.lb1 = None
        self.id = None
        self.interpretador_finalizado = True

        self.interpretador_status = 'parado'

        # Carrega um dicionário com as primeiras letras de todos os comandos disponíveis
        self.dicLetras = Interface.carregar_dicionario_letra(self.dic_comandos)
        self.style_terminal = Interface.carregar_estilos_terminal(self)

        self.dic_regex_compilado = None
        self.re_comandos = None
        Interface.gerar_regex_compilado_interpretador(self)
        self.regex_interpretador = compile(r"^\:(.*?)\:(.*?)\:(.*?)\:(.*)")

    def gerar_regex_compilado_interpretador(self) -> None:
        print("Inicializador do orquestrador iniciado")
        diretorio_base = ''
        bool_ignorar_todos_breakpoints = True
        bool_logs = False


        instancia = Interpretador(
            bool_logs,
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"],
            bool_ignorar_todos_breakpoints,
            diretorio_base,
            self.dicLetras,
            self.dic_comandos,
            self.idioma,
            dic_regex_compilado=self.dic_regex_compilado,
            re_comandos = self.re_comandos)

        self.dic_regex_compilado = instancia.dic_regex_compilado
        self.re_comandos = instancia.re_comandos 
        del instancia





    def carregar_estilos_terminal(self):

        relief_titulo = self.design.dic["titulo_terminal"]["relief"]

        background_titulo = self.design.dic["titulo_terminal"]["background"]
        foreground_titulo = self.design.dic["titulo_terminal"]["foreground"]

        active_foreground_titulo = self.design.dic["titulo_terminal"]["active_foreground"]
        active_background_titulo = self.design.dic["titulo_terminal"]["active_background"]

        pressed_foreground_titulo = self.design.dic["titulo_terminal"]["pressed_foreground"]
        pressed_background_titulo = self.design.dic["titulo_terminal"]["pressed_background"]

        background_linha = self.design.dic["linha_terminal"]["background"]
        foreground_linha = self.design.dic["linha_terminal"]["foreground"]
        fieldbackground_linha = self.design.dic["linha_terminal"]["fieldbackground"]

        self.style_terminal = Style()
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
            background=self.design.dic["titulo_terminal"]["background"],
            foreground=self.design.dic["titulo_terminal"]["foreground"],
            relief=relief_titulo)

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
                ('active', '!disabled', active_background_titulo)]
        )

        return self.style_terminal

    def carregar_dicionario_letra(dic_comandos:dict) -> dict:
        """

        """
        dic_letras = {}

        # Anda por todos os comandos
        for k, v in dic_comandos.items():

            # Cria uma lista pela chave de cada comando
            dic_letras[k] = []

            # Para cada subcomando
            for valor in v["comando"]:

                # Pega a primeira letra do subcomando
                valor = valor[0].strip()

                # Adiona no dicionário a primeira letra do comando
                if valor == "":
                    dic_letras[k].append(valor)
                else:
                    valor = valor.lower()

                    if valor[0] not in dic_letras[k]:
                        dic_letras[k].append(valor[0])
        return dic_letras

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
                    # FINALIZAÇÃO COMPLETA
                    # Delete a instância
                    del self.instancia

                    # Insere mensagem de finalização
                    self.cont_lin1.linha_analise = 0
                    self.cont_lin1.desenhar_linhas()

                    self.bt_playP.configure(image=self.icone_play_stop)
                    print("############### FIM ############")
                    self.interpretador_status = 'parado'

            except Exception as erro:
                print("Instância inexistente")

            return 0

        elif self.interpretador_status == 'parado':
            self.interpretador_status = 'iniciado'
            self.interpretador_finalizado = False

            # Configura o icone de parar
            self.bt_playP.configure(image=self.icone_stop)
            self.bt_playP.update()
            
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
            self.tela.update()
            self.tx_editor_codigo.update()
            self.tx_terminal.update()

            # Linha que o interpretador está executando
            self.linha_analise = None

            # Obter o código
            linhas = self.tx_editor_codigo.get('1.0', END)[0:-1]

            # Adicionar marcação do número da linha
            linhas = Interface.colocar_linhas_codigo(self, linhas)

            # Obter o diretório base
            diretorio_base = self.dic_abas[self.num_aba_focada]["arquivoSalvo"]["link"]

            # Obter apenas o diretório
            diretorio_base = re.sub('([^\\/]{1,})$', '', diretorio_base)

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
                    self.tela.update()
                    self.tx_editor_codigo.update()
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
                    self.tx_editor_codigo.update()
                    self.tela.update()


                acao = ""
                # Obtem uma instrução do interpretador
                acao = self.instancia.controle_interpretador

                # Se existe uma ação
                if acao != "":
                    valores = None
                    valores = re.search(self.regex_interpretador, acao)

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


                            except:
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
                                self.tela.update()
                                self.tx_editor_codigo.update()
                                self.tx_terminal.update()
                            except:
                                self.instancia.aconteceu_erro = True
                                break

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
                        self.instancia.controle_interpretador = ""

                        # Limpa o terminal
                        try:
                            self.tx_terminal.delete('1.0', END)

                            # Atualiza o interpretador para continuar
                            self.instancia.controle_interpretador = ""
                        except Exception as erro:
                            self.instancia.aconteceu_erro = True
                            break


                    elif acao == 'aguardando_breakpoint':
                            # Aguarda o breakpoint ser liberado

                            try:
                                # Marca que chegou até a linha
                                linha_analise = int(self.instancia.num_linha)

                                self.cont_lin1.linha_analise = linha_analise
                                self.cont_lin1.desenhar_linhas() 
                                self.tx_editor_codigo.update()
                                self.tela.update()

                                
                                # Enquanto o breakpoint estiver preso
                                self.libera_breakpoint = False

                                # Enquanto o breakpoint não for liberado
                                while not self.libera_breakpoint:

                                    # Atualiza a tela
                                    self.tx_terminal.update()
                                    self.tx_editor_codigo.update()
                                    self.tela.update()

                                    if self.instancia.aconteceu_erro:
                                        break

                                # Libera o interpretador
                                self.instancia.controle_interpretador = ""

                                # Deixa breakpoint liberado
                                self.libera_breakpoint = False


                            except Exception as erro:
                                self.instancia.aconteceu_erro = True
                                break
                    else:
                        print("Instrução do Interpretador não é reconhecida => '{}'".format(acao))

            if self.instancia.aconteceu_erro:
                # Se o erro foi avisado
                if self.instancia.erro_alertado is True:

                    # Se não foi interrompido
                    if self.instancia.mensagem_erro != "Interrompido":

                        # Se não foi erro ao iniciar
                        if self.instancia.mensagem_erro != "Erro ao iniciar o Interpretador":

                            # Mostre uma mensagem complementar na tela
                            Interface.mostrar_mensagem_de_erro(self, self.instancia.mensagem_erro, self.instancia.dir_script_aju_erro, self.instancia.linha_que_deu_erro)

            else:
                try:
                    self.tx_terminal.insert(END, self.interface_idioma["script_finalizado"][self.idioma].format(time() - inicio))
                    self.tx_terminal.see("end")

                except Exception as erro:
                    print('Impossível exibir mensagem de finalização, erro: '+str(erro))

            self.interpretador_finalizado = True

            # Em modo que não seja debug, finalize o interpretador
            if tipo_execucao == 'continua' or not self.instancia.aconteceu_erro:
                Interface.inicializar_interpretador(self, tipo_execucao = 'parar')

            return 0

    def liberar_breakpoint_ou_inicicar(self, tipo_execucao):

        print(self.interpretador_status)

        if self.interpretador_status == 'parado':
            Interface.inicializar_interpretador(self, tipo_execucao='debug')
        else:
            self.libera_breakpoint = True

    # ************************************************************************* #
    #                             INTERFACE PRINCIPAL                           #
    # ************************************************************************* #
    def carregar_tela_principal(self):

        self.tela.overrideredirect(0) # Traz barra de titulo
        self.tela.withdraw() # Ocultar tkinter

        self.fr_tela = Frame(self.tela)
        self.fr_tela.grid(row=1, column=1, sticky=NSEW)
        self.fr_tela.update()
        self.tela.title('Combratec -  Safira Lang')
        self.tela.call('wm', 'iconphoto', self.tela._w, PhotoImage(file='imagens/icone.png'))
        self.fr_tela.rowconfigure(2, weight=1)
        self.fr_tela.grid_columnconfigure(1, weight=1)



        # COMANDOS
        comando_abrir_arquivo = lambda event=None: Interface.manipular_arquivos(self, None, "salvar_arquivo_dialog")
        comando_salvar_arquivo_como = lambda event=None: Interface.manipular_arquivos(self, None, "salvar_arquivo_como_dialog")
        comando_acao_salvararq = lambda event=None: Interface.manipular_arquivos(self, None, "salvar_arquivo")
        comando_inserir_breakp = lambda event=None: Interface.adicionar_remover_breakpoint(self, event)


        
        comando_executar_brakp = lambda event=None: Interface.liberar_breakpoint_ou_inicicar(self, tipo_execucao='debug')
        comando_parar_execucao = lambda event=None: Interface.inicializar_interpretador(self, tipo_execucao='parar')
        comando_executar_progr = lambda event=None: Interface.inicializar_interpretador(self, tipo_execucao='continua')

        comando_limpa_breakpon = lambda event=None: Interface.limpar_breakpoints(self)
        comando_abrir_abrir_nova_aba = lambda event=None: Interface.abrir_nova_aba(self, event)
        comando_ativar_fullscr = lambda event: Interface.ativar_desativar_full_screen(self, event)
        comando_abrir_disponiv = lambda: webbrowser.open(self.path + "/tutorial/comando.html")
        comando_abrir_comunida = lambda: webbrowser.open("https://safiraide.blogspot.com/p/comunidade.html")
        comando_abrirl_projeto = lambda: webbrowser.open("http://safiraide.blogspot.com/")
        comando_abrirlnk_ajuda = lambda: webbrowser.open(self.path + "/tutorial/comando.html")
        comando_ativaropc_logs = lambda: Interface.ativar_logs(self)
        comando_ativarop_debug = lambda: Interface.ativar_modo_debug_temas(self)
        comando_atualizar_idioma = lambda: Interface.atualizar_idioma(self)
        comando_aumentar_fonte = lambda: Interface.aumentar_diminuir_fonte(self, "+")
        comando_diminuir_fonte = lambda: Interface.aumentar_diminuir_fonte(self, "-")
        comando_copiar = lambda: Interface.copiar_selecao(self)
        comando_colar = lambda: Interface.colar_selecao(self)

        # TECLAS DE ATALHOS
        self.tela.bind('<Control-n>', comando_abrir_abrir_nova_aba)
        self.tela.bind('<Control-s>', comando_acao_salvararq)
        self.tela.bind('<Control-o>', comando_abrir_arquivo)
        self.tela.bind('<Control-S>', comando_salvar_arquivo_como)
        self.tela.bind('<F5>', comando_executar_progr)
        self.tela.bind('<F7>', comando_executar_brakp)
        self.tela.bind('<F10>', comando_inserir_breakp)
        self.tela.bind('<F11>', comando_ativar_fullscr)

        # MENU
        self.mn_barra = Menu(self.tela)
        self.tela.config(menu=self.mn_barra)

        # MENU OPCOES
        self.mn_intfc = Menu(self.mn_barra)
        self.mn_exect = Menu(self.mn_barra)
        self.mn_exemp = Menu(self.mn_barra)
        self.mn_arqui = Menu(self.mn_barra)
        self.mn_edita = Menu(self.mn_barra)
        self.mn_ajuda = Menu(self.mn_barra)
        self.mn_devel = Menu(self.mn_barra)

        # ADICAO DOS MENUS NA INTERFACE
        self.mn_barra.add_cascade(label=self.interface_idioma["label_arquivo"][self.idioma], menu=self.mn_arqui)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_executar"][self.idioma], menu=self.mn_exect)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_exemplos"][self.idioma], menu=self.mn_exemp)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_interface"][self.idioma], menu=self.mn_intfc)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_ajuda"][self.idioma], menu=self.mn_ajuda)
        self.mn_barra.add_cascade(label=self.interface_idioma["label_dev"][self.idioma], menu=self.mn_devel)

        # MENU ARQUIVOS
        self.mn_arqui.add_command(label=self.interface_idioma["label_abrir_arquivo"][self.idioma], command=comando_abrir_arquivo)
        self.mn_arqui.add_command(label=self.interface_idioma["label_nova_aba"][self.idioma], command=comando_abrir_abrir_nova_aba)
        self.mn_arqui.add_command(label=self.interface_idioma["label_salvar"][self.idioma], command=comando_acao_salvararq)
        self.mn_arqui.add_command(label=self.interface_idioma["label_salvar_como"][self.idioma], command=comando_salvar_arquivo_como)

        # MENU EXECUTAR
        self.mn_exect.add_command(label=self.interface_idioma["label_executar_tudo"][self.idioma], command=comando_executar_progr)
        self.mn_exect.add_command(label=self.interface_idioma["label_ate_breakpoint"][self.idioma], command=comando_executar_brakp)
        self.mn_exect.add_command(label=self.interface_idioma["label_parar_execucao"][self.idioma], command=comando_parar_execucao)
        self.mn_exect.add_command(label=self.interface_idioma["label_inserir_breakpoint"][self.idioma], command=comando_inserir_breakp)

        # MENU INTERFACE
        Interface.carregar_cascata_scripts(self)
        Interface.carregar_cascata_temas(self)
        Interface.carregar_cascata_sintaxe(self)

        print(1)

        self.mn_intfc.add_command(label=self.interface_idioma["label_mais"][self.idioma], command=comando_aumentar_fonte)
        self.mn_intfc.add_command(label=self.interface_idioma["label_menos"][self.idioma], command=comando_diminuir_fonte)

        # MENU AJUDA
        self.mn_ajuda.add_command(label=self.interface_idioma["label_ajuda"][self.idioma], command=comando_abrirlnk_ajuda)
        self.mn_ajuda.add_command(label=self.interface_idioma["label_comandos_disponiveis"][self.idioma], command=comando_abrir_disponiv)
        self.mn_ajuda.add_command(label=self.interface_idioma["label_reportar_bug"][self.idioma], command=lambda event=None: self.bug.interface())
        self.mn_ajuda.add_command(label=self.interface_idioma["label_verificar_atualizacao"][self.idioma], command=lambda event=None: self.atualizar.verificar_versao())
        
        # MENU DESENVOLVIMENTO
        self.mn_devel.add_command(label=self.interface_idioma["label_logs"][self.idioma], command=comando_ativaropc_logs)
        self.mn_devel.add_command(label='  Debug', command=comando_ativarop_debug)

        # IMAGENS PARA O MENU DE ACESSO RÁPIDO
        self.ic_left = PhotoImage(file='imagens/left.png')
        self.ic_rigth = PhotoImage(file='imagens/right.png')
        self.icone_salvar = PhotoImage(file='imagens/ic_salvar.png')
        self.icone_play_stop = PhotoImage(file='imagens/ic_play.png')
        self.icone_stop = PhotoImage(file='imagens/ic_parar.png')
        self.icone_breakpoint = PhotoImage(file='imagens/ic_play_breakpoint.png')
        self.ic_brk_p = PhotoImage(file='imagens/breakPoint.png')
        self.icone_ajuda = PhotoImage(file='imagens/ic_duvida.png')
        self.icone_pesquisa = PhotoImage(file='imagens/ic_pesquisa.png')
        self.ic_nsalv = PhotoImage(file="imagens/nao_salvo.png")
        self.iclp_bkp = PhotoImage(file="imagens/limpar_bkp.png")
        self.icone_idioma = PhotoImage(file="imagens/{}".format(self.dic_imgs[self.idioma]))

        # AJUSTES NO TAMANHO
        self.icone_salvar = self.icone_salvar.subsample(4, 4)
        self.icone_play_stop = self.icone_play_stop.subsample(4, 4)
        self.icone_stop = self.icone_stop.subsample(4, 4)
        self.icone_breakpoint = self.icone_breakpoint.subsample(4, 4)
        self.ic_brk_p = self.ic_brk_p.subsample(4, 4)
        self.icone_ajuda = self.icone_ajuda.subsample(4, 4)
        self.icone_pesquisa = self.icone_pesquisa.subsample(4, 4)
        self.ic_nsalv = self.ic_nsalv.subsample(2, 2)
        self.iclp_bkp = self.iclp_bkp.subsample(4, 4)
        self.icone_idioma = self.icone_idioma.subsample(4, 4)
        self.ic_left  = self.ic_left.subsample(4, 4)
        self.ic_rigth = self.ic_rigth.subsample(4, 4)

        # CRIANDO AS OPÇÔES RÁPIDAS
        self.fr_opcoe = Frame(self.fr_tela)

        # CARREGANDO AS OPÇÔES
        self.botao_salvar = Button(self.fr_opcoe, image=self.icone_salvar, command=comando_acao_salvararq)
        self.bt_playP = Button(self.fr_opcoe, image=self.icone_play_stop, command=comando_executar_progr)
        self.bt_breaP = Button(self.fr_opcoe, image=self.icone_breakpoint, command=comando_executar_brakp)
        self.bt_brk_p = Button(self.fr_opcoe, image=self.ic_brk_p, command=comando_inserir_breakp)
        self.bt_lp_bk = Button(self.fr_opcoe, image=self.iclp_bkp, command=comando_limpa_breakpon)
        self.botao_ajuda = Button(self.fr_opcoe, image=self.icone_ajuda)
        self.botao_pesquisar = Button(self.fr_opcoe, image=self.icone_pesquisa)
        self.botao_idioma = Button(self.fr_opcoe, image=self.icone_idioma, command=comando_atualizar_idioma)
        self.bt_left = Button(self.fr_opcoe, image=self.ic_left)
        self.bt_rigth = Button(self.fr_opcoe, image=self.ic_rigth)
        self.botao_copiar = Button(self.fr_opcoe, text="copiar", command=comando_copiar)
        self.botao_colar = Button(self.fr_opcoe, text="colar", command=comando_colar)


        self.fr_princ = Frame(self.fr_tela)
        self.fr_princ.grid_columnconfigure(2, weight=1)
        self.fr_princ.rowconfigure(1, weight=1)

        self.fr__abas = Frame(self.fr_princ, height=20)
        self.fr__abas.rowconfigure(1, weight=1)
        self.fr_espac = Label(self.fr__abas, width=5)

        Interface.carregar_abas_inicio(self)

        # ************ Tela de desenvolvimento do código ****************** #
        self.tx_editor_codigo = EditorDeCodigo(self.fr_princ, undo=True, autoseparators=True, maxundo=50, tabs=4)
        self.tx_editor_codigo.focus_force()

        self.tx_editor_codigo.bind('<Control-c>', lambda event=None: Interface.copiar_selecao(self))
        self.tx_editor_codigo.bind("<<Paste>>", lambda event=None: Interface.colar_selecao(self))
        self.tx_editor_codigo.bind('<Control-a>', lambda event=None: Interface.selecionar_tudo(self))
        self.tx_editor_codigo.bind("<<Change>>", lambda event: Interface.desenhar_atualizar_linhas(self, event))
        self.tx_editor_codigo.bind("<Configure>", lambda event: Interface.desenhar_atualizar_linhas(self, event))
        self.tx_editor_codigo.bind('<Button>', lambda event:  Interface.obter_posicao_do_cursor(self, event))
        self.tx_editor_codigo.bind('<KeyRelease>', lambda event: Interface.ativar_coordernar_coloracao(self, event))
        self.tx_editor_codigo.bind('<Control-MouseWheel>', lambda event: Interface.aumentar_diminuir_fonte(self, "+") if int(event.delta) > 0 else Interface.aumentar_diminuir_fonte(self, "-"))

        self.sb_codfc = Scrollbar(self.fr_princ, orient="vertical", command=self.tx_editor_codigo.yview, relief=FLAT)
        self.tx_editor_codigo.configure(yscrollcommand=self.sb_codfc.set)


        self.cont_lin = ContadorLinhas(self.fr_princ, self.design, bool_tem_linha = True)
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas
        self.cont_lin.atribuir(self.tx_editor_codigo)

        self.cont_lin1 = ContadorLinhas(self.fr_princ, self.design, bool_tem_linha = False)
        self.cont_lin1.aba_focada2 = self.num_aba_focada
        self.cont_lin1.dic_abas2 = self.dic_abas
        self.cont_lin1.atribuir(self.tx_editor_codigo)

        self.fr_espac.grid(row=1, column=0, sticky=NSEW)
        self.fr_opcoe.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        self.botao_salvar.grid(row=1, column=1)
        self.bt_playP.grid(row=1, column=4)
        self.bt_breaP.grid(row=1, column=5)
        self.bt_brk_p.grid(row=1, column=6)
        self.bt_lp_bk.grid(row=1, column=8)
        self.botao_ajuda.grid(row=1, column=11)
        self.botao_pesquisar.grid(row=1, column=12)
        self.botao_idioma.grid(row=1, column=13)
        self.botao_copiar.grid(row=1, column=14)
        self.botao_colar.grid(row=1, column=15)
        self.fr_princ.grid(row=2, column=1, sticky=NSEW)
        self.fr__abas.grid(row=0, column=1, columnspan=4, sticky=NSEW)
        self.cont_lin.grid(row=1, column=0, sticky=NSEW)
        self.cont_lin1.grid(row=1, column=1, sticky=NSEW)
        self.tx_editor_codigo.grid(row=1, column=2, sticky=NSEW)
        self.sb_codfc.grid(row=1, column=3, sticky=NSEW)

        # ******** Manipulação dos arquivos **************** #
        self.controle_arquivos = Arquivo(self.dic_abas, self.num_aba_focada, self.tx_editor_codigo)
        Interface.atualizar_design_interface(self)

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tela.geometry("{}x{}+0+0".format(t_width, t_heigth))
        self.colorir_codigo.tela = self.tela

        #Interface.manipular_arquivos(self, None, "abrirArquivo", 'script.safira')

        self.splash.splash_fim()

        self.tela.deiconify()
        self.tela.update()

        t = Thread(target=lambda self=self: Interface.buscar_atualização(self))
        t.start()
 
        self.tela.mainloop()

    def buscar_atualização(self):
        self.atualizar.verificar_versao(primeira_vez=True)

    def carregar_cascata_temas(self):
        self.mn_intfc_casct_temas = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label=self.interface_idioma["label_cascate_temas"][self.idioma], menu=self.mn_intfc_casct_temas)

        for file in listdir('temas/'):
            if 'theme.json' in file:

                arquivo = " " + file
                if self.arquivo_configuracoes["tema"] == file:
                    arquivo = "*" + file

                funcao = lambda link = file: Interface.atualizar_tema_sintaxe_da_interface(self, 'tema', str(link))
                self.mn_intfc_casct_temas.add_command(label=arquivo, command=funcao)

    def carregar_cascata_sintaxe(self):
        self.mn_intfc_casct_sintx = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label=self.interface_idioma["label_cascate_sintaxe"][self.idioma], menu=self.mn_intfc_casct_sintx)

        for file in listdir('temas/'):
            if 'sintaxe.json' in file:

                arquivo = " " + file
                if self.arquivo_configuracoes["sintaxe"] == file:
                    arquivo = "*" + file

                funcao = lambda link = file: Interface.atualizar_tema_sintaxe_da_interface(self, 'sintaxe', str(link))
                self.mn_intfc_casct_sintx.add_command(label=arquivo, command=funcao)

    def carregar_cascata_scripts(self):
        for file in listdir('scripts/' + self.idioma):
            if file.endswith("safira"):
                funcao = lambda link = file:  Interface.abrir_um_script(self, link)
                self.mn_exemp.add_command(label="  " + file + "  ", command=funcao)

    def abrir_um_script(self, link):
        if self.dic_abas[self.num_aba_focada]["arquivoAtual"]["texto"].strip() != "":
            Interface.abrir_nova_aba(self, None)

        Interface.manipular_arquivos(self, None, "abrirArquivo" , 'scripts/'+ self.idioma + '/' + str(link) )

    def manipular_arquivos(self, event, comando, link=None):
        if self.controle_arquivos is None: return 0
        retorno_salvar_como = None

        self.controle_arquivos.atualiza_infos(self.dic_abas, self.num_aba_focada, self.tx_editor_codigo)

        if comando == "abrirArquivo": self.controle_arquivos.abrirArquivo(link)
        elif comando == "salvar_arquivo_dialog": self.controle_arquivos.salvar_arquivo_dialog(event)
        elif comando == "salvar_arquivo": retorno_salvar_como = self.controle_arquivos.salvar_arquivo(event)
        elif comando == "salvar_arquivo_como_dialog": self.controle_arquivos.salvar_arquivo_como_dialog(event)

        self.num_aba_focada = self.controle_arquivos.aba_focada
        self.dic_abas = self.controle_arquivos.dic_abas

        if comando in ["abrirArquivo", "salvar_arquivo_como_dialog", "salvar_arquivo_dialog"] or retorno_salvar_como == "salvar_arquivo_como_dialog":
            Interface.atualizar_codigo_editor(self, self.num_aba_focada)

        return 0

    def aumentar_diminuir_fonte(self, acao):
        print("aumentar_diminuir_fonte")

        if acao == "+": adicao = 1
        else: adicao = -1

        self.design.dic["cor_menu"]["font"][1] = int(self.design.dic["cor_menu"]["font"][1]) + adicao
        self.design.dic["lb_sobDeTitulo"]["font"][1] = int(self.design.dic["lb_sobDeTitulo"]["font"][1]) + adicao
        self.design.dic["dicBtnMenus"]["font"][1] = int(self.design.dic["dicBtnMenus"]["font"][1]) + adicao
        self.design.dic["tx_terminal"]["font"][1] = int(self.design.dic["tx_terminal"]["font"][1]) + adicao
        self.design.dic["tx_codificacao"]["font"][1] = int(self.design.dic["tx_codificacao"]["font"][1]) + adicao
        self.design.dic["fonte_ct_linha"]["font"][1] = int(self.design.dic["fonte_ct_linha"]["font"][1]) + adicao
        self.design.dic["fonte_ct_linha"]["width"] = int(self.design.dic["fonte_ct_linha"]["width"]) + adicao

        self.tx_editor_codigo.configure(self.design.dic["tx_codificacao"])
        self.cont_lin.desenhar_linhas()
        self.cont_lin1.desenhar_linhas()

        self.tela.update()

    # ************************************************************************* #
    #                             MENU DE IDIOMAS                               #
    # ************************************************************************* #

    def interface_idioma(self):
        self.tp_interface_idioma = Toplevel(self.tela, bd=10, bg="#efefef")
        self.fr_top_idioma = Frame(self.tp_interface_idioma, bg="#efefef")
        self.fr_top_idioma.grid(row=1, column=1)

        self.lb1 = Label(self.fr_top_idioma, fg="#343434", bg="#efefef", text=self.interface_idioma["texto_atualizacao"][self.idioma])
        self.lb1.grid(row=1, column=1)

        self.fr_idionas = Frame(self.tp_interface_idioma, bg="#efefef")
        self.fr_idionas.grid(row=2, column=1)

        # Carregar as imagens
        self.imgs = []
        for k, v in self.dic_imgs.items():
            self.imgs.append(PhotoImage(file=self.base+v))

        # Carregar os botões
        x = 0
        self.lista_botoes = []
        for k, v in self.dic_imgs.items():

            if self.idioma == k:
                self.fr_bt = Frame(self.fr_idionas, bd=10, bg="#bbbbbb")
                self.bt_bt = Button(self.fr_bt,  image=self.imgs[x], bg="#bbbbbb", activebackground="#bbbbbb", highlightthickness=0, relief=FLAT, bd=0)
                self.lb_bt = Label(self.fr_bt,  text=k, bg="#bbbbbb", activebackground="#bbbbbb", highlightthickness=0, relief=FLAT, bd=0, fg="green")
            else:
                self.fr_bt = Frame(self.fr_idionas, bd=10, bg="#efefef")
                self.bt_bt = Button(self.fr_bt,  image=self.imgs[x], bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)
                self.lb_bt = Label(self.fr_bt,  text=k, bg="#efefef", activebackground="#efefef", highlightthickness=0, relief=FLAT, bd=0)

            self.bt_bt["command"] = lambda bt_bt=self.bt_bt : Interface.marcar_opcao_idioma(self, bt_bt)

            self.lista_botoes.append([self.fr_bt, self.bt_bt, self.lb_bt])

            self.fr_bt.grid(row=1, column=x)
            self.bt_bt.grid(row=1, column=x)
            self.lb_bt.grid(row=2, column=x)

            x += 1

    def marcar_opcao_idioma(self, botao):
        for bandeira in self.lista_botoes:
            if bandeira[1] == botao:
                bandeira[0].configure(bg="#bbbbbb")
                bandeira[1].configure(bg="#bbbbbb", activebackground="#bbbbbb")
                bandeira[2].configure(bg="#bbbbbb", activebackground="#bbbbbb", fg="green" )
                self.idioma = bandeira[2]["text"]

                self.icone_idioma = PhotoImage( file="imagens/{}".format(self.dic_imgs[self.idioma]) )
                self.icone_idioma = self.icone_idioma.subsample(4, 4)
                self.botao_idioma["image"] = self.icone_idioma

                Interface.atualizar_tema_sintaxe_da_interface(self, "idioma", self.idioma)

                self.tp_interface_idioma.destroy()

                self.tp_interface_idioma = None
                self.fr_top_idioma = None
                self.lb1 = None
                self.fr_idionas = None
                self.fr_bt = None
                self.bt_bt = None
                self.lb_bt = None
                self.bt_bt = None

            else:
                bandeira[0].configure(bg="#efefef")
                bandeira[1].configure(bg="#efefef", activebackground="#efefef")
                bandeira[2].configure(bg="#efefef", activebackground="#efefef", fg="black")

    # ************************************************************************* #
    #                                  Abas                                     #
    # ************************************************************************* #
    def ativar_coordernar_coloracao(self, event=None):
        Interface.fechar_mensagem_de_erro(self)
        Interface.atualizar_coloracao_codigo_aba(self, True, event)

        if self.dic_abas != {}:
            self.dic_abas[ self.num_aba_focada ]["arquivoAtual"]['texto'] = self.tx_editor_codigo.get(1.0, END)
            if self.dic_abas[ self.num_aba_focada ]["arquivoAtual"]['texto'] != self.dic_abas[ self.num_aba_focada ]["arquivoSalvo"]['texto']:

                if self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] == False:
                    self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = True

                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()
                    largura_original = self.dic_abas[self.num_aba_focada]["listaAbas"][3].winfo_reqwidth()

                    self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(image=self.ic_nsalv, width=largura_original)

            else:
                self.dic_abas[self.num_aba_focada]["listaAbas"][3].config(image='', width=0)
                self.dic_abas[self.num_aba_focada]["ja_foi_marcado_nao_salvo"] = False

            self.dic_abas[self.num_aba_focada]["listaAbas"][3].update()

        if hasattr(event, "keysym"):
            Interface.obter_posicao_do_cursor(self, event)

    def configurar_cor_aba(self, dic_cor_abas, bg_padrao, dic_cor_botao, dic_cor_marcador):
        self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(dic_cor_botao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][3].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground=bg_padrao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][2].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][1].configure(dic_cor_marcador)
        self.dic_abas[self.num_aba_focada]["listaAbas"][1].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][0].configure(background=bg_padrao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][0].update()

    def carregar_abas_inicio(self):
        """
            Usado apenas no inicio do programa *****1 VEZ*****
        """
        for num_aba, dados_aba in self.dic_abas.items():
            # Coloração da aba
            if dados_aba["foco"]:
                self.num_aba_focada = num_aba
                dic_cor_marcador = self.design.dic["dic_cor_marcador_focado"]
                dic_cor_finao = self.design.dic["dic_cor_abas_focada"]
                dic_cor_botao = self.design.dic["dic_cor_abas_focada_botao"]
            else:
                dic_cor_marcador = self.design.dic["dic_cor_marcador_nao_focado"]
                dic_cor_finao = self.design.dic["dic_cor_abas_nao_focada"]
                dic_cor_botao = self.design.dic["dic_cor_abas_nao_focada_botao"]

            fr_uma_aba = Frame(self.fr__abas, backgroun=dic_cor_finao["background"])
            fr_uma_aba.rowconfigure(1, weight=1)

            nome_arquivo = str(dados_aba["arquivoSalvo"]["link"]).split("/")
            nome_arquivo = str(nome_arquivo[-1])

            txt_btn = "x "

            if nome_arquivo.strip() == "":
                nome_arquivo = "            "
            else:
                nome_arquivo = " " + nome_arquivo

            fr_marcador = Frame(fr_uma_aba, dic_cor_marcador, padx=100, bd=10)
            lb_aba = Button(fr_uma_aba, dic_cor_finao, text=nome_arquivo, border=0, highlightthickness=0)
            bt_fechar = Button(fr_uma_aba, dic_cor_botao, text=txt_btn, relief=FLAT, border=0, highlightthickness=0)

            bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Interface.realcar_cor_botao_fechar_aba(self, bt_fechar))
            bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Interface.voltar_cor_botao_fechar_aba(self, padrao, bt_fechar))

            lb_aba.bind('<ButtonPress>', lambda event=None, num_aba=num_aba: Interface.atualizar_foco_da_aba(self, num_aba))
            bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Interface.fechar_uma_aba(self, bt_fechar))

            fr_uma_aba.update()
            fr_marcador.update()
            lb_aba.update()
            bt_fechar.update()

            fr_uma_aba.grid(row=1, column=num_aba+2, sticky=N)
            fr_marcador.grid(row=0, column=1, columnspan=2, sticky=NSEW)
            lb_aba.grid(row=1, column=1, sticky=NSEW)
            bt_fechar.grid(row=1, column=2)

            self.dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
            self.dic_abas[num_aba]["listaAbas"].append(fr_marcador)
            self.dic_abas[num_aba]["listaAbas"].append(lb_aba)
            self.dic_abas[num_aba]["listaAbas"].append(bt_fechar)

    def abrir_nova_aba(self, event=None):
        # Adicionar na posição 0
        posicao_adicionar = 0

        if len(self.dic_abas) != 0:
            dic_cor_finao = self.design.dic["dic_cor_abas_nao_focada"]
            dic_cor_botao = self.design.dic["dic_cor_abas_nao_focada_botao"]
            dic_cor_marcador = self.design.dic["dic_cor_marcador_nao_focado"]

            Interface.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
            posicao_adicionar = max(self.dic_abas.keys())+1

        self.dic_abas[posicao_adicionar] = funcoes.carregar_json("configuracoes/guia.json")

        dic_cor_finao = self.design.dic["dic_cor_abas_focada"]

        dic_cor_botao = self.design.dic["dic_cor_abas_focada_botao"]
        dic_cor_marcador = self.design.dic["dic_cor_marcador_focado"]


        fr_uma_aba = Frame(self.fr__abas, background=dic_cor_finao["background"])

        fr_marcador = Frame(fr_uma_aba, dic_cor_marcador)
        lb_aba = Button(fr_uma_aba, dic_cor_finao, text="              ", border=0, highlightthickness=0)
        bt_fechar = Button(fr_uma_aba, dic_cor_botao, text="x ", relief=FLAT, border=0, highlightthickness=0)

        lb_aba.bind('<ButtonPress>', lambda event=None, num_aba=posicao_adicionar: Interface.atualizar_foco_da_aba(self, num_aba))
        bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Interface.fechar_uma_aba(self, bt_fechar))
        bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Interface.realcar_cor_botao_fechar_aba(self, bt_fechar))
        bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Interface.voltar_cor_botao_fechar_aba(self, padrao, bt_fechar))

        fr_uma_aba.rowconfigure(1, weight=1)

        fr_uma_aba.grid(row=1, column=posicao_adicionar+2, sticky=N)
        fr_marcador.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_marcador)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

        self.num_aba_focada = posicao_adicionar
        Interface.atualizar_codigo_editor(self, self.num_aba_focada)

    def fechar_uma_aba(self, bt_fechar):
        bool_era_focado = False

        dic_cor_abas = self.design.dic["dic_cor_abas"]
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:

                while chave in self.lst_historico_abas_focadas:
                    self.lst_historico_abas_focadas.remove(chave)

                if len(self.dic_abas) == 1:
                    self.dic_abas[chave]["nome"] =""
                    self.dic_abas[chave]["lst_breakpoints"] = []
                    self.dic_abas[chave]["arquivoSalvo"] = {"link": "", "texto": ""}
                    self.dic_abas[chave]["arquivoAtual"] = {"texto": ""}

                    Interface.atualizar_codigo_editor(self, chave)
                    self.lst_historico_abas_focadas.append(chave)
                    return 0

                else:
                    self.dic_abas[chave]["listaAbas"][3].update()
                    self.dic_abas[chave]["listaAbas"][3].grid_forget()
                    self.dic_abas[chave]["listaAbas"][2].update()
                    self.dic_abas[chave]["listaAbas"][2].grid_forget()
                    self.dic_abas[chave]["listaAbas"][1].update()
                    self.dic_abas[chave]["listaAbas"][1].grid_forget()
                    self.dic_abas[chave]["listaAbas"][0].update()
                    self.dic_abas[chave]["listaAbas"][0].grid_forget()

                    if self.dic_abas[chave]["foco"] is True:
                        bool_era_focado = True
                    del self.dic_abas[chave]
                    break

        # Aba fechada era a focada
        if bool_era_focado:

            try:
                chave = self.lst_historico_abas_focadas[-1]
            except:
                for k, valor in self.dic_abas.items():
                    chave = k
                    break

            dic_cor_finao = self.design.dic["dic_cor_abas_focada"]
            dic_cor_botao = self.design.dic["dic_cor_abas_focada_botao"]
            dic_cor_marcador = self.design.dic["dic_cor_marcador_focado"]
            self.num_aba_focada = chave
            self.dic_abas[chave]["foco"] =True

            Interface.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
            Interface.atualizar_codigo_editor(self, chave)

            self.lst_historico_abas_focadas.append(chave)
            Interface.atualizar_coloracao_codigo_aba(self)
            return 0

    def atualizar_foco_da_aba(self, num_aba):
        if num_aba == self.num_aba_focada:
            return 0

        dic_cor_finao = self.design.dic["dic_cor_abas_nao_focada"]
        dic_cor_botao = self.design.dic["dic_cor_abas_nao_focada_botao"]
        dic_cor_marcador = self.design.dic["dic_cor_marcador_nao_focado"]
        Interface.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)

        self.dic_abas[self.num_aba_focada]["foco"] = False

        dic_cor_finao = self.design.dic["dic_cor_abas_focada"]
        dic_cor_botao = self.design.dic["dic_cor_abas_focada_botao"]
        dic_cor_marcador = self.design.dic["dic_cor_marcador_focado"]


        self.num_aba_focada = num_aba
        self.dic_abas[num_aba]["foco"] = True

        self.lst_historico_abas_focadas.append(num_aba)

        Interface.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
        Interface.atualizar_codigo_editor(self, num_aba)

        Interface.atualizar_coloracao_codigo_aba(self)

    def atualizar_coloracao_codigo_aba(self, limpar=False, event=None):
        # num_modulos_acionados => 0

        if event is not None:
            if event.keysym in ('Down', 'Up', 'Left', 'Right', 'Return', 'BackSpace'):
                return 0

        self.num_modulos_acionados += 1

        if self.num_modulos_acionados > 3:
            return 0

        if self.num_modulos_acionados == 2:
            while self.num_modulos_acionados != 0:
                self.tela.update()
            self.num_modulos_acionados += 1

        if limpar:
            self.colorir_codigo.historico_coloracao = []
        self.colorir_codigo.coordena_coloracao(None, tx_editor_codigo=self.tx_editor_codigo)

        self.num_modulos_acionados = 0

    def atualizar_codigo_editor(self, num_aba):
        self.tx_editor_codigo.delete(1.0, END)
        self.tx_editor_codigo.insert(END, str(self.dic_abas[num_aba]["arquivoAtual"]["texto"])[0:-1])

        nome_arquivo = self.dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if nome_arquivo.strip() == "":
            nome_arquivo = " " * 14

        self.dic_abas[num_aba]["listaAbas"][2].configure(text=nome_arquivo)

        for x in range(0, 3):
            self.dic_abas[num_aba]["listaAbas"][x].update()

        Interface.atualizar_coloracao_codigo_aba(self, True)

    def realcar_cor_botao_fechar_aba(self, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(self.design.dic["dic_cor_abas_botao_fechar_focada"])
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def voltar_cor_botao_fechar_aba(self, padrao, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(foreground=padrao)
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    # ************************************************************************* #
    #                      TERMINAL COM A EXECUÇÂO                              #
    # ************************************************************************* #
    def destruir_instancia_terminal(self):
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

    def iniciar_terminal_direto(self):
        Interface.destruir_instancia_terminal(self)

        self.top_janela_terminal = Toplevel(self.tela)
        self.top_janela_terminal.protocol("WM_DELETE_WINDOW", lambda event=None: Interface.destruir_instancia_terminal(self))

        self.top_janela_terminal.grid_columnconfigure(1, weight=1)
        self.top_janela_terminal.rowconfigure(1, weight=1)
        # Ocultar tkinter
        self.top_janela_terminal.withdraw()

        t_width  = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.top_janela_terminal.geometry("720x450+{}+{}".format(int(t_width/720/2), int(t_heigth/450/2)))
        self.top_janela_terminal.deiconify()
        self.tela.update()
        self.tx_terminal = Text(self.top_janela_terminal)

        try:
            self.tx_terminal.configure(self.design.dic["tx_terminal"])
        except Exception as erro:
            print("Erro 2 ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Interface.alterar_status_pressionou_enter(self, event))
        #self.tx_terminal.bind("<KeyRelease>", lambda event: Interface.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)
        self.tx_terminal.update()
        self.tx_terminal.get(1.0, END)
        self.lista_terminal_destruir = [self.top_janela_terminal, self.tx_terminal]

    def iniciar_terminal_debug(self):
        Interface.destruir_instancia_terminal(self)

        coluna_identificadores = (
            self.interface_idioma["debug_variavel"][self.idioma],
            self.interface_idioma["debug_tipo"][self.idioma],
            self.interface_idioma["debug_valor"][self.idioma])

        frame_terminal_e_grid = Frame(self.fr_princ, bg="#191913")
        frame_terminal_e_grid.grid(row=1, column=4, rowspan=2, sticky=NSEW)
        frame_terminal_e_grid.grid_columnconfigure(1, weight=1)
        frame_terminal_e_grid.rowconfigure(1, weight=1)

        fr_fechar_menu = Frame(frame_terminal_e_grid, height=10, bg="#191913")
        fr_fechar_menu.grid_columnconfigure(1, weight=1)
        fr_fechar_menu.grid(row=0, column=1, sticky=NSEW)

        bt_fechar = Button(fr_fechar_menu, text="x", fg="#f1f1f1", bg="#191913", activebackground="#191913", command=lambda event=None: Interface.destruir_instancia_terminal(self))
        bt_fechar.configure(relief=FLAT, highlightthickness=0, bd=0, font=("", 12))
        bt_fechar.grid(row=0, column=1, sticky="E")

        self.tx_terminal = Text(frame_terminal_e_grid)

        try:
            self.tx_terminal.configure(self.design.dic["tx_terminal"])
        except Exception as erro:
            print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Interface.alterar_status_pressionou_enter(self))
        #self.tx_terminal.bind("<KeyRelease>", lambda event: Interface.capturar_tecla_terminal(self, event))
        self.tx_terminal.focus_force()
        self.tx_terminal.grid(row=1, column=1, sticky=NSEW)

        fram_grid_variaveis = Frame(frame_terminal_e_grid, self.design.dic["cor_grid_variaveis"])
        fram_grid_variaveis.grid(row=2, column=1, sticky=NSEW)

        fram_grid_variaveis.grid_columnconfigure(1, weight=1)
        fram_grid_variaveis.rowconfigure(2, weight=1)

        self.texto_busca = Label(fram_grid_variaveis, self.design.dic["cor_grid_variaveis_texto_busca"], text=self.interface_idioma["debug_faca_busca"][self.idioma])
        self.campo_busca = Entry(fram_grid_variaveis, self.design.dic["cor_grid_variaveis_campo_busca"])
        self.campo_busca.bind("<KeyRelease>", lambda event: Interface.retornar_variaveis(self))

        self.arvores_grid = Treeview(fram_grid_variaveis, columns=coluna_identificadores, show="headings", style="Custom.Treeview")
        self.arvores_grid.tag_configure('RED_TAG', foreground='red', font=('arial', 12))

        vsroolb = Scrollbar(fram_grid_variaveis, self.design.dic["cor_grid_variaveis_scrollbar"], relief=FLAT, orient="vertical", command=self.arvores_grid.yview)
        hsroolb = Scrollbar(fram_grid_variaveis, self.design.dic["cor_grid_variaveis_scrollbar"], relief=FLAT, orient="horizontal", command=self.arvores_grid.xview)

        self.arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)

        for coluna in coluna_identificadores:
            # parametro a se analisar = selectmode="#f1a533")
            self.arvores_grid.heading(coluna, text=coluna.title())

            # selectmode="orange")
            self.arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title())+20)

        self.texto_busca.grid(row=0, column=1, sticky=NSEW)
        self.campo_busca.grid(row=1, column=1, sticky=NSEW)
        self.arvores_grid.grid(row=2, column=1, sticky=NSEW)

        vsroolb.grid(row=2, column=2, sticky='ns')
        hsroolb.grid(row=3, column=1,  sticky='ew')

        Interface.retornar_variaveis(self)
        self.lista_terminal_destruir = [
            frame_terminal_e_grid,
            fram_grid_variaveis,
            self.arvores_grid,
            self.tx_terminal,
            self.texto_busca,
            self.campo_busca,
            fr_fechar_menu,
            bt_fechar,
            vsroolb,
            hsroolb]

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
        Interface.abrir_nova_aba(self)
        Interface.manipular_arquivos(self, None, "abrirArquivo", 'scripts/'+dir_script)

    def fechar_mensagem_de_erro(self, remover_marcacao=True):

        Interface.destruir_widget_mensagem_erro(self, self.bt_erro_aviso_fechar)
        Interface.destruir_widget_mensagem_erro(self, self.bt_erro_aviso_exemplo)
        Interface.destruir_widget_mensagem_erro(self, self.tx_erro_aviso_texto_erro)
        Interface.destruir_widget_mensagem_erro(self, self.fr_erro_aviso_texto_erro)
        Interface.destruir_widget_mensagem_erro(self, self.fr_erro_aviso)

        if remover_marcacao:
            self.tx_editor_codigo.tag_delete("codigoErro")

    def realizar_coloração_erro(self, linha_que_deu_erro):
        lista = self.tx_editor_codigo .get(1.0, END)

        if linha_que_deu_erro is not None:
            lista = self.tx_editor_codigo.get(1.0, END).split("\n")

            palavra = "codigoErro"
            linha1 = str(linha_que_deu_erro) + ".0"
            linha2 = str(linha_que_deu_erro) + "." + str(len(lista[int(linha_que_deu_erro) - 1]))

            self.tx_editor_codigo.tag_add(palavra, linha1, linha2)
            self.tx_editor_codigo.tag_config(palavra, background="#572929")

    def mostrar_mensagem_de_erro(self, msg_erro, dir_script, linha_que_deu_erro):
        Interface.realizar_coloração_erro(self, linha_que_deu_erro)

        try:
            Interface.fechar_mensagem_de_erro(self, remover_marcacao=False)
        except Exception as e:
            print("Não foi possível abrir uma possível mensagem de erro", e)

        self.fr_erro_aviso = Frame(self.fr_princ, height=50, bg="#111121", bd=10, highlightthickness=10, highlightbackground="#222232", highlightcolor="#222232")
        self.fr_erro_aviso.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso.grid(row=2, column=2, sticky=NSEW)

        self.fr_erro_aviso_texto_erro = Frame(self.fr_erro_aviso, bg="#111121")
        self.fr_erro_aviso_texto_erro.grid_columnconfigure(1, weight=1)
        self.fr_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        self.tx_erro_aviso_texto_erro = Text(self.fr_erro_aviso_texto_erro, bg="#111121", fg="#ff9696", height=2, highlightthickness=0, relief=FLAT)
        self.tx_erro_aviso_texto_erro.insert(1.0, msg_erro)
        self.tx_erro_aviso_texto_erro.configure(state="disable", selectbackground="#222232")
        self.tx_erro_aviso_texto_erro.grid(row=1, column=1, sticky=NSEW)

        if dir_script != "":
            self.bt_erro_aviso_exemplo = Button(self.fr_erro_aviso, text=self.interface_idioma["erro_ver_exemplo"][self.idioma], relief="flat", fg="green", activeforeground="green", bg="#111121", activebackground="#111121", font=("", 13), command=lambda abc=self: Interface.abrir_dica_script_erro(abc, self.arquivo_scripts[dir_script][self.idioma]))
            self.bt_erro_aviso_exemplo.grid(row=1, column=2)

        self.bt_erro_aviso_fechar = Button(self.fr_erro_aviso, text="x", relief="sunken", fg="#ff9696", activeforeground="#ff9696", bg="#111121", activebackground="#111121", font=("", 13), highlightthickness=0, bd=0, command=lambda event=None: Interface.fechar_mensagem_de_erro(self))
        self.bt_erro_aviso_fechar.grid(row=1, column=3)

    # ************************************************************************* #
    #                            PONTOS DE PARADA                               #
    # ************************************************************************* #

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

        Interface.desenhar_atualizar_linhas(self, event=None)

    def limpar_breakpoints(self):
        if self.dic_abas[self.num_aba_focada]["lst_breakpoints"] == []:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = [x for x in range(0, len(self.tx_editor_codigo.get(1.0, END).split("\n")))]

        else:
            self.dic_abas[self.num_aba_focada]["lst_breakpoints"] = []
        
        Interface.desenhar_atualizar_linhas(self, event=None)

        try:
            self.instancia.lst_breakpoints = self.dic_abas[self.num_aba_focada]["lst_breakpoints"]
        except Exception as e:
            print("Programa não está em execução, bkp ignorados", e)

    def liberar_um_breakpoint(self):
        self.libera_breakpoint = True

    # ************************************************************************* #
    #                           GRID DE VARIÀVEIS                               #
    # ************************************************************************* #

    def retornar_variaveis(self):
        try:
            dic_variaveis = self.instancia.dic_variaveis

        except Exception as e:
            print("instancia de variáveos não pronta ", e)

        else:
            # IDS como argumentos
            self.arvores_grid.delete(*self.arvores_grid.get_children())

            palavra = self.campo_busca.get()

            for k, v in dic_variaveis.items():
                if palavra in k:
                    caracteres = ""
                    if v[1] == 'lista':
                        for x in v[0]:
                            if caracteres == "":
                                caracteres += '"' + str(x[0]) + '"'
                            else:
                                caracteres += ', "' + str(x[0]) + '"'
                    else:
                        caracteres = v[0]

                    self.arvores_grid.insert('', END, values=(k, v[1], caracteres))

    # ************************************************************************* #
    #                             USOS DIVERSOS                                 #
    # ************************************************************************* #

    def alterar_status_pressionou_enter(self, event=None):
        self.esperar_pressionar_enter = False

    def ativar_logs(self, event=None):
        self.bool_logs = False if self.bool_logs else True

    def atualizar_idioma(self):
        Interface.interface_idioma(self)

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
        self.tela.update()

    def ativar_desativar_full_screen(self, event=None):
        self.bool_tela_em_fullscreen = False if self.bool_tela_em_fullscreen else True

        self.tela.attributes("-fullscreen", self.bool_tela_em_fullscreen)
        self.tela.update()

    def copiar_selecao(self):
        self.tx_editor_codigo.event_generate("<<Copy>>")

    def colar_selecao(self):
        try:
            self.tx_editor_codigo.delete("sel.first", "sel.last")
        except:
            pass

        self.tx_editor_codigo.insert("insert", self.tx_editor_codigo.clipboard_get())
        return "break"

    def selecionar_tudo(self):
        self.tx_editor_codigo.tag_add(SEL, "1.0", END)
        self.tx_editor_codigo.mark_set(INSERT, "1.0")
        self.tx_editor_codigo.see(INSERT)
        return 'break'

    def atualizar_design_objeto(self, objeto, menu):
        try:
            objeto.configure(self.design.dic[menu])
            objeto.update()

        except Exception as erro:
            print("Erro Atualiza interface config = " + str(erro))

    def atualizar_design_interface(self):
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas

        self.cont_lin1.aba_focada2 = self.num_aba_focada
        self.cont_lin1.dic_abas2 = self.dic_abas


        Interface.atualizar_design_objeto(self, self.mn_intfc_casct_sintx, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_intfc_casct_temas, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_intfc, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_exect, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_arqui, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_edita, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_exemp, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_barra, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_ajuda, "cor_menu")
        Interface.atualizar_design_objeto(self, self.mn_devel, "cor_menu")
        Interface.atualizar_design_objeto(self, self.botao_salvar, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.bt_playP, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.bt_breaP, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.botao_ajuda, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.botao_pesquisar, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.botao_copiar, "dicBtnCopiarColar")
        Interface.atualizar_design_objeto(self, self.botao_colar, "dicBtnCopiarColar")
        Interface.atualizar_design_objeto(self, self.botao_idioma, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.bt_brk_p, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.bt_lp_bk, "dicBtnMenus")
        Interface.atualizar_design_objeto(self, self.fr_princ, "fr_princ")
        Interface.atualizar_design_objeto(self, self.tela, "tela")
        Interface.atualizar_design_objeto(self, self.tx_editor_codigo, "tx_codificacao")
        Interface.atualizar_design_objeto(self, self.sb_codfc, "scrollbar_text")
        Interface.atualizar_design_objeto(self, self.fr_opcoe, "fr_opcoes_rapidas")
        Interface.atualizar_design_objeto(self, self.cont_lin, "lb_linhas")
        Interface.atualizar_design_objeto(self, self.cont_lin1, "lb_linhas")
        Interface.atualizar_design_objeto(self, self.fr__abas, "dic_cor_abas_frame")
        Interface.atualizar_design_objeto(self, self.fr_espac, "dic_cor_abas_frame")

    def obter_posicao_do_cursor(self, event=None):
        try:
            numPosicao = str(self.tx_editor_codigo.index(INSERT))
            posCorrente = int(float(self.tx_editor_codigo.index(CURRENT)))

        except Exception as erro:
            print("Erro ao obter a posição o cursor =", erro)

        else:
            p1, p2 = str(numPosicao).split('.')
            if event.keysym == "braceleft" or event.keysym == "{":
                self.tx_editor_codigo.insert('{}.{}'.format(p1, int(p2)), '\n    \n}')
                self.tx_editor_codigo.mark_set("insert", "{}.{}".format(int(p1)+1, int(p2)+4))

            self.num_lin_bkp = posCorrente

    def arquivo_de_configuracoes_interface(self, chave, novo):
        arquivo = 'configuracoes/configuracoes.json'

        config_json = funcoes.carregar_json(arquivo)
        config_json[chave] = novo
        config_json = str(config_json).replace('\'', '\"')

        funcoes.salvar_arquivo(arquivo, config_json)

    def atualizar_tema_sintaxe_da_interface(self, chave, novo):
        while True:
            try:
                Interface.arquivo_de_configuracoes_interface(self, chave, novo)
            except Exception as e:
                print('Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas')
                return 0

            self.dic_comandos, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()
            self.design.update_design_dic()

            try:
                self.colorir_codigo.alterar_cor_comando(self.cor_do_comando)

                Interface.atualizar_design_interface(self)
                self.cont_lin.aba_focada2 = self.num_aba_focada
                self.cont_lin.dic_abas2 = self.dic_abas

                self.cont_lin1.aba_focada2 = self.num_aba_focada
                self.cont_lin1.dic_abas2 = self.dic_abas
                Interface.atualizar_coloracao_codigo_aba(self)

            except Exception as erro:
                print('ERRO: ', erro)
            else:
                print('Temas atualizados')

            self.tela.update()
            self.tx_editor_codigo.update()

            if not self.bool_debug_temas:
                break


if __name__ == "__main__":
    app = Safira()
    app.main()
