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
import sap_connect as sap
import notebook_hwcode
#import odoo_hwinfo_byhand as odoo_hwinfo


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
    
    print("\n\nInforme o número da Ordem de Servico: ")
    var_os = input("Ordem: ")
    
    hw_os = sap.sistema(var_os)
    hw_name = sap.description(var_os)
    hw_code = notebook_hwcode.nb_code(hw_name)
    hw_screen = notebook_hwcode.nb_tela(hw_code)
    
    print(
        "Instalar %s no produto [%s] %s com tela de %s polegadas (SN=%s)." % (
            hw_os, hw_code, hw_name, hw_screen, serial_number
        )
    )

    # ### MO 16088


    if serial_number[:4] == "AVNB" and serial_number[-3:] == "000":
        color('red')
        print('\n\n\n\n\nNumero serial apenas para teste!\nNAO EXPEDIR!\n\n\n\n\n')
        time.sleep(99999)
        sys.exit(99)

    if str(hw_os) in ['Sem sistema operacional', 'Sem SO']:

        print("\n\n\nSem sistema operacional. Fim.\n\n\n")

       
        sys.exit(0)
    else:



        


        if str(hw_os) in ["Windows 10 HSL", "Windows 10 Home"]:
            print("Microsoft Windows 10 Home Single Language\n")
            msoa3_2.make_cfg(
                'KU9-00001',
                hw_code,
                serial_number,
                hw_screen,
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

        elif str(hw_os) in ["Windows 10 Pro", "Windows 10 PRO","Windows 10 Professional", "Virtuo"]:
            print("Microsoft Windows 10 Professional\n")
            
            msoa3_2.make_cfg(
                'FQC-08797',
                hw_code,
                serial_number,
                hw_screen,
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

####
        elif str(hw_os) in ["Windows 11 HSL", "Windows 11 Home"]:
            print("Microsoft Windows 11 Home Single Language\n")
            msoa3_2.make_cfg(
                'KU9-00130',
                hw_code,
                serial_number,
                hw_screen,
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

        elif str(hw_os) in ["Windows 11 PRO", "Windows 11 Professional"]:
            print("Microsoft Windows 11 Professional\n")
            
            msoa3_2.make_cfg(
                'FQC-10428',
                hw_code,
                serial_number,
                hw_screen,
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)


####


        else:
            print('Unknow Operating System')
            sys.exit(5)

        if hw_code[:3] == 'BON':
            command = 'z:\\scripts\\TFGTools\\Intel_BON\\AfuMfgWINx64.exe /A:x:\\' + serial_number + '.bin'
        else:
            command = 'z:\\scripts\lictool\\afuwinx64.exe /A:x:\\' + serial_number + '.bin'
        
        out_bin = subprocess.call(command)
        if out_bin == 0:
            print("AFU Writing OK!")
            command = 'z:\\scripts\\lictool\\oa3tool.exe /Report /ConfigFile=x:\\' + serial_number + '.cfg /LogTrace=x:\\' + serial_number + '.log'
            out_report = subprocess.call(command)
            print("OA3 + Report OK!")
            
    
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
