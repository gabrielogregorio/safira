from util.funcoes import carregar_json
from platform import system as platform_system

#objeto['font'] = ('Ubuntu Mono', '')
#fonte = "Lucida Sans"
#if (platform_system() == 'Linux'):
#    fonte = 'Ubuntu Mono'

class Colors():
    def __init__(self):
        self.dic = {}

    def __get_sett_file(self):
        return carregar_json("configuracoes/configuracoes.json")["tema"]

    def update_design_dic(self):
        try:
            texto_json = "temas/interface/{}".format(self.__get_sett_file())
            self.dic = carregar_json(texto_json)
        except Exception as e:
            return [False, e]
    def get(self, chave):
        try:
            return self.dic[chave]
        except Exception as e:
            print(e)
            return {}



    def get_design_dic(self):
        return self.dic
