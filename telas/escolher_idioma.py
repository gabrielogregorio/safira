from tkinter import Toplevel
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter import GROOVE
from tkinter import NSEW
from tkinter import PhotoImage
from tkinter import Tk
import util.funcoes as funcoes 
from telas.design import Design 


class Idioma():
    def __init__(self, tela, design, idioma, interface_idioma, icon):
        self.icon = icon
        self.idioma = idioma
        self.interface_idioma = interface_idioma
        self.design = design
        self.tela = tela
        self.base = "imagens/" 
        self.tp_interface_idioma = None
        self.bt_idioma = None
        self.lb1 = None
        self.dic_imgs = None

    def selecionar_idioma(self, dic_imgs): 
        self.dic_imgs = dic_imgs 
        self.tp_interface_idioma = Toplevel(self.tela, self.design.dic["idioma_tp"]) 
        self.tp_interface_idioma.withdraw()

        self.tp_interface_idioma.tk.call('wm', 'iconphoto', self.tp_interface_idioma._w, self.icon)
        self.tp_interface_idioma.grid_columnconfigure(1, weight=1)
        self.tp_interface_idioma.title('Escolha de Idioma')

        self.fr_top_idioma = Frame(self.tp_interface_idioma, self.design.dic["idioma_fr"])
        self.fr_top_idioma.grid_columnconfigure(1, weight=1)
        self.fr_top_idioma.grid(row=1, column=1, sticky=NSEW)

        self.lb1 = Label(self.fr_top_idioma, self.design.dic['idioma_lb'], text=self.interface_idioma["texto_atualizacao"][self.idioma])
        self.lb1.grid(row=1, column=1, sticky=NSEW)

        self.fr_idionas = Frame(self.tp_interface_idioma, self.design.dic['idioma_fr2'])
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
                self.fr_bt = Frame(self.fr_idionas, self.design.dic['idioma_fr3'])
                self.bt_bt = Button(self.fr_bt, self.design.dic['idioma_bt'], relief=GROOVE, image=self.imgs[x], )
                self.lb_bt = Label(self.fr_bt, self.design.dic['idioma_lb2'], relief=GROOVE, text=k, )
            else:
                self.fr_bt = Frame(self.fr_idionas, self.design.dic['idioma_fr4'])
                self.bt_bt = Button(self.fr_bt, self.design.dic['idioma_bt2'], relief=GROOVE, image=self.imgs[x],)
                self.lb_bt = Label(self.fr_bt, self.design.dic['idioma_lb3'], relief=GROOVE, text=k)

            self.bt_bt["command"] = lambda bt_bt=self.bt_bt, dic=self.dic_imgs : self.marcar_opcao_idioma(bt_bt, dic)

            self.lista_botoes.append([self.fr_bt, self.bt_bt, self.lb_bt])

            self.fr_bt.grid(row=1, column=x)
            self.bt_bt.grid(row=1, column=x)
            self.lb_bt.grid(row=2, column=x)

            x += 1

        self.tp_interface_idioma.update()

        t_width  = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        j_heigth = self.tp_interface_idioma.winfo_screenmmheight()
        j_width = self.tp_interface_idioma.winfo_screenmmwidth()

        self.tp_interface_idioma.geometry("+{}+{}".format(j_width, j_heigth, int(t_width/2-(j_width/2)), int(t_heigth/2-(j_heigth/2))))
        self.tp_interface_idioma.deiconify()

    def marcar_opcao_idioma(self, botao, dic_imgs):
        self.dic_imgs = dic_imgs
        self.tp_interface_idioma.withdraw()

        for bandeira in self.lista_botoes:
            if bandeira[1] == botao:
                self.idioma = bandeira[2]["text"]

                self.ic_idioma = PhotoImage( file="imagens/{}".format(self.dic_imgs[self.idioma]) )
                self.ic_idioma = self.ic_idioma.subsample(4, 4)
                funcoes.arquivo_de_configuracoes_interface("idioma", self.idioma)


                #self.lb1.configure(text=self.interface_idioma["texto_atualizacao"][self.idioma])

                self.tp_interface_idioma.destroy()
                del bandeira

                self.selecionar_idioma(self.dic_imgs)

            else:
                pass
        return 10, 20

def atualizar_sistema(idioma):
    idioma.selecionar_idioma({"pt-br": "ic_pt_br.png", "en-us": "ic_en_us.png", "es": "ic_es.png"})

if __name__ == '__main__':
    master = Tk()

    design = Design()
    design.update_design_dic()

    # Configurações da IDE
    arquivo_configuracoes = funcoes.carregar_json("configuracoes/configuracoes.json")

    # Idioma que a safira está configurada
    idioma = arquivo_configuracoes['idioma']
    interface_idioma = funcoes.carregar_json("configuracoes/interface.json")

    icon = PhotoImage(file='imagens/icone.png')

    idioma = Idioma(master, design, idioma, interface_idioma, icon)
    Button(master, text="acao", command=lambda id=idioma: atualizar_sistema(id)).grid()

    master.mainloop()
