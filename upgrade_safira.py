from AtualizarSafira import Upgrade
import os
from datetime import datetime
data = str(datetime.now()).split('.')[0]
data = data.replace(' ', '-')
data = data.replace(':', '-')


# Destino dos Downloads
dest_download = os.path.join(os.getcwd(), 'AtualizarSafira')
dest_backup = os.path.join(os.getcwd(), 'backups' , data)



up = Upgrade.Upgrade(dest_download, dest_backup)
dic_versoes = up.obter_informacoes_versao()

atualizar = up.baixar_versao(dic_versoes['10/11/2020'])
if atualizar[0]:
    resultado = up.aplicar_versao(dic_versoes['10/11/2020'])
    print(resultado)

print(atualizar[1])

