import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont

root = tk.Tk()
root.grid_columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

style = ttk.Style()
style.theme_use("clam")


style.configure("Custom.Treeview", 
    background="blue",
    insertbackground="orange",
    activebackground="red",
    activeforeground="pink",
    fieldbackground="green",
    selectmode="red",
    fieldforeground="yellow",
    foreground="white",
    selectbackground= "#333343",
    selectforeground= "#ffffff",
    relief=FLAT)

                
style.configure("Custom.Treeview.Heading", 
    background="blue",
    insertbackground="orange",
    activebackground="red",
    activeforeground="pink",
    fieldbackground="green",
    fieldforeground="yellow",
    foreground="white",
    selectbackground= "#333343",
    selectforeground= "#ffffff",
    relief=FLAT)


style.configure("Custom.Treeview.Column", 
    background="blue",
    insertbackground="orange",
    activebackground="red",
    activeforeground="pink",
    fieldbackground="green",
    fieldforeground="yellow",
    foreground="white",
    selectbackground= "#333343",
    selectforeground= "#ffffff",
    relief=FLAT)



frame_terminal_e_grid = Frame(root)
frame_terminal_e_grid.grid(row=1, column=1, sticky=NSEW)

frame_terminal_e_grid.grid_columnconfigure(1, weight=1)
frame_terminal_e_grid.rowconfigure(1, weight=1)

# Debug
coluna_identificadores = ('Variavel', 'Tipo','Valor')
fram_grid_variaveis = Frame(frame_terminal_e_grid, background="red")
fram_grid_variaveis.grid(row=2, column=1, sticky = NSEW)

fram_grid_variaveis.grid_columnconfigure(1, weight=1)
fram_grid_variaveis.rowconfigure(2, weight=1)

arvores_grid = ttk.Treeview(fram_grid_variaveis, columns=coluna_identificadores, show="headings", style="Custom.Treeview")


vsroolb = Scrollbar(fram_grid_variaveis, orient="vertical", command=arvores_grid.yview, bg="#a122cd")
hsroolb = Scrollbar(fram_grid_variaveis, orient="horizontal", command=arvores_grid.xview, bg="#12df2f")
arvores_grid.configure(yscrollcommand=vsroolb.set, xscrollcommand=hsroolb.set)


for coluna in coluna_identificadores:
    arvores_grid.heading(coluna, text=coluna.title() )
    arvores_grid.column(coluna, width=tkFont.Font().measure(coluna.title()) + 20)

arvores_grid.insert('', END, values=("v0", "v1", "v2"))
arvores_grid.insert('', END, values=("va", "vb", "vc"))
arvores_grid.insert('', END, values=("v01", "v10", "v11"))



arvores_grid.grid(row=2,column=1,  sticky='NSEW')
vsroolb.grid(row=2,column=2, sticky='NSEW')
hsroolb.grid(row=3,column=1,  sticky='NSEW')


root.mainloop()