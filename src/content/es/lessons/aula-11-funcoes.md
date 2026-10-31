# Funciones

Una función es un bloque de código con nombre. La escribes una vez y la usas cuantas veces quieras.

## Crear y llamar

Crear la función no ejecuta nada. Solo se ejecuta cuando llamas a su nombre.

```safira
funcion hola {
    muestra "¡Hola!"
    muestra "¿Cómo estás?"
}

hola()
hola()
```

## Pasar un valor

La función puede recibir valores para trabajar con ellos.

```safira
funcion saludar(nombre) {
    muestra "Hola, " + nombre
}

saludar("Ana")
saludar("Bea")
```

## Devolver un resultado

`volver` entrega un resultado a quien llamó.

```safira
funcion doble(numero) {
    volver numero * 2
}

muestra doble(4)
```

## Desafío: suma

Crea la función `sumar`, que recibe dos números y devuelve la suma. Después muestra `sumar(2, 3)`.

```safira
# Crea la función aquí.

# Muestra sumar(2, 3) aquí.

```

```solution
funcion sumar(a, b) {
    volver a + b
}

muestra sumar(2, 3)
```

```check
{ "uses": ["functionDeclaration", "return", "call"], "hint": "Empieza con funcion sumar(a, b) { y usa volver a + b.", "cases": [{ "shows": ["5"] }] }
```
