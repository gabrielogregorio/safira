class Basicos():
    def __init__():
        pass

    def verifica_se_tem(self, linha, a_buscar):
        analisar = True
        lista = []

        for caractere in range(len(linha)):
            if linha[caractere] == '"' and analisar == True:
                analisar = False

            elif linha[caractere] == '"' and analisar == False:
                analisar = True

            if analisar:
                if len(linha) >= caractere + len(a_buscar):

                    if linha[caractere: caractere + len(a_buscar)] == a_buscar:
                        lista.append([caractere, caractere + len(a_buscar)])

        return lista

