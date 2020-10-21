from tkinter import Toplevel
from tkinter import Frame
from tkinter import Button
from tkinter import Message
from tkinter import Label
from tkinter import FLAT, NSEW
from threading import Thread
from tkinter import messagebox
import webbrowser
import requests
from tkinter import Tk
from design import Design
import libs.funcoes as funcoes


VERSAO_ATUAL = {"versao": 0.3}


class Atualizar():
    def __init__(self, tela, design, idioma, interface_idioma):
        self.interface_idioma = interface_idioma
        self.tp_atualizacao = None
        self.idioma = idioma
        self.design = design
        self.tela = tela

    def obter_versao_mais_recente_dev(self):
        resposta = requests.get("https://safiralang.blogspot.com/p/downloads.html")
        texto = str(resposta.text)

        lista = texto.split('id="idenficador_de_versao">')

        temporario = lista[1][0:70]
        temporario2 = temporario.split("</span>")

        return float(temporario2[0].strip())

    def verificar_versao(self, primeira_vez=False):
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
                messagebox.showinfo("ops", self.interface_idioma["erro_generico"][self.idioma] + str(erro))

        return True

    def abrir_site(self, link):
        t = Thread(target=lambda event=None: webbrowser.open(link))
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

        j_width = self.tp_atualizacao.winfo_reqwidth()
        j_height = self.tp_atualizacao.winfo_reqheight()
        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tp_atualizacao.title(self.interface_idioma["titulo_aviso_atualizacao"][self.idioma])

        fr_atualizaca = Frame(self.tp_atualizacao, self.design.dic["aviso_versao_fr_atualizada"])
        lb_versao_dev = Label(fr_atualizaca, self.design.dic["aviso_versao_lb_dev_atualizada"], text=self.interface_idioma["versao_nova_disponivel"][self.idioma])
        lb_versao_tex = Message(fr_atualizaca, self.design.dic["aviso_versao_ms_atualizada"], text='{}'.format(self.interface_idioma["texto_update_disponivel"][self.idioma]).format(recente))
        fr_botoes = Frame(fr_atualizaca, self.design.dic["aviso_versao_fr_inf_atualizada"])
        bt_cancela = Button(fr_botoes, self.design.dic["aviso_bt_cancelar"], text=self.interface_idioma["versao_nao_quero"][self.idioma])

        bt_atualiza = Button(fr_botoes, text=self.interface_idioma["atualizar_agora"][self.idioma])

        fr_atualizaca.configure(self.design.dic["aviso_versao_fr_atualizacao"])
        lb_versao_dev.configure(self.design.dic["aviso_versao_lb_dev"])
        lb_versao_tex.configure(self.design.dic["aviso_versao_ms"])
        fr_botoes.configure(self.design.dic["aviso_versao_btn"])
        bt_cancela.configure(self.design.dic["aviso_versao_btn_cancela"], relief=FLAT)
        bt_atualiza.configure(self.design.dic["aviso_versao_btn_atualiza"], relief=FLAT)

        bt_atualiza.configure(command=lambda event=None: Atualizar.abrir_site(self, "https://safiralang.blogspot.com/p/downloads.html"))
        bt_cancela.configure(command=lambda event=None: self.tp_atualizacao.destroy())

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1)
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

        j_width = self.tp_atualizacao.winfo_reqwidth()
        j_height = self.tp_atualizacao.winfo_reqheight()
        t_width = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        self.tp_atualizacao.title(self.interface_idioma["titulo_aviso_atualizado"][self.idioma])

        fr_atualizaca = Frame(self.tp_atualizacao, self.design.dic["aviso_versao_fr_atualizada"])
        lb_versao_dev = Label(fr_atualizaca, self.design.dic["aviso_versao_lb_dev_atualizada"], text=self.interface_idioma["atualizado_versao_ultima"][self.idioma])
        lb_versao_tex = Message(fr_atualizaca, self.design.dic["aviso_versao_ms_atualizada"], text='{}'.format(self.interface_idioma["texto_atualizado"][self.idioma]).format(baixada["versao"]), relief=FLAT)
        fr_botoes = Frame(fr_atualizaca, self.design.dic["aviso_versao_fr_inf_atualizada"])

        bt_cancela = Button(fr_botoes, self.design.dic["aviso_bt_cancelar"], text=self.interface_idioma["texto_nao_quero"][self.idioma])
        bt_facebook = Button(fr_botoes, self.design.dic["aviso_versao_bt_facebook_atualizada"], text=self.interface_idioma["atualizado_facebook"][self.idioma], relief=FLAT)
        bt_blogger_ = Button(fr_botoes, self.design.dic["aviso_versao_bt_blog_atualizada"], text=self.interface_idioma["atualizado_blog"][self.idioma], relief=FLAT)
        bt_cancela.configure(command=lambda event=None: self.tp_atualizacao.destroy())
        bt_facebook.configure(command=lambda event=None: Atualizar.abrir_site(self, "https://www.facebook.com/safiralang/"))
        bt_blogger_.configure(command=lambda event=None: Atualizar.abrir_site(self, "https://safiralang.blogspot.com/"))

        fr_atualizaca.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(1, weight=1)
        fr_botoes.grid_columnconfigure(2, weight=1)
        fr_botoes.grid_columnconfigure(3, weight=1)

        fr_atualizaca.grid(row=1, column=1, sticky=NSEW)
        lb_versao_dev.grid(row=1, column=1)
        lb_versao_tex.grid(row=2, column=1, sticky=NSEW)
        fr_botoes.grid(row=3, column=1, sticky=NSEW)
        bt_cancela.grid(row=1, column=1)
        bt_facebook.grid(row=1, column=2)
        bt_blogger_.grid(row=1, column=3)

        self.tp_atualizacao.geometry("+{}+{}".format(int(t_width/2)-int(j_width/2), int(t_heigth/2)-int(j_height/2)))
        self.tp_atualizacao.deiconify()
        self.tp_atualizacao.update()



if __name__ == '__main__':

    # Simular estar atualizado
    VERSAO_ATUAL = {"versao": 0.3}

    # Simular estar desatualizado
    # VERSAO_ATUAL = {"versao": 0.1}




    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

    atualizar = Atualizar(master, design, idioma, interface_idioma)




    # Quando a safira é iniciado
    # Verificar a primeira vez
    # Primeira vez não mostra mensagem de erro
    # e nem mensagem se estiver atualizado
    #atualizar.verificar_versao(primeira_vez=True)

    # Quando o usuário tenta buscar atualizações de
    atualizar.verificar_versao()






    master.mainloop()




