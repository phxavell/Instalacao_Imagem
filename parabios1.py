#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
from threading import Thread
import sys
import time
import subprocess

import av_art
import av_factory
import av_os_image_2024
import notebook_hwinfo
import notebook_hwecbios #Importante
import a_sap_connect23new as sap
import notebook_hwcode #Importante
import teste_envio_cbr_interno
import shutil

start_time = time.time()
#print('DEBUG: start_time=%s\n' % start_time)

def logstep(stepinfo):
    print("LOG: %s. Time: %2.fs" % (stepinfo, time.time() - start_time))
    time.sleep(2)


def color(colorname):
    colorcode = 0

    if colorname == 'green':
        colorcode = '03'
    elif colorname == 'yellow':
        colorcode = '06'
    elif colorname == 'red':
        colorcode = '04'
    elif colorname == 'red-reverse':
        colorcode = '40'
    elif colorname == 'red-white':
        colorcode = 'F4'    
    else:
        colorcode = '07'

    colorful = lambda: os.system(
        'color ' + str(colorcode)
    )  # on Windows System

    colorful()


def main():
    '''Main function to install and activate Windows'''

    # av_art.screen_clear()
    av_art.art_plm()
    '''
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

    while not notebook_hwinfo.battery_status(): # Verifica se o notebook está conectado na fonte
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
    logstep("00500 - Getting computer UUID")

    notebook['uuid'] = str(
        notebook_hwinfo.get_uuid()['uuid']
    )
    
    # #################################################
    # TRACK START #####################################
    logstep("00600 - Connect to Avell's SAP API")

    sap.connect()

    # #################################################
    # TRACK START #####################################
    logstep("00700 - SAP Inventory & manufacturing handle")

    # #################################################
    # Utilizado um campo para gravar as informações da OS
    
    notebook['ordemservico'] = str(
        notebook_hwinfo.get_os()['SerialNumber']
    )
    
    # #################################################
    # #################################################
    
    #if notebook.get('ordemservico') == 'Standard' or notebook.get('ordemservico') == 'M1BC052001C7':
    
    
    if not notebook.get('ordemservico') is None:  #===================================================#
        while True:
            #av_art.art_plm()
            print('\n\nDIGITE O NÚMERO DE SÉRIE\n\n')
            var_os = input("S/N: ")
            if var_os[:4] == 'INTR':  # Feito para identificar quando a máquina for uma interna
                notebook['ordemservico'] = var_os
                break
            else:
                hwz = sap.description(var_os)
                if hwz:
                    notebook['ordemservico'] = var_os
                    notebook['code'] = notebook_hwcode.nb_code(sap.description(notebook.get('ordemservico')))
                    if notebook.get('code')[:3] == 'A55':
                        command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -BS %s''' % notebook.get('ordemservico')
                        print("DEBUG Command: %s" % command)
                    elif notebook.get('code')[:3] == 'A57':
                        command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -BS %s''' % notebook.get('ordemservico')
                        print("DEBUG Command: %s" % command)
                    elif notebook.get('code')[:3] == 'BOL':
                        command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -BS %s''' % notebook.get('ordemservico')
                    elif notebook.get('code')[:4] == 'BOLB':  # --->>> ADICIONANDO O B.ON LITE NEW
                        command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -BS %s''' % notebook.get('ordemservico')
                    else:
                        command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /BS %s''' % notebook.get('ordemservico')
                        print("DEBUG Command: %s" % command)

                    operation = av_factory.cmdexec(command)
                    if not operation['success']:
                        print("Falha 00720 - Comando:", command)
                        sys.exit(5)
                    break
                else:
                    print("Algo deu errado. Chamar Gabriel nesse caso!!!")

        notebook['code'] = notebook_hwcode.nb_code(sap.description(notebook.get('ordemservico')))

        # TRACK START
        logstep("00800 - Writing computer serial number")  # Escrita do número de série na placa

        if notebook.get('ordemservico')[:4] == 'INTR':  # Para maquina interna
            print("Informe o Numero de série: ")
            notebook['serialnumber'] = input("Serial: ")
        else:
            notebook['serialnumber'] = sap.serial(notebook.get('ordemservico'))

        if notebook.get('code')[:3] == 'A55':
            command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -SS %s''' % notebook.get('serialnumber')
        elif notebook.get('code')[:3] == 'A57':
            command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -SS %s''' % notebook.get('serialnumber')
        elif notebook.get('code')[:4] == 'BOLB':
            command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -SS %s''' % notebook.get('serialnumber')
        elif notebook.get('code')[:3] == 'BOL':
            command = '''Z:\\scripts\\clevo\\H2OSDE-Wx64.exe -SS %s''' % notebook.get('serialnumber')
        else:
            command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /SS %s''' % notebook.get('serialnumber')

        operation = av_factory.cmdexec(command)
        command = ""  # Cleanup

        # TRACK START
        logstep('00900 - Factory parameters')
        color('green')

        notebook['os'] = sap.sistema(notebook.get('ordemservico'))
        if notebook.get('ordemservico')[:4] == 'INTR':  # Pra pegar o codigo quando for uma maquina interna
            notebook['code'] = notebook.get('ordemservico')[4:12]
        else:
            notebook['code'] = notebook_hwcode.nb_code(sap.description(notebook.get('ordemservico')))
        notebook['screen'] = notebook_hwcode.nb_tela(notebook.get('code'))
        notebook['ec'] = notebook_hwinfo.get_ecversion()['ec']
        notebook['bios'] = notebook_hwinfo.get_biosversion()['bios']

        print(
            "INFO: Install %s in [%s] (screen size = %s inches; SN=%s).\nINFO: EC=%s and BIOS=%s." % (
                notebook.get('os'),
                sap.description(notebook.get('ordemservico')),
                notebook.get('screen'),
                notebook.get('serialnumber'),
                notebook.get('ec'),
                notebook.get('bios')
            )
        )

        image = av_os_image_2024.check(
            notebook.get('code'),
            notebook.get('os')
        )
 

    # This operator requires Python 3.9 or earlier
    notebook = notebook | image
    
    

    # #################################################
    # TRACK START #####################################
    logstep("01000 - Firmware Confirm")

    color('green')
      
    
    logstep("01100 - Writing UEFI UUID (if needed)")

    '''
    If this notebook has the standard factory UUID (by ODM), than we will
    write the new random (AUTO) UUID.
    '''
    if notebook.get('uuid') == '03000200-0400-0500-0006-000700080009': # Verificar em novos modelos

        command = '''Z:\Scripts\TFGTools\AMIDEWINx64.EXE /SU AUTO''' # Only works in TF 11th Models
        operation = av_factory.cmdexec(command)

        if not operation['success']:
            print(
               "Falha 15.5 - Comando:", command
            )
            sys.exit(15)

        command = "" # Cleanup

    # #################################################
    # TRACK START #####################################
    logstep("01200 - Setting storage device to install the operating system")

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
    logstep("01300 - Keyboard Settings (Tong Fang Tools / OEM Parameters)") # Gabriel focar nessa parte (Necessario alteração)
    print(
        "DEBUG: ", notebook.get('code')
    )
 

        #=========== ADICIONAR TODOS OS MOBs AQUI ===========#       

    if (notebook.get('code')[:8] == 'a52d115k'):
        command = "z:\\construtor\\MOB\\OEM\\%s.bat "
            
        
        #====================================================##====================================================#
                                        ############# ADICIONADO A62 LIV ###############
                                                  #### PEDIDO ESPECIAL ####
    elif (notebook.get('code')[:8] == 'A62D107B'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]   
        
        #====================================================##====================================================#
    


        # A52 HYB NEW i7 #
        
    elif (notebook.get('code')[:8] == 'A52D127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ALL\\OEM\\%s W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]


        # A52 HYB NEW i5 #
        
    elif (notebook.get('code')[:8] == 'A52D125K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ALL\\OEM\\%s W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]    
         
        
        # A52 ION #
        
    elif (notebook.get('code')[:8] == 'A52D127N'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]
        
        # A72 ION #
        
    elif (notebook.get('code')[:8] == 'A72D137Q'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]   
    
        # A70 ION # 
    
    elif (notebook.get('code')[:8] == 'A70D137P'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]
    
        # STORM GO 4060 #
        
    elif (notebook.get('code')[:8] == 'STGD137P'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]
    
        # STORM GO 4070 #
        
    elif (notebook.get('code')[:8] == 'STGD137Q'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]


        # STORM GO BRANCO 4060 #==================================================

    elif (notebook.get('code')[:8] == 'GM6PX0Z'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]
        # STORM GO BRANCO 4060 #==================================================
    
        # STORM GO BRANCO 4070 #==================================================

    elif (notebook.get('code')[:8] == 'GM6PX7Z'):
        command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]
        # STORM GO BRANCO 4070 #==================================================


        # STORM X 4080  - Feito modificação no caminho do arquivo para executar direto com as ferramentas enviadas pela TF para o modelo#

    elif (notebook.get('code')[:8] == 'STXD137R'):
        command = "Z:\\construtor\\ALL\\OEM\\STXD137R\\%s.bat " % notebook.get('code')[:8]

        # STORM X 4090  - Feito modificação no caminho do arquivo para executar direto com as ferramentas enviadas pela TF para o modelo#

    elif (notebook.get('code')[:8] == 'STXD139S'):
        command = "Z:\\construtor\\ALL\OEM\\STXD139S\\%s.bat " % notebook.get('code')[:8]


        #ADICIONADO PARA A SERIE STORM BS=========================================================================================================================================

        #ADICAO PARA STORM BS 3050 I5
    elif (notebook.get('code')[:8] == 'STBD125K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ALL\\OEM\\%s W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]

        #ADICAO PARA STORM BS 3050 I7 - NOVO
    elif (notebook.get('code')[:8] == 'STBD127K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ALL\\OEM\\%s W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]

        #ADICAO PARA STORM BS 4050 I7 - NOVO
    elif (notebook.get('code')[:8] == 'STBD127N'):
         command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]

        #ADICIONADO PARA A SERIE STORM BS=========================================================================================================================================

        
        
        #ADICIONADO A65 ION 4060 =========================================================================================================================================
        
    elif (notebook.get('code')[:8] == 'A65D129P'):
         command = "z:\\construtor\\ALL\\OEM\\%s.bat " % notebook.get('code')[:8]

        #ADICIONADO A65 ION 4060=========================================================================================================================================

    
    ## Funcional apenas para Clevo
    
    elif (notebook.get('code')[:3] == 'A55'):
        command = ""
    elif (notebook.get('code')[:3] == 'A57'):
        command = ""
    
    elif (notebook.get('code')[:4] == 'BOLB'):    #ADICIONADO BON LITE NEW - INÁCIO 21.07.2023
        command = ""
    
    elif (notebook.get('code')[:3] == 'BOL'):     #ALTEREI AQUI 19.08.2022 - GABRIEL INACIO
        command = ""    
    

        #===== ADICIONAR TODOS OS HYB AQUI =====#

        
        # A70 HYB 3060 #
        
        
    elif (notebook.get('code')[:8] == 'A70D127H'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ALL\\OEM\\%s W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]

        
        #=======================================#
        
    
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

    # Parametros BIOS
    # #################################################
    # TRACK START #####################################
    
    
    
###     NECESSÁRIO VERIFICAR NOVO CAMINHO PARA NOVOS MODELOS ION / GO / X E ETC    
    
    
    logstep("01400 - Write BIOS/UEFI selected parameters")
    
    command = "z:\\construtor\\ALL\\ParamBios\\%s.bat " % notebook.get('code')[:8] # Necessário trocar endereço e talvez gerar um codigo novo? Pensar nisso
    
    
    operation = av_factory.cmdexec(command)

    if not operation['success']:
        print(
            "Falha 23 - Comando:", command
        )
        print(
            "DEBUG:", operation
        )
        sys.exit(23)

    command = "" # Cleanup
    
    print(" ")
    print("GERANDO LOG COMPARADOR...")
    
    
    
    
    if not (notebook.get('ordemservico')[:4] == 'INTR'): # Pra pegar o codigo quando for uma maquina interna
        ecbios_updated = notebook_hwecbios.nb_compare(notebook.get('code'), notebook.get('ec'), notebook.get('bios'))
        if not ecbios_updated:
            time.sleep(5)
            for counter in range(5, 0, -1):
             print("." * counter, counter)
             time.sleep(1)
            
            print('\nBIOS/EC DIVERGENTE (-_-)\n')
            print("        O  ")
            print("       <|> ")
            print("       / \ ")
            
            print('\nATUALIZAR PARA PROSSEGUIR')
            ('red')
            time.sleep(9999)
    
    

    
    
    
    directory = 'z:\logcompare2023\ion_2023'
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"{directory}\{notebook.get('serialnumber')} {timestamp}.txt"

    result = subprocess.run(['z:\\scripts\\avell_comparador.cmd'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    logsap = (f'''\n\n OP: {notebook.get('ordemservico')} \n\n DESCRIÇÃO: {sap.description(notebook.get('ordemservico'))} \n\n Code: {notebook.get('code')} \n\n Tela: {notebook.get('screen')} \n\n Sistema Operacional: {notebook.get('os')} \n\n BIOS: {notebook.get('bios')} \n\n NS: {notebook.get('serialnumber')}\n\n''' + "\n")

    with open(filename, 'a') as output_file:
     output_file.write(logsap)
     output_file.write(output)

# Copiando para o diretório C://TESTES_AVELL  - PARA SERVIR COMO CHAVE NO NOVO SCRIPT DE LICENÇAS
    destination_dir = 'W:\\'
    shutil.copy(filename, destination_dir)



    for counter in range(5, 0, -1):
        print("." * counter, counter)
        time.sleep(1)
        
    print('LOG GERADO COM SUCESSO\n')
    time.sleep(2)
    

    command = "z:\\scripts\\avell_abrir1.cmd"
    operation = av_factory.cmdexec(command)
 

    arquivo = open('z:\\logcompare2023\sistema.txt','a')
    arquivo.write(f'''\n\n OP: {notebook.get('ordemservico')} \n\n DESCRIÇÃO: {sap.description(notebook.get('ordemservico'))} \n\n Code: {notebook.get('code')} \n\n Tela: {notebook.get('screen')} \n\n Sistema Operacional: {notebook.get('os')} \n\n BIOS: {notebook.get('bios')} \n\n NS: {notebook.get('serialnumber')}\n\n Data/Hora: {datetime.datetime.now()}\n\n ___________________________________________________________________________________________________________''' + "\n")
    arquivo.close()

    command = "z:\\scripts\\avell_fechar1.cmd"
    operation = av_factory.cmdexec(command)

    command = "" # Cleanup
    
    # #################################################
    # TRACK START #####################################
    logstep("01500 - Dump computer's device drivers")

    # ROBOCOPY FLAGS
    # /NFL : No File List - don't log file names.
    # /NDL : No Directory List - don't log directory names.
    # /NJH : No Job Header.
    # /NJS : No Job Summary.
    # /NP  : No Progress - don't display percentage copied.
    # /NS  : No Size - don't log file sizes.
    # /NC  : No Class - don't log file classes
    #if notebook.get('os') in ['Windows 11 Pro', 'Windows 11 PRO', 'Windows 11 Professional', 'Windows 11 Home', 'Windows 11 HSL']:
    
    
    
    
        # A52 HYB NEW i5 #
    
    if (notebook.get('code')[:8]=='A52D125K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
    #====================================================##====================================================#
                                        ############# ADICIONADO A62 LIV ###############
                                                  #### PEDIDO ESPECIAL ####
    
    elif (notebook.get('code')[:8]=='A62D107B'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\LIV\\DriversA62Liv1650 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
        # A52 HYB NEW i7 #
    
    elif (notebook.get('code')[:8]=='A52D127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A52 ION #
   
    elif (notebook.get('code')[:8]=='A52D127N'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversA52ION k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A72 ION #
    
    elif (notebook.get('code')[:8]=='A72D137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversA72ION k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" 
    
        # A70 ION #

    elif (notebook.get('code')[:8]=='A70D137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversA70ION k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" 
    
        # STORM GO 4060 #
        
    elif (notebook.get('code')[:8]=='STGD137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTGO k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" 

        # STORM GO 4070 #
        
    elif (notebook.get('code')[:8]=='STGD137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTGO k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" 


    # STORM GO BRANCO 4060 #================BRANCO====================================================================================
        
    elif (notebook.get('code')[:8]=='GM6PX0Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTGO k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    # STORM GO 4060 #================BRANCO============================================================================================

    # STORM GO BRANCO 4070 #================BRANCO=====================================================================================
        
    elif (notebook.get('code')[:8]=='GM6PX7Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTGO k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    # STORM GO 4070 #================BRANCO============================================================================================
        
        # STORM X 4080 #
        
    elif (notebook.get('code')[:8]=='STXD137R'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTX k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"     
        
        # STORM X 4090 #
        
    elif (notebook.get('code')[:8]=='STXD139S'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversSTX k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" 
    
    
    #ADICIONADO PARA A SERIE STORM BS=========================================================================================================================================

        # STORM BS 3050 I5 - NOVO #
        # MESMOS DRIVERS DO A52 HYB 3050 - I5
    elif (notebook.get('code')[:8]=='STBD125K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # STORM BS 3050 I7 - NOVO #
        # MESMOS DRIVERS DO A52 HYB 3050 - I7
    elif (notebook.get('code')[:8]=='STBD127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # STORM BS 4050 I7 - NOVO #
        # MESMOS DRIVERS DO A52 ION 4050 - I7
    elif (notebook.get('code')[:8]=='STBD127N'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversA52ION k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    #ADICIONADO PARA A SERIE STORM BS=========================================================================================================================================
    
    elif (notebook.get('code')[:8]=='A65D129P'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversA65 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

    #ADICIONADO DRIVERS A65ION=========================================================================================================================================
    
   
    elif (notebook.get('code')[7] == 'K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif (notebook.get('code')[:3]=='A7B'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3050 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    #elif (notebook.get('code')[:3]=='A52'):
     #   command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers1650 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif (notebook.get('code')[:3]=='A55'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\DriversClevo k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif (notebook.get('code')[:3]=='A57'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\DriversClevo k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif (notebook.get('code')[7] == 'X'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\DriversBonlite k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
    
    
    
    ### ADICIONAR AQUI TODOS OS MODELOS MOB
    
    elif (notebook.get('code')[:8]=='A52D115K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\%s\\Drivers k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:8]
    

    
############################################################################################################################################################    
    
    elif (notebook.get('code')[7] == 'U'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversBonLiteNew k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    elif (notebook.get('code')[7] == 'T'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\DriversBonLiteNew k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"

 ##################################################################################################################################################################   
    
    else:
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Drivers3060 k:\\ /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
    
    
    #Chamada de Thread para gravação em paralelo
    
    t1 = Thread(target=av_factory.cmdexec,args=(command,))
    t1.start()
    
    # modo de espera operacional // espera necessaria para
    # nao travar o 'dism'
    
    command = "" # Cleanup
    
    # #################################################
    # TRACK START #####################################
    logstep("01600 - Dump data in storage - Recovery (step 1 of 2)")
    time.sleep(5)
    command = "Dism /apply-image /imagefile:" + str(notebook.get('recovery')) + " /index:1 /ApplyDir:R:\ "
    # print("DEBUG:", command )
    # Windows 11 nao tem recovery
    if not notebook.get('os') in ['Windows 11 Pro', 'Windows 11 PRO', 'Windows 11 Professional', 'Windows 11 Home', 'Windows 11 HSL']:
        operation = av_factory.cmdexec(command)
        if not operation['success']:
            #print(
            #   "Falha 21 - Comando:", command
            #)
            #sys.exit(21)

            command = "" # Cleanup
    
    # Verifica a Regra Virtuo
    regra_virtuo_aplicada = False

    if 'Virtuo' in notebook.get('os') or 'virtuo' in notebook.get('os'):
        if 'A52 ION' in sap.description(notebook.get('ordemservico')):
            command = "Dism /apply-image /imagefile:Z:\\windows_images\\DWOS\\IMG_A52ION_A70ION\\A52Ion_1_0_0.wim /index:1 /ApplyDir:W:\\"
            os.system(command)
            print("[Straumann] Imagem Virtuo A52 ION")
            regra_virtuo_aplicada = True

    if 'Virtuo' in notebook.get('os') or 'virtuo' in notebook.get('os'):
        if 'A70 ION' in sap.description(notebook.get('ordemservico')):
            command = "Dism /apply-image /imagefile:Z:\\windows_images\\DWOS\\IMG_A52ION_A70ION\\A70Ion_1_0_0.wim /index:1 /ApplyDir:W:\\"
            os.system(command)
            print("[Straumann] Imagem Virtuo A70 ION")
            regra_virtuo_aplicada = True

    if not regra_virtuo_aplicada:
    # #################################################
    # TRACK START #####################################
        logstep("01700 - Dump data in storage - System (step 2 of 2)")

    # modo de espera operacional
        time.sleep(5)
        command = "Dism /apply-image /imagefile:" + str(notebook.get('system')) + " /index:1 /ApplyDir:w:\\ "

        operation = av_factory.cmdexec(command)

    if not operation['success']:
        #print("Imagem aplicada:", command)
        #print("Falha 22 - Comando:", command)
        #sys.exit(22)

        command = ""  # Cleanup
   
    # #################################################
    # TRACK START #####################################
    logstep("01800 - Memory Test Initial")

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
    
    
    
    
    # #################################################
    # TRACK START #####################################
    logstep("02000 - Copy Testing tools to Administrator's Desktop (step 1 of 2)")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Desktop\\ W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np"

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
    logstep("02100 - Copy Testing tools to Administrator's Desktop (step 2 of 2)") # Gabriel focar nessa parte (Necessario alteração)

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    if (notebook.get('code')[:3]=='ST2'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www2\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np" 
    elif (notebook.get('code')[:3]=='A55'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www3\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np" 
    elif (notebook.get('code')[:3]=='A57'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www3\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
    
    elif (notebook.get('code')[:3]=='BOL'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www4\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    elif (notebook.get('code')[:3]=='C65'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www1\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    elif (notebook.get('code')[:3]=='A72'):
       command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www1\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"

        
     # BON LITE NEW #
    
    elif (notebook.get('code')[:4]=='BOLB'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwbonlitenew\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"   
         
        
     # A52 HYB NEW i5 #
    
    elif (notebook.get('code')[:8]=='A52D125K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwhybnew\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A52 HYB NEW i7 #
    
    elif (notebook.get('code')[:8]=='A52D127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwhybnew\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A52 ION #
   
    elif (notebook.get('code')[:8]=='A52D127N'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwion\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A72 ION #
    
    elif (notebook.get('code')[:8]=='A72D137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwion\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # A70 ION #

    elif (notebook.get('code')[:8]=='A70D137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwion\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # STORM GO 4060 #
        
    elif (notebook.get('code')[:8]=='STGD137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstgo\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # STORM GO 4070 #
        
    elif (notebook.get('code')[:8]=='STGD137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstgo\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"


        # STORM GO BRANCO 4060 #
        
    elif (notebook.get('code')[:8]=='GM6PX0Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstgo\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
    
        # STORM GO BRANCO 4070 #
        
    elif (notebook.get('code')[:8]=='GM6PX7Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstgo\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"

        
        # STORM X 4080 #
        
    elif (notebook.get('code')[:8]=='STXD137R'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstx\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"    
        
        # STORM X 4090 #
        
    elif (notebook.get('code')[:8]=='STXD139S'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstx\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"


        #ADICIONADO PARA A SERIE STORM BS======================================================================================================================
        # STORM BS 3050 I5
    elif (notebook.get('code')[:8]=='STBD125K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstbs\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"

        # STORM BS 3050 I7
    elif (notebook.get('code')[:8]=='STBD127K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstbs\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"

        # STORM BS 4050 I7
    elif (notebook.get('code')[:8]=='STBD127N'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwstbs\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
        #ADICIONADO PARA A SERIE STORM BS======================================================================================================================
    
    # A65 ION - ADICIONADO 25/11/2023 - INACIO
    elif (notebook.get('code')[:8]=='A65D129P'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\wwwion\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
        #ADICIONADO PARA A SERIE STORM BS======================================================================================================================
        
        
    # A62 LIV - ADICIONADO 05/12/2023 - INACIO
    elif (notebook.get('code')[:8]=='A62D107B'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\LIV\\www\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"
        
   

    #print("DEBUG ESTOU AQUI")
    
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
                "Falha  Testes Amaury", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped 26")
    command = "" # Cleanup
    
    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Desktop1\\ W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np"
    # command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\DesenvolvimentoMao\\ATALHO\\ W:\\Users\Administrador\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup /e /NFL /NDL /NJH /NJS /nc /ns /np"
    if command:
        operation = av_factory.cmdexec(command)

        if int(operation['exitstatus']) not in [0, 1, 2, 3]:
            print(
                "Falha Testes Eng:", command
            )
            print("ExitStatus=", operation['exitstatus'])

            sys.exit(26)
    else:
        print("Skipped Testes Amaury")
    
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


    #command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\teclado\\%s\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np" % notebook.get('code')[:3]
    #if command:
        #operation = av_factory.cmdexec(command)

        #if int(operation['exitstatus']) not in [0, 1, 2, 3]:
         #   print(
          #      "Falha 26 - Comando:", command
           # )
            #print("ExitStatus=", operation['exitstatus'])

            #sys.exit(26)
    #else:
     #   print("Skipped 26")

    #command = "" # Cleanup
    
    logstep("01900 - Dump computer's manual") 
    

    '''
    if (notebook.get('code')[:8]=='A52D127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\HYBNEW\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
        
    elif (notebook.get('code')[:4]=='A52D125K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\HYBNEW\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]

    
    elif (notebook.get('code')[:4]=='BOLB'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:4]
        
    elif (notebook.get('code')[:8]=='A52D127N'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]    
    
    '''
    
    
    
    # BON LITE NEW #
    
    if (notebook.get('code')[:4]=='BOLB'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:4]
         
        
     # A52 HYB NEW i5 #
    
    elif (notebook.get('code')[:8]=='A52D125K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\HYBNEW\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # A52 HYB NEW i7 #
    
    elif (notebook.get('code')[:8]=='A52D127K'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\HYBNEW\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # A52 ION #
   
    elif (notebook.get('code')[:8]=='A52D127N'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]
    
        # A72 ION #
    
    elif (notebook.get('code')[:8]=='A72D137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # A70 ION #

    elif (notebook.get('code')[:8]=='A70D137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # STORM GO 4060 #
        
    elif (notebook.get('code')[:8]=='STGD137P'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # STORM GO 4070 #
        
    elif (notebook.get('code')[:8]=='STGD137Q'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]


        # STORM GO BRANCO 4060 #===========================================================================================================================
        
    elif (notebook.get('code')[:8]=='GM6PX0Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
        # STORM GO BRANCO 4070 #===========================================================================================================================
        
    elif (notebook.get('code')[:8]=='GM6PX7Z'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]


        # STORM X 4080 #
        
    elif (notebook.get('code')[:8]=='STXD137R'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]   
        
        # STORM X 4090 #
        
    elif (notebook.get('code')[:8]=='STXD139S'):
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    

    #ADICIONADO PARA A SERIE STORM BS======================================================================================================================
    #AJUSTANDO... FALTA ADICIONAR O MANUAL NOVO
        # STORM BS 3050 I5
    elif (notebook.get('code')[:8]=='STBD125K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]

    elif (notebook.get('code')[:8]=='STBD127K'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]

    elif (notebook.get('code')[:8]=='STBD127N'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:8]

    #ADICIONADO PARA A SERIE STORM BS======================================================================================================================
    
   
    #ADICIONADO A65 ION 25/11/2023 - INACIO ======================================================================================================================
    elif (notebook.get('code')[:8]=='A65D129P'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]

    #ADICIONADO A62 LIV 05/12/2023 - INACIO ======================================================================================================================
    elif (notebook.get('code')[:8]=='A62D107B'):
         command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\LIV\\MANUAL\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]


    #ADICIONADO PARA A SERIE STORM BS======================================================================================================================

    else:
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\Manual\\%s\\ w:\\users\\public\\Desktop\\ *.pdf /e" % notebook.get('code')[:3]
    
    
    
        
        
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
    
    
    
    logstep("00000 - Writing SKU NB")
    
    

    codigo_item = sap.cod_item(notebook.get('ordemservico'))

   
    command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /SK %s''' % codigo_item

    operation = av_factory.cmdexec(command)

    command = ""  # Limpeza
    
    
   
    
    t1.join()
       
    # #################################################
    # TRACK START #####################################
    logstep("02200 - At least, finishing...")

    # Comandos a seguir servem para gravar um log do sistema que é usado para a aplicação da imagem.
    
    
    #####################VERIFICAR AQUI SOBRE O AVELL LIC  /   TALVEZ DAR UM REBOOT AQUI.
    
    
    #if "Windows" in notebook.get('os'):
    #    color('yellow')
    #    print(
    #        '''\n\n\n\n\n\n
    #            Executar o comando a seguir, para ativar o sistema operacional:
    #            \n
    #            avell lic23
    #            \n\n\n\n\n\n
    #        '''
    #    )
    #elif "Virtuo" in notebook.get('os'):
    #    color('yellow')
    #    print(
    #        '''\n\n\n\n\n\n
    #            Executar o comando a seguir, para ativar o sistema operacional:
    #            \n
    #            avell lic23
    #            \n\n\n\n\n\n
    #        '''
    #    )
    ##else:
    #    print("Sem sistema operacional.")
    #    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\SEMSO.txt W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" # Copiado um arquivo para travar o work quando for dado no teste
        
        #operation = av_factory.cmdexec(command)
        #command = "" # Cleanup


        #Gravacao de CBR
    #    command = ""
            
    #    operation = av_factory.cmdexec(command)
    #    if not operation['success']:
    #        print(
    #            "FALHA AO GRAVAR LOG DE CBR:", command
    #            )
    #        print(
    #            "DEBUG:", operation
    #            )
    #        sys.exit(23)
        
    time.sleep(5)
    
    av_art.art_finished()
    command = "" # Cleanup


if __name__ == "__main__":
    start_time = time.time()
    main()