from json    import load

class Mensagens:
    def __init__(self, idioma):
        self.idioma = idioma
        try:
            with open('libs/mensagens.json', encoding='utf8') as json_file:
                self.mensagens = load(json_file)
        except:
            with open('mensagens.json', encoding='utf8') as json_file:
                self.mensagens = load(json_file)

    def text(self, chave):
        if chave == "":
            return None

        return self.mensagens[chave][self.idioma]
