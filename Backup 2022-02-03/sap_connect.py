import sap_config as sap
import time
import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import json

global session
session = requests.Session()
session.verify = False

def connect():

    data = '''{"CompanyDB": "%s", "UserName": "%s", "Password": "%s"}''' % (sap.COMPANYDB, sap.USERNAME, sap.PASSWORD)
    url=sap.URL
    urllib3.disable_warnings() #Desabilita os avisos de permissão HTTPS
    aaa = session.post(url,data) #Da um Post com o as informações do banco para conexão com a API
    return aaa


def description(var_os):
    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://177.85.33.53:50579/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2) # Dá um get para buscar as informações solicitadas na URL
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['ItemDescription']
        i+=1
    
    
def cod_item(var_ped):
    url2 = "https://177.85.33.53:50579/b1s/v1/OBJ_SERVICO(%s)" % var_ped #Passa o numero da OS como parametro para retornar o numero do pedido
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    return db.get('U_ProdItemCod') # Retorna o codigo do ITEM



def pedido(var_ped):
    url2 = "https://177.85.33.53:50579/b1s/v1/OBJ_SERVICO(%s)" % var_ped #Passa o numero da OS como parametro para retornar o numero do pedido
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    return db.get('U_PedVend') # Retorna o numero do pedido

    
def sis(var_os):
    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://177.85.33.53:50579/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['U_AVELL_SO'] # Retorna se o sistema é Virtuo ou não
        i+=1



def virtuo(var_os):
    pd = pedido(var_os) # Adiciona o numero do pedido a uma variavel
    coditem = cod_item(var_os)
    url2 = "https://177.85.33.53:50579/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    i=0
    for n in bbb_dic['DocumentLines']:
        if (bbb_dic['DocumentLines'][i]['ItemCode'] == coditem):
            return bbb_dic['DocumentLines'][i]['U_AVELL_SIS_Virtuo'] # Retorna se o sistema é Virtuo ou não
        i+=1
    
    

def serial(var_os):
    url2 = "https://177.85.33.53:50579/b1s/v1/OBJ_SERVICO(%s)" % var_os # Passa por parametros a ordem de venda para buscar o Numero de série na tabela OBJ_SERVICO
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    for n in db['OBJ_SERVICO_5Collection']:
        return (n.get('U_Rastreio'))


def sistema(var_os):
    pd = pedido(var_os)
    url2 = "https://177.85.33.53:50579/b1s/v1/Orders(%s)?$select=DocumentLines" % pd # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    bbb = session.get(url2)
    bbb_dic = bbb.json()
    var_sis = sis(var_os)
    #Faz a verificação de qual sistema será instalado
    var_10h = ['Windows 10 Home Single Language', 'Windows 10 HSL']
    var_10p = ['Windows 10 Professional', 'Windows 10 PRO','Windows 10 Pro']
    var_11h = ['Windows 11 Home Single Language', 'Windows 11 HSL']
    var_11p = ['Windows 11 Professional', 'Windows 11 PRO','Windows 11 Pro']
    vir = virtuo(var_os)
    if vir:
        return("Virtuo") # Se for um virtuo, é feito o retorno antecipado, não indo para as proximas linhas
        
    for n in var_10h:
        if n in var_sis:
            return ("Windows 10 HSL")
    for n in var_10p:
        if n in var_sis:
            return ("Windows 10 PRO")
    for n in var_11h:
        if n in var_sis:
            return ("Windows 11 HSL")
    for n in var_11p:
        if n in var_sis:
            return ("Windows 11 PRO")
    
    else: return ("SEM SO")