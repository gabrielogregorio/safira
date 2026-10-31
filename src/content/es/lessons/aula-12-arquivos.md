# Archivos

Los archivos guardan información. Todo lo que el programa crea aparece en la barra de archivos del proyecto.

## Crear y escribir

Mira la barra de archivos después de ejecutar.

```safira
crea el archivo "recado.txt"
agregue "Comprar pan" al archivo "recado.txt"
```

## Leer

Con `lea el archivo` guardas el contenido en una variable.

```safira
crea el archivo "nota.txt"
sobrescribir "Nota 10" al archivo "nota.txt"

texto = lea el archivo "nota.txt"
muestra texto
```

## Comprobar y borrar

Puedes borrar un archivo y preguntar si todavía existe.

```safira
crea el archivo "viejo.txt"
eliminar el archivo "viejo.txt"

si el archivo "viejo.txt" no existe entonces {
    muestra "El archivo desapareció"
}
```

## Desafío: diario

Crea el archivo `diario.txt`, escribe `Hoy aprendí Safira` en él, lee el archivo y muestra el texto.

```safira
# Crea el archivo, escribe, lee y muestra.

```

```solution
crea el archivo "diario.txt"
sobrescribir "Hoy aprendí Safira" al archivo "diario.txt"

texto = lea el archivo "diario.txt"
muestra texto
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Usa crea el archivo, sobrescribir ... al archivo y lea el archivo.", "cases": [{ "shows": ["Hoy aprendí Safira"] }] }
```
