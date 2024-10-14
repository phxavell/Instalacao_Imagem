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

    # #################################################
    # TRACK START #####################################

    # #################################################
    # TRACK START #####################################
    logstep("02200 - Dump data in storage (step 2 of 2)")

    # modo de espera operacional
    time.sleep(5)

    #command = "Dism /apply-image /imagefile:Z:\\windows_images\\WIN11-23H2_14_11_2023\\WIN11_PRO_X64_23H2.wim /index:1 /ApplyDir:W:\ "
    #habilitar novamente esta linha
    #command = "Dism /apply-image /imagefile:Z:\\windows_images\\WIN11\\win11pro.wim /index:1 /ApplyDir:W:\ "

    #TESTE NOVA IMAGEM VIRTUO======================================================================================================
    #command = "Dism /apply-image /imagefile:Z:\\windows_images\\DWOS\\NOVA_IMAGEM_2024\\A70HYB_1_5_0.wim /index:1 /ApplyDir:W:\ "
    #TESTE NOVA IMAGEM VIRTUO======================================================================================================

    #NOVA IMAGEM WINDOWS 23H2
    command = "Dism /apply-image /imagefile:Z:\\windows_images\\IMG-23H2_NEW\\Win11ProV1_Final.wim /index:1 /ApplyDir:W:\ "
    #command = "Dism /apply-image /imagefile:Z:\\windows_images\\IMG-23H2_NEW\\Win11HSLV1_Final.wim /index:1 /ApplyDir:W:\ "
    
    #Linha utilizada para aplicar imagem no novo HYB MOB - Testado OK!
    #command = "Dism /apply-image /imagefile:Z:\\windows_images\\IMAGE_VIRTUO\\A70HYB.wim /index:1 /ApplyDir:W:\ "

    
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

    


    # #################################################
    # TRACK START #####################################
    logstep("02500 - Copy Testing tools to Administrator's Desktop")

    command = "x:\\Windows\\System32\\robocopy.exe z:\\construtor\\HYB\\www\\ W:\\Users\Administrador\Desktop\Teste /e /NFL /NDL /NJH /NJS /nc /ns /np"

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
    logstep("???? - Copy Wallpaper to Windows Wallpapers path.")

    command = "copy z:\\scripts\\go_to_desktop\\teste\\wallpaper\\*.jpg W:\\Windows\\Web\\Wallpaper\\"

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
    logstep("02700 - At least, finishing...")

    av_art.art_finished()


if __name__ == "__main__":
    start_time = time.time()
    main()
