# Funções

Uma função é um bloco de código com nome. Você escreve uma vez e usa quantas vezes quiser.

## Criar e chamar

Criar a função não executa nada. Ela só roda quando você chama o nome dela.

```safira
funcao saudar {
    mostre "Olá!"
    mostre "Tudo bem?"
}

saudar()
saudar()
```

## Passar um valor

A função pode receber valores para trabalhar com eles.

```safira
funcao saudar(nome) {
    mostre "Olá, " + nome
}

saudar("Ana")
saudar("Bia")
```

## Devolver um resultado

`retorne` entrega um resultado para quem chamou.

```safira
funcao dobro(numero) {
    retorne numero * 2
}

mostre dobro(4)
```

## Desafio: soma

Crie a função `somar`, que recebe dois números e retorna a soma. Depois mostre `somar(2, 3)`.

```safira
# Crie a função aqui.

# Mostre somar(2, 3) aqui.

```

```solution
funcao somar(a, b) {
    retorne a + b
}

mostre somar(2, 3)
```

```check
{ "uses": ["functionDeclaration", "return", "call"], "hint": "Comece com funcao somar(a, b) { e use retorne a + b.", "cases": [{ "shows": ["5"] }] }
```
