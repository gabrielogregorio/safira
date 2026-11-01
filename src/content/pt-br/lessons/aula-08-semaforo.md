# Semáforo

## Semáforo

`limpe a tela` apaga o que foi mostrado, e `repita 2 vezes {` repete.

Faça um semáforo que repete 2 vezes: mostre `Pare` por 4 segundos, `Siga` por 4 segundos e `Atenção` por 2 segundos, limpando a tela entre eles.

```safira
# Escreva aqui.
```

```solution
repita 2 vezes {
    limpe a tela
    mostre "🔴 Pare"
    espere 4 segundos

    limpe a tela
    mostre "🟢 Siga"
    espere 4 segundos

    limpe a tela
    mostre "🟠 Atenção"
    espere 2 segundos
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Dentro do repita: limpe a tela, mostre e espere, três vezes.", "cases": [{"shows": ["Pare", "Siga", "Atenção"]}]}
```
