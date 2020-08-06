import json

class Log:
    def __init__(self, arquivo):
        self.arquivo = 'configuracoes/logs.json'

    def __carregar_arquivo(self):

        a = open(self.arquivo, 'r', encoding='utf-8')
        text = a.read()
        a.close()

        return Log.__transformar_um_json(self, text)

    def __transformar_um_json(self, texto):
        return json.load(texto)

    def __alterar_valor_chave(self, chave, novo_valor):
        pass
    
    def registrar_vezes_iniciadas(self):
        json = Log.__carregar_arquivo(self)

        Log.__alterar_valor_chave(self, "acessos", json["acessos"] + 1)




    def registra_inicio(self):



    def registra_fim(self):
        pass

l = Log():
l.registra_inicio()