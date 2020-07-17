# Comandos
dic = {
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

print(dic)

# Reduzir complexidade
n = 0
dic_formatada = {}
for k, v in dic.items():
    n+= 1
    dic_formatada[k] = ";" + str(n)

print(dic_formatada)


codigo_tratado = ""
codigo = """

mostre na tela 2

quando 1 == 1
"""

lista = codigo.split('\n')

for linha in lista:
    comando_localizado = False

    for k, v in dic_formatada.items():
        dic_comando = dic[k]['comando']

        for comando in dic_comando:
            comando = comando[0]

            teste = linha.startswith(comando)

            if teste:
                codigo_tratado += v + " " +linha[len(comando):]

                comando_localizado = True
                break

        if comando_localizado:
            break

    if not comando_localizado:
        codigo_tratado += linha
    codigo_tratado += "\n"

print(codigo)
print(codigo_tratado)