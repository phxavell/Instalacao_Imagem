'''Document this'''


import os
import sys
# import pywintypes
import subprocess
import time
# import win32com.client
import av_art
import msoa3_2_new
#import notebook_hwinfo
#import odoo_hwinfo
#import sap_connect as sap
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

    #sap.connect()
    # Forcar mensagem ao montador para conectar
    # fonte de energia externa.
#    while not notebook_hwinfo.battery_status():
#        color('red')
#        print("Ligar a fonte de alimentacao!!!\n\n")
#        time.sleep(0.75)

    color('green')


    print('\n\nInsira a Versão do Sistema para continuar: \n\n')
    print('10 HSL')
    print('10 PRO')
    print('11 HSL')
    print('11 PRO')

    hw_os = input("Sistema: ")
    
    print('\n\nInsira o Numero de Serie para continuar: \n\n')
    serial_number = input("Serie: ")
    # ### MO 16088


    if str(hw_os) in ['Sem sistema operacional', 'Sem SO']:

        print("\n\n\nSem sistema operacional. Fim.\n\n\n")

       
        sys.exit(0)
    else:



        if str(hw_os) in ["10 HSL", "10 hsl"]:
            
            print("Microsoft Windows 10 Home Single Language\n")
            msoa3_2_new.make_cfg(
                'FQC-05607',
                'Avell',
                serial_number,
                '15,6',
                'x:\\' + serial_number + '.cfg'
            )
            
            command = 'z:\\scripts\\lictool\\oa3tool-old.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)
            
        elif str(hw_os) in ["10 PRO", "10 pro"]:

            
            print("Microsoft Windows 10 Professional\n")
            
            msoa3_2_new.make_cfg(
                'FQC-05607',
                'Avell',
                serial_number,
                '15,6',
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool-old.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

        elif str(hw_os) in ["11 HSL", "11 hsl"]:
            print("Microsoft Windows 11 Home Single Language\n")
            msoa3_2_new.make_cfg(
                'FQC-05607',
                'Avell',
                serial_number,
                '15,6',
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool-old.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_home = subprocess.call(command)
            if out_home == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)

        elif str(hw_os) in ["11 PRO", "11 pro"]:
            print("Microsoft Windows 11 Professional\n")
            
            msoa3_2_new.make_cfg(
                'FQC-05607',
                'Avell',
                serial_number,
                '15,6',
                'x:\\' + serial_number + '.cfg'
            )

            command = 'z:\\scripts\\lictool\\oa3tool-old.exe /Assemble /ConfigFile=x:\\' + serial_number + '.cfg'
            out_pro = subprocess.call(command)
            
            if out_pro == 0:
                print("OA3 + Assemble OK!")
            else:
                print("FAIL: OA3 + Assemble")
                sys.exit(5)


####
     

####


        else:
            print('Unknow Operating System')
            sys.exit(5)
        # Defina os comandos
        command1 = f'z:\\scripts\\clevo2\\H2OOAE-Wx64.exe -W x:\\{serial_number}.bin -S'
        command2 = f'z:\\scripts\lictool\\afuwinx64.exe /A:x:\\{serial_number}.bin'

        try:
            # Executa o primeiro comando
            result = subprocess.run(command1, check=True, shell=True)
            print("O primeiro comando foi executado com sucesso.")
            time.sleep(5)
        except subprocess.CalledProcessError:
            print("O primeiro comando falhou. Tentando o segundo comando...")
            time.sleep(5)
        try:
        # Executa o segundo comando se o primeiro falhar
            result = subprocess.run(command2, check=True, shell=True)
            print("O segundo comando foi executado com sucesso.")
            time.sleep(5)
        except subprocess.CalledProcessError:
            print("Ambos os comandos falharam.")
            time.sleep(5)
            sys.exit(5)

        #command = 'z:\\scripts\lictool\\afuwinx64.exe /A:x:\\' + serial_number + '.bin'
        out_bin = subprocess.call(command)
        if out_bin == 0:
            print("AFU Writing OK!")
            command = 'z:\\scripts\\lictool\\oa3tool-old.exe /Report /ConfigFile=x:\\' + serial_number + '.cfg /LogTrace=x:\\' + serial_number + '.log'
            out_report = subprocess.call(command)
            print("OA3 + Report OK!")
            av_art.art_finished()
    
            if out_report == 0:
                print("OA3 + AFU Completed!")

                command = 'z:\\scripts\lictool\\oa3tool-old.exe /Validate'
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
