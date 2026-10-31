## Comando de condições  
Este comando testa se uma ou mais condições são verdadeiras, a primeira condição que for verdadeira, será executada, as demais serão ignoradas, mesmo que também sejam verdadeiras.
```
# Variável texto com o valor de "cadastrar"
escolha = "cadastrar"

se escolha for igual a "cadastrar" entao
{
    mostre "Cadastramento de clientes iniciado!"
}
senao se escolha for igual a "visualizar" ou escolha for igual a "editar" entao
{
    mostre "Abrindo sistema de visualização e edição"
}
senao 
{
    mostre "Por favor, escolha uma opção válida!"
}

```

O "senao se" e o "senao" não são obrigatórios, você pode usa-los ou não.
