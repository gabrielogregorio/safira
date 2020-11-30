import util.funcoes as funcoes

class Mensagens:
    def __init__(self, idioma:str):
        self.idioma = idioma
        json_link = "mensagens.json"

        self.mensagens = funcoes.carregar_json('interpretador/{}'.format(json_link))

    def text(self, chave:str) -> str:
        if chave == "":
            return None

        return self.mensagens[chave][self.idioma]
