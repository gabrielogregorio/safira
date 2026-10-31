# Preguntar al usuario

Un programa es más divertido cuando conversa con quien lo usa.

## Leer un texto

`lo que escribe el usuario` detiene el programa y espera. Escribe en el campo del panel de salida y presiona Enter.

```safira
muestra "¿Cómo te llamas?"
nombre = lo que escribe el usuario

muestra "Hola, " + nombre
```

## Leer un número

Para hacer cuentas con lo que se escribió, pide un número.

```safira
muestra "Escribe un número:"
numero = el número que ingresa el usuario

doble = numero * 2
muestra "El doble es " + doble
```

## Desafío: el triple

Pide un número y muestra el triple.

```safira
# Pídele un número al usuario.

# Muestra el número por 3.

```

```solution
muestra "Escribe un número:"
numero = el número que ingresa el usuario

muestra numero * 3
```

```check
{ "uses": ["input"], "hint": "Usa numero = el número que ingresa el usuario y después muestra numero * 3.", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
