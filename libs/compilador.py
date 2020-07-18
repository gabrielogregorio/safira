
from re import finditer
def analisa_inicio_codigo(linha):
    linha = linha.strip()
    posicoes = finditer(r'^(\[\d*\])', linha)

    num_linha = 0
    for uma_posicao in posicoes:
        num_linha = uma_posicao.end()
        break

    return num_linha


def cortar_comentarios(codigo):
    lista= codigo.split('\n')

    string = ""
    for linha in lista:
        bool_iniciou_string = False
        linha = linha.strip()
        temp= ""

        for char in range(len(linha)):

            if linha[char] == '"':
                if not bool_iniciou_string:
                    bool_iniciou_string = True
                else:
                    bool_iniciou_string = False

            if not bool_iniciou_string:
                if linha[char] == "#" or linha[char:char+2] == "//":
                    break

            temp += linha[char]

        temp = temp.strip()

        if analisa_inicio_codigo(temp) != len(temp):
            string += temp + "\n"

    return string


# Comandos
dic_comandos = {
  "print":{
    "comando":[
      ["print ","pt-br"],
      ["mostre na tela ","pt-br"]
    ],
    "cor":"lista"
  },
  "if":{
    "comando":[
      ["se ","pt-br"],
      ["if ","pt-br"],
      ["quando ","pt-br"]
    ],
    "cor":"lista"
  }
}

def simplica_comandos(dic_comandos):
    # Reduzir complexidade
    n = 0
    dic_formatada = {}
    for k, v in dic_comandos.items():
        n+= 1
        dic_formatada[k] = {"comando": [";" + str(n)]}

    return dic_formatada


def simplica_codigo(dic_comandos, dic_formatada, codigo):
    codigo_tratado = ""

    lista = codigo.split('\n')

    for linha in lista:
        comando_localizado = False

        for k, v in dic_formatada.items():
            dic_comando = dic_comandos[k]['comando']

            for comando in dic_comando:
                comando = comando[0]

                teste = linha.startswith(comando)

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

#dic_formatada = simplica_comandos(dic_comandos)
#codigo = "print ola mundo"
#print(simplica_codigo(dic_comandos, dic_formatada, codigo))