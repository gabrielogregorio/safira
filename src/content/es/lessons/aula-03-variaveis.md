# Variables

Una variable es una cajita con un nombre. Guarda un valor para que lo uses después.

## Guardar un valor

El `=` guarda el valor en la cajita. Después solo usas el nombre.

```safira
nombre = "Ana"
edad = 20

muestra nombre
muestra edad
```

## Mira las variables

Después de ejecutar, mira el panel Variables: muestra el nombre, el valor y el tipo de cada una.

¿Quieres verlo paso a paso? Abre el menú Ejecutar y elige Ejecutar línea por línea.

```safira
puntos = 10
puntos = puntos + 5

muestra puntos
```

## Unir texto y variable

El `+` une textos y variables en una sola frase.

```safira
nombre = "Ana"
edad = 20

muestra "Mi nombre es " + nombre
muestra "Tengo " + edad + " años"
```

## Desafío: tu ciudad

Crea una variable llamada `ciudad` con el valor `Lima` y muestra la frase `Vivo en Lima`, uniendo el texto con la variable.

```safira
# Crea la variable aquí.

# Muestra la frase aquí.

```

```solution
ciudad = "Lima"
muestra "Vivo en " + ciudad
```

```check
{ "uses": ["assign", "variable"], "hint": "Crea la variable con ciudad = \"Lima\" y usa el + para unir.", "cases": [{ "shows": ["Vivo en Lima"] }] }
```
