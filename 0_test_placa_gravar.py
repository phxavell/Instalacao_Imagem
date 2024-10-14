import sap_config23new as sap
import requests
import urllib3
import json

# Desabilita os avisos de permissão HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cria uma sessão global
session = requests.Session()
session.verify = False

def connect():
    data = '''{"CompanyDB": "%s", "UserName": "%s", "Password": "%s"}''' % (sap.COMPANYDB, sap.USERNAME, sap.PASSWORD)
    url = sap.URL
    response = session.post(url, data)
    return response

# Conectar à API
connection_response = connect()
if connection_response.status_code != 200:
    print("Erro ao conectar:", connection_response.status_code)
    print(connection_response.text)
else:
    print("Conexão bem-sucedida!")

    # Solicite ao usuário que insira o valor de U_AV_NR_SERIE
    u_av_nr_serie = input("Digite o valor de U_AV_NR_SERIE: ")

    # Defina a URL base e o filtro
    base_url = "https://avell.ramo.com.br:50000/b1s/v1/ProductionOrders"
    query = f"?$filter=U_AV_NR_SERIE eq '{u_av_nr_serie}'"
    url = base_url + query

    # Faça a solicitação GET à API
    response = session.get(url)

    # Verifique a resposta
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
