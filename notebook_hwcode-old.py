import json
import time


database = '''
{
  "av_system": "Avell Pass Antigo CODE",
  "av_version": 1,
  "av_lastchange": "2022-01-17T00:00:00.000Z",
  "notebooks": [
    {
      "tela": "15.6 - 144Hz",
      "hw_nome": "Notebook Avell A52 MOB",
      "hw_code": "A52D115K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A55 MOB 1650",
      "hw_code": "A55D115B"
    },
    {
      "tela": "15.6 - 144Hz",
      "hw_nome": "Notebook Avell A57 MOB",
      "hw_code": "A57D117B"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A65 MOB 3060 i7-11800H RTX 3060" ,
      "hw_code": "A65D117H"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A65 MOB 3070",
      "hw_code": "A65D117I"
    },
    {
      "tela": "15.6 - 144Hz",
      "hw_nome": "Notebook Avell A70 MOB 3050 i7-11800H RTX 3050",
      "hw_code": "A70D117K"
    },
    {
      "tela": "15.6 - 165Hz",
      "hw_nome": "Notebook Avell A70 MOB 3060",
      "hw_code": "A70D117H"
    },
    {
      "tela": "15.6 - 165Hz",
      "hw_nome": "Notebook Avell A70 MOB i7-11800H",
      "hw_code": "A70D117H"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B11 MOB 3050 i7-11370H RTX 3050",
      "hw_code": "B11D117K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB i7-11800H RTX 3050",
      "hw_code": "C62D117K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB 3050",
      "hw_code": "C62D115K"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C62 MOB i7-11800H RTX 3060",
      "hw_code": "C62D117H"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 3070 MOB i7-11800H RTX 3070",
      "hw_code": "C65D117I"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 MOB 3080",
      "hw_code": "C65D119J"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 MOB 3080 i7-11800H RTX 3080",
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
    },
    {
      "tela": "15 - 144Hz",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3050 Black 144 Hz BS",
      "hw_code": "A7BD127S"
    },
    {
      "tela": "17 - 240Hz",
      "hw_nome": "Notebook Avell C65 HYB i7-12700H RTX 3080 TI",
      "hw_code": "C65D127M"
    },
    {
      "tela": "17 - 240Hz",
      "hw_nome": "Notebook Avell C65 HYB i7-12700H RTX 3080",
      "hw_code": "C65D127J"
    },
    {
      "tela": "17 - 240Hz",
      "hw_nome": "Notebook Avell C65 HYB i9-12900H RTX 3080 TI",
      "hw_code": "C65D129M"
    },
    {
      "tela": "17 - 165Hz",
      "hw_nome": "Notebook Avell STORM TWO i7-12700H RTX 3060",
      "hw_code": "ST2D127H"
    },
    {
      "tela": "17 - 240Hz",
      "hw_nome": "Notebook Avell STORM TWO i7-12700H RTX 3070 TI",
      "hw_code": "ST2D127L"
    },
    {
      "tela": "15 - 240Hz",
      "hw_nome": "Notebook Avell A72 HYB i7-12700H RTX 3070 TI",
      "hw_code": "A72D127L"
    },
    {
      "tela": "15 - 165Hz",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3060",
      "hw_code": "A70D127H"
    },
    {
      "tela": "15 - 144Hz",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3050",
      "hw_code": "A70D127K"
    },
    {
      "tela": "15 - 144Hz",
      "hw_nome": "Notebook Avell A55 HYB i5-12500H GTX 1650",
      "hw_code": "A55D125B"
    },
    {
      "tela": "15 - 144Hz",
      "hw_nome": "Notebook Avell A57 HYB i7-12700H GTX 1650",
      "hw_code": "A57D127B"
    },
    {
      "tela": "15 - 60Hz",
      "hw_nome": "Notebook Avell B.ON LITE i5-1135G7 Iris XE 80",
      "hw_code": "BOLD125X"
    },
    {
      "tela": "15 - 60Hz",
      "hw_nome": "Notebook Avell B.ON LITE i7-1165G7 Iris XE 96",
      "hw_code": "BOLD127X"
    },
    {
      "tela": "15 - 144Hz",
      "hw_nome": "Notebook Avell A52 HYB i5-12450H GTX 1650",
      "hw_code": "A52D125B"
    },
    {
      "tela": "17 - 165Hz",
      "hw_nome": "Notebook Avell C65 LIV ULTIMATE i7-10875H RTX 3070",
      "hw_code": "A52D125B"
    },
    {
      "tela": "15.6 Display FHD 1920x1080 - 60Hz",
      "hw_nome": "Notebook Avell B.ON LITE NEW i5-1235U Iris XE 80 Silver",
      "hw_code": "BOLB125T"
    },
    {
      "tela": "15.6 Display FHD 1920x1080 - 60Hz",
      "hw_nome": "Notebook Avell B.ON LITE NEW i7-1255U Iris XE 96 Silver",
      "hw_code": "BOLB127U"
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
