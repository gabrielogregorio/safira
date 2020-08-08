from libs.funcoes import carregar_json


class Design():
    def __init__(self):
        self.dic = {}

    def __get_sett_file(self):
        return carregar_json("configuracoes/configuracoes.json")["tema"]

    def update_design_dic(self):
        texto_json = "temas/{}".format(Design.__get_sett_file(self))
        self.dic = carregar_json(texto_json)

    def get_design_dic(self):
        return self.dic
