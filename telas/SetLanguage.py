from tkinter import Toplevel
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter import GROOVE
from tkinter import NSEW
from tkinter import PhotoImage
from tkinter import Tk
import util.funcoes as funcoes


class SetLanguage():
    def __init__(self):#, tela, design, idioma, interface_idioma, icon):
        self.__base = "imagens/" 
        self.__tp_interface_idioma = None
        self.__bt_idioma = None
        self.__lb1 = None

    def selecionar_idioma(self): 

        self.__tp_interface_idioma = Toplevel(self.master, self.design.dic["idioma_tp"]) 
        self.__tp_interface_idioma.withdraw()

        self.__tp_interface_idioma.tk.call('wm', 'iconphoto', self.__tp_interface_idioma._w, self.icon)
        self.__tp_interface_idioma.grid_columnconfigure(1, weight=1)
        self.__tp_interface_idioma.title('Escolha de Idioma')

        self.fr_top_idioma = Frame(self.__tp_interface_idioma, self.design.dic["idioma_fr"])
        self.fr_top_idioma.grid_columnconfigure(1, weight=1)
        self.fr_top_idioma.grid(row=1, column=1, sticky=NSEW)

        self.__lb1 = Label(self.fr_top_idioma, self.design.dic['idioma_lb'], text=self.interface_idioma["texto_atualizacao"][self.idioma])
        self.__lb1.grid(row=1, column=1, sticky=NSEW)

        self.__fr_idiomas = Frame(self.__tp_interface_idioma, self.design.dic['idioma_fr2'])
        self.__fr_idiomas.grid(row=2, column=1)

        # Carregar as imagens
        self.__imgs = []
        for k, v in self.dic_imgs.items():
            self.__imgs.append(PhotoImage(file=self.__base+v))

        # Carregar os botões
        x = 0
        self.__lista_botoes = []
        for k, v in self.dic_imgs.items():

            if self.idioma == k:
                self.__fr_bt = Frame(self.__fr_idiomas, self.design.dic['idioma_fr3'])
                self.__bt_bt = Button(self.__fr_bt, self.design.dic['idioma_bt'], relief=GROOVE, image=self.__imgs[x], )
                self.__lb_bt = Label(self.__fr_bt, self.design.dic['idioma_lb2'], relief=GROOVE, text=k, )
            else:
                self.__fr_bt = Frame(self.__fr_idiomas, self.design.dic['idioma_fr4'])
                self.__bt_bt = Button(self.__fr_bt, self.design.dic['idioma_bt2'], relief=GROOVE, image=self.__imgs[x],)
                self.__lb_bt = Label(self.__fr_bt, self.design.dic['idioma_lb3'], relief=GROOVE, text=k)

            self.__bt_bt["command"] = lambda bt_bt=self.__bt_bt: self.__marcar_opcao_idioma(bt_bt)

            self.__lista_botoes.append([self.__fr_bt, self.__bt_bt, self.__lb_bt])

            self.__fr_bt.grid(row=1, column=x)
            self.__bt_bt.grid(row=1, column=x)
            self.__lb_bt.grid(row=2, column=x)

            x += 1

        self.__tp_interface_idioma.update()

        t_width  = self.master.winfo_screenwidth()
        t_heigth = self.master.winfo_screenheight()

        j_heigth = self.__tp_interface_idioma.winfo_screenmmheight()
        j_width = self.__tp_interface_idioma.winfo_screenmmwidth()

        self.__tp_interface_idioma.geometry("+{}+{}".format(j_width, j_heigth, int(t_width/2-(j_width/2)), int(t_heigth/2-(j_heigth/2))))
        self.__tp_interface_idioma.deiconify()

    def __marcar_opcao_idioma(self, botao):
        self.__tp_interface_idioma.withdraw()

        for bandeira in self.__lista_botoes:
            if bandeira[1] == botao:
                self.idioma = bandeira[2]["text"]

                self.__ic_idioma = PhotoImage( file="imagens/{}".format(self.dic_imgs[self.idioma]) )
                self.__ic_idioma = self.__ic_idioma.subsample(4, 4)
                funcoes.arquivo_de_configuracoes_interface("idioma", self.idioma)


                #self.__lb1.configure(text=self.interface_idioma["texto_atualizacao"][self.idioma])

                self.__tp_interface_idioma.destroy()
                del bandeira

                self.selecionar_idioma()

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

    idioma = SetLanguage(master, design, idioma, interface_idioma, icon)
    Button(master, text="acao", command=lambda id=idioma: atualizar_sistema(id)).grid()

    master.mainloop()
