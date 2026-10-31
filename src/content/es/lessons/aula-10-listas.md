# Listas

Una lista guarda varios valores en una sola variable.

## Crear una lista

Las posiciones empiezan en 1.

```safira
lista de frutas recibe "uva", "manzana", "mango"

muestra frutas
muestra lista de frutas en posición 1
muestra el tamaño de la lista de frutas
```

## Añadir y quitar

Puedes poner un elemento al final y quitar otro de la lista.

```safira
lista de frutas recibe "uva", "manzana"

añadir "mango" al final de la lista de frutas
eliminarlo "uva" de la lista de frutas

muestra frutas
```

## Pasar por todos los elementos

El bloque se ejecuta una vez por cada elemento de la lista.

```safira
lista de frutas recibe "uva", "manzana", "mango"

desplazarse por la lista de frutas asignando en fruta {
    muestra "Me gusta " + fruta
}
```

## Desafío: lista de compras

Crea la lista `compras` con `arroz` y `frijoles`. Añade `leche` al final y muestra cada elemento en una línea.

```safira
# Crea la lista aquí.

# Añade la leche aquí.

# Muestra cada elemento aquí.

```

```solution
lista de compras recibe "arroz", "frijoles"

añadir "leche" al final de la lista de compras

desplazarse por la lista de compras asignando en elemento {
    muestra elemento
}
```

```check
{ "uses": ["listDeclare", "listInsert", "forEach"], "hint": "Usa lista de ... recibe, añadir ... al final de la lista de ... y desplazarse por la lista de ...", "cases": [{ "shows": ["arroz", "frijoles", "leche"] }] }
```
