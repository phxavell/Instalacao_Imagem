#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import subprocess
import sys
import time

import av_art
import av_factory
import av_os_image_copy
import notebook_hwinfo
import odoo_hwinfo
#import odoo_hwinfo_byhand as odoo_hwinfo

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
    '''if 1:
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
    '''
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
    logstep("00700 - Connect to Avell's Odoo API")

    hwz = odoo_hwinfo.process(
        notebook.get('serialnumber')
    )

    # #################################################
    # TRACK START #####################################
    logstep("00800 - Odoo Inventory & manufacturing handle")

    if not hwz:
        print(
            "Falha 00800 - Numero de Serie inexistente",
            notebook.get('serialnumber')
        )

        while True:

            av_art.art_serial()

            print('\n\nInsira novo numero de serie para continuar\n\n')
            print('Semana do ano: %s \n' % datetime.datetime.now().isocalendar()[1])

            new_serial1 = input("Serial: ")
            new_serial2 = input("\n\nSerial: ")
            if str(new_serial1) == str(new_serial2):
                print("\n\nO novo numero de serie serah:", "AVNB21" + str(new_serial2))
                hwz = odoo_hwinfo.process(str(new_serial2))
                if hwz:
                    notebook['serialnumber'] = str(new_serial2)
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

    notebook['os'] = hwz.get('os')
    notebook['screen'] = hwz.get('screen')
    notebook['name_tm'] = hwz.get('name_tm')
    notebook['code'] = hwz.get('code')
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

    image = av_os_image_copy.check(
        notebook.get('code'),
        notebook.get('os')
    )

    # This operator requires Python 3.9 or earlier
    notebook = notebook | image

    if notebook.get('code') == 'False':
        color('red')
        print(
            "FAIL: ---> Codigo de produto nao criado. Chamar Sr. Kennyson para cadastrar codigo!! <---"
        )
        sys.exit(5)


    # print('debug: serial_number=', notebook.get('serialnumber'))
    # print('debug: serial_number_len=', len(notebook.get('serialnumber')))


    # if not notebook.get('serialnumber')[:6] == 'AVNB21':
    #     color('red')
    #     print(
    #         '''Numero de serie com prefixo errado (Chamar Kennyson ou Trober)'''
    #     )
    #     sys.exit(5)

    #if not notebook.get('serialnumber')[6:11].isnumeric():
        #color('red')
        #print(
            #'''Numero de serial nao parece ser numericamente valido (Chamar Kennyson ou Trober)'''
        #)
        #sys.exit(5)

    if int(notebook.get('serialnumber')[6:8]) > 54:
        color('red')
        print(
            '''Numero da semana estah errado (Chamar Kennyson ou Trober)'''
        )
        sys.exit(5)

    # #################################################
    # TRACK START #####################################
    logstep('01000 - Intel Manufacturing mode - Unlock')


    if notebook.get('code')[:7] == "A60D91C":
        command = '''z:\scripts\TFGTools\Intel\AfuMfgWINx64.EXE /OEMSMI:AC /CMD:"{MU}"'''

        operation = av_factory.cmdexec(command)

        if not operation['success']:
            print(
                "Falha z00900 - Comando:", command
            )
            sys.exit(15)

        command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01100 - Setting hostname")

    sethostname_param = '''reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TCPIP\Parameters /f /v Hostname /t reg_sz /d  %s''' % notebook.get('serialnumber')
    operation_hostname = av_factory.cmdexec(sethostname_param)


    # #################################################
    # TRACK START #####################################
    logstep("01200 - DHCP Challenge - Start")

    ip_param = '''ipconfig //renew'''
    operation_iprenew = av_factory.cmdexec(ip_param)

    time.sleep(5)

    # #################################################,
    # TRACK START #####################################
    logstep("01300 - Firmware parsing")

    color('green')

    ec_updated = True
    bios_updated = True
    
    #??? Feito para teste
    if notebook.get('code')[:8] == "A70D117K":
        # WMIC nao tem suporte a REVISION, nao sendo possivel ler
        # os ultimos caracteres da versao.
        # if notebook.get('ec') == '1.03.10':
        #     ec_updated = True
        ec_updated = True
        bios_updated = True

    
    # A40 LIV // A40A35M
    elif notebook.get('code')[:7] == "A40A35M":
        # WMIC nao tem suporte a REVISION, nao sendo possivel ler
        # os ultimos caracteres da versao.
        # if notebook.get('ec') == '1.03.10':
        #     ec_updated = True
        ec_updated = True

        if notebook.get('bios') == 'N.1.00':
            bios_updated = True

    # A52 LIV GTX // A52D105B
    elif notebook.get('code')[:8] == "A52D105B":
        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # A52 LIV GTX // A52D105D
    elif notebook.get('code')[:8] == "A52D105D":
        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # G1513 MUV GTX 1050 // A52F91A
    elif notebook.get('code')[:7] == "A52F91A":
        if notebook.get('ec') == '1.10.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.03':
            bios_updated = True

    # A60 MUV GTX 1660TI // A60D91C
    elif notebook.get('code')[:7] == "A60D91C":
        ec_updated = True
        if notebook.get('ec') in [
            # '1.11.00',
            # '1.16.00'
            '1.25.00'
        ]:
            ec_updated = True


        if notebook.get('bios') in [
            # 'QCCFL357.0037.2019.0613.2243',
            # 'QCCFL357.0048.2019.0808.1937'
            'QCCFL357.0122.2020.0911.1520'
        ]:

            bios_updated = True

    # G1555 MUV GTX 1650 // A62D91B (revisar)
    elif notebook.get('code')[:7] == "A62D91B":
        if notebook.get('ec') == '1.10.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.03':
            bios_updated = True

    # A62 LIV GTX // A62D107B
    elif notebook.get('code')[:8] == "A62D107B":
        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # A62 LIV GTX // A62D107D
    elif notebook.get('code')[:8] == "A62D107D":
        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # A62 LIV RTX // A62D107E
    elif notebook.get('code')[:8] == "A62D107E":

        if notebook.get('ec') == '1.16.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # G1555 MUV GTX 1650 // A62F91B
    elif notebook.get('code')[:7] == "A62F91B":

        if notebook.get('ec') == '1.10.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.03':
            bios_updated = True

    # A65 LIV RTX 2060 // A65D107E
    elif notebook.get('code')[:8] == "A65D107E":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.01':
            bios_updated = True

    # A65 LIV RTX 2070 // A65D107F
    elif notebook.get('code')[:8] == "A65D107F":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.01':
            bios_updated = True

    # C62 LIV GTX // C62D105B
    elif notebook.get('code')[:8] == "C62D105B":

        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # C62 LIV GTX 1650 // C62D107B
    elif notebook.get('code')[:8] == "C62D107B":

        if notebook.get('ec') == '1.17.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # C62 LIV GTX 1650TI // C62D107D
    elif notebook.get('code')[:8] == "C62D107D":

        if notebook.get('ec') == '1.16.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True

    # C62 LIV RTX 2060 // C62D107E
    elif notebook.get('code')[:8] == "C62D107E":

        if notebook.get('ec') == '1.16.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.02':
            bios_updated = True


    # Workaround G1750MUV
    elif notebook.get('code')[:7] == 'C65D91B':
        ec_updated = True
        bios_updated = True

    # C65 LIV RTX 2070 // C65D107F
    elif notebook.get('code')[:8] == "C65D107F":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.03':
            bios_updated = True

    # C65 LIV RTX 2080 // C65D107G
    elif notebook.get('code')[:8] == "C65D107G":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.01':
            bios_updated = True

    # C65 LIV RTX 2070 // C65D109F
    elif notebook.get('code')[:8] == "C65D109F":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.01':
            bios_updated = True

    # C65 LIV RTX 2080 // C65D109G
    elif notebook.get('code')[:8] == "C65D109G":

        if notebook.get('ec') == '1.9.00':
            ec_updated = True

        if notebook.get('bios') == 'N.1.01':
            bios_updated = True
            
    # ST1 // ST1A4
    elif notebook.get('code')[:5] == "ST1A4":
        if notebook.get('ec') == '1.27.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.05AVE01':
            bios_updated = True
            
    # A70 // A70D107H
    elif notebook.get('code')[:8] == "A70D107H":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True

           
    # A70 // A70D107I
    elif notebook.get('code')[:8] == "A70D107I":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True

          
    # A72 // A72D107H
    elif notebook.get('code')[:8] == "A72D107H":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True

    # A72 // A72D107I
    elif notebook.get('code')[:8] == "A72D107I":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True
            
            
    # ??? Novos, testar?
    #C62D107H        
    elif notebook.get('code')[:8] == "C62D107H":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True
            
    #C65D107H        
    elif notebook.get('code')[:8] == "C65D107H":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True

    #C65D107I
    elif notebook.get('code')[:8] == "C65D107I":
        if notebook.get('ec') == '1.14.00':
            ec_updated = True
        if notebook.get('bios') == 'N.1.07AVE00':
            bios_updated = True



    #else:
        #color('red-reverse')
        #print('\n\nNotebook sem cadastro na verificacao de EC + BIOS!!!\n\n')
        #print('(Chamar Trober)\n\n')
        #time.sleep(99999)

    if not ec_updated:
        print('\n\n\nATUALIZAR EC!!!\n\n\n')
        color('red')
        time.sleep(99999)

    if not bios_updated:
        print('\n\n\nATUALIZAR BIOS!!!\n\n\n')
        color('red')
        time.sleep(99999)


    # #################################################
    # TRACK START #####################################
    logstep("01400 - Setting UEFI parameters")

    if '1513' in notebook['name_tm']:
        notebook['bios_name'] = 'Avell G1513 MUV / A52 MUV'
    elif '1555' in notebook['name_tm']:
        notebook['bios_name'] = 'Avell G1555 MUV / A62 MUV'
    elif '1750' in notebook['name_tm']:
        notebook['bios_name'] = 'Avell G1750 MUV / C65 MUV'
    else:
        if not notebook['name_tm']:
            print(
                "Falha 14 - Nome de BIOS nao existe"
            )
            sys.exit(14)
        else:
            notebook['bios_name'] = notebook['name_tm'][9:]

    # #################################################
    # TRACK START #####################################
    logstep("01500 - Writing UEFI serial number")

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
    logstep("01600 - Writing UEFI UUID (if needed)")

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
    logstep("01700 - Writing UEFI manufacturer info")

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
    logstep("01800 - Setting storage device to install the operating system")

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
    logstep("01900 - Keyboard Settings (Tong Fang Tools)")


    print(
        "DEBUG: ", notebook.get('code')
    )

    if not notebook.get('code'):
        # parei aqui
        print('Falha 01900 - Sem codigo')
        sys.exit(128)

    elif notebook.get('code')[:3]=="A40":
        # PF4PN2F (A40A35M)
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Subwoofer /set 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe KBLSupport /Set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 6')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 33')

    elif notebook.get('code')[:7]=="A60D91C":
        # A60
        process = subprocess.Popen('z:\scripts\TFGTools\oem_a60d91c.bat')
        time.sleep(1)

    elif notebook.get('code')[:3]=="A52" or notebook.get('code')[:3]=="A62":

        # A62/A52 (IDV)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 2')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 2')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051097V1110100"')
        time.sleep(1)

    elif notebook.get('code')[:8] == 'A65D107E':
        # A65D107E
        process = subprocess.Popen('z:\scripts\TFGTools\oem_a65d107e.bat')
        time.sleep(1)

    elif notebook.get('code')[:8] == 'A65D107F':
        # A65D107F
        av_factory.cmdexec('z:\scripts\TFGTools\oem_a65d107f.bat')
        time.sleep(1)

    elif notebook.get('code')[:3] == 'C62':
        # C62 (IDR)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0')
        time.sleep(1)

        if notebook.get('code')[:8] == 'C62D107E':
            # GK7MR0R
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 2')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 36')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051097R1110100"')
            time.sleep(1)
          
        # ??? C62 Ultimate
        elif notebook.get('code')[:8] == 'C62D107H':
            # GM7MG0R
            pass
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 2')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe ColorCalibration /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051123R1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 36')
            time.sleep(1)
          
        
        else:
            # Any kind of C62...
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 0')
            time.sleep(1)
            
        

    elif notebook.get('code')[:3] == 'C65':
        if notebook.get('code')[:8] == 'C65D107F':

            # GM7MPHP
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D05108AP1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)
            
        
        # ??? C65 ULTIMATE
        elif notebook.get('code')[:8] == 'C65D107H':

            # GM7MG0P
            pass
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 255')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051116P1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)
            
        # ??? C65 ULTIMATE
        elif notebook.get('code')[:8] == 'C65D107I':

            # GM7MG7P
            pass
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 255')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051116P1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)
        
        

        elif notebook.get('code')[:8] == 'C65D107G':
            # GM7MQ8P: (C65D107G)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051089P1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)

        elif notebook.get('code')[:8] == 'C65D109F':
            # Kit GM7MPHP: (C65D109F)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051089P1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)

        elif notebook.get('code')[:8] == 'C65D109G':
            # Kit GM7MQ8P: (C65D109G)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051089P1110100"')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe  Nbtype /Table 36')
            time.sleep(1)
        
    
    elif notebook.get('code')[:3]=="ST1":
        # GM7NG0M (ST1A4)
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
        time.sleep(1)
        
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 255')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 8')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 36')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051115M1110100"')
        
        
    elif notebook.get('code')[:8]=="A70D107H":
        # GM5MG0O/GM5MG7O (A70D107H)
        
        
        #time.sleep(1)
        #Teste Para uso de Dump process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rwblock0 /load /file "z:\scripts\oem_a70d107.txt" ')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 2')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 3')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 36')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051122O1110100"')
        
        
        
         
    elif notebook.get('code')[:7]=="A72D107":
        # GM5MG0Y/GM5MG7Y (A72D107H/A72D107I)
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 1')
        #time.sleep(1)
        #process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Subwoofer /set 0')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe kblbid /setkbl 1')
        #time.sleep(1)
        #process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe KBLSupport /Set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Nbtype /Table 36')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\AMIDEWINx64.exe /OS 16 "1D051121Y1110100"')
        
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rgblb /setmode 255')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe ColorCalibration /set 1')
        time.sleep(1)
        process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 6')
        
        
        '''
        else:

            # C65 (IDP) // ANY C65
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /clear')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /MK 0 /WK 1 /FB 1 /RGBKB 0 /CHINA 0 /OC 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe oemtdr /settdr 0xa')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe RGBKB /set 005050')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /RGBKB 1')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe SetApCtrl /BL 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe AdpType /set 4')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe turbomode /set 0')
            time.sleep(1)
            process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe Modelid /set 4')
            time.sleep(1)
        '''
    #???
    elif notebook.get('code')[:8]=="A70D117k":
        pass
        
    #else:
    #    print("Falha 23.597 - Verificacao de placa-mae [", notebook.get('code') ,"]")
    #    sys.exit(24)

    if command:
        #operation = av_factory.cmdexec(command)

        #if int(operation['exitstatus']) not in [0, 1, 2, 3]:
        #    print(
        #        "Falha 25 - Comando:", command
        #    )
        #    print("ExitStatus=", operation['exitstatus'])

        #    sys.exit(25)

        process = subprocess.Popen(command)
        print("INFO: Driver's copy in parallel process...")

    ################################ TECLADOS - FIM #######

    # #################################################
    # TRACK START #####################################
    logstep("02000 - Write BIOS/UEFI selected parameters")

    #

    if notebook.get('code')[:7] == 'A40A35M':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A40 LIV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "LIV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A40 LIV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture


    elif notebook.get('code')[:8] == 'A52D105B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A52 LIV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "LIV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A52 LIV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture

    elif notebook.get('code')[:8] == 'A52D105D':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A52 LIV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "LIV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A52 LIV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture

    elif notebook.get('code')[:7] == 'A52F91A':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A52 LIV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "LIV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A52 LIV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture

    elif notebook.get('code')[:7] == 'A60D91C':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A60 MUV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A60 MUV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A60 MUV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:7] == 'A62F91B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "G1555 MUV / A62 MUV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "MUV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell G1555 MUV / A62 MUV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture

    elif notebook.get('code')[:7] == 'A62D91B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "G1555 MUV / A62 MUV"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "MUV"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell G1555 MUV / A62 MUV"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture

    elif notebook.get('code')[:7] == 'A62D91C':
        # REVISAR
        print("ERRO: Produto %s nao configurado!" % notebook.get('code'))
        sys.exit(23)


    elif notebook.get('code')[:8] == 'A62D107B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A62D107D':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A62D107E':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A65D107F':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A65D107D':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A65D107E':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'A65D107F':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C62D105B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C62D107B':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C62D107D':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C62D107E':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
        
    # ??? C62 LIV ULTIMATE
    
    elif notebook.get('code')[:8] == 'C62D107H':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C62 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
    
    

    elif notebook.get('code')[:7] == 'C65D91B':
        # REVISAR
        print("ERRO: Produto %s nao configurado!" % notebook.get('code'))
        sys.exit(23)

    elif notebook.get('code')[:7] == 'C65D91C':
        # REVISAR
        pass  # REMOVER este pass apos 2021-01-07a
        # print("ERRO: Produto %s nao configurado!" % notebook.get('code'))
        # sys.exit(23)

    elif notebook.get('code')[:8] == 'C65D107F':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C65D107G':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C65D109F':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')

    elif notebook.get('code')[:8] == 'C65D109G':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
        
    # ??? C65 LIV ULTIMATE
    
    elif notebook.get('code')[:8] == 'C65D107H':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
    # ??? C65 LIV ULTIMATE
    elif notebook.get('code')[:8] == 'C65D107I':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "C65 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
        

    elif notebook.get('code')[:5] == 'ST1A4':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"') # System Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "Storm One"') # System Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "Storm"') # System Family
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "1"') # SKU Number
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"') # Baseboard Manufacture
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell Storm One"') # Baseboard Product
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"') # Chassis Manufacture
        
    elif notebook.get('code')[:7] == 'A72D107':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A72 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A72 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A72 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A72 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
        
    #??? Feito para teste
    elif notebook.get('code')[:7] == 'A70D117K':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A70 MOB"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A70 MOB"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A70 MOB"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A70 MOB"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')    
    
    elif notebook.get('code')[:7] == 'A70D107':
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SP "A70 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SF "A70 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SK "A70 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BM "Avell High Performance"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /BP "Avell A70 LIV"')
        time.sleep(1)
        process = subprocess.Popen('Z:\Scripts\TFGTools\AMIDEWINx64.EXE /CM "Avell High Performance"')
        
    
        
      
    
    elif notebook.get('code')[:7] == 'ZZZZ_EM_STANDBY':
        # REVISAR
        print("ERRO: Produto %s nao configurado!" % notebook.get('code'))
        sys.exit(23)
    
    #???
    #else:
    #    print("Falha 23.599 - Verificacao de placa-mae [", notebook.get('code') ,"]")
    #    sys.exit(24)

    
    # #################################################
    # TRACK START #####################################
    logstep("z???? - Dump computer's device drivers")

    # ROBOCOPY FLAGS
    # /NFL : No File List - don't log file names.
    # /NDL : No Directory List - don't log directory names.
    # /NJH : No Job Header.
    # /NJS : No Job Summary.
    # /NP  : No Progress - don't display percentage copied.
    # /NS  : No Size - don't log file sizes.
    # /NC  : No Class - don't log file classes

   
    if notebook.get('code')[:5] == 'ST1A4':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_st1a4 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
    elif notebook.get('code')[:7] == 'A70D107':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a70d107 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
    elif notebook.get('code')[:7] == 'A72D107':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a72d107 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
    elif notebook.get('code')[:8] == 'C62D107H':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c62d107h k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
    elif notebook.get('code')[:8] == 'C65D107H':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107h k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
    elif notebook.get('code')[:8] == 'C65D107I':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107i k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    # ???? Drivers, imagens estão indo com a partição vazia, resolver o problema
    
    if notebook.get('code')[:7] == 'A40A35M':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a40_liv k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
    elif notebook.get('code')[:8] == 'A52D105B':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a52d105b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'A52F91A':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'A60D91C':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a60d91c k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
        # command = ''

    elif notebook.get('code')[:7] == 'A62F91B':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'A62D91B':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'A62D91C':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"


    elif notebook.get('code')[1:8] == '62D105B':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62d107b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[1:8] == '62D107B':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62d107b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"


    elif notebook.get('code')[1:8] == '62D107D':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62d107d k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[1:8] == '62D107E':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62d107e k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'A65D107E':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a65d107e k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'A65D107F':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a65d107f k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'C65D91B':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'C65D91C':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'C65D107F':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107f k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'C65D107G':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107g k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'C65D109F':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107g k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:8] == 'C65D109G':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_c65d107g k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif notebook.get('code')[:8] == 'A70D117K':
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\a70d117k\\Drivers k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    elif notebook.get('code')[:7] == 'ZZZZ_EM_STANDBY':
        # REVISAR
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\uwd_a62f91b k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    # ???? Drivers, imagens estão indo com a partição vazia, resolver o problema
    
    if command:
        #operation = av_factory.cmdexec(command)

        #if int(operation['exitstatus']) not in [0, 1, 2, 3]:
        #    print(
        #        "Falha 25 - Comando:", command
        #    )
        #    print("ExitStatus=", operation['exitstatus'])
        #    sys.exit(25)

        process = subprocess.Popen(command)
        print("INFO: Driver's copy in parallel process...")

    else:
        print("Skipped 25")

    command = "" # Cleanup
    
    """
    else:
        print("Falha 24 - Verificacao de placa-mae [", notebook.get('code') ,"]")
        sys.exit(24)


    if command:
        #operation = av_factory.cmdexec(command)

        #if int(operation['exitstatus']) not in [0, 1, 2, 3]:
        #    print(
        #        "Falha 25 - Comando:", command
        #    )
        #    print("ExitStatus=", operation['exitstatus'])

        #    sys.exit(25)

        process = subprocess.Popen(command)
        print("INFO: Driver's copy in parallel process...")

    else:
        print("Skipped 25")

    command = "" # Cleanup

    # PARALELOS AQUI


    """

    # #################################################
    # TRACK START #####################################
    logstep("02100 - Dump data in storage (step 1 of 2)")

    command = "Dism /apply-image /imagefile:" + str(notebook.get('recovery')) + " /index:1 /ApplyDir:R:\ "

    #operation = av_factory.cmdexec(command)

    #if not operation['success']:
        #print(
            #"Falha 21 - Comando:", command
        #)
        #sys.exit(21)

    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("02200 - Dump data in storage (step 2 of 2)")

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
    logstep("02300 - Windows Recovery and other copy")

    command = 'z:\\scripts\\aplica_imagem_etapa_2.bat'

    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 23 - Comando:", command
        )
        sys.exit(23)

    command = "" # Cleanup

    """

    # #################################################
    # TRACK START #####################################
    logstep("???? - Copy drivers (old)")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\drivers\\ k:\\ /e"

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

    """

    # #################################################
    # TRACK START #####################################
    logstep("02400 - Dump computer's manual")
    
    if notebook.get('code')[:7] == 'A40A35M':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a40_liv\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:5] == 'A52D1':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a52_liv\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'A52F91A':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a52_muv\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:3] == 'A60':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a60_liv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'A62D91B':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_muv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'A62D91C':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_muv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'A62F91B':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_muv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'A62D107B':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_liv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'A62D107D':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_liv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'A62D107E':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a62_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:3] == 'A65':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a65_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C62D105B':  # Checked 2020-01-25
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c62_liv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C62D107B':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c62_liv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C62D107E':  # Checked 2020-01-18
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c62_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"
    
    elif notebook.get('code')[:8] == 'C62D107H':  # Checked 2020-07-21
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c62_liv_ultimate\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'C65D91B':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_muv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:7] == 'C65D91C':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_muv_gtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C65D107F':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C65D107G':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C65D109F':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"

    elif notebook.get('code')[:8] == 'C65D109G':  # Checked 2020-01-16
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"
        
    elif notebook.get('code')[:8] == 'C65D107H':  # Checked 2020-07-21
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_ultimate\ w:\\users\\public\\Desktop\\ *.pdf /e"
        
    elif notebook.get('code')[:8] == 'C65D107I':  # Checked 2020-07-21
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_c65_liv_ultimate\ w:\\users\\public\\Desktop\\ *.pdf /e"
    
    elif notebook.get('code')[:5] == 'ST1A4':  # Checked 2020-06-14
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_st1a4\ w:\\users\\public\\Desktop\\ *.pdf /e"
    
    elif notebook.get('code')[:7] == 'A70D107':  # Checked 2020-06-14
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a70_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"
    
    elif notebook.get('code')[:7] == 'A72D107':  # Checked 2020-06-14
        command = "x:\\Windows\\System32\\robocopy.exe z:\\UWDrivers\\man_a72_liv_rtx\ w:\\users\\public\\Desktop\\ *.pdf /e"
    
    #???
    elif notebook.get('code')[:8] == 'A70D117K':  # Checked 2020-06-14
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\a70d117k\Manual w:\\users\\public\\Desktop\\ *.pdf /e"
    '''    
    else:
        print("Falha 27 - Verificacao de manual faltante = [%s]." % notebook.get('code'))
        color('red')
        sys.exit(25)

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
    '''
    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("02500 - Copy Testing tools to Administrator's Desktop")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\scripts\\go_to_desktop\\ W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np"

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










