import os.path as teste
from os import mkdir
from datetime import datetime

class Logs():
    def __init__(self):
        pass

    def gerar_data(self):
        data = str(datetime.now())
        data = data.replace("-","_")
        data = data.replace(":",".")

        return data

    def __normalizar_ambiente(self):

        if not teste.exists("LOGS/"):
            mkdir("LOGS/")

        if not teste.exists("LOGS/EXECUCAO/"):
            mkdir("LOGS/EXECUCAO/")

        if not teste.exists("LOGS/SCRIPTS/"):
            mkdir("LOGS/SCRIPTS/")

    
    def __registrar(self, link, valor):
        Logs.__normalizar_ambiente(self)
        valor = "[{}] - {}".format(Logs.gerar_data(self), valor)

        if teste.exists(link):
            a = open(link, "a", encoding="utf-8")
            a.write(valor)
            a.close()

        else:
            a = open(link, "w", encoding="utf-8")
            a.write(valor)
            a.close()

    def registrar_Exec(self, complemento,  valor):
        return 0
        Logs.__registrar(self, "LOGS/EXECUCAO/logs_execuc_{}.txt".format(complemento), valor)

    def registrar_Scri(self, complemento, valor):
        return 0
        Logs.__registrar(self, "LOGS/SCRIPTS/logs_script_{}.txt".format(complemento), valor)

