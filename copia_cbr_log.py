import os
import subprocess
import shutil

def copiar_arquivos():
    # Diretório onde os arquivos estão localizados
    diretorio_origem = 'C:\\'










    # Diretório de destino onde você deseja criar a pasta
    diretorio_destino_base = 'Z:\\CBR'

    for filename in os.listdir(diretorio_origem):
        if filename.startswith('AVNB'):
            # Remove a extensão do nome do arquivo para criar o diretório
            nome_pasta = os.path.splitext(filename)[0]
            diretorio_destino = os.path.join(diretorio_destino_base, nome_pasta)

            # Cria a pasta de destino com base no nome do arquivo (sem extensão)
            os.makedirs(diretorio_destino, exist_ok=True)

            origem_arquivo = os.path.join(diretorio_origem, filename)
            destino_arquivo = os.path.join(diretorio_destino, filename)

            # Copia o arquivo para a pasta de destino
            shutil.copy(origem_arquivo, destino_arquivo)

    # Exclui o arquivo temporário (se existir)
    temp_serial_file = 'temp_serial.txt'
    if os.path.exists(temp_serial_file):
        os.remove(temp_serial_file)

# A função copiar_arquivos não será executada automaticamente,
# você precisa chamá-la explicitamente quando desejar executar a lógica.
