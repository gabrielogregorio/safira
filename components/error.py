from tkinter import PhotoImage
from tkinter import Button
from tkinter import Label
from tkinter import Frame
from tkinter import Text
from tkinter import NSEW
from tkinter import Tk


class Error():
    def __init__(self, titulo:str, mensagem:str):

        # Basic Config
        root = Tk()
        root.rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.title(titulo)
        root.configure(bg="#fefefe")
        img_icone = PhotoImage(file='imagens/error_icon.png')
        img_icone = img_icone.subsample(2, 2)
        root.call('wm', 'iconphoto', root._w, img_icone)

        # Image and Message error
        fr_base = Frame(root, bg="#fefefe", pady=10, padx=10)
        fr_base.rowconfigure(1, weight=1)
        fr_base.grid_columnconfigure(2, weight=1)
        fr_base.grid(row=1, column=1, sticky=NSEW)

        lb_image = Label(fr_base, image=img_icone, bg="#fefefe")
        lb_image.grid(row=1, column=1)

        txt_message = Text(fr_base, height=4, bg="#fefefe", bd=0)
        txt_message.insert(0.0, mensagem)
        txt_message.grid(row=1, column=2, sticky=NSEW)

        # Buttons, copy and report
        fr_butons = Frame(root, bg="#fefefe",  pady=5, padx=10, )
        fr_butons.rowconfigure(1, weight=1)
        fr_butons.grid_columnconfigure(2, weight=1)
        fr_butons.grid(row=2, column=1, sticky='ew')

        # Button Copy
        fr_copy = Frame(fr_butons, bg='#ffffff',  highlightthickness=1, highlightbackground="#ff2660", highlightcolor="green", bd=0)
        fr_copy.grid(row=2, column=2, sticky='e')

        btn_copy = Button(fr_copy, text="Copiar Mensagem", bg='#ffffff', fg='#ff2660',relief='flat', activebackground="#fefefe", activeforeground="#ff2660", highlightthickness=5, bd=0)
        btn_copy.grid(row=1, column=1, sticky='e')

        # white space
        fr_white = Frame(fr_butons, bg="#fefefe", width=5)
        fr_white.grid(row=2, column=3)

        # Button Report
        fr_report = Frame(fr_butons, bg='#ffffff',  highlightthickness=1, highlightbackground="#ff2660", highlightcolor="green", bd=0)
        fr_report.grid(row=2, column=5, sticky='e')

        btn_report = Button(fr_report, text="Reportar Bug", bg='#ff2660', fg='#ffffff',relief='flat', activebackground="#ff2660", activeforeground="#ffffff", highlightthickness=5, bd=0)
        btn_report.grid(row=1, column=1, sticky='e')

        root.mainloop()


Error(titulo='Erro durante a execução da Safira', mensagem='Registro global de erro.\nErro no interpretador {sss Kpa}\nHorário: 12:23:34\n[copie a mensagem de erro e poste no forum]')
