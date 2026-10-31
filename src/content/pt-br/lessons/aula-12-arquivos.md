# Arquivos

Arquivos guardam informações. Tudo o que o programa cria aparece na barra de arquivos do projeto.

## Criar e escrever

Olhe a barra de arquivos depois de executar.

```safira
crie o arquivo "recado.txt"
adicione "Comprar pão" no arquivo "recado.txt"
```

## Ler

`leia o arquivo` traz o texto de volta para uma variável. `sobrescreva` troca todo o texto do arquivo.

```safira
crie o arquivo "nota.txt"
sobrescreva "Nota 10" no arquivo "nota.txt"

texto = leia o arquivo "nota.txt"
mostre texto
```

## Conferir e apagar

Dá para perguntar se um arquivo existe e apagar o que não serve mais.

```safira
crie o arquivo "velho.txt"
delete o arquivo "velho.txt"

se o arquivo "velho.txt" nao existe então {
    mostre "O arquivo sumiu"
}
```

## Desafio: diário

Crie o arquivo `diario.txt`, escreva `Hoje aprendi Safira` nele, leia o arquivo e mostre o texto.

```safira
# Crie o arquivo, escreva, leia e mostre.

```

```solution
crie o arquivo "diario.txt"
sobrescreva "Hoje aprendi Safira" no arquivo "diario.txt"

texto = leia o arquivo "diario.txt"
mostre texto
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Use crie o arquivo, sobrescreva ... no arquivo e leia o arquivo.", "cases": [{ "shows": ["Hoje aprendi Safira"] }] }
```
