---
name: Report de bugs
about: Reporte um bug aos desenvolvedores
title: ''
labels: ''
assignees: ''

---

**Descreva o bug**
Quando executo um script com o comando de criar arquivo, ele cria o arquivo no caminho relativo ao interpretador ao invés da pasta onde o script está.

**Contexto**
Execução pelo Console. Quando executo pela interface gráfica funciona como esperado.

**Como reproduzir o bug?**
1. crie um arquivo chamado script.safira
2. Dentro dele, adicione o comando 'crie um arquivo chamado "teste.txt"'
3. Execute o comando pelo console. "safira script.safira"
3. Você verá que o arquivo teste.txt será criado dentro da pasta onde está o interpretador, ao invés da pasta onde estou executando o script

**Screenshots**
Não tenho nenhuma

**Informações do seu ambiente**
 - Windows 10
 - 64 bit
- Windows Power Shell

**Algo mais?**
O problema só acontece com esse comando
