## Interpretador

O interpretador recebe os seguintes parametros

```
| numero |      parametros               |  exemplos      | descrição                                                           |
|-----|----------------------------------|----------------|---------------------------------------------------------------------|
|1   | bool_logs                         | True/False     |  para exibir logs de rastreio do interpretador (reduz o desempenho) |
|2   | lst_breakpoints                   | [1, 2, 3]      |  lista com todos os breakpoints para considerar, exemplo            |
|3   | bool_ignorar_todos_breakpoints    | True/False     |  se é para ignorar todos os breakpoints                             |
|4   | diretorio_base                    | "/home/safira" |  diretório que o script está sendo executado                        |
|5   | dicLetras                         | {}             |  dicionário com as letras iniciais de cada conjunto de comandos     |
|6   | dic_comandos                      | {}             |  dicionário de comandos                                             |
|7   | idioma                            | idioma         | linguagem para o interpretador exibir as mensagem                   |
``` 

## Exemplo de dicionário de comandos
```json
{
  "funcoes":{
    "comando":[
      ["function ","pt-br"],
      ["funcion ","es"],
      ["def ","en-us"]
    ],
    "cor":"tempo"
  },
  "enquanto":{
    "comando":[
      ["enquanto ","pt-br"],
      ["while ","en-us"],
      ["mientras que ","es"],
    ],
    "cor":"condicionais"
  }
}
```

## Como criar um dicionário de letras?
```python
    """
        dic_comandos = é o dicionário com todos os comandos do interpretador
    """

    # Criar um dicionário de letras
    dicLetras = {}
    for k, v in dic_comandos.items():
        dicLetras[k] = []
        for valor in v["comando"]:
            valor = valor[0].strip()

            if valor == "":
                dicLetras[k].append(valor)
            else:
                valor = valor.lower()

                if valor[0] not in dicLetras[k]:
                    dicLetras[k].append(  valor[0] )

```
O resultado é um dicionário desta forma ()MAIS OU MENO_S+)

```json
{
    "mostre":["m", "p"]
}

```

## idiomas disponíveis
* pt-br
* en-us

## Exemplo de 