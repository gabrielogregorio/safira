# Variáveis

Uma variável é uma caixinha com um nome. Ela guarda um valor para você usar depois.

## Guardar um valor

O `=` guarda o valor na caixinha. Depois é só usar o nome.

```safira
nome = "Ana"
idade = 20

mostre nome
mostre idade
```

## Veja as variáveis

Depois de executar, olhe o painel Variáveis: ele mostra o nome, o valor e o tipo de cada uma.

Quer ver passo a passo? Abra o menu Executar e escolha Executar linha por linha.

```safira
pontos = 10
pontos = pontos + 5

mostre pontos
```

## Juntar texto e variável

O `+` junta textos e variáveis em uma frase só.

```safira
nome = "Ana"
idade = 20

mostre "Meu nome é " + nome
mostre "Tenho " + idade + " anos"
```

## Desafio: sua cidade

Crie uma variável chamada `cidade` com o valor `"Lima"` e mostre a frase `Eu moro em Lima`, juntando o texto com a variável.

```safira
# Crie a variável aqui.

# Mostre a frase aqui.

```

```solution
cidade = "Lima"
mostre "Eu moro em " + cidade
```

```check
{ "uses": ["assign", "variable"], "hint": "Crie a variável com cidade = \"Lima\" e use o + para juntar.", "cases": [{ "shows": ["Eu moro em Lima"] }] }
```
