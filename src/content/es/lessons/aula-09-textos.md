# Trabajar con textos

Se puede cambiar la forma de un texto y mirarlo letra por letra.

## Mayúsculas y minúsculas

Un texto puede quedar todo grande, todo pequeño o solo con la primera letra grande.

```safira
nombre = "ana maria"

muestra nombre en mayusculas
muestra nombre en minusculas
muestra nombre captalizado
```

## Letra por letra

`desplazar` pasa por cada letra, una a la vez.

```safira
palabra = "Sol"

desplazar palabra asignando en letra {
    muestra letra
}
```

## Desafío: gritar

Pide un texto y muestra ese texto todo en mayúsculas.

```safira
muestra "Escribe una palabra:"
palabra = lo que escribe el usuario

# Muestra la palabra en mayúsculas aquí.

```

```solution
muestra "Escribe una palabra:"
palabra = lo que escribe el usuario

muestra palabra en mayusculas
```

```check
{ "uses": ["case"], "exact": true, "hint": "Escribe: muestra palabra en mayusculas", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
