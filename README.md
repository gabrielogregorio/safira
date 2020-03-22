# <ALERTA>. O interpretador está sendo refeito para atender melhor as necessidades
# Uma linguagem de programação natural
Uma linguagem de programação universal, simples e focada em na lógica.

> Atenção: Esse projeto está na versão beta, contém erros, códigos ineficientes e não possui versões compiladas, dependendo de um interpretador Python

# Introdução

## Tópicos
- [objetivo](#Objetivo)
- [Como fazer um print](#Como-fazer-um-print)
- [Como fazer um print nessa linha](#Como-fazer-um-print-nessa-linha)
- [Como declarar uma variável](#Como-declarar-variáveis)
- [Como fazer uma condicional](#Como-fazer-uma-condicional)
- [como usar funcoes](#Como-usar-funções)
- [Como ler o que o usuário digitar](#Como-ler-o-que-o-usuário-digitar)
- [Como fazer um loop enquanto](#Como-fazer-um-loop-enquanto)
- [como fazer um loop repetir](#Como-fazer-um-loop-repetir)
- [como fazer um delay](#Como-fazer-um-Delay)
- [Como sortear um número aleatório](#Como-sortear-um-número-aleatório)
- [Como limpar a tela](#Como-limpar-a-tela)
- [Como trabalhar com listas](#Como-trabalhar-com-listas)


## Objetivo  

Desenvolvimento uma linguagem de programação para crianças e para pessoas sem nenhum conhecimento em programação. A longo prazo, pretendemos criar uma IDE com uma linguagem de programação simples. A idéia é que ela seja uma ponte simples para que possoas possam aprender uma linguagem de programação com pouca ou sem nenhuma base do assunto.

A linguagem funciona utilizando termos relativamente simples, como: **mostre**,**exiba**, **mostre nessa linha**, **exiba nessa linha**, etc. Também pretendemos permitir o uso de palavras chaves em múltiplos idiomas.

Com isso, pretendemos suavizar a curva de aprendizagem de lógica de programação, e ao mesmo tempo preparando as pessoas para linguagens mais rápidas e poderosas de mais baixo nível, portanto, conceitos como sintaxe ainda estarão presentes na linguagem.

Esperamos que ela possa suavizar o aprendizado de linguagens como Python, Javascript, R, C#, C, C++,etc...

Isso não significa que ela será pensada apenas para quem quer entrar no assunto, ela é principalmente focada na lógica de programação, portanto, qualquer pessoa poderá escrever seus algorítimos de forma muito rápida.

# Como fazer as coisas?
## Como fazer um print
```
mostre "Hello World"
exiba "Olá mundo"

n = 10  
imprima 10 + 20  
escreva na tela 'string'   
display "string"  
mostre n / n  
escreva n  
exiba n elevado a 4  
```

## Como fazer um print nessa linha
```
escola = "Fatec"
seunome = "Denise"
semestre = 1

mostre "--------------- Exemplos --------------- "
mostre nessa linha "Sala de aula: ", 09
exiba nessa linha " | Escola: ", escola
escreva nessa linha " |  Aluno: ",seunome
imprima nessa linha " | Semestre: ", semestre
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

function mostraIdade
{
    mostre 9999
}

nota1 = 9.8 
nota2 = 8.7
nota3 = 7.9

calculaMedia passando parametros nota1,nota2,nota3
mostraIdade
```

## Como ler o que o usuário digitar
```
mostre nessa linha 'Digite seu nome: '
nome recebe o que for digitado

se nome == 'Catiana'
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

x = 4
repeat x vezes
{
    mostre "Repetindo x vezes"
}
```

## Como fazer um Delay
```
espere 1 segundo
mostre "olá?"

aguarde 2 segundos
mostre "Tudo bem?"

espere 5000 ms
mostre 'Como você vai?'
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

## Como trabalhar com listas
```
lista de nomes recebe "Peter", "Mariana"
mostre nomes

remova "Mariana" da lista de nomes
mostre nomes

tamanho da lista nomes

adicione "Jacson" a lista de nomes
mostre nomes

se 1 for igual a 1 e tiver "Peter" na lista de nomes
{
    mostre "Tem sim!"
}

```

