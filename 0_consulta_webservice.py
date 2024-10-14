import os
import re
import requests
import json

import os
import re
import requests
import json
from datetime import datetime

def consultar_webservice(op_number):
    url = f"http://avell.ramo.com.br:8089/?token=ZJBIx0ML8zf9xML5d4fjnRzZGToe538UDAep0q2yfYxSk9OE3togCd5IyjmsdlEh&query=ConsultaOP({op_number})"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        resultado_formatado = []
        for item in data:
            op = item.get('OP', 'N/A')
            nomeproduto = item.get('NOMEPRODUTO', 'N/A')
            pedido = item.get('PEDIDO', 'N/A')
            linha_pedido = item.get('LINHA_PEDIDO', 'N/A')
            serial = item.get('SERIAL', 'N/A')
            cd_mem = item.get('CD_MEM', 'N/A')
            nome_mem = item.get('NOME_MEM', 'N/A')
            cod_ssd1 = item.get('COD_SSD1', 'N/D') if item.get('COD_SSD1') else 'N/D'
            nome_ssd1 = item.get('NOME_SSD1', 'N/D') if item.get('NOME_SSD1') else 'N/D'
            cod_ssd2 = item.get('COD_SSD2', 'N/D') if item.get('COD_SSD2') else 'N/D'
            nome_ssd2 = item.get('NOME_SSD2', 'N/D') if item.get('NOME_SSD2') else 'N/D'
            so_pedido = item.get('SO_PEDIDO', 'N/A')
            so_instalacao = item.get('SO_INSTALACAO', 'N/A')

            # Obter a hora atual
            hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            resultado_formatado.append(f"\n \n Pedido: {pedido}\n \n Ordem de Produção: {op}\n \n Descrição: {nomeproduto}\n \n Serial: {serial}\n \n Sistema Operacional: {so_pedido}\n \n Chave de Ativação: {so_instalacao}\n \n")

        return resultado_formatado
    else:
        print(f"Erro na solicitação ao webservice. Código de status: {response.status_code}")

# Pedir ao usuário o número da OP
op_number = input("Por favor, insira o número da OP: ")

# Realizar a consulta ao webservice com o número da OP fornecido pelo usuário
resultado_consulta = consultar_webservice(op_number)

# Imprimir o resultado da consulta
if resultado_consulta:
    for item in resultado_consulta:
        print(item)
        print()  # Adiciona uma linha em branco após cada resultado
else:
    print("Erro ao consultar o webservice.")
