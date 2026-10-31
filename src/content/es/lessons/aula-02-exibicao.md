# Mostrar en pantalla

El `muestra` no escribe solo texto. También hace cuentas y usa colores.

## Texto y números

El texto va entre comillas. El número va sin comillas, y el computador hace la cuenta por ti.

```safira
muestra "Dos más dos es:"
muestra 2 + 2
muestra 10 * 3
```

## Colores

Pon `en color` después del texto. Vale el nombre del color o un código como `#ff1122`.

```safira
muestra "Azul" en color azul
muestra "Morado" en color morado
muestra "Rojo" en color #ff1122
```

## Desafío: la cuenta

Muestra el resultado de `25 * 4`. Deja que el computador haga la cuenta, sin escribir el resultado.

```safira
# Muestra aquí el resultado de 25 * 4.

```

```solution
muestra 25 * 4
```

```check
{ "uses": ["print"], "hint": "Sin comillas, el computador hace la cuenta: muestra 25 * 4", "cases": [{ "shows": ["100"] }] }
```
