# -*- coding: utf-8 -*-

# Theme One Dark
# sudo apt install python3-distutils
# sudo apt install python3-tk
# sudo apt-get install python3-pip
# sudo apt-get install python3-tk tk-dev

from interface import *
from tkinter   import Tk
from sys       import version
from time      import sleep


__author__      = 'Gabriel Gregório da Silva'
__email__       = 'gabriel.gregorio.1@outlook.com'
__project__     = 'Combratec'
__github__      = 'https://github.com/Combratec/'
__description__ = 'Linguagem de programação focada em lógica'
__version__     = '0.21'
__status__      = 'Desenvolvimento'
__date__        = '01/08/2019'

class Safira():
    def __init__(self):
        self.dic_comandos, self.dic_design, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

        self.tela = Tk()
        self.tela.withdraw()
        self.tela.overrideredirect(1)
        self.tela.rowconfigure(1, weight=1)
        self.tela.grid_columnconfigure(1, weight=1)

    def main(self):
        splash = Splash(self.tela, self.dic_design)
        interf = Interface(self.tela, self.dic_comandos, self.dic_design, self.cor_do_comando)

        splash.splash_inicio()
        sleep(3)
        splash.splash_fim()
        interf.inicioScreen()

if __name__ == "__main__":
    app = Safira()
    app.main()
