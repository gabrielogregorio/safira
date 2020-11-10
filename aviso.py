from tkinter import PhotoImage
from tkinter import Toplevel
from tkinter import GROOVE
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import NSEW
from tkinter import Tk
from design import Design 
import util.funcoes as funcoes 


class Aviso():
    def __init__(self, tela, design, idioma, interface_idioma, icon):
        self.icon = icon
        self.idioma = idioma
        self.interface_idioma = interface_idioma
        self.design = design
        self.tela = tela
        self.tp_interface_idioma = None
        self.lb1 = None
        self.icone_alta_1 = None

    def aviso_resolucao(self): 
        self.icone_alta_1 = PhotoImage(file='imagens/Avisos/resolucao/alta.png')
        self.icone_alta_1 = self.icone_alta_1.subsample(2, 2)

        self.tp_interface_idioma = Toplevel(self.tela, self.design.dic["idioma_tp"]) 
        self.tp_interface_idioma.withdraw()

        self.tp_interface_idioma.tk.call('wm', 'iconphoto', self.tp_interface_idioma._w, self.icon)
        self.tp_interface_idioma.grid_columnconfigure(1, weight=1)
        self.tp_interface_idioma.title('Alerta de resolução de tela')

        self.fr_top_idioma = Frame(self.tp_interface_idioma, self.design.dic["idioma_fr"])
        self.fr_top_idioma.grid_columnconfigure(1, weight=1)
        self.fr_top_idioma.grid(row=1, column=1, sticky=NSEW)

        self.lb1 = Label(self.fr_top_idioma, self.design.dic['idioma_lb'], text="""A resolução de tela está muito alta, experimente\nabaixa-la para 1366x768.\nLembre-se de anotar a sua resolução antes de mudar.""")
        self.lb1.grid(row=1, column=1, sticky=NSEW)

        self.fr_idionas = Label(self.fr_top_idioma, self.design.dic['idioma_lb'], image=self.icone_alta_1)
        self.fr_idionas.grid(row=2, column=1)

        self.tp_interface_idioma.update()

        t_width  = self.tela.winfo_screenwidth()
        t_heigth = self.tela.winfo_screenheight()

        j_heigth = self.tp_interface_idioma.winfo_screenmmheight()
        j_width = self.tp_interface_idioma.winfo_screenmmwidth()

        self.tp_interface_idioma.geometry("+{}+{}".format(j_width, j_heigth, int(t_width/2-(j_width/2)), int(t_heigth/2-(j_heigth/2))))
        self.tp_interface_idioma.deiconify()



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

    idioma = Aviso(master, design, idioma, interface_idioma, icon)
    Button(master, text="acao", command=lambda: idioma.aviso_resolucao()).grid()

    master.mainloop()
