import util.funcoes as funcoes

class Mensagens:
    def __init__(self, idioma):
        self.idioma = idioma
        json_link = "mensagens.json"

        self.mensagens = funcoes.carregar_json('interpretador/{}'.format(json_link))


    def text(self, chave):
        if chave == "":
            return None

        return self.mensagens[chave][self.idioma]
