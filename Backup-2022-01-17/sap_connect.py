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
    urllib3.disable_warnings()
    aaa = session.post(url,data)
    #session = requests.Session()
    #session.verify = False
    return aaa


def description(var_os):
    #url2 = "https://177.85.33.53:50579/b1s/v1/Orders(%s)?$select=DocumentLines" % var_os # Passa por parametros a ordem de venda para buscar a descrição do computador. Usar a mesma para tirar o sistema e o modelo do notebook
    url2 = "https://177.85.33.53:50579/b1s/v1/OBJ_SERVICO(%s)" % var_os
    
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    return db.get('U_TituOSEmp')
    #t1 = db.get('value')
    #t1 = json.dumps(t1) # Usada para transformar a Json e um dicionario
    #t1=t1[1:-1] # Usada para retirar o primeiro e ultimo caracter
    #t1 = json.loads(t1) # Volta a ser um Json
    #for n in t1['DocumentLines']:
        #return (n.get('ItemDescription'))
    

def serial(var_os):
    url2 = "https://177.85.33.53:50579/b1s/v1/OBJ_SERVICO(%s)" % var_os # Passa por parametros a ordem de venda para buscar o Numero de série na tabela OBJ_SERVICO
    bbb = session.get(url2)
    db = json.loads(bbb.text)
    for n in db['OBJ_SERVICO_5Collection']:
        return (n.get('U_Rastreio'))


def sistema(var_os):
    var_sis = description(var_os)
    var_10h = ['Windows 10 Home Single Language', 'Windows 10 HSL']
    var_10p = ['Windows 10 Professional', 'Windows 10 PRO','Windows 10 Pro']
    var_11h = ['Windows 11 Home Single Language', 'Windows 11 HSL']
    var_11p = ['Windows 11 Professional', 'Windows 11 PRO','Windows 11 Pro']
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