TEXTO_UPDATE_DISPONIVEL = """\n
A versão {} esta disponível para download. Avalie a posiblidade de fazer a \
atualização. A atualizações de software pode trazer novos comandos e recursos \
de segurança, porém, também pode trazer novos bugs.\n"""

TEXTO_ATUALIZADO = """\nVocê está usando a versão {}. Se você quer\
receber aviso de novas versões, nos acompanhe no Facebook ou no nosso blog.\n"""

ERRO_GENERICO = """Aconteceu um erro ao buscar a \atualização, você precisa\
estar conectado a internet para buscar a atualizações"""

VERSAO_ATUAL = {"versao":0.3}

from tkinter import Toplevel
from tkinter import Frame
from tkinter import Button
from tkinter import Message
from tkinter import Label
from tkinter import FLAT, NSEW
from threading import Thread
import webbrowser
from tkinter import messagebox
import requests

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
            if not primeira_vez:
                messagebox.showinfo("ops", ERRO_GENERICO + str(erro))

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
