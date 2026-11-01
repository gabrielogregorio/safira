# Lista de compras

## Lista de compras

`lista de frutas recibe "uva", "pera"` crea una lista. `añadir "kiwi" al final de la lista de frutas` la aumenta. `desplazarse por la lista de frutas asignando en item {` pasa por todos.

Crea la lista `compras` con `arroz` y `frijol`, añade `leche` al final y muestra cada item.

```safira
# Escribe aquí.
```

```solution
lista de compras recibe "arroz", "frijol"
añadir "leche" al final de la lista de compras

desplazarse por la lista de compras asignando en item {
    muestra item
}
```

```check
{"uses": ["listDeclare", "listInsert", "forEach"], "hint": "Crea, añade y recorre la lista.", "cases": [{"shows": ["arroz", "frijol", "leche"]}]}
```