#ADICIONADO AQUI PARA TESTES DESENVOLVIMENTO:***************************************************************************
    ######################  LINHA DE COMANDO PARA ADICIONAR TESTES DO DESENVOLVIMENTO ################## ADICIONADO EM 08.03.2023
    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\DesenvolvimentoMao\\TESTES_AVELL\\ W:\\TESTES_AVELL /e /NFL /NDL /NJH /NJS /nc /ns /np"
    print("Copiando arquivos de testes da Engenharia de Desenvolvimento e Qualidade...")
    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Falha  Testes", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped 26")
    command = "" # Cleanup
    
    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Desktop1\\ W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np"
    # command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\DesenvolvimentoMao\\ATALHO\\ W:\\Users\Administrador\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup /e /NFL /NDL /NJH /NJS /nc /ns /np"
    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Falha Testes:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped Testes")
    
    origem = r"z:\construtor\DesenvolvimentoMao\ATALHO"

    # Caminho completo de destino para a cópia do diretório
    destino = r"W:\Users\Administrador\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

    # Comando para copiar o diretório usando o comando xcopy do prompt de comando do Windows
    comando = 'cmd /c xcopy "{}" "{}" /s'.format(origem, destino)

    # Executa o comando usando o módulo subprocess
    subprocess.run(comando, shell=True)
    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Teste de Copiar Para o Startup via CMD:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Teste de Copiar Para o Startup via CMD")
        #ADICIONADO AQUI PARA TESTES DESENVOLVIMENTO:***************************************************************************











    """
    # #################################################
    # TRACK START #####################################
    logstep("???? - Copy Wallpaper (LIV) to Windows Wallpapers path.")

    command = "copy z:\\scripts\\go_to_desktop\\wallpaper\\*.jpg W:\\Windows\\Web\\Wallpaper\\"

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
    """

    # #################################################
    # TRACK START #####################################
    logstep('02600 - Intel Manufacturing mode - Lock')

    if notebook.get('code')[:7] == "A60D91C":
        command = '''z:\scripts\TFGTools\Intel\AfuMfgWINx64.EXE /OEMSMI:AC /CMD:"{ML}"'''
        operation = av_factory.cmdexec(command)
        if not operation['success']:
            print('Falha z02800 - Comando:', command)
            exit(15)
    command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("02700 - At least, finishing...")

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
