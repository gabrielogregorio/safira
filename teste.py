from pyglet import resource
from pyglet import font


fonte = 'fonte/Source_Code_Pro/SourceCodePro-Regular.ttf'
resource.add_font(fonte)
action_man = font.load('Source Code Pro')


from tkinter import *

tela = Tk()
tx = Text(tela, font=("Source Code Pro", 15))
tx.grid()


tela.mainloop()


'''
AAAAAAAA
aaaaaaaa
llllllll
LLLLLLLL
QQQQQQQQ
WWWWWWWW
(((())))
********
mostrene
if 1==1:
'''