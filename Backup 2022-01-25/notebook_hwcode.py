import json
import time


database = '''
{
  "av_system": "Avell Pass Antigo CODE",
  "av_version": 1,
  "av_lastchange": "2022-01-17T00:00:00.000Z",
  "notebooks": [
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A52 MOB 3050",
      "hw_code": "A52D115K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A65 MOB 3060",
      "hw_code": "A65D117H"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A65 MOB 3070",
      "hw_code": "A65D117I"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 MOB 3050",
      "hw_code": "A70D117K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 MOB 3060",
      "hw_code": "A70D117H"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B11 MOB 3050",
      "hw_code": "B11D117K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB 3050",
      "hw_code": "C62D117K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB 3050",
      "hw_code": "C62D115K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB 3060",
      "hw_code": "C62D117H"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 MOB 3070",
      "hw_code": "C65D117I"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 MOB 3080",
      "hw_code": "C65D119J"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 MOB 3080",
      "hw_code": "C65D117J"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON i5-1135G7",
      "hw_code": "BOND115X"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON i7-1165G7",
      "hw_code": "BOND117X"
    }
    
  ]
}
'''


db = json.loads(database)



def nb_code(var_Desc):
    for nb in db['notebooks']:
        if nb.get('hw_nome') in var_Desc:
            return nb.get('hw_code')
            

def nb_tela(var_code):
    for nb in db['notebooks']:
        if nb.get('hw_code') == var_code[:8]:
            return nb.get('tela') 
