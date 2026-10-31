# Te damos la bienvenida a Safira

Safira es un lenguaje de programación en el que escribes casi como hablas.

## Tu primer programa

Un programa es una lista de órdenes para el computador. Esta tiene una sola orden: mostrar un texto en la pantalla.

Presiona ▶ Ejecutar y mira el resultado al lado.

```safira
muestra "¡Hola, mundo!"
```

## Una orden después de otra

Safira lee de arriba hacia abajo, una línea a la vez. Cada `muestra` escribe en una línea nueva.

```safira
muestra "Primero"
muestra "Segundo"
muestra "Tercero"
```

## Comentarios

Una línea que empieza con `#` es un comentario. Es una nota para quien lee el código, y el computador la ignora.

```safira
# Esta línea no aparece en la pantalla.
muestra "¡Esta sí aparece!"
```

## Desafío: háblame

Haz que el programa muestre el texto `¡Hola, Safira!`.

```safira
# Escribe tu código aquí abajo.

```

```solution
muestra "¡Hola, Safira!"
```

```check
{ "uses": ["print"], "hint": "Usa el comando muestra con el texto entre comillas.", "cases": [{ "shows": ["¡Hola, Safira!"] }] }
```
