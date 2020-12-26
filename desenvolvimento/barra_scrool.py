from tkinter import *

"""
Criação de uma barra de Scrool Personalizada
"""

class barra():
    def __init__(self, tela):
        self.tela = tela

        self.tx_editor = Text(self.tela, font=('', 9))
        self.fr_barra = Frame(self.tela)
        self.fr_barra_2 = Frame(self.fr_barra, bg='#00aaff', width=10)

        self.fr_barra_2.bind('<B1-Motion>',self.ao_rolar_scrool)
        self.tela.bind('<Key>', self.ao_rodar_eventos)
        self.tela.bind('<Configure>', self.ao_rodar_eventos)
        self.tx_editor.bind('<MouseWheel>', self.ao_rodar_eventos)

        self.fr_barra_2.grid(row=1)
        self.fr_barra.grid(row=1, column=1, sticky=NSEW)
        self.tx_editor.grid(row=1, column=0, sticky=NSEW)


    def ao_rolar_scrool(self, event):
        widget = event.widget

        inicio_y = widget.winfo_y()
        tela_h = self.tela.winfo_height()
        widget_h = widget.winfo_height()

        mouse = (inicio_y+event.y)-int(widget_h/2)

        if mouse > 0 and mouse + widget_h < tela_h:
            widget.place(y=mouse)

        elif mouse <= 0: widget.place(y=0)
        else: widget.place(y=tela_h-widget_h)


    def ao_rodar_eventos(self, event):
        wd_h = self.tx_editor.winfo_height()
        

        linhas_visiveis = self.tx_editor.winfo_height()/15
        linhas_totais = len(self.tx_editor.get(1.0, END)[0:-1].split('\n'))



        if linhas_visiveis >= linhas_totais:
            posicao = wd_h
        else:
            x = (linhas_visiveis * 100)/linhas_totais
            posicao = wd_h*(x/100)


        self.fr_barra_2.configure(height=posicao)

        inicio = self.fr_barra_2.winfo_y()
        tamanho_icone = self.fr_barra_2.winfo_height() + inicio

        maxi = wd_h-(tamanho_icone-inicio)
        
        try:
            x = (100*inicio)/maxi
        except ZeroDivisionError:
            x = 0

        if x > 100:
            x = 100
        elif x < 0:
            x = 0

        x = abs(x)

        try:
            area_texto = x/100
        except ZeroDivisionError:
            area_texto = 1

        porcentagem_tamanho_um_icone  = (linhas_visiveis * 100)/linhas_totais

        scrool = round(x / 100 *linhas_totais, 4)/100
        self.tx_editor.yview_moveto(area_texto * porcentagem_tamanho_um_icone/100)


tela = Tk()
tela.grid_rowconfigure(1, weight=1)
tela.rowconfigure(1, weight=1)

barra(tela)

tela.mainloop()
