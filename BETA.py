''' 
condicao {
	string condicional string
	inteiro condicional inteiro
	# alerta erro se for igual
}

problema_valores{
	valor + valor
	valor , valor

}


comando_exibicao problema_valores             # MOSTRE 2+2
comando_condicional (condicao).               # SE       (X FOR IGUAL A Y)
	comando_exibicao problema_valores         # MOSTRE variavel + 1
	comando_condicional_normal (condicao).    # SE       (X FOR IGUAL A 5)
	comando_condicional_loop   (condicao).    # ENQUANTO (X FOR IGUAL A 5)


objeto comando_atribuicao OBJETO/VALOR        # OBJETO RECEBE 7
objeto comando_atribuicao OBJETO/VALOR        # OBJETO RECEBE 'OLÁ'
objeto comando_atribuicao OBJETO/VALOR        # OBJETO RECEBE OBJETO2

comando_condicional_loop (condicao).          # ENQUANTO (X FOR IGUAL A 5)


'''