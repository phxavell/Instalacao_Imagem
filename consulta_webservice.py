import os
import re
import requests
import json

def consultar_webservice():
    os.chdir("C:/")

    arquivos = os.listdir('.')
    arquivos_op = [arq for arq in arquivos if arq.startswith('AVNB')]

    if arquivos_op:
        nome_arquivo = arquivos_op[0]
        with open(nome_arquivo, 'r') as file:
            content = file.read()
            match = re.search(r'OP:\s*(\d+)', content)
        
            if match:
                op_number = match.group(1)
            else:
                print("Número da OP não encontrado no arquivo.")
                exit(1)
    else:
        print("Nenhum arquivo com o padrão 'AVNB' encontrado.")
        op_number = input("Por favor, insira o número da OP: ")

    url = f"http://avell.ramo.com.br:8089/?token=ZJBIx0ML8zf9xML5d4fjnRzZGToe538UDAep0q2yfYxSk9OE3togCd5IyjmsdlEh&query=ConsultaOP({op_number})"

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        for item in data:
            op = item.get('OP', 'N/A')
            nomeproduto = item.get('NOMEPRODUTO', 'N/A')
            pedido = item.get('PEDIDO', 'N/A')
            linha_pedido = item.get('LINHA_PEDIDO', 'N/A')
            serial = item.get('SERIAL', 'N/A')
            cd_mem = item.get('CD_MEM', 'N/A')
            nome_mem = item.get('NOME_MEM', 'N/A')
            cod_ssd1 = item.get('COD_SSD1', 'N/A')
            nome_ssd1 = item.get('NOME_SSD1', 'N/A')
            cod_ssd2 = item.get('COD_SSD2', 'N/A')
            nome_ssd2 = item.get('NOME_SSD2', 'N/A')
            so_pedido = item.get('SO_PEDIDO', 'N/A')
            so_instalacao = item.get('SO_INSTALACAO', 'N/A')
            
        return {
            'op': op,
            'nomeproduto': nomeproduto,
            'pedido': pedido,
            'linha_pedido': linha_pedido,
            'serial': serial,
            'cd_mem': cd_mem,
            'nome_mem': nome_mem,
            'cod_ssd1': cod_ssd1,
            'nome_ssd1': nome_ssd1,
            'cod_ssd2': cod_ssd2,
            'nome_ssd2': nome_ssd2,
            'so_pedido': so_pedido,
            'so_instalacao': so_instalacao
        }
    else:
        print(f"Erro na solicitação ao webservice. Código de status: {response.status_code}")
