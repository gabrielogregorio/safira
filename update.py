import requests
from libs.funcoes import transformar_em_json, carregar_json

def obter_versao_mais_recente():
    resposta = requests.get("https://raw.githubusercontent.com/Combratec/feynman_code/master/versao/update.json")
    return transformar_em_json(resposta.text)

def obter_versao_baixada():
    return carregar_json("versao/update.json")

recente = obter_versao_mais_recente()
baixada = obter_versao_baixada()

if (recente["versao"] > baixada["versao"]):
    print("Por favor, atualize sua conta, você não está usando a versão mais recente deste projeto")

elif recente["versao"] != baixada["versao"]:
    print("Por favor, Você não está usando a mesma versão do github")

else:
    print("Você está usando a versão mais atualizada!")