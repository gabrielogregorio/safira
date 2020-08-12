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

    def adicionar_novo_acesso(self, arquivo, chave):
        try:
            json = Log.abrir_json(self, arquivo)
            json[chave] = json[chave] + 1
    
            json = str(json).replace('\'', '\"')
    
            Log.salvar_json(self, arquivo, json)
            return json
        except:
            print("Erro ao salvar log: , arquivo='{}', chave='{}'".format(arquivo, chave))
            return False

if __name__ == '__main__':
    l = Log()
    l.adicionar_novo_acesso('logs/registros.json', 'vezes_interpretador_iniciado')
    l.adicionar_novo_acesso('logs/registros.json', 'acessos')