"""
Funções do orquestrador
* Analisar blocos de código
* Executar comandos no interpretador
* Analisar blocos condicionais
* Analisar blocos de funções
* analisar loops enquanto e repetir
"""

def orquestrador_interpretador(codigo):
    tamanho_codigo = len(codigo)

    analisando_texto = False
    analisando_comentario = False
    penetracao_bloco = 0

    for n_caractere in range(0, tamanho_codigo):
        caractere = codigo[n_caractere]
        print(caractere, end = "")

        # Começou um comentário fora de um texto
        if caractere == '#' and not analisando_texto:
            print("<iniciou comentário>", end = "")
            analisando_comentario = True

        elif caractere == "\n":
            print("<finalizou tudo>")
            analisando_comentario = False
 
        # Começou uma string e não está analisando um comentário
        if caractere == '"' and not analisando_texto and not analisando_comentario:
            analisando_texto = True
            print("<iniciou Texto>", end = "")

        elif caractere == '"' and analisando_texto and not analisando_comentario:
            print("<Finalizou texto>", end = "")
            analisando_texto = False

        if caractere == "{" and not analisando_texto and not analisando_comentario:
            penetracao_bloco += 1
            print("<inicio de bloco>", end = "")

        elif caractere == "}" and not analisando_texto and not analisando_comentario:
            penetracao_bloco -= 1
            print("<fim de bloco>", end = "")

codigo = r'''
mostre "Olá{}{}{} # mundo" # Comentário {}{}{} "" 

se 2 for igual a 5 # comentário feralll
{
    mostre "iai"
}
'''

print(orquestrador_interpretador(codigo))