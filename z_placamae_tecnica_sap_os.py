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
import sap_connect as sap
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
        colorcode = '02'
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
    av_art.art_avell_notebooks()

    # #################################################
    # TRACK START #####################################
    logstep('00100 - Avell Notebooks - Starting setup')
    #for counter in range(5, 0, -1):
    #    print("." * counter, counter)
    #    time.sleep(1)

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

        #time.sleep(1.5)

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
    
    var_sn = sap.serial_chave()
    print(var_sn)
    #av_art.art_os()
    
    if not notebook.get('ordemservico') is None:  #===================================================#
        while True:
            
            #print('OP:' var_sn)
            var_os = var_sn
            #if var_os[:4] == 'INTR':  # Feito para identificar quando a máquina for uma interna
            notebook['ordemservico'] = var_os
            #    break
            #else:
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

        #if notebook.get('ordemservico')[:4] == 'INTR':  # Para maquina interna
        #    print("Informe o Numero de série: ")
        #    notebook['serialnumber'] = input("Serial: ")
        #else:
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
        #if notebook.get('ordemservico')[:4] == 'INTR':  # Pra pegar o codigo quando for uma maquina interna
        #    notebook['code'] = notebook.get('ordemservico')[4:12]
        #else:
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
    '''
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
    '''
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
    
    
    
    
    #if not (notebook.get('ordemservico')[:4] == 'INTR'): # Pra pegar o codigo quando for uma maquina interna
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
    
    

    
    
    
    directory = 'z:\logplaca2024'
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"{directory}\{notebook.get('serialnumber')} {timestamp}.txt"

    result = subprocess.run(['z:\\scripts\\avell_comparador.cmd'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    logsap = (f'''\n\n OP: {notebook.get('ordemservico')} \n\n DESCRIÇÃO: {sap.description(notebook.get('ordemservico'))} \n\n Code: {notebook.get('code')} \n\n Tela: {notebook.get('screen')} \n\n Sistema Operacional: {notebook.get('os')} \n\n BIOS: {notebook.get('bios')} \n\n NS: {notebook.get('serialnumber')}\n\n''' + "\n")

    with open(filename, 'a') as output_file:
     output_file.write(logsap)
     output_file.write(output)

    '''
# Copiando para o diretório C://TESTES_AVELL  - PARA SERVIR COMO CHAVE NO NOVO SCRIPT DE LICENÇAS
    destination_dir = 'W:\\'
    shutil.copy(filename, destination_dir)



    for counter in range(5, 0, -1):
        print("." * counter, counter)
        time.sleep(1)
        
    print('LOG GERADO COM SUCESSO\n')
    time.sleep(2)
    
    '''
    command = "z:\\scripts\\avell_abrir1.cmd"
    operation = av_factory.cmdexec(command)
 

    arquivo = open('z:\\logplaca2024\sistema.txt','a')
    arquivo.write(f'''\n\n OP: {notebook.get('ordemservico')} \n\n DESCRIÇÃO: {sap.description(notebook.get('ordemservico'))} \n\n Code: {notebook.get('code')} \n\n Tela: {notebook.get('screen')} \n\n Sistema Operacional: {notebook.get('os')} \n\n BIOS: {notebook.get('bios')} \n\n NS: {notebook.get('serialnumber')}\n\n Data/Hora: {datetime.datetime.now()}\n\n ___________________________________________________________________________________________________________''' + "\n")
    arquivo.close()

    command = "z:\\scripts\\avell_fechar1.cmd"
    operation = av_factory.cmdexec(command)

    command = "" # Cleanup
        
   
    logstep("Writing SKU NB")
    
    

    codigo_item = sap.cod_item(notebook.get('ordemservico'))

   
    command = '''Z:\\Scripts\\TFGTools\\AMIDEWINx64.EXE /SK %s''' % codigo_item

    operation = av_factory.cmdexec(command)

    command = ""  # Limpeza
    
       
    # #################################################
    # TRACK START #####################################
    logstep("02200 - At least, finishing...")

    # Comandos a seguir servem para gravar um log do sistema que é usado para a aplicação da imagem.
    
    
    #####################VERIFICAR AQUI SOBRE O AVELL LIC  /   TALVEZ DAR UM REBOOT AQUI.
    
    
    if "Windows" in notebook.get('os'):
        color('yellow')
        print(
            '''
            \n\n\n\n\n\n
                Executar o comando a seguir, para ativar o sistema operacional:
                \n
                avell lic3
                \n\n\n\n\n\n
            '''
        )
    elif "Virtuo" in notebook.get('os'):
        color('yellow')
        print(
            '''
            \n\n\n\n\n\n
                Executar o comando a seguir, para ativar o sistema operacional:
                \n
                avell lic3
                \n\n\n\n\n\n
            '''        
        )
    else:
        print("Sem sistema operacional.")
        command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\ION\\SEMSO.txt W:\\Users\Administrador\Desktop /e /NFL /NDL /NJH /NJS /nc /ns /np" # Copiado um arquivo para travar o work quando for dado no teste
        
        operation = av_factory.cmdexec(command)
        command = "" # Cleanup

    
    av_art.art_finished()
    command = "" # Cleanup
    
    
if __name__ == "__main__":
    start_time = time.time()
    main()