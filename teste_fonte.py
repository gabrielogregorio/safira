from pyglet import resource
from pyglet import font
from tkinter import *

texto = """
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
"""

tela = Tk()

fonte = 'fonte/Roboto_Mono/RobotoMono-Regular.ttf'
resource.add_font(fonte)
action_man = font.load('Roboto Mono')

tx = Text(tela, font=("Ubuntu Mono", 15))
tx.insert(1.0, texto)
tx.grid()

tela.mainloop()


