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
      "hw_nome": "Notebook Avell A52 MOB",
      "hw_code": "A52D115K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A55 MOB 1650",
      "hw_code": "A55D115B"
    },
    {
      "tela": "15.6",
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
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 MOB 3050 i7-11800H RTX 3050",
      "hw_code": "A70D117K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 MOB 3060",
      "hw_code": "A70D117H"
    },
    {
      "tela": "15.6",
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
      "hw_nome": "Notebook Avell C62 MOB",
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
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3050 Black 144 Hz BS",
      "hw_code": "A7BD127S"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 HYB i7-12700H RTX 3080 TI",
      "hw_code": "C65D127M"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 HYB i7-12700H RTX 3080",
      "hw_code": "C65D127J"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 HYB i9-12900H RTX 3080 TI",
      "hw_code": "C65D129M"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM TWO i7-12700H RTX 3060",
      "hw_code": "ST2D127H"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM TWO i7-12700H RTX 3070 TI",
      "hw_code": "ST2D127L"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A72 HYB i7-12700H RTX 3070 TI",
      "hw_code": "A72D127L"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3060",
      "hw_code": "A70D127H"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A70 HYB i7-12700H RTX 3050",
      "hw_code": "A70D127K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A55 HYB i5-12500H GTX 1650",
      "hw_code": "A55D125B"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A57 HYB i7-12700H GTX 1650",
      "hw_code": "A57D127B"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON LITE i5-1135G7 Iris XE 80",
      "hw_code": "BOLD125X"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON LITE i7-1165G7 Iris XE 96",
      "hw_code": "BOLD127X"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A52 HYB i5-12450H GTX 1650",
      "hw_code": "A52D125B"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell C65 LIV ULTIMATE i7-10875H RTX 3070",
      "hw_code": "A52D125B"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A52 ION i7-12650H RTX 4050 Black",
      "hw_code": "A52D127N"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell A70 ION i7-13700H RTX 4060 Grafite",
      "hw_code": "A70D137P"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell A72 ION i7-13700H RTX 4070 Grafite",
      "hw_code": "A72D137Q"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A52 HYB NEW i5-12450H RTX 3050 Black",
      "hw_code": "A52D125K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A52 HYB NEW i7-12650H RTX 3050 Black",
      "hw_code": "A52D127K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON LITE NEW i5-1235U Iris XE 80 Silver",
      "hw_code": "BOLB125U"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell B.ON LITE NEW i7-1255U Iris XE 96 Silver",
      "hw_code": "BOLB127U"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM GO i7-13700HX RTX 4060 Silver",
      "hw_code": "STGD137P"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM GO i7-13700HX RTX 4070 Silver",
      "hw_code": "STGD137Q"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM GO i7-13700HX RTX 4060 White",
      "hw_code": "GM6PX0Z"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM GO i7-13700HX RTX 4070 White",
      "hw_code": "GM6PX7Z"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM X i7-13700HX RTX 4080 Black",
      "hw_code": "STXD137R"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM X i9-13900HX RTX 4090 Black",
      "hw_code": "STXD139S"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM BS I5-12450H  RTX 3050 Black",
      "hw_code": "STBD125K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM BS I7-12650H RTX 3050 Black",
      "hw_code": "STBD127K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM BS i7-12650H RTX 4050 Black",
      "hw_code": "STBD127N"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell A65 ION",
      "hw_code": "A65D129P"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell A62 LIV",
      "hw_code": "A62D107B"
    },                                                         
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell HYB A52i i7-13620H RTX 3050 Black 165Hz",
      "hw_code": "A52iD137K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM 350 i7-13620H RTX 3050 Black 165Hz",
      "hw_code": "ST35D137K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell ION A52i i7-13620H RTX 4050 Black 165Hz",
      "hw_code": "A52iD137N"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM 450 i7-13620H RTX 4050 Black 165Hz",
      "hw_code": "ST45D137N"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell HYB A52r R7-7735HS RTX 3050 Black 165Hz",
      "hw_code": "A52rA777K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM 350r R7-7735HS RTX 3050 Black 165Hz",
      "hw_code": "ST35A777K"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell ION A52r R7-7735HS RTX 4050 Black 165Hz",
      "hw_code": "A52rA777N"
    },
    {
      "tela": "15.6",
      "hw_nome": "Notebook Avell STORM 450r R7-7735HS RTX 4050 Black 165Hz",
      "hw_code": "ST45A777N"
    },
    {
      "tela": "15.3",
      "hw_nome": "Notebook Avell ION A70i i9-14900HX RTX 4060 White 120Hz",
      "hw_code": "A70iD149P"
    },
    {
      "tela": "15.3",
      "hw_nome": "Notebook Avell ION A70i i7-14650HX RTX 4060 White 120Hz",
      "hw_code": "A70iD147P"
    },
    {
      "tela": "14",
      "hw_nome": "Notebook Avell B.ON Smart Ultra 7 155H Arc Graphics Silver/Black 120Hz",
      "hw_code": "BOSMLU7V"
    },
    {
      "tela": "14",
      "hw_nome": "Notebook Avell B.ON 145 i5-1235U Iris Xe Graphics Gray 60Hz",
      "hw_code": "B145B125X"
    },
    {
      "tela": "14",
      "hw_nome": "Notebook Avell B.ON 147 i7-1255U Iris Xe Graphics Gray 60Hz",
      "hw_code": "B147B127X"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell B.ON 165 i5-1235U Iris Xe Graphics Gray 60Hz",
      "hw_code": "B165B125X"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell B.ON 167 i7-1255U Iris Xe Graphics Gray 60Hz",
      "hw_code": "B167B127X"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM 460 i9-14900HX RTX 4060",
      "hw_code": "ST46D149P"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM 460 i7-14650HX RTX 4060",
      "hw_code": "ST46D147P"
    },
    {
      "tela": "16",
      "hw_nome": "Notebook Avell STORM 470 i9-14900HX RTX 4070",
      "hw_code": "ST47D149Q"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM 480 i9-14900HX RTX 4080 Black 240Hz",
      "hw_code": "ST48D149R"
    },
    {
      "tela": "17",
      "hw_nome": "Notebook Avell STORM 490 i9-14900HX RTX 4090 Black 240Hz",
      "hw_code": "ST49D149S"
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
