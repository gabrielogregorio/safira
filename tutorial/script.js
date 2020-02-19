cor_da_sintaxe = {
  "numerico": {
    "foreground": "#04ba10"
  },
  "atribuicao": {
    "foreground": "#64b512"
  },
  "loops": {
    "foreground": "#c29800"
  },
  "lista": {
    "foreground": "#366eff"
  },
  "logico": {
    "foreground": "#f522f5"
  },
  "entrada": {
    "foreground": "#f522f5"
  },
  "exibicao": {
    "foreground": "#0e9bc9"
  },
  "tempo": {
    "foreground": "#366eff"
  },
  "condicionais": {
    "foreground": "#c29800"
  },
  "contas": {
    "foreground": "#f522f5"
  },
  "string": {
    "foreground": "#8f05ff"
  },
  "comentario": {
    "foreground": "#3d3d3d"
  },
  "pare": {
    "foreground": "#ff1212"
  }
}

dic_com = {
  "declaraListas": [
    ["lista de ","pt-br"],
    ["lista ","pt-br"]
  ],
  "adicionarItensListas": [
    ["adicione ","pt-br"]
  ],
  "RemoverItensListas": [
    ["remova ","pt-br"]
  ],
  "tamanhoDaLista": [
    ["o tamanho da lista de","pt-br"],
    ["o tamanho da lista","pt-br"],
    ["tamanho da lista de","pt-br"],
    ["tamanho da lista","pt-br"]
  ],
  "tiverLista": [
    ["tiver","pt-br"]
  ],
  "aleatorio": [
    ["um numero aleatorio entre ","pt-br"],
    ["numero aleatorio entre ","pt-br"]
  ],
  "mostreNessa": [
    ["mostre nessa linha ","pt-br"],
    ["exiba nessa linha ","pt-br"]
  ],
  "mostre": [
    ["mostre ","pt-br"],
    ["exiba ","pt-br"],
    ["printf ","en-us"],
    ["display ","en-us"],
    ["print ","en-us"]

  ],
  "declaraVariaveis": [
    [" recebe ","pt-br"],
    [" vale ","pt-br"],
    [" = ","all"]
  ],
  "funcoes": [
    ["funcao ","pt-br"]
  ],
  "loopsss": [
    ["enquanto ","pt-br"],
    ["while ","pt-br"]
  ],
  "aguarde": [
    ["espere ","pt-br"],
    ["aguarde ","pt-br"]
  ],
  "repita": [
    ["repita ","pt-br"],
    ["repitir ","pt-br"]
  ],
  "se": [
    ["quando ","pt-br"],
    ["se ","pt-br"],
    ["if ","en-us"]
  ],
  "limpatela": [
    ["limpar a tela","pt-br"],
    ["limpatela","pt-br"],
    ["clear","en-us"]
  ],
  "digitado":[
    ["o numero que o usuario digitar","pt-br"],
    ["numero que o usuario digitar","pt-br"],
    ["o numero que for digitado","pt-br"],
    ["numero que for digitado","pt-br"],
    ["o que o usuario digitar","pt-br"],
    ["que o usuario digitar","pt-br"],
    ["o que for digitado","pt-br"],
    ["que for digitado","pt-br"],
    ["numero digitado","pt-br"],
    ["digitado","pt-br"],
    ["entrada","pt-br"]
  ]
}

dic_sub = {
  "repitaVezes": [
    [" vezes","pt-br"],
    [" vez","pt-br"]
  ],
  "logico": [
    [" for maior ou igual a ","pt-br"],
    [" for menor ou igual a ","pt-br"],
    [" for diferente de ","pt-br"],
    [" for maior que ","pt-br"],
    [" for menor que ","pt-br"],
    [" for igual a ","pt-br"],
    [" and ","en-us"],
    [" && ","all"],
    [" ou ","pt-br"],
    [" or ","en-us"],
    [" || ","all"],
    [" == ","all"],
    [" >= ","all"],
    [" <= ","all"],
    [" != ","all"],
    [" e ","pt-br"],
    [" > ","all"],
    [" < ","all"]
  ],
  "matematica": [
    [" multiplicado por ","pt-br"],
    [" dividido por ","pt-br"],
    [" multiplique ","pt-br"],
    [" elevado por ","pt-br"],
    [" elevado a ","pt-br"],
    [" elevado ","pt-br"],
    [" divide ","pt-br"],
    [" menos ","pt-br"],
    [" mais ","pt-br"],
    [" ** ","all"],
    [" - ","all"],
    [" * ","all"],
    [" % ","all"],
    [" / ","all"],
    [" + ","all"]
  ],
  "esperaEm": [
    [" milisegundos","pt-br"],
    [" milisegundo","pt-br"],
    [" segundos","pt-br"],
    [" segundo","pt-br"],
    [" ms","pt-br"],
    [" s","pt-br"]
  ],
  "passandoParametros": [
    [" passando parametros ","pt-br"],
    [" passando parametro ","pt-br"],
    [" parametros ","pt-br"],
    [" parametro ","pt-br"],
    [" passando ","pt-br"]
  ],
  "recebeParametros": [
    [" recebe parametros ","pt-br"]
  ],
  "declaraListas": [
    [" recebe ","pt-br"]
  ],
  "acesarListas": [
    [" na posicao ","pt-br"]
  ],
  "adicionarItensListas": [
    [" no inicio da lista de ","pt-br"],
    [" no inicio a lista de ","pt-br"],
    [" no final da lista de ","pt-br"],
    [" no final a lista de ","pt-br"],
    [" no inicio na lista ","pt-br"],
    [" no final na lista ","pt-br"],
    [" da lista de ","pt-br"],
    [" na posicao ","pt-br"],
    [" na lista de ","pt-br"],
    [" a lista de ","pt-br"],
    [" na lista ","pt-br"],
    [" a lista ","pt-br"]
  ],
  "RemoverItensListas": [
    [" da lista de ","pt-br"],
    [" da lista ","pt-br"]
  ],
  "tiverLista": [
    ["na lista de","pt-br"],
    ["na lista","pt-br"],
    ["em","pt-br"]
  ]
}
function strip(str) {
    return str.toString().replace(/^\s+|\s+$/g, '');
}

