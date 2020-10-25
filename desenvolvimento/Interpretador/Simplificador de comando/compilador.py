from re import finditer
from libs.funcoes import atualiza_configuracoes_temas

class Compilar():
    def __init__(self):
        pass

    def simplica_comandos(self, dic_comandos):

        # Reduzir complexidade
        n = 0
        dic_formatada = {}
        for k, v in dic_comandos.items():
            n+= 1
            dic_formatada[k] = {"comando": [";" + str(n)]}

        return dic_formatada

    def simplica_codigo(self, dic_comandos, dic_formatada, codigo):
        codigo_tratado = ""

        lista = codigo.split('\n')

        for linha in lista:
            linha = linha.strip()
            comando_localizado = False

            for k, v in dic_formatada.items():
                dic_comando = dic_comandos[k]['comando']

                for comando in dic_comando:
                    comando = comando[0]
                    teste = linha.startswith(comando)

                    if comando == "":
                        continue

                    if teste:
                        codigo_tratado += v["comando"][0] + " " + linha[len(comando):]
                        comando_localizado = True
                        break

                if comando_localizado:
                    break

            if not comando_localizado:
                codigo_tratado += linha
            codigo_tratado += "\n"

        return codigo_tratado

codigo = """println ola mundo
if 1 == 1 {
    mostre "ola mundo"
}
"""

dic_comandos,  remover, cor_do_comando = atualiza_configuracoes_temas()

cp = Compilar()

dic_formatada = cp.simplica_comandos(dic_comandos)

print(cp.simplica_codigo(dic_comandos, dic_formatada, codigo))