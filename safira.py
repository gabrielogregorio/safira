# Theme One Dark
# sudo apt install python3-distutils
# sudo apt install python3-tk
# sudo apt-get install python3-pip
# sudo apt-get install python3-tk tk-dev

__author__ = 'Gabriel Gregório da Silva'
__email__ = 'gabriel.gregorio.1@outlook.com'
__github__ = 'https://github.com/Combratec/safira'
__description__ = 'Linguagem de programação focada em lógica'
__version__ = '0.3'
__project__ = 'Combratec'
__status__ = 'Desenvolvimento'
__date__ = '01/08/2019'


class Safira():
    """Classe que carrega o programa"""

    def __init__(self):
        self.dic_comandos, self.cor_do_comando = funcoes.atualiza_configuracoes_temas()

        self.design = Design()
        self.design.update_design_dic()

        # Obter o design configurado atualmente
        self.dic_design = self.design.get_design_dic()
        


    def main(self):

        # Carregarmento do splash e da interface
        self.splash = Splash(self.design)
        interf = Interface(self.tela, self.dic_comandos, self.design, self.cor_do_comando, self.interface_idioma, self.splash)

        self.splash.splash_inicio()
        sleep(1)

        interf.carregar_tela_principal()