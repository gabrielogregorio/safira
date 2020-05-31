from libs.funcoes import transformar_em_json, carregar_json
import requests
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Frame
from tkinter import W
from tkinter import GROOVE
from tkinter import NSEW
from tkinter import messagebox
import webbrowser


class Atualizar():
    def __init__(self, tela):
        self.tela = tela

    def obter_versao_baixada(self):
        return carregar_json("versao/update.json")

    def obter_versao_mais_recente_dev(self):
        resposta = requests.get("https://raw.githubusercontent.com/Combratec/feynman_code/master/versao/update.json")
        return transformar_em_json(resposta.text)

    def verificar_versao(self):

        baixada = Atualizar.obter_versao_baixada(self)
        recente = Atualizar.obter_versao_mais_recente_dev(self)

        texto_versao_dev = ""
        link_versao_dev = ""

        if (recente["versao"] > baixada["versao"]):
            texto_versao_dev = "  A versão {} de desenvolvimento está disponível ".format(recente["versao"])
            link_versao_dev = recente["url"]

        elif recente["versao"] != baixada["versao"]:
            "  Por favor, Você está usando uma versão do futuro, que bizarro, não sei oque fazer!"

        else:
            "  Você está usando a versão de desenvolvimento mais atualizada"

        if texto_versao_dev != "":
            Atualizar.aviso_versao(self, baixada, texto_versao_dev, link_versao_dev)
        else:
            messagebox.showinfo("Aviso", "Você está usando a versão mais recente disponível")

        return True

    def aviso_versao(self, baixada, texto_versao_dev, link_versao_dev):

        tp_atualizacao = Toplevel(self.tela)

        tp_atualizacao.update()
        tp_atualizacao.withdraw()

        j_width  = tp_atualizacao.winfo_reqwidth()
        j_height = tp_atualizacao.winfo_reqheight()
        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()



        tp_atualizacao.title("Aviso de atualização")

        fr_atualizaca = Frame(tp_atualizacao, bg="#2e2e2e")
        fr_atualizaca.grid_columnconfigure(1, weight=1)

        lb_para_qual = Label(fr_atualizaca, fg="white", text= "  Verifique quais sãos as versões disponíveis para atualização\n\n", bg="#2e2e2e")
        lb_versao_usando = Label(fr_atualizaca, text="  Minha versão {} de {}\n".format(baixada["versao"], baixada["tipo"] ), bg="#2e2e2e", fg="white")
        fr_versao_dev = Frame(fr_atualizaca, bg="#2e2e2e")


        if texto_versao_dev != "":
            lb_versao_dev = Label(fr_versao_dev, text=texto_versao_dev, fg="#b2ff54", bg="#2e2e2e")
            bt = Button(fr_versao_dev, text="Baixar", bg="#2e2e2e", activebackground="#2e2e2e", relief=GROOVE, fg="#b2ff54", activeforeground="#b2ff54", highlightthickness=0, bd=0)
            bt.configure(command = lambda link=link_versao_dev:webbrowser.open( link ) )
            bt.grid(row=1, column=2)

        lb_versao_dev.grid(row=1, column=1)
        lb_versao_est = Label(fr_atualizaca, text="\n  Nenhuma versão estável existente\n", bg="#2e2e2e", fg="white")

        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_para_qual.grid(row=1, column=1, sticky=NSEW)
        lb_versao_usando.grid(row=2, column=1, sticky=W)
        fr_versao_dev.grid(row=3, column=1, sticky=W)
        lb_versao_est.grid(row=4, column=1, sticky=W)
        tp_atualizacao.resizable (False, False)

        tp_atualizacao.geometry("+{}+{}".format( int(t_width / 2) - int(j_width / 2), int(t_heigth / 2 ) - int (j_height / 2) ))
        tp_atualizacao.deiconify()
        tp_atualizacao.update()
