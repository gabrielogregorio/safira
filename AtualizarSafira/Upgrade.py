import requests
import zipfile
import shutil
import os
import io
import re

class Upgrade:
    def __init__(self, dest_download, dest_backup):
        """ Realiza a atualização de uma versão da safira"""

        self.dest_download = dest_download
        self.dest_backup = dest_backup
        self.msg = ""

    def obter_informacoes_versao(self):
        """Obtém as versões oficiais da safira"""
        dic_versoes = {}

        # Obter versões
        try:
            r = requests.get('https://raw.githubusercontent.com/safira-lang/upgrades/main/upgrades.json', timeout=15)
            r.json()
        except Exception as erro:
            return {"erro":str(erro)}

        if r.status_code != 200:
            return {"erro":'Resposta esperada era 200. Resposta: {}'.format(r.status_code)}
        return r.json()

    def baixar_versao(self, version):
        """Realiza o download de uma versão, salvando um .zip"""

        zip_url = 'https://github.com/safira-lang/safira-ide/archive/{}.zip'.format(version)
        print('url download "{}"'.format(zip_url))

        r = requests.get(zip_url, stream=True)
        print('resposta: ', r.status_code)

        # Se deu resposta ok
        if r.status_code != 200:
            return [False, "Erro ao baixar versão: " + str(r.status_code), '']

        return [True, "Versão baixada com sucesso", r]


    def extrair_versao(self, r):
        """ Extrai os arquivos baixados em uma pasta """

        try:
            # Carregar o zip
            z = zipfile.ZipFile(io.BytesIO(r.content))

            # Extração no diretório atual
            z.extractall(self.dest_download)
        except Exception as erro:
            return [False, 'Erro ao extrair arquivos da nova versão: ', erro]

        return [True, 'Arquivo Extraido com sucesso!']


    def listar_arquivos2(self, alvo):
        """Lista os arquivos de um diretório para o backup"""

        lista_arquivos = []
        for folder, _, file in os.walk(alvo):
            for f in file:

                # Arquivo a ser movido
                arquivo = os.path.join(folder, f)

                
                # Não atualizar o arquivo de atualização
                if 'Upgrade' in arquivo or 'backups/' in arquivo or '.git/' in arquivo or 'github/ISSUE_TEMPLATE' in arquivo or '__pycache__' in arquivo:
                    #print("Arquivo update ignorado")
                    continue

                lista_arquivos.append(arquivo)
        return lista_arquivos

    def fazer_backup_versao(self):
        """Faz uma cópia dos arquivos em um diretório de backups"""

        lista_arquivos = self.listar_arquivos2('.')

        for arquivo_origem in lista_arquivos:
            arquivo_origem = arquivo_origem.strip('/')
            # Obter o diretório anterior ../
            regx2 = '(.{1,})\\/.*$'

            destino_final_file = self.dest_backup
            destino_final_arquivo = os.path.join(destino_final_file, arquivo_origem)

            ultimo_diretorio_destino = re.search(regx2, destino_final_arquivo).group(1)

            # Se o diretório não existe, crie-o
            if not os.path.exists(ultimo_diretorio_destino):
                print('[cria] ', ultimo_diretorio_destino)

                # Cria os diretórios e subdiretórios
                os.makedirs(ultimo_diretorio_destino)
            else:
                print('[exis] ', ultimo_diretorio_destino)


            try:
                print('[de  ] ', arquivo_origem)
                print('[para] ', destino_final_arquivo)
                # Tenta copiar o arquivo para o destino
                shutil.copy(arquivo_origem, destino_final_arquivo)
            except Exception as erro:
                return [False, "Erro ao copiar arquivo: " + erro + 'Arquivo' + arquivo_origem + 'destino' + destino_final_arquivo]

        return [True, ""]


    def restaurar_versao(self):
        return [True, ""]

    def atualizar_arquivos(self, versao):
        """ Pega os arquivos baixados de uma versão e sobrescreve os arquivos
        da versão atualmente em execução """

        destino_upgrade = os.path.join(self.dest_download, 'safira-ide-{}/'.format(versao))

        lista_arquivos = self.listar_arquivos(destino_upgrade, versao)

        for arquivo in lista_arquivos:
            arquivo = arquivo.strip('/')

            # Obter o diretório anterior ../
            regx2 = '(.{1,})\\/.*$'

            destino_1 = re.search(regx2, str(self.dest_download)).group(1)

            destino_final = os.path.join(destino_1, arquivo)
            local_arquivo_enviar = os.path.join(destino_upgrade, arquivo)

            ultimo_diretorio_destino = re.search(regx2, destino_final).group(1)

            # Se o diretório não existe, crie-o
            if not os.path.exists(ultimo_diretorio_destino):
                print('[cria] ', ultimo_diretorio_destino)

                # Cria os diretórios e subdiretórios
                os.makedirs(ultimo_diretorio_destino)
            else:
                print('[exis] ', ultimo_diretorio_destino)

            try:
                print('[de  ] ', local_arquivo_enviar)
                print('[para] ', destino_final)
                # Tenta copiar o arquivo para o destino
                shutil.copy(local_arquivo_enviar, destino_final)
            except Exception as erro:
                return [False, "Erro ao copiar arquivo: " + erro + 'Arquivo' + local_arquivo_enviar + 'destino' + destino_final]
        return [True, ""]

    def listar_arquivos(self, alvo, versao):
        """Lista os arquivos de um diretório baixado"""

        # Futuramente vamos unificar as funções, tem muito código duplicado
        lista_arquivos = []
        for folder, _, file in os.walk(alvo):
            for f in file:

                # Arquivo a ser movido
                arquivo = os.path.join(folder, f)

                # Não atualizar o arquivo de atualização
                if 'Upgrade' in arquivo or 'backups/' in arquivo or arquivo.startswith('safira'):
                    print("Arquivo update ignorado")
                    continue

                arquivo = arquivo.split('safira-ide-{}'.format(versao))[1]

                lista_arquivos.append(arquivo)
        return lista_arquivos

