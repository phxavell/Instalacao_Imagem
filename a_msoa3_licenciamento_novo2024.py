'''Document this'''


import os
import sys
# import pywintypes
import subprocess
import time
# import win32com.client
import av_art
import msoa3_2
import notebook_hwinfo
import odoo_hwinfo
import a_sap_connect23new as sap
import notebook_hwcode2024
import copia_cbr_log
from consulta_webservice import consultar_webservice



#import odoo_hwinfo_byhand as odoo_hwinfo

import shutil#Copiar arquivos


def color(colorname):
    colorcode = 0

    if colorname == 'green':
        colorcode = '02'
    elif colorname == 'yellow':
        colorcode = '06'
    elif colorname == 'red':
        colorcode = '04'
    elif colorname == 'red-reverse':
        colorcode = '40'
    else:
        colorcode = '07'

    colorful = lambda: os.system(
        'color ' + str(colorcode)
    )  # on Windows System

    colorful()


def main():
    '''Default function'''

    sap.connect()
    # Forcar mensagem ao montador para conectar
    # fonte de energia externa.
    while not notebook_hwinfo.battery_status():
        color('red')
        print("Ligar a fonte de alimentacao!!!\n\n")
        time.sleep(0.75)

    color('green')

    serial_number = str(notebook_hwinfo.get_serialnumber()['SerialNumber'])

    var_os = str(notebook_hwinfo.get_os()['SerialNumber'])
    
    hw_os = sap.sistema(var_os)
    hw_name = sap.description(var_os)
    hw_code = notebook_hwcode2024.nb_code(hw_name)
    hw_screen = notebook_hwcode2024.nb_tela(hw_code)
    
    print(
        "Instalar %s no produto [%s] %s com tela de %s polegadas (SN=%s)." % (
            hw_os, hw_code, hw_name, hw_screen, serial_number
        )
    )

    # ### MO 16088
    
    # Chamando a função para obter os dados
    hw_os = consultar_webservice()

    # Atribuindo o resultado de 'so_instalacao' a uma variável para facilitar o uso
    sistema_operacional = hw_os['so_instalacao']

    
    if sistema_operacional in ['Sem Sistema', 'Sem SO']:
        print("\n\n\nSem sistema operacional. Fim.\n\n\n")
    
        sys.exit(0)
    else:
        

    #### INSTALA O WINDOWS HOME STANDARD SINGLE LANGUAGE - KU9-00130 



        if sistema_operacional in ["WIN Home Standard SL"]:
            
            print("Microsoft Windows 11 Home Standard Single Language\n")
            msoa3_2.make_cfg(
                'KU9-00130',
                hw_code,
                serial_number,
                hw_screen,
                'c:\\' + serial_number + '.cfg'
            )
            

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=c:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)
            
            
            
#######################################################################################################################################################            
            
            
    ### INSTALA O WINDOWS HOME PLUS SINGLE LANGUAGE - NA3-00013 

    
            
        elif sistema_operacional in ["WIN Home Plus SL"]:
            
            print("Microsoft Windows 11 Home Plus Single Language\n")
            msoa3_2.make_cfg(
                'NA3-00013',
                hw_code,
                serial_number,
                hw_screen,
                'c:\\' + serial_number + '.cfg'
            )
           
            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=c:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)
            


#######################################################################################################################################################            
            
            
    ### INSTALA O WINDOWS HOME ADVANCED - KUK-00003  


        elif sistema_operacional in ["WIN Home Advanced SL"]:
        
            print("Microsoft Windows 11 Home Advanced\n")
            msoa3_2.make_cfg(
                'KWV-00003',
                hw_code,
                serial_number,
                hw_screen,
                'c:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=c:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)



#######################################################################################################################################################            
            
            
    ### INSTALA O WINDOWS PRO STANDARD - FQC-10428   /// VIRTUO

       
        elif sistema_operacional in ["WIN Pro Standard", "Virtuo"]:
            print("Microsoft Windows 11 PRO Standard\n")
            
            msoa3_2.make_cfg(
                'FQC-10428',
                hw_code,
                serial_number,
                hw_screen,
                'c:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=c:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

#######################################################################################################################################################################################


    ### INSTALA O WINDOWS PRO HIGH-END - MUP-00005



        elif sistema_operacional in ["WIN Pro High-End"]:
            
            
            print("Microsoft Windows 11 Pro High-end\n")
            msoa3_2.make_cfg(
                'MUP-00005',
                hw_code,
                serial_number,
                hw_screen,
                'c:\\' + serial_number + '.cfg'
            )
           
            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=c:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)
            
            
            
    
    
        else:
            print('Unknow Operating System')
            sys.exit(5)
        print("DEBUG IS ON")
        if hw_code[:3] == 'BOL':
            command = 'z:\\scripts\\clevo2\\H2OOAE-Wx64.exe -W c:\\' + serial_number + '.bin -S'
        elif hw_code[:3] == 'BON':        
            command = 'z:\\scripts\\TFGTools\\Intel_BON\\AfuMfgWINx64.exe /A:c:\\' + serial_number + '.bin'
        elif hw_code[:3] == 'A55':
            command = 'z:\\scripts\\clevo2\\H2OOAE-Wx64.exe -W c:\\' + serial_number + '.bin -S'
            #command = 'z:\\scripts\insyde\\H2OOAE-Wx64.exe -W c:\\' + serial_number + '.bin -S'
        elif hw_code[:3] == 'A57':
            command = 'z:\\scripts\\clevo2\\H2OOAE-Wx64.exe -W c:\\' + serial_number + '.bin -S'
            #command = 'z:\\scripts\insyde\\H2OOAE-Wx64.exe -W c:\\' + serial_number + '.bin -S'
        
        else:
            command = 'c:\\TESTES_AVELL\\.executaveisAux\\AFUWINx64.exe /A:c:\\' + serial_number + '.bin'
        print("DEBUG COMMAND: " + command)
        out_bin = subprocess.call(command)
        if out_bin == 0:
            print("AFU Writing OK!")
            command = 'z:\\scripts\\lictool\\oa3tool.exe /Report /ConfigFile=c:\\' + serial_number + '.cfg /LogTrace=c:\\' + serial_number + '.log'
            out_report = subprocess.call(command)

            print("OA3 + Report OK!")
            
            copia_cbr_log.copiar_arquivos()
    
            if out_report == 0:
                print("OA3 + AFU Completed!")

                command = 'z:\\scripts\lictool\\oa3tool.exe /Validate'
                out_validate = subprocess.call(command)
                if out_validate == 0:
                    print('OA3 + Validate OK!')

                    av_art.art_finished()

                else:
                    print('OA3 + Validate FAIL')
                    sys.exit(5)

        else:
            print("FAIL: AFU Process")
        
        
        
if __name__ == '__main__':
    main()
