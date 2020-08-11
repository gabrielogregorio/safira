import json
import datetime

class Log:
    def __init__(self):
        self.arquivo_logs = 'logs/exec.txt'
        self.arquivo_json = 'logs/registros.json'

    def criar_arquivo(self, arquivo):
        a = open(arquivo, 'w', encoding='utf-8')
        a.write("")
        a.close()
        return True

    def abrir_json(self, arquivo):
        a = open(arquivo, 'r', encoding='utf8')
        txt = a.read()
        a.close()
        print(txt)
        return json.loads(txt)

    def salvar_json(self, arquivo, json):
        a = open(arquivo, 'w', encoding='utf-8')
        a.write(str(json))
        a.close()
        return True

    def registrar_log(self, msg):
        a = open(self.arquivo_logs, 'a', encoding='utf-8')
        base = "[{}] ".format(str(datetime.datetime.now()))
        a.write(base + msg)
        a.close()

    def atualizar_dicionario(self, arquivo, chave, valor):
        json = Log.abrir_json(self, arquivo)
        json[chave] = valor

        json = str(json).replace('\'', '\"')

        Log.salvar_json(self, arquivo, json)
        return json

l = Log()
l.atualizar_dicionario('logs/registros.json', 'acessos', 1000)


#l.registrar_log("\nInicio da execução\n")
#l.registrar_log("Guia Aberta\n")
#l.registrar_log("Guia fechada\n")
#l.registrar_log("Interpretador acionado\n")
#l.registrar_log("Interpretador Finalizado!\n")
#l.registrar_log("Programa finalizado\n")
