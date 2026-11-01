# Cuenta regresiva

## Cuenta regresiva

```safira
muestra "Preparados..."

# Espera 1 segundo antes de seguir.
esperar 1 segundo
muestra "Ya!"
```

## Desafío: Cuenta regresiva

```safira
# Desafío: Muestra 3, 2 y 1, con una espera entre ellos.
# Al final, muestra Fuego!

```

```solution
muestra 3
esperar 1 segundo
muestra 2
esperar 1 segundo
muestra 1
esperar 1 segundo
muestra "Fuego!"
```

```check
{"uses": ["wait"], "hint": "Pon esperar 1 segundo entre los muestra.", "cases": [{"shows": ["3", "2", "1", "Fuego"]}]}
```
