# -*- coding: utf-8 -*-

from tkinter               import SEL
from tkinter               import CURRENT
from tkinter               import INSERT
from tkinter               import RAISED
from tkinter               import FLAT 
from tkinter               import END
from tkinter               import NSEW
from tkinter               import N
from tkinter               import W
from tkinter               import Toplevel
from tkinter               import PhotoImage
from tkinter               import messagebox
from tkinter               import Scrollbar
from tkinter               import Button
from tkinter               import Frame
from tkinter               import Label
from tkinter               import Entry
from tkinter               import Message
from tkinter               import Tk
from tkinter               import messagebox
from tkinter               import Text
from tkinter               import Menu
from os.path               import abspath
from tkinter.ttk           import Treeview
from tkinter.ttk           import Style
from threading             import Thread
from time                  import sleep
from time                  import time
from json                  import load
from os                    import getcwd
from os                    import listdir
from sys                   import version
import tkinter.font as tkFont
import re
import webbrowser

import webbrowser
import requests

from libs.funcoes          import carregar_json
from libs.interpretador    import Interpretador
from libs.funcoes          import carregar_json
from libs.visualizacao     import ContadorLinhas
from libs.visualizacao     import EditorDeCodigo
from libs.colorir          import Colorir
from libs.arquivo          import Arquivo
import libs.funcoes as funcoes


# -*- coding: utf-8 -*-

# Theme One Dark
# sudo apt install python3-distutils
# sudo apt install python3-tk
# sudo apt-get install python3-pip
# sudo apt-get install python3-tk tk-dev


__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'
__project__     = 'Combratec'
__github__      = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__version__     = '0.3'
__status__      = 'Desenvolvimento'
__date__        = '01/08/2019'


TEXTO_UPDATE_DISPONIVEL = """\n
A versão {} esta disponível para download. Avalie a posiblidade de fazer a \
atualização. A atualizações de software pode trazer novos comandos e recursos \
de segurança, porém, também pode trazer novos bugs.\n"""

TEXTO_ATUALIZADO = """\nVocê está usando a versão {}. Se você quer\
receber aviso de novas versões, nos acompanhe no Facebook ou no nosso blog.\n"""

ERRO_GENERICO = """Aconteceu um erro ao buscar a \atualização, você precisa\
estar conectado a internet para buscar a atualizações"""

VERSAO_ATUAL = {"versao":0.3}

global esperar_pressionar_enter
global libera_breakpoint

libera_breakpoint = False
esperar_pressionar_enter = False

class Design():
    def __init__(self):
        self.dic = {}

    def __get_sett_file(self):
        return carregar_json("configuracoes/configuracoes.json")["tema"]

    def update_design_dic(self):
        self.dic = carregar_json("temas/{}".format(Design.__get_sett_file(self)))

    def get_design_dic(self):
        return self.dic


class Safira():
    def __init__(self):
        self.dic_comandos, self.dic_designRemover, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

        self.design = Design()
        self.design.update_design_dic()
        self.dic_design = self.design.get_design_dic()

        self.tela = Tk()
        self.tela.withdraw()
        self.tela.overrideredirect(1)
        self.tela.rowconfigure(1, weight=1)
        self.tela.grid_columnconfigure(1, weight=1)

    def main(self):
        splash = Splash(self.tela, self.design)
        interf = Interface(self.tela, self.dic_comandos, self.design, self.cor_do_comando)

        splash.splash_inicio()
        sleep(3)
        splash.splash_fim()

        interf.inicioScreen()


