# Exibiçao  
Os comandos de exibição servem para mostrar alguma coisa na tela, em especial um texto.

## Dicionário
**Strings ou textos**
São textos entre aspas, exemplo: "Isso é um texto e o número 1 é maior que o 0"

**Floats ou Numéricos**
São números sem aspas, você pode fazer calculos com eles. Exemplo: 2, ou 2 + 2

## Usando Exibiçao
Para usar os comandos de exibição você só precisa usar o comando mostre. Esse comando mostra cada texto em uma linha diferente.

```
mostre "Olá mundo"
mostre "Isso é um texto qualquer"
mostre 10
```

## Variações
Se você quiser exibir um texto e um número por exemplo, você pode usar o %, ele servirá para você inserir alguma coisa no meio do texto, desta forma:

```
mostre "A soma de 2 + 2 é %" inserindo 4
```

Você também pode fazer operações matemáticas:
```
mostre "A soma de 2 + 2 é %" inserindo 2 + 2
```

Neste exemplo acima, você pode ver que no lugar do % é inserido o resultado da operação 2 + 2, que é numérico.

Podemos aprofundar o uso desse recurso, veja um exemplo:
```
mostre "A soma de % + % é %" inserindo 2, 3, 2 + 3
```
Perceba que ao usar a virgula, os valores são inseridos nas posições que o % está:

```
mostre "A soma de % + % é %" inserindo 2, 3, 2 + 3
#                 \   \   \___________/__/____/
#                  \   \_____________/__/
#                   \_______________/
```

## Exibindo na mesma linha
E se você quiser exibir tudo na mesma linha, você pode usar o comando de exibir na mesma linha, todos os textos serão exibidos em uma unica linha.

```
mostre nessa linha "Olá Amigo, "
mostre nessa linha "Tudo bem?"
```

## Exibindo linhas coloridas
Você também pode dar uma cor aos textos exibidos, bastando informar um código Hexadecimal ou o nome das cores, por enquanto em inglês. Pesquise por esse código no Google por '#88ffff'


## Variações
Se você se sentir confortável, pode executar esses mesmos comandos de várias outras formas diferentes, veja estes exemplos.

### Exibição na mesma linha
**Formas recomendadas**
```
print "olá mundo"
```

**Outras formas**
```
display "olá mundo"
mostre nessa linha "olá mundo"
escreva nessa linha "olá mundo"
```


### Exibição na mesma linha
**Formas recomendadas**
```
printf "olá mundo"
println "olá mundo"
```

**Outras formas**
```
mostre "olá mundo"
show "olá mundo"
exiba "olá mundo"
```


### Inserindo itens no meio do texto.
É importante lembrar que o comando inicial não interfere no comando secundário, ou seja, você pode usar qualquer combinação acima, como o mostre, printf, show, display com qualquer combinação abaixo que deverá funcionar, mas é recomendado usar somente um idioma, no caso, preferencialmente o inglês para você ir se acostumando.

**Formas recomendadas**
```
mostre "Olá %" inserindo "Enzo"
mostre "Olá %" format "Enzo"
mostre "Olá %" % "Enzo"
```

**Outras formas**
```
mostre "Olá %" formatting "Enzo"
mostre "Olá %" inserting "Enzo"
mostre "Olá %" formatando "Enzo"
```


### Exibindo textos coloridos
**Formas recomendadas**
```
mostre "olá mundo" in color "#ffaa11"
mostre "olá mundo" in color "blue"
```

**Outras formas**
```
mostre "olá mundo" na cor "#ffcc22"
mostre "olá mundo" en color "white"
```

## Combinando valores
Você pode combinar o inserindo com o na cor, desta forma, você irá inserir valores em um texto e exibi-lo e uma cor especifica.
```
mostre "Olá %" inserindo "gabriel" na cor "#ff55ff"
```