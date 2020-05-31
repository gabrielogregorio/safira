import requests
from libs.funcoes import carregar_json

resposta = requests.get("https://github.com/Combratec/feynman_code/blob/master/README.md")
print(resposta.text)

carregar_json

#headers
#history
#json
#