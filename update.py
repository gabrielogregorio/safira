from libs.funcoes import carregar_json
import requests
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Frame, Message
from tkinter import W
from tkinter import Tk
from tkinter import FLAT
from tkinter import NSEW
import webbrowser
from threading import Thread
from tkinter import messagebox

texto_geral = """\nA versão {} esta disponível para download. Avalie a posiblidade de fazer a atualização. A atualizações de software pode trazer novos comandos e recursos de segurança, porém, também pode trazer novos bugs.\n"""

class Atualizar():
    def __init__(self, tela):
        self.tela = tela
        self.tp_atualizacao = None

    def obter_versao_baixada(self):
        return carregar_json("versao/update.json")

    def obter_versao_mais_recente_dev(self):
        resposta = requests.get("https://safiraide.blogspot.com/p/downloads.html")
        texto = str(resposta.text)

        lista = texto.split('id="idenficador_de_versao">')

        temporario = lista[1][0:70] # 0.2</span>
        temporario2 = temporario.split("</span>") # 0.2

        return float( temporario2[0].strip() )

    def verificar_versao(self, primeira_vez = False):
        try:

            baixada = Atualizar.obter_versao_baixada(self)
            recente = Atualizar.obter_versao_mais_recente_dev(self)

            if float(baixada["versao"]) < recente:
                Atualizar.aviso_versao(self, baixada, recente)
            else:
                if not primeira_vez:
                    messagebox.showinfo("Atualizado!", "Você está usando a versão mais recente da Safira")

        except Exception as erro:
            if not primeira_vez:
                print(erro)
                messagebox.showinfo("ops", "Aconteceu um erro ao buscar a atualização, você precisa estar conectado a internet para buscar a atualizações")

        return True

    def abrir_site(self):
        t = Thread(target=lambda event=None: webbrowser.open( "https://safiraide.blogspot.com/p/downloads.html" ))
        t.start()

        self.tp_atualizacao.destroy()

    def aviso_versao(self, baixada, recente):

        self.tp_atualizacao = Toplevel(self.tela , bd=20, bg="#fafafa", highlightcolor="#fafafa")
        self.tp_atualizacao.withdraw()

        self.tp_atualizacao.wm_attributes('-type', 'splash')
        self.tp_atualizacao.grid_columnconfigure(1, weight=1)

        j_width  = self.tp_atualizacao.winfo_reqwidth()
        j_height = self.tp_atualizacao.winfo_reqheight()

        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tp_atualizacao.title("Aviso de atualização")

        fr_atualizaca = Frame(self.tp_atualizacao, bg="#fafafa")
        lb_versao_dev = Label(fr_atualizaca, text="Nova versão disponível!".format(recente), fg="#744aff", bg="#fafafa", font=("", 20))
        lb_versao_tex = Message(fr_atualizaca, anchor="nw", fg="#343434", bg="#fafafa", font=("", 11),  text='{}'.format(texto_geral).format(recente))
        fr_botoes = Frame(fr_atualizaca, bg="#fafafa")
        bt_cancela = Button(fr_botoes, text="Não quero", bg="#c7c7c7", activebackground="#c7c7c7", relief=FLAT, fg="#323232", activeforeground="#323232")
        bt_atualiza = Button(fr_botoes, text="Atualizar Agora", bg="#21d9c6", activebackground="#21d9c6", relief=FLAT, fg="#094d46", activeforeground="#094d46", )

        bt_atualiza.configure(command = lambda event=None: Atualizar.abrir_site(self) )
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
        # self.tp_atualizacao.resizable (False, False)

        self.tp_atualizacao.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))
        self.tp_atualizacao.deiconify()
        self.tp_atualizacao.update()
