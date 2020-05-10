def md_to_html(txt_md):
    txt_html = txt_md
    return txt_html
    
with open("README.md", "r", encoding='utf-8') as arquivo:
    texto = arquivo.read()


print(texto)


with open("help.html", "w") as arquivo:
    arquivo.write( texto )