class Atualizar():
    def __init__(self, tela, design):
        self.tela = tela
        self.tp_atualizacao = None
        self.design =design

    def obter_versao_mais_recente_dev(self):
        resposta = requests.get("https://safiraide.blogspot.com/p/downloads.html")
        texto = str(resposta.text)

        lista = texto.split('id="idenficador_de_versao">')

        temporario = lista[1][0:70] # 0.2</span>
        temporario2 = temporario.split("</span>") # 0.2

        return float(temporario2[0].strip())

    def verificar_versao(self, primeira_vez = False):
        try:
            if 1 == 1:

                baixada = VERSAO_ATUAL
                recente = Atualizar.obter_versao_mais_recente_dev(self)

                if float(baixada["versao"]) < recente:
                    Atualizar.aviso_versao(self, baixada, recente)
                else:
                    if not primeira_vez:
                        Atualizar.aviso_versao_atualizada(self, baixada)

        except Exception as erro:
            print(erro,"*"*20)
            if not primeira_vez:
                messagebox.showinfo("ops", ERRO_GENERICO)
        
        return True

    def abrir_site(self, link):
        t = Thread(target=lambda event=None: webbrowser.open( link ))
        t.start()

        self.tp_atualizacao.destroy()

    def aviso_versao(self, baixada, recente):
        self.tp_atualizacao = Toplevel(self.tela, self.design.dic["aviso_versao_top_level"])
        self.tp_atualizacao.withdraw()

        try:
            self.tp_atualizacao.wm_attributes('-type', 'splash')
        except Exception as erro:
            print("Erro ao remover barra de titulos => ", erro)

        self.tp_atualizacao.grid_columnconfigure(1, weight=1)

        j_width  = self.tp_atualizacao.winfo_reqwidth()
        j_height = self.tp_atualizacao.winfo_reqheight()
        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tp_atualizacao.title("Aviso de atualização")

        fr_atualizaca = Frame(self.tp_atualizacao, self.design.dic["aviso_versao_fr_atualizada"])
        lb_versao_dev = Label(fr_atualizaca, self.design.dic["aviso_versao_lb_dev_atualizada"], text="Nova versão disponível!")
        lb_versao_tex = Message(fr_atualizaca, self.design.dic["aviso_versao_ms_atualizada"], text='{}'.format(TEXTO_UPDATE_DISPONIVEL).format(recente))
        fr_botoes = Frame(fr_atualizaca, self.design.dic["aviso_versao_fr_inf_atualizada"])
        bt_cancela = Button(fr_botoes, self.design.dic["aviso_bt_cancelar"], text="Não quero")
        bt_atualiza = Button(fr_botoes, text="Atualizar Agora")

        fr_atualizaca.configure(self.design.dic["aviso_versao_fr_atualizacao"])
        lb_versao_dev.configure(self.design.dic["aviso_versao_lb_dev"])
        lb_versao_tex.configure(self.design.dic["aviso_versao_ms"])
        fr_botoes.configure(self.design.dic["aviso_versao_btn"])
        bt_cancela.configure(self.design.dic["aviso_versao_btn_cancela"], relief=FLAT)
        bt_atualiza.configure(self.design.dic["aviso_versao_btn_atualiza"], relief=FLAT)

        bt_atualiza.configure(command = lambda event=None: Atualizar.abrir_site(self, "https://safiraide.blogspot.com/p/downloads.html") )
        bt_cancela.configure(command = lambda event=None: self.tp_atualizacao.destroy() )

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1 )
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        bt_cancela.grid(row=1, column=1)
        bt_atualiza.grid(row=1, column=2)

        self.tp_atualizacao.geometry("+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2)))
        self.tp_atualizacao.deiconify()
        self.tp_atualizacao.update()

    def aviso_versao_atualizada(self, baixada):

        self.tp_atualizacao = Toplevel(self.tela, self.design.dic["aviso_versao_tp_atualizada"])
        self.tp_atualizacao.withdraw()

        try:
            self.tp_atualizacao.wm_attributes('-type', 'splash')
        except Exception as erro:
            print("Erro ao remover barra de titulos => ", erro)
            
        self.tp_atualizacao.grid_columnconfigure(1, weight=1)

        j_width  = self.tp_atualizacao.winfo_reqwidth()
        j_height = self.tp_atualizacao.winfo_reqheight()
        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tp_atualizacao.title("Você está Atualizado!")

        fr_atualizaca = Frame(self.tp_atualizacao, self.design.dic["aviso_versao_fr_atualizada"])
        lb_versao_dev = Label(fr_atualizaca, self.design.dic["aviso_versao_lb_dev_atualizada"], text="Sua versão é a última!")
        lb_versao_tex = Message(fr_atualizaca,self.design.dic["aviso_versao_ms_atualizada"], text='{}'.format(TEXTO_ATUALIZADO).format(baixada["versao"]), relief=FLAT)
        fr_botoes = Frame(fr_atualizaca, self.design.dic["aviso_versao_fr_inf_atualizada"])
        bt_cancela = Button(fr_botoes, self.design.dic["aviso_bt_cancelar"], text="Não quero")
        bt_facebook = Button(fr_botoes, self.design.dic["aviso_versao_bt_facebook_atualizada"], text="Facebook", relief=FLAT)
        bt_blogger_ = Button(fr_botoes, self.design.dic["aviso_versao_bt_blog_atualizada"], text="Blog", relief=FLAT)
        bt_cancela.configure(command = lambda event=None: self.tp_atualizacao.destroy() )
        bt_facebook.configure(command = lambda event=None: Atualizar.abrir_site(self, "https://www.facebook.com/safiraide/") )
        bt_blogger_.configure(command = lambda event=None: Atualizar.abrir_site(self, "https://safiraide.blogspot.com/") )

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_botoes.grid_columnconfigure(3, weight=1)

        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1 )
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        bt_cancela.grid(row=1, column=1)
        bt_facebook.grid(row=1, column=2)
        bt_blogger_.grid(row=1, column=3)

        self.tp_atualizacao.geometry("+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2 )-int(j_height/2)))
        self.tp_atualizacao.deiconify()
        self.tp_atualizacao.update()


class Bug():
    def __init__(self, tela, design):
        self.design =design
        self.tela = tela
        self.bt_report = None
        self.image_bug = None
        self.bt_cancel = None
        self.fr_botoes = None
        self.lb_label3 = None
        self.lb_label2 = None
        self.lb_label1 = None
        self.tp_princi = None

    def __acessar_site_reporte(self):
        self.bt_report.configure(text="Abrindo formulário do Google")

        t = Thread(target=lambda event=None: webbrowser.open("https://forms.gle/J4kE2Li8c58fz4hh6") )
        t.start()        

        Bug.__destruir_interface(self)

    def __destruir_interface(self):
        self.bt_report.destroy()
        self.bt_cancel.destroy()
        self.fr_botoes.destroy()
        self.lb_label3.destroy()
        self.lb_label2.destroy()
        self.lb_label1.destroy()
        self.tp_princi.destroy()

    def interface(self):
        self.image_bug = PhotoImage(file="imagens/bug.png")
        self.image_bug = self.image_bug.subsample(4)

        self.tp_princi = Toplevel(self.tela, bd=10, bg="#3e4045")
        # self.design.dic[""]


        self.tp_princi.withdraw()

        try:
            self.tp_princi.wm_attributes('-type','splash')
        except Exception as erro:
            print("Erro ao remover barra de titulos => ", erro)

        self.lb_label1 = Label(self.tp_princi, self.design.dic["lb1_encontrou_bug"],  text="  Então você encontrou um bug?  ")
        self.lb_label2 = Label(self.tp_princi, self.design.dic["lb2_encontrou_bug"], image = self.image_bug)
        self.lb_label3 = Label(self.tp_princi, self.design.dic["lb3_encontrou_bug"], text="""\nVocê gostaria de reportar para nós?\n Isso nos ajuda a produzir algo melhor, vamos\n ficar felizes em ter o seu feedback!\n""")

        self.fr_botoes = Frame(self.tp_princi, self.design.dic["fr_bt_encontrou_bug"])
        self.bt_cancel = Button(self.fr_botoes, self.design.dic["bt_canc_encontrou_bug"], text="Depois", relief=FLAT)
        self.bt_report = Button(self.fr_botoes, self.design.dic["bt_report_encontrou_bug"], text="Reportar o BUG", relief=FLAT)

        self.tp_princi.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(1, weight=1)
        self.fr_botoes.grid_columnconfigure(2, weight=1)

        self.bt_cancel.configure(command=lambda event=None: Bug.__destruir_interface(self))
        self.bt_report.configure(command=lambda event=None: Bug.__acessar_site_reporte(self))

        self.lb_label1.grid(row=1, column=1, sticky=NSEW)
        self.lb_label2.grid(row=2, column=1, sticky=NSEW)
        self.lb_label3.grid(row=3, column=1, sticky=NSEW)
        self.fr_botoes.grid(row=4, column=1, sticky=NSEW)
        self.bt_cancel.grid(row=1, column=1)
        self.bt_report.grid(row=1, column=2)

        self.tp_princi.deiconify()
        self.tp_princi.update()


class Splash():
    def __init__(self, tela, design):
        self.frame_splash = None
        self.fr_splash = None
        self.l1_splash = None
        self.l2_splash = None
        self.tela = tela
        self.design = design

    def splash_inicio(self):
        self.frame_splash = Frame(self.tela)

        self.frame_splash.configure(background = self.design.dic["cor_intro"]["background"])
        self.frame_splash.rowconfigure(1, weight=1)
        self.frame_splash.grid_columnconfigure(0, weight=1)

        self.fr_splash = Frame(self.frame_splash)
        self.l1_splash = Label(self.frame_splash, self.design.dic["cor_intro"])
        self.l2_splash = Label(self.frame_splash, self.design.dic["cor_intro"])

        self.fr_splash.configure(background = self.design.dic["cor_intro"]["background"])
        self.l1_splash.configure(text=" COMBRATEC ", font=( "Lucida Sans", 90), bd=80)
        self.l2_splash.configure(text="Safira IDE beta 0.3", font=("Lucida Sans", 12))

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

class Interface():
    def __init__(self, tela, dic_comandos, design, cor_do_comando):

        self.design = design

        self.cor_do_comando                  = cor_do_comando
        self.dic_comandos                    = dic_comandos
        self.tela                            = tela

        self.bool_tela_em_fullscreen         = False
        self.bool_debug_temas                = False
        self.bool_logs                       = False

        self.lst_historico_abas_focadas      = []
        self.lista_terminal_destruir         = []
        self.lista_breakponts                = []
        self.lst_abas                        = []

        self.num_lin_bkp                     = 0
        self.valor_threads                   = 0
        self.linha_analise                   = 0
        self.posAbsuluta                     = 0
        self.posCorrente                     = 0
        self.num_aba_focada                  = 0
        self.num_modulos_acionados           = 0

        self.tx_erro_aviso_texto_erro        = None
        self.fr_erro_aviso_texto_erro        = None
        self.bt_erro_aviso_exemplo           = None
        self.bt_erro_aviso_fechar            = None
        self.controle_arquivos               = None
        self.cont_lin                        = None
        self.fr_opcoe                        = None
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
        self.fr__abas                        = None
        self.bt_play                         = None

        self.arquivo_configuracoes           = funcoes.carregar_json("configuracoes/configuracoes.json")
        self.colorir_codigo                  = Colorir(self.cor_do_comando, self.dic_comandos)
        self.path                            = abspath(getcwd())

        self.bug                             = Bug(self.tela, design)
        self.dic_abas                        = { 0:funcoes.carregar_json("configuracoes/guia.json") }
        self.atualizar                       = Atualizar(self.tela, design)

        self.dicLetras = {}
        for k, v in self.dic_comandos.items():
            self.dicLetras[k] = []
            for valor in v["comando"]:
                valor = valor[0].strip()

                if valor != "":
                    valor = valor.lower()

                    if valor[0] not in self.dicLetras[k]:
                        self.dicLetras[k].append(  valor[0] )


    def atualizar_coloracao_aba(self, limpar=False, event=None):
        # num_modulos_acionados => 0

        if event is not None:
            if event.keysym in ('Down', 'Up', 'Left', 'Right', 'Return'):
                return 0

        self.num_modulos_acionados += 1

        if self.num_modulos_acionados > 3:
            return 0

        if self.num_modulos_acionados == 2:
            while self.num_modulos_acionados != 0:
                self.tela.update()
            self.num_modulos_acionados += 1

        if limpar: self.colorir_codigo.historico_coloracao = []
        self.colorir_codigo.coordena_coloracao(None, tx_codfc = self.tx_codfc)

        self.num_modulos_acionados = 0

    def atualiza_texto_tela(self, num_aba):
        self.tx_codfc.delete(1.0, END)
        self.tx_codfc.insert(END, str(self.dic_abas[num_aba]["arquivoAtual"]["texto"])[0:-1])

        nome_arquivo = self.dic_abas[num_aba]["arquivoSalvo"]["link"].split("/")
        nome_arquivo = str(nome_arquivo[-1])

        if nome_arquivo.strip() == "":
            nome_arquivo = " " * 14

        self.dic_abas[num_aba]["listaAbas"][2].configure(text=nome_arquivo)

        for x in range(0, 3):
            self.dic_abas[num_aba]["listaAbas"][x].update()

        Interface.atualizar_coloracao_aba(self, True)

    def configurar_cor_aba(self, dic_cor_abas, bg_padrao, dic_cor_botao, dic_cor_marcador):
        self.dic_abas[self.num_aba_focada]["listaAbas"][3].configure(dic_cor_botao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][3].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][2].configure(dic_cor_abas, activebackground = bg_padrao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][2].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][1].configure(dic_cor_marcador)
        self.dic_abas[self.num_aba_focada]["listaAbas"][1].update()
        self.dic_abas[self.num_aba_focada]["listaAbas"][0].configure(background = bg_padrao)
        self.dic_abas[self.num_aba_focada]["listaAbas"][0].update()

    def fecha_aba(self, bt_fechar):
        bool_era_focado = False

        dic_cor_abas = self.design.dic["dic_cor_abas"]
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:

                while chave in self.lst_historico_abas_focadas:
                    self.lst_historico_abas_focadas.remove(chave)

                if len(self.dic_abas) == 1:
                    self.dic_abas[chave]["nome"] =""
                    self.dic_abas[chave]["lst_breakpoints"] = []
                    self.dic_abas[chave]["arquivoSalvo"] = {"link": "","texto": ""}
                    self.dic_abas[chave]["arquivoAtual"] = {"texto": ""}

                    Interface.atualiza_texto_tela(self, chave)
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

                    if self.dic_abas[chave]["foco"] == True:
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
            Interface.atualiza_texto_tela(self, chave)

            self.lst_historico_abas_focadas.append(chave)
            Interface.atualizar_coloracao_aba(self)
            return 0

    def atualiza_aba_foco(self, num_aba):
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
        Interface.atualiza_texto_tela(self, num_aba)


        Interface.atualizar_coloracao_aba(self)
    def nova_aba(self, event=None):

        posicao_adicionar = 0 # Adicionar na posição 0

        if len(self.dic_abas) != 0:
            dic_cor_finao = self.design.dic["dic_cor_abas_nao_focada"] 
            dic_cor_botao = self.design.dic["dic_cor_abas_nao_focada_botao"] 
            dic_cor_marcador = self.design.dic["dic_cor_marcador_nao_focado"] 

            Interface.configurar_cor_aba(self, dic_cor_finao, dic_cor_finao["background"], dic_cor_botao, dic_cor_marcador)
            posicao_adicionar = max(self.dic_abas.keys()) + 1

        self.dic_abas[ posicao_adicionar ] = funcoes.carregar_json("configuracoes/guia.json")

        dic_cor_finao = self.design.dic["dic_cor_abas_focada"] 
        dic_cor_botao = self.design.dic["dic_cor_abas_focada_botao"]
        dic_cor_marcador = self.design.dic["dic_cor_marcador_focado"] 

        fr_uma_aba = Frame(self.fr__abas, background=dic_cor_finao["background"])

        fr_marcador = Frame(fr_uma_aba, dic_cor_marcador)
        lb_aba = Button(fr_uma_aba, dic_cor_finao, text="              ", border=0, highlightthickness=0)
        bt_fechar = Button(fr_uma_aba, dic_cor_botao, text="x ", relief=FLAT, border=0, highlightthickness=0)

        lb_aba.bind('<ButtonPress>', lambda event=None, num_aba = posicao_adicionar: Interface.atualiza_aba_foco(self, num_aba) )
        bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Interface.fecha_aba(self, bt_fechar) )

        bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Interface.muda_cor_fecha_botao(self, bt_fechar))
        bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Interface.volta_cor_fecha_botao(self, padrao, bt_fechar))

        fr_uma_aba.rowconfigure(1, weight=1)
             
        fr_uma_aba.grid(row=1, column=posicao_adicionar + 2, sticky=N)
        fr_marcador.grid(row=0, column=1,columnspan=2, sticky=NSEW)
        lb_aba.grid(row=1, column=1, sticky=NSEW)
        bt_fechar.grid(row=1, column=2)

        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_uma_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(fr_marcador)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(lb_aba)
        self.dic_abas[posicao_adicionar]["listaAbas"].append(bt_fechar)

        self.num_aba_focada = posicao_adicionar
        Interface.atualiza_texto_tela(self, self.num_aba_focada)

    def muda_cor_fecha_botao(self, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(self.design.dic["dic_cor_abas_botao_fechar_focada"])
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def volta_cor_fecha_botao(self, padrao, bt_fechar):
        for chave, valor in self.dic_abas.items():
            if self.dic_abas[chave]["listaAbas"][3] == bt_fechar:
                self.dic_abas[chave]["listaAbas"][3].configure(foreground=padrao)
                self.dic_abas[chave]["listaAbas"][3].update()
                return 0

    def renderizar_abas_inicio(self):
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

            fr_uma_aba = Frame(self.fr__abas, background = dic_cor_finao["background"])
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

            bt_fechar.bind("<Enter>", lambda event=None, bt_fechar=bt_fechar: Interface.muda_cor_fecha_botao(self, bt_fechar))
            bt_fechar.bind("<Leave>", lambda event=None, padrao=dic_cor_botao["foreground"], bt_fechar=bt_fechar: Interface.volta_cor_fecha_botao(self, padrao, bt_fechar))

            lb_aba.bind('<ButtonPress>', lambda event=None, num_aba = num_aba: Interface.atualiza_aba_foco(self, num_aba) )
            bt_fechar.bind('<ButtonPress>', lambda event=None, bt_fechar=bt_fechar: Interface.fecha_aba(self, bt_fechar))

            fr_uma_aba.update()
            fr_marcador.update()
            lb_aba.update()
            bt_fechar.update()

            fr_uma_aba.grid(row=1, column=num_aba + 2, sticky=N)
            fr_marcador.grid(row=0, column=1,columnspan=2, sticky=NSEW)
            lb_aba.grid(row=1, column=1, sticky=NSEW)
            bt_fechar.grid(row=1, column=2)

            self.dic_abas[num_aba]["listaAbas"].append(fr_uma_aba)
            self.dic_abas[num_aba]["listaAbas"].append(fr_marcador)
            self.dic_abas[num_aba]["listaAbas"].append(lb_aba)
            self.dic_abas[num_aba]["listaAbas"].append(bt_fechar)


    def ativar_logs(self, event=None):
        if self.bool_logs:
            self.bool_logs = False
        else:
            self.bool_logs = True

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
                    if v[1] == 'lista':
                        for x in v[0]:
                            if caracteres == "":
                                caracteres += '"' + str(x[0]) + '"'
                            else:
                                caracteres += ', "' + str(x[0]) + '"'
                    else:
                        caracteres = v[0]

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


    def libera_breakpoint_exe(self):
        global libera_breakpoint
        libera_breakpoint = True


    def inicializa_orquestrador(self, event = None, libera_break_point_executa = False, linha_linha = False):

        print("Inicializador do orquestrador iniciado")

        self.bt_playP.configure(image=self.ic_PStop)
        self.bt_playP.update()

        tipo_exec = 'producao'
        if linha_linha == True:
            if len( self.tx_codfc.get(1.0, END).split("\n") ) != len(self.instancia.lst_breakpoints):
                self.instancia.lst_breakpoints = [x for x in range(0, len(   self.tx_codfc.get(1.0, END).split("\n")  ))]
            else:
                Interface.libera_breakpoint_exe(self)

        print("\n Orquestrador iniciado")
 
        # Se o interpretador já foi iniciado e o breakpoint for falso
        try:
            print(self.instancia.numero_threads_ativos)
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
                Interface.libera_breakpoint_exe(self)
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

        diretorio_base = re.sub('([^\\/]{1,})$','', diretorio_base) # Obter diretório apenas

        linhas = nova_linha

        self.tela.update()
        self.tx_codfc.update()
        self.tx_terminal.update()
        self.instancia = Interpretador( self.bool_logs, self.dic_abas[self.num_aba_focada]["lst_breakpoints"], bool_ignorar_todos_breakpoints, diretorio_base, self.dicLetras, self.dic_comandos)

        linhas = self.instancia.cortar_comentarios(linhas)

        t = Thread(target=lambda codigoPrograma = linhas: self.instancia.orquestrador_interpretador_(codigoPrograma))
        t.start()

        valor_antigo = 0

        tx_terminal = self.tx_terminal
        global libera_breakpoint
        while self.instancia.numero_threads_ativos != 0 or not self.instancia.boo_orquestrador_iniciado:
            self.tela.update()
            self.tx_codfc.update()
            self.tx_terminal.update()


            if tx_terminal is not None:
                self.tela.update()
                self.tx_terminal.update()

            acao = self.instancia.controle_interpretador
            if acao != "":

                if acao.startswith(':nessaLinha:'):
                    
                    if self.tx_terminal is None:
                        print(acao[len(':nessaLinha:') : ], end="")
                    else:
                        self.tx_terminal.insert(END, acao[len(':nessaLinha:') : ])
                    
                    self.instancia.controle_interpretador = ""

                elif acao.startswith(':mostreLinha:'):
                    if self.tx_terminal is None:
                        print(acao[len(':mostreLinha:') : ])
                    else:
                        self.tx_terminal.insert(END, acao[len(':mostreLinha:') : ] + '\n')

                    self.instancia.controle_interpretador = ""

                elif acao == ':input:':

                    if self.tx_terminal is None:
                        self.instancia.texto_digitado = input()

                    else:
                        textoOriginal = len(self.tx_terminal.get(1.0, END))
                        global esperar_pressionar_enter

                        esperar_pressionar_enter = True
                        while esperar_pressionar_enter:
                            self.tx_terminal.update()
                            self.tx_codfc.update()
                            self.tela.update()

                        print("SAIU")

                        digitado = self.tx_terminal.get(1.0, END)
                        digitado = digitado[textoOriginal - 1:-2]

                        esperar_pressionar_enter = False
                    
                    self.instancia.texto_digitado = digitado.replace("\n", "")
                    self.instancia.controle_interpretador = ""

                elif acao == 'limpar_tela':
                    if self.tx_terminal is None:
                        clear()
                    else:
                        self.tx_terminal.delete('1.0', END)
                    self.instancia.controle_interpretador = ""

                elif acao == 'aguardando_breakpoint':

                    # Modo debug
                    if tipo_exec == 'debug':
                        try:
                            self.linha_analise = int(self.instancia.num_linha)
                            if self.linha_analise != valor_antigo:
                                valor_antigo = self.linha_analise
                                self.cont_lin.linha_analise = self.linha_analise
                                self.cont_lin.desenhar_linhas()
                                self.tela.update()
                                self.tx_codfc.update()
                        except Exception as erro:
                            print("Erro update", erro)

                    libera_breakpoint = False
                    while not libera_breakpoint:
                        self.tx_terminal.update()
                        self.tx_codfc.update()
                        self.tela.update()

                    libera_breakpoint = False

                    self.instancia.controle_interpretador = ""
                else:
                    print("INFORMAÇÂO NAO MAPEADA")

        # Se o erro foi avisado
        if self.instancia.erro_alertado == True:
            if self.instancia.mensagem_erro != "Interrompido":
                if self.instancia.mensagem_erro != "Erro ao iniciar o Interpretador":
                    Interface.mostrar_mensagem_de_erro(self, self.instancia.mensagem_erro, self.instancia.dir_script_aju_erro, self.instancia.linha_que_deu_erro)

        #print("Instância deletada")
        del self.instancia

        try:
            #self.tx_terminal.config(state=NORMAL)
            self.tx_terminal.insert(END, '\n\nScript finalizado em {:.5} segundos'.format(time() - inicio))
            self.tx_terminal.see("end")

        except Exception as erro:
            print('Impossível exibir mensagem de finalização, erro: '+ str(erro))
        
        self.cont_lin.linha_analise = 0
        self.cont_lin.desenhar_linhas()
        self.tela.update()

        self.bt_playP.configure(image=self.ic_playP)
        self.bool_interpretador_iniciado = False

    def altera_status_enter(self, event=None):
        global esperar_pressionar_enter
        esperar_pressionar_enter = False

    def destruir_instancia_terminal(self):
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
            self.tx_terminal.configure(self.design.dic["tx_terminal"])
        except Exception as erro:
            print("Erro ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Interface.altera_status_enter(self))
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
            self.tx_terminal.configure(self.design.dic["tx_terminal"])
        except Exception as erro:
            print("Erro 2 ao configurar os temas ao iniciar o terminal: ", erro)

        self.tx_terminal.bind('<Return>', lambda event: Interface.altera_status_enter(self, event))
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

        self.fr_opcoe = Frame(self.frame_tela)

        self.bt_salva = Button( self.fr_opcoe, image=self.ic_salva, command = comando_acao_salvararq )
        self.bt_playP = Button( self.fr_opcoe, image=self.ic_playP, command = comando_executar_progr )
        self.bt_breaP = Button( self.fr_opcoe, image=self.ic_breaP, command = comando_executar_brakp )
        self.bt_brk_p = Button( self.fr_opcoe, image=self.ic_brk_p, command = comando_inserir_breakp )
        self.bt_brkp1 = Button( self.fr_opcoe, image=self.ic_brkp1, command = comando_executar_linha )
        self.bt_lp_bk = Button( self.fr_opcoe, image=self.iclp_bkp, command = comando_limpa_breakpon )
        self.bt_ajuda = Button( self.fr_opcoe, image=self.ic_ajuda)
        self.bt_pesqu = Button( self.fr_opcoe, image=self.ic_pesqu)

        self.fr_princ = Frame(self.frame_tela)
        self.fr_princ.grid_columnconfigure(2, weight=1)
        self.fr_princ.rowconfigure(1, weight=1)

        self.fr__abas = Frame(self.fr_princ, height=20)
        self.fr__abas.rowconfigure(1, weight=1)
        self.fr_espac = Label(self.fr__abas, width=5)

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
        self.tx_codfc.bind('<KeyRelease>', lambda event: Interface.ativar_coordernar_coloracao(self, event))
        self.tx_codfc.bind('<Control-MouseWheel>', lambda event: Interface.mudar_fonte(self, "+") if int(event.delta) > 0 else Interface.mudar_fonte(self, "-"))

        self.sb_codfc = Scrollbar(self.fr_princ, orient="vertical", command=self.tx_codfc.yview, relief=FLAT)
        self.tx_codfc.configure(yscrollcommand=self.sb_codfc.set)

        self.cont_lin = ContadorLinhas(self.fr_princ, self.design)
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas
        self.cont_lin.atribuir(self.tx_codfc)

        self.fr_espac.grid(row=1, column=0, sticky=NSEW)
        self.fr_opcoe.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        self.bt_salva.grid(row=1, column=1)
        self.bt_playP.grid(row=1, column=4)
        self.bt_breaP.grid(row=1, column=5)
        self.bt_brk_p.grid(row=1, column=6)
        self.bt_brkp1.grid(row=1, column=7)
        self.bt_lp_bk.grid(row=1, column=8)
        self.bt_ajuda.grid(row=1, column=10)
        self.bt_pesqu.grid(row=1, column=11)
        self.fr_princ.grid(row=2, column=1, sticky=NSEW)
        self.fr__abas.grid(row=0, column=1, columnspan=4, sticky=NSEW)
        self.cont_lin.grid(row=1, column=1, sticky=NSEW)
        self.tx_codfc.grid(row=1, column=2, sticky=NSEW)
        self.sb_codfc.grid(row=1, column=3, sticky=NSEW)

        # ******** Manipulação dos arquivos **************** #
        self.controle_arquivos = Arquivo(self.dic_abas, self.num_aba_focada, self.tx_codfc)
        Interface.atualiza_design_interface(self)

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()
        self.tela.geometry("{}x{}+0+0".format(t_width - 1, t_heigth - 1 ))
        self.colorir_codigo.tela = self.tela

        #Interface.funcoes_arquivos_configurar(self, None, "abrirArquivo", 'script.safira')

        self.tela.deiconify()
        self.tela.update()

        self.atualizar.verificar_versao(primeira_vez=True)

        self.tela.mainloop()

    def cascate_temas_temas(self):

        self.mn_intfc_casct_temas = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  Temas', menu=self.mn_intfc_casct_temas)

        for file in listdir('temas/'):
            if 'theme.json' in file:

                arquivo = " " + file
                if self.arquivo_configuracoes["tema"] == file:
                    arquivo = "*" + file

                funcao = lambda link = file: Interface.atualiza_dados_interface(self, 'tema', str(link))
                self.mn_intfc_casct_temas.add_command(label=arquivo, command=funcao)

    def cascate_temas_sintaxe(self):

        self.mn_intfc_casct_sintx = Menu(self.mn_intfc, tearoff=False)
        self.mn_intfc.add_cascade(label='  sintaxe', menu=self.mn_intfc_casct_sintx)

        for file in listdir('temas/'):
            if 'sintaxe.json' in file:

                arquivo = " " + file
                if self.arquivo_configuracoes["sintaxe"] == file:
                    arquivo = "*" + file

                funcao = lambda link = file: Interface.atualiza_dados_interface(self, 'sintaxe', str(link))
                self.mn_intfc_casct_sintx.add_command(label=arquivo, command=funcao)

    def cascate_scripts(self):

        for file in listdir('scripts/'):
            if file.endswith("safira"):
                funcao = lambda link = file:  Interface.abrir_script(self, link)
                self.mn_exemp.add_command(label="  " + file + "  ", command = funcao)

    def abrir_script(self, link):

        Interface.nova_aba(self, None)
        Interface.funcoes_arquivos_configurar(self, None, "abrirArquivo" , 'scripts/' + str(link) )

    def fechar_um_widget_erro(self, objeto):

        try:
            if objeto is not None:
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

        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas
        self.cont_lin.desenhar_linhas()
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


    def realiza_coloracao_erro(self, linha_que_deu_erro):
        lista = self.tx_codfc .get(1.0, END)

        if linha_que_deu_erro is not None:

            lista = self.tx_codfc.get(1.0, END).split("\n")

            palavra = "codigoErro"
            linha1 = str(linha_que_deu_erro) + ".0"
            linha2 = str(linha_que_deu_erro) + "." + str(len(lista[int(linha_que_deu_erro) - 1]))

            self.tx_codfc.tag_add(palavra, linha1 , linha2)
            self.tx_codfc.tag_config(palavra, background = "#572929")


    def mostrar_mensagem_de_erro(self, msg_erro, dir_script, linha_que_deu_erro):
        Interface.realiza_coloracao_erro(self, linha_que_deu_erro)

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

        self.bt_erro_aviso_fechar = Button(self.fr_erro_aviso, text="x", relief="sunken", fg="#ff9696",activeforeground="#ff9696", bg="#111121", activebackground="#111121", font=("", 13), highlightthickness=0, bd=0, command=lambda event=None: Interface.fechar_mensagem_de_erro(self))
        self.bt_erro_aviso_fechar.grid(row=1, column=3)

    def mudar_fonte(self, acao):

        print("mmudar a fonte")

        if acao == "+": adicao = 1
        else: adicao = -1

        self.design.dic["cor_menu"]["font"][1] = int(self.design.dic["cor_menu"]["font"][1]) + adicao
        self.design.dic["lb_sobDeTitulo"]["font"][1] = int(self.design.dic["lb_sobDeTitulo"]["font"][1]) + adicao
        self.design.dic["dicBtnMenus"]["font"][1] = int(self.design.dic["dicBtnMenus"]["font"][1]) + adicao
        self.design.dic["tx_terminal"]["font"][1] = int(self.design.dic["tx_terminal"]["font"][1]) + adicao
        self.design.dic["tx_codificacao"]["font"][1] = int(self.design.dic["tx_codificacao"]["font"][1]) + adicao
        self.design.dic["fonte_ct_linha"]["font"][1] = int(self.design.dic["fonte_ct_linha"]["font"][1]) + adicao
        self.design.dic["fonte_ct_linha"]["width"] = int(self.design.dic["fonte_ct_linha"]["width"]) + adicao

        self.tx_codfc.configure(self.design.dic["tx_codificacao"])
        self.cont_lin.desenhar_linhas()
        self.tela.update()


    def atualiza_interface_config(self, objeto, menu):
        try:
            objeto.configure(self.design.dic[menu])
            objeto.update()

        except Exception as erro:
            print("Erro Atualiza interface config = " + str(erro))

    def atualiza_design_interface(self):
        self.cont_lin.aba_focada2 = self.num_aba_focada
        self.cont_lin.dic_abas2 = self.dic_abas

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
        Interface.atualiza_interface_config(self, self.fr_opcoe, "fr_opcoes_rapidas")
        Interface.atualiza_interface_config(self, self.cont_lin, "lb_linhas")
        Interface.atualiza_interface_config(self, self.fr__abas, "dic_cor_abas_frame")
        Interface.atualiza_interface_config(self, self.fr_espac, "dic_cor_abas_frame")

    def atualiza_dados_interface(self, chave, novo):
        while True:
            try:
                Interface.arquivoConfiguracao(self, chave, novo)
            except Exception as e:
                print('Erro ao atualizar o arquivo \'configuracoes/configuracoes.json\'. Sem esse arquivo, não é possível atualizar os temas')
                return 0

            dic_comandos, self.dic_designRemover, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()
            self.design.update_design_dic()        

            try:
                self.colorir_codigo.alterar_cor_comando(self.cor_do_comando)

                Interface.atualiza_design_interface(self)
                self.cont_lin.aba_focada2 = self.num_aba_focada
                self.cont_lin.dic_abas2 = self.dic_abas

            except Exception as erro:
                print('ERRO: ', erro)
            else:
                print('Temas atualizados')

            self.tela.update()
            self.tx_codfc.update()

            if not self.bool_debug_temas:
                break
    
    def ativar_coordernar_coloracao(self, event = None):
        Interface.fechar_mensagem_de_erro(self)
        Interface.atualizar_coloracao_aba(self, True, event)

        if self.dic_abas != {}:
            self.dic_abas[ self.num_aba_focada ]["arquivoAtual"]['texto'] = self.tx_codfc.get(1.0, END)
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
            Interface.obterPosicaoDoCursor(self, event)
        
    def obterPosicaoDoCursor(self, event=None):
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

        if self.controle_arquivos is None:
            return 0

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


if __name__ == "__main__":
    app = Safira()
    app.main()