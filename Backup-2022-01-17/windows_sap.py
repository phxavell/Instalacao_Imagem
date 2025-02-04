#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
from threading import Thread
import sys
import time

import av_art
import av_factory
import av_os_image
import notebook_hwinfo
import odoo_hwinfo
import notebook_hwecbios
import sap_connect as sap
import notebook_hwcode

start_time = time.time()
print('DEBUG: start_time=%s\n' % start_time)

def logstep(stepinfo):
    print("LOG: %s. Time: %2.fs" % (stepinfo, time.time() - start_time))
    time.sleep(2)


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
    '''Main function to install and activate Windows'''

    # av_art.screen_clear()
    av_art.art_avell_notebooks()

    # #################################################
    # TRACK START #####################################
    logstep('00100 - Avell Notebooks - Starting setup')
    for counter in range(5, 0, -1):
        print("." * counter, counter)
        time.sleep(1)

    # #################################################
    # TRACK START #####################################
    logstep('00200 - Check external power source')

    # Forcar mensagem ao montador para conectar
    # fonte de energia externa.
    # vmcond = notebook_hwinfo.get_vmstatus()
    
    powerflip = False
    logstep(
        '00300 - Fonte de alimentacao externa!!!'
    )

    while not notebook_hwinfo.battery_status():
        if powerflip:
            color('red')
        else:
            color('red-reverse')
        powerflip = not powerflip

        time.sleep(1.5)

    # #################################################
    # TRACK START #####################################
    logstep("00400 - External power source connected")

    color('green')

    notebook = {}

    notebook['extpower'] = True

    # #################################################
    # TRACK START #####################################
    logstep("00500 - Getting computer serial number")

    notebook['serialnumber'] = str(
        notebook_hwinfo.get_serialnumber()['SerialNumber']
    )

    # #################################################
    # TRACK START #####################################
    logstep("00600 - Getting computer UUID")

    notebook['uuid'] = str(
        notebook_hwinfo.get_uuid()['uuid']
    )

    # #################################################
    # TRACK START #####################################
    logstep("00700 - Connect to Avell's SAP API")

    sap.connect()

    # #################################################
    # TRACK START #####################################
    logstep("00800 - SAP Inventory & manufacturing handle")

    while True:

        av_art.art_serial()

        print('\n\nInsira o Numero do pedido para continuar: \n\n')

        var_os = input("SO: ")
        hwz = sap.description(var_os)
        print(hwz)
        if hwz:
            break
        else:
            print("Algo deu errado. Chamar Gabriel nesse caso!!!")
    
    # #################################################
    # TRACK START #####################################
    logstep("00?00 - Serial Number")
        
    #notebook['serialnumber'] = str(sap.serial(var_os))
    #print("\nDebug: %s" % notebook.get('serial') 
    
    
    #command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /SS %s''' % notebook.get('serialnumber')
    #operation = av_factory.cmdexec(command)
    while True:

        
        print('\n\nInsira novo numero de serie para continuar\n\n')
        print('Semana do ano: %s \n' % datetime.datetime.now().isocalendar()[1])

        new_serial1 = input("Serial: AVNB22")
        new_serial2 = input("\n\nSerial: AVNB22")
        if str(new_serial1) == str(new_serial2):
            print("\n\nO novo numero de serie serah:", "AVNB22" + str(new_serial2))
            notebook['serialnumber'] = "AVNB22" + str(new_serial2)
            command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /SS %s''' % notebook.get('serialnumber')
            operation = av_factory.cmdexec(command)
            if not operation['success']:
                print(
                    "Falha 00720 - Comando:", command
                )
                sys.exit(5)
            break
        else:
                print("\n\nAinda continua sem existir o numero de serie")

    command = "" # Cleanup



    # #################################################
    # TRACK START #####################################
    logstep('00900 - Factory parameters')

    color('green')

    notebook['os'] = sap.sistema(var_os)
    notebook['code'] = notebook_hwcode.nb_code(hwz)
    #hw_screen = notebook_hwcode.nb_tela(notebook.get(code))
    notebook['ec'] = notebook_hwinfo.get_ecversion()['ec']
    notebook['bios'] = notebook_hwinfo.get_biosversion()['bios']

    print(
        "INFO: Install %s in [%s] %s (screen size = %s inches; SN=%s).\nINFO: EC=%s and BIOS=%s." % (
            notebook.get('os'),
            notebook.get('code'),
            notebook.get('name_tm'),
            notebook.get('screen'),
            notebook.get('serialnumber'),
            notebook.get('ec'),
            notebook.get('bios')
        )
    )

    image = av_os_image.check(
        notebook.get('code'),
        notebook.get('os')
    )

    # This operator requires Python 3.9 or earlier
    notebook = notebook | image

   

    # print('debug: serial_number=', notebook.get('serialnumber'))
    # print('debug: serial_number_len=', len(notebook.get('serialnumber')))

    if len(notebook.get('serialnumber')) != 12:
        color('red')
        print(
            '''Numero de serie com tamanho errado'''
        )
        sys.exit(5)
        
    if not notebook.get('serialnumber')[6:12].isnumeric():
        color('red')
        print(
            '''Numero de serial nao parece ser numericamente valido'''
        )
        sys.exit(5)

    if int(notebook.get('serialnumber')[6:8]) > 54:
        color('red')
        print(
            '''Numero da semana estah errado'''
        )
        sys.exit(5)

    
    # #################################################
    # TRACK START #####################################
    logstep("01000 - Firmware Confirm")

    color('green')

    #Verificação de EC
    
    ecbios_updated = notebook_hwecbios.nb_compare(notebook.get('code'), notebook.get('ec'), notebook.get('bios'))
    
    # ecbios_updated = True
    
    if not ecbios_updated:
        print('\n\nATUALIZAR EC E BIOS')
        color('red')
        time.sleep(9999)
    
    # #################################################
    # TRACK START #####################################
    logstep("01100 - Writing UEFI serial number")

    command = '''Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP \
"%s"''' % notebook.get('bios_name')

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 15 - Comando:", command
        )
        sys.exit(15)

    command = "" # Cleanup

    ###################################################
    # TRACK START #####################################
    logstep("01200 - Writing UEFI UUID (if needed)")

    '''
    If this notebook has the standard factory UUID (by ODM), than we will
    write the new random (AUTO) UUID.
    '''
    if notebook.get('uuid') == '03000200-0400-0500-0006-000700080009':

        command = '''Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SU AUTO'''
        operation = av_factory.cmdexec(command)

        if not operation['success']:
            print(
               "Falha 15.5 - Comando:", command
            )
            sys.exit(15)

        command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01300 - Writing UEFI manufacturer info")

    # ??? Verificar


    command = '''Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP \
"%s"''' % notebook.get('bios_name')

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 16 - Comando:", command
        )
        sys.exit(16)

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01400 - Setting storage device to install the operating system")

    command = 'wscript /d z:\\scripts\\avell-comparativo.vbs'

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 17 - Comando:", command
        )
        sys.exit(17)

    # modo de espera operacional // espera necessaria para
    # nao travar o 'dism'
    time.sleep(5)

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01500 - Keyboard Settings (Tong Fang Tools / OEM Parameters)")
    print(
        "DEBUG: ", notebook.get('code')
    )
    
    command = "z:\\construtor\\%s\\Parametros\\oem.bat " % notebook.get('code')[:8]

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 23 - Comando:", command
        )
        sys.exit(23)

    command = "" # Cleanup

    # Parametros BIOS
    # #################################################
    # TRACK START #####################################
    
    logstep("01600 - Write BIOS/UEFI selected parameters")
    command = "z:\\construtor\\%s\\Parametros\\bios.bat " % notebook.get('code')[:8]

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 23 - Comando:", command
        )
        sys.exit(23)

    command = "" # Cleanup
    
    # #################################################
    # TRACK START #####################################
    logstep("01700 - Dump computer's device drivers")

    # ROBOCOPY FLAGS
    # /NFL : No File List - don't log file names.
    # /NDL : No Directory List - don't log directory names.
    # /NJH : No Job Header.
    # /NJS : No Job Summary.
    # /NP  : No Progress - don't display percentage copied.
    # /NS  : No Size - don't log file sizes.
    # /NC  : No Class - don't log file classes
    
    if notebook.get('os') in ['Windows 11 Pro', 'Windows 11 PRO', 'Windows 11 Professional', 'Windows 11 Home', 'Windows 11 HSL']:
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\Drivers k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
     
    else: 
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\%s\\Drivers k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]
    
    
    #Chamada de Thread para gravação em paralelo
    
    t1 = Thread(target=av_factory.cmdexec,args=(command,))
    t1.start()
    
    # modo de espera operacional // espera necessaria para
    # nao travar o 'dism'
    
    command = "" # Cleanup
    
    # #################################################
    # TRACK START #####################################
    logstep("01800 - Dump data in storage - Recovery (step 1 of 2)")
    time.sleep(5)
    command = "Dism /apply-image /imagefile:" + str(notebook.get('recovery')) + " /index:1 /ApplyDir:R:\ "
    # print("DEBUG:", command )
    if not notebook.get('os') in ['Windows 11 Pro', 'Windows 11 PRO', 'Windows 11 Professional', 'Windows 11 Home', 'Windows 11 HSL']:
        operation = av_factory.cmdexec(command)
        if not operation['success']:
            print(
                "Falha 21 - Comando:", command
            )
            #sys.exit(21)

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01900 - Dump data in storage - System (step 2 of 2)")

    # modo de espera operacional
    time.sleep(5)
    command = "Dism /apply-image /imagefile:" + str(notebook.get('system')) + " /index:1 /ApplyDir:w:\ "

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 22 - Comando:", command
        )
        sys.exit(22)

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("02000 - Memory Test Initial")

    command = 'z:\\scripts\\aplica_imagem_etapa_2.bat'

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 23 - Comando:", command
        )
        sys.exit(23)

    command = "" # Cleanup

  
    # #################################################
    # TRACK START #####################################
    logstep("02100 - Dump computer's manual")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\%s\\Manual\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]
    
    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [1, 2, 3]:
            print(
                "Falha 28 - Comando:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(28)
    else:
        print("Skipped 28")

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("02200 - Copy Testing tools to Administrator's Desktop (step 1 of 2)")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\%s\\Desktop\\ W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]

    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Falha 26 - Comando:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped 26")

    command = "" # Cleanup
    
    # #################################################
    # TRACK START #####################################
    logstep("02300 - Copy Testing tools to Administrator's Desktop (step 2 of 2)")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\%s\\www\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]

    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Falha 26 - Comando:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped 26")

    command = "" # Cleanup

    # Join para esperar todas as threads serem finalizadas.
    
    t1.join()
    
    # #################################################
    # TRACK START #####################################
    logstep("02400 - At least, finishing...")

    if "Windows" in notebook.get('os'):
        color('yellow')
        print(
            '''\n\n\n\n\n\n
                Executar o comando a seguir, para ativar o sistema operacional:
                \n
                avell lic
                \n\n\n\n\n\n
            '''
        )
    else:
        print("Sem sistema operacional.")
        av_art.art_finished()


if __name__ == "__main__":
    start_time = time.time()
    main()
