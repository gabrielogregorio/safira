# Lista de compras

## Lista de compras

```safira
# Crea la lista.
lista de frutas recibe "uva", "pera"

# Añade al final.
añadir "kiwi" al final de la lista de frutas

# Pasa por todos los items.
desplazarse por la lista de frutas asignando en item {
    muestra item
}
```

## Desafío: Lista de compras

```safira
# Desafío: Crea la lista compras con arroz y frijol, añade
# leche al final y muestra cada item.

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