/* Coloração de palavras */
function colorirPalavra(regex, cor) 
{
    texto = document.getElementById('texto');

    textoFinal = texto.innerHTML;

    cor = cor['foreground'];

    console.log("Regex: ", regex);
    console.log("Cor  : ", cor);

    if (regex == "comentario"){
        console.log('Comentário');

    } else if (regex == "\"") {
        console.log('String');

    } else if (regex == "numerico"){
        console.log('Numérico');

    } else {
        console.log('Frase por si só');

    }

    texto.innerHTML = textoFinal;
}

function colorirCodigo(){
    
        for (i = 0; i < dic_com['declaraVariaveis'].length; i++){
            colorirPalavra(dic_com['declaraVariaveis'][i][0], cor_da_sintaxe["atribuicao"]);
        }

        for (i = 0; i < dic_com['declaraListas'].length; i++){
            colorirPalavra(dic_com['declaraListas'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['adicionarItensListas'].length; i++){
            colorirPalavra(dic_com['adicionarItensListas'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['tiverLista'].length; i++){
            colorirPalavra(dic_com['tiverLista'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['RemoverItensListas'].length; i++){
            colorirPalavra(dic_com['RemoverItensListas'][i][0], cor_da_sintaxe["logico"]);
        }

        for (i = 0; i < dic_com['tamanhoDaLista'].length; i++){
            colorirPalavra(dic_com['tamanhoDaLista'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['digitado'].length; i++){
            colorirPalavra(dic_com['digitado'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_com['loopsss'].length; i++){
            colorirPalavra(dic_com['loopsss'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['repita'].length; i++){
            colorirPalavra(dic_com['repita'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_com['se'].length; i++){
            colorirPalavra(dic_com['se'][i][0], cor_da_sintaxe["condicionais"]);
        }

        for (i = 0; i < dic_com['mostre'].length; i++){
            colorirPalavra(dic_com['mostre'][i][0], cor_da_sintaxe["exibicao"]);
        }

        for (i = 0; i < dic_com['mostreNessa'].length; i++){
            colorirPalavra(dic_com['mostreNessa'][i][0], cor_da_sintaxe["exibicao"]);
        }

        for (i = 0; i < dic_com['funcoes'].length; i++){
            colorirPalavra(dic_com['funcoes'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_com['aguarde'].length; i++){
            colorirPalavra(dic_com['aguarde'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_com['aleatorio'].length; i++){
            colorirPalavra(dic_com['aleatorio'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_com['limpatela'].length; i++){
            colorirPalavra(dic_com['limpatela'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_sub['passandoParametros'].length; i++){
            colorirPalavra(dic_sub['passandoParametros'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_sub['acesarListas'].length; i++){
            colorirPalavra(dic_sub['acesarListas'][i][0], cor_da_sintaxe["lista"]);
        }
        /* 

        for (i = 0; i < dic_sub['adicionarItensListas'].length; i++){
            colorirPalavra(dic_sub['adicionarItensListas'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_sub['RemoverItensListas'].length; i++){
            colorirPalavra(dic_sub['RemoverItensListas'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_sub['tiverLista'].length; i++){
            colorirPalavra(dic_sub['tiverLista'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_sub['recebeParametros'].length; i++){
            colorirPalavra(dic_sub['recebeParametros'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_sub['esperaEm'].length; i++){
            colorirPalavra(dic_sub['esperaEm'][i][0], cor_da_sintaxe["tempo"]);
        }

        for (i = 0; i < dic_sub['matematica'].length; i++){
            colorirPalavra(dic_sub['matematica'][i][0], cor_da_sintaxe["contas"]);
        }

        for (i = 0; i < dic_sub['repitaVezes'].length; i++){
            colorirPalavra(dic_sub['repitaVezes'][i][0], cor_da_sintaxe["lista"]);
        }

        for (i = 0; i < dic_sub['logico'].length; i++){
            colorirPalavra(dic_sub['logico'][i][0], cor_da_sintaxe["logico"]);
        }
        */

        colorirPalavra('numerico'     , cor_da_sintaxe["numerico"])
        colorirPalavra('"'            , cor_da_sintaxe["string"])
        colorirPalavra('comentario'   , cor_da_sintaxe["comentario"])

}
console.log('Javascript Carregado');
