# Lista de compras

## Lista de compras

```safira
# Crea una lista con dos frutas.
lista de frutas recibe "uva", "pera"

# Pone una fruta más al final.
añadir "kiwi" al final de la lista de frutas

# Muestra cada fruta, una por línea.
desplazarse por la lista de frutas asignando en item {
    muestra item
}
```

## Desafío: Lista de compras

```safira
# Desafío: Crea una lista llamada compras con arroz y
# frijol.
# Pon leche al final.
# Muestra cada cosa.

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
