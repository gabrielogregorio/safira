# pip install crypto graphy
# pip install pycrypto

from cryptography.fernet import Fernet
import bcrypt
# pip3.8screeninfo install screeninfo
from datetime import datetime
from screeninfo import get_monitors
import platform
import psutil
import requests
from copy import deepcopy
from json import dumps

host = 'http://0.0.0.0:5723/gravar/'

class Report: 
    """
        Reporta dados de acesso a combratec, informando dezenas de informações de uso
        sobre a plataforma a fim de coletarmos dados que possam fornecer insights sobre
        a experiência no uso da safira
    """
    def __init__(self, id):
        self.data = {
            'id': id,
            'data_inicio':str(datetime.now()),
            'data_fim':''
            }

        self.data["movimento_mouse"] = []
        self.data["ajuste_janela"] = []
        self.data["cliques_mouse"] = []



    def hardware(self):
        monitores = []

        for monitor in get_monitors():
            monitores.append(monitor)

        
        # Visualização
        self.data["resolucao_tela"]: str(monitores)

        # Processamento
        self.data['processaddor'] = platform.processor()
        self.data['quantidade_nucleos'] = str(psutil.cpu_count())

        self.data["taxa_uso_cpu_5"] = str(psutil.cpu_percent(interval=5, percpu=True))
        self.data["frequencia_cpu"] = str(psutil.cpu_freq(percpu=True))


        # Sistema
        self.data['release'] = platform.release()
        self.data['sistema'] = platform.system()
        self.data['arquitetura'] = platform.architecture()
        self.data['platforma'] = platform.platform()
        self.data['versao'] = platform.version()

        # Benchmark
        self.data["tempo_calculo"] = ""

        # Memória RAM
        self.data["memoria_ram_livre"] = int(psutil.virtual_memory().free)
        self.data["memoria_ram_total"] = int(psutil.virtual_memory().total)


    def posicao_mouse(self, state, x, y):
        self.data["movimento_mouse"].append([str(datetime.now()), state, x, y])


    def clique_mouse(self, state, num, x, y):
        self.data["cliques_mouse"].append([str(datetime.now()), state, num, x, y])


    def ajuste_tela(self, width, height):
        self.data["ajuste_janela"].append([str(datetime.now()), width, height])


    def salvar_report(self):
        self.data['data_fim'] = str(datetime.now())


    def enviar_report(self):
        print(self.data)
        try:
            requests.post(host, json=self.data)
        except Exception as erro:
            print("Erro ao enviar dados: ", erro)



#report = Report('1312312312312')
#report.hardware()
#report.salvar_report()
#report.enviar_report()
'''


import uuid

chave1 = str(uuid.uuid4())

chave2 = Fernet.generate_key()
cipher_suite = Fernet(chave2)

cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")

cipher_text_uuid = cipher_text[0:10] + chave1 + cipher_text[10:]

plain_text = cipher_suite.decrypt(cipher_text)

print(chave)
print(plain_text)
print(cipher_text)

'''
