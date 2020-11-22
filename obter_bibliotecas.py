from os import path, walk
from re import findall, MULTILINE, sub
lista_imports = []

for _, dirs, files in walk('.'):



    for dir in dirs:
        for file in files:
            file_full = path.join(_, file)

            try:
                with open(file_full, 'r', encoding='utf-8') as f:
                    texto = str(f.read())

                regex = '^from\\s*.{1,}$|^import\\s*.{1,}$'

                itens = findall(regex, texto, MULTILINE)
                if itens is not None:
                    for imports in itens:
                        imports = imports.strip()
                        imports = sub('\\s{1,}', ' ', imports)

                        if imports not in lista_imports:
                            lista_imports.append(imports)
            except Exception as e:
                print(e)

print('\n'*10)

for imp in lista_imports:
    print(imp)