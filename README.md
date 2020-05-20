# AVISO
Esse projeto está na versão beta 0.1

# Introdução
Uma linguagem de programação introdutória universal, simples e focada em na lógica.

![Imagem](imagens/safira.png)

# Como executar  
1. Baixe o Python3.7 no seu computador
2. Execute o arquivo "programa.py"
3. Programe!

## Tópicos
- [objetivo](#Objetivo)
- [Como-trabalhar-com-listas](#Trabalhando-com-listas)
- [Como exibir algo na tela](#Como-fazer-um-print)
- [Como exibir na mesma linha](#Como-fazer-um-print-nessa-linha)
- [Como declarar uma variável](#Como-declarar-variáveis)
- [Como testar uma condição](#Como-fazer-uma-condicional)
- [Como criar e usar uma função](#Como-usar-funções)
- [Como ler o que o usuário digitar](#Como-ler-o-que-o-usuário-digitar)
- [Como fazer um loop testando uma condição](#Como-fazer-um-loop-enquanto)
- [Como fazer um loop for](#Loop-para-cada)
- [Como fazer um loop por x vezes](#Como-fazer-um-loop-repetir)
- [Como esperar um tempo](#Como-fazer-um-Delay)
- [Como gerar um número aleatório](#Como-sortear-um-número-aleatório)
- [Como limpar a tela](#Como-limpar-a-tela)
- [Como incrementar uma variável](#Incrementar-ou-decrementar-uma-variável-numérica)

# Objetivo  
Linguagem de programação para crianças e para pessoas sem nenhum conhecimento em programação. A longo prazo, pretendemos criar uma IDE com uma linguagem de programação simples. A idéia é que ela seja uma ponte simples para que possoas possam aprender uma linguagem de programação com pouca ou sem nenhuma base do assunto.

A linguagem funciona utilizando termos relativamente simples, como: **mostre**,**exiba**, **mostre nessa linha**, **exiba nessa linha**, etc.

Com isso, pretendemos suavizar a curva de aprendizagem de lógica de programação e ao mesmo tempo preparar as pessoas para linguagens mais rápidas e poderosas de mais baixo nível.

Esperamos que ela possa suavizar o aprendizado de linguagens como Python, Javascript, R, C#, C, C++, etc...

-------------------------------------

# Como fazer as coisas?

## Como fazer um print
```
mostre "Hello World"
exiba "Olá mundo"
print "Hello World"
display "Cobol"
mostre 2 * 2
```

## Como fazer um print nessa linha
```
mostre "--------------- Exemplos --------------- "
mostre nessa linha "Sala de aula: ", 09
exiba nessa linha " | Escola: "
escreva nessa linha " |  Aluno: "
imprima nessa linha " | Semestre: "
```

## Como declarar variáveis
```
base = 2
numero vale base ** 2
idade recebe 20 + 1
curso = "ADS"
nome recebe "gabriel"
```

## Como fazer uma condicional
```
nome2 = "Carolina"
x = 10

se "Carolina" for igual a nome2
{
    mostre "Esse nome é legal"
}

if x >= 10
{
    mostre "É verdade esse bilhete"
}
```

## Como usar funções
```
funcao calculaMedia recebe parametros nota1, nota2, nota3
{
    mostre (nota1 + nota2 + nota3) / 3
}

nota1 = 9.8 
nota2 = 8.7
nota3 = 7.9

calculaMedia passando parametros nota1,nota2,nota3
```

## Como ler o que o usuário digitar
```
mostre nessa linha "Digite seu nome: "
nome recebe o que for digitado

se nome == "Catiana"
{
    mostre "Seu nome é: ", nome
}
```

## Como fazer um loop enquanto
```
x recebe 0
enquanto 10 for maior que x
{
    x recebe x mais 1
    mostre x
}

while x > 1
{
    x = x - 1
    mostre x 
}
```

## Como fazer um loop repetir
```
repita 10 vezes
{
    mostre "Repetindo 10 vezes"
}
```

## Como fazer um Delay
```
espere 1 segundo
mostre "olá?"

aguarde 2 segundos
mostre "Tudo bem?"

espere 5000 ms
mostre "Como você vai?"
```

## Como sortear um número aleatório
```
sorteado recebe um numero aleatorio entre 10 e 20
mostre sorteado
```

## Como limpar a tela
```
mostre "Pressione enter"

i = o que o usuario digitar
limpatela

mostre "Tela limpa"
```

## Incrementar ou decrementar uma variável numérica
```
numContador = 10

incremente 2 em numContador
mostre numContador

decremente 2 em numContador
mostre numContador


```

## Loop para cada
```
para cada x de 10 ate 20
{
    mostre x
}

```

## Trabalhando com listas
```
lista de nomes com 10 posicoes
lista de nomes na posicao 2 recebe "Atena"

lista de cidades recebe "Recife", "São Paulo", "Londres"
se tiver "Los Angeles" na lista de nomes
{
    remova "Los Angeles" da lista de nomes    
}

adicione "Rio de Janeiro" na posicao 2 da lista de cidades
adicione "Rio de Janeiro" no final da lista de cidades
adicione "Rio de Janeiro" no inicio da lista de cidades
adicione "Rio de Janeiro" na lista de cidades

mostre lista de cidades na posicao 3
mostre tamanho da lista de nomes

```


