#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def check(HWCode=None, OS=None):

    image = {}

    if OS in [
        'Windows 10 Home',
        'Windows 10 HSL',
        'Sem Sistema operacional',
        'Sem sistema operacional',
        'Sem SO'
    ]:
        image['winname'] = 'Windows 10 Home Single Language'
        image['wincode'] = 'win10hsl'

    elif OS in [
        'Windows 10 Pro',
        'Windows 10 Professional'
    ]:
        image['winname'] = 'Windows 10 Professional'
        image['wincode'] = 'win10pro'


    if HWCode[:7] == "A40A35M":

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A40LIV\\Windows10HSL20H2\\WINDOWS10HSL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A40LIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A40LIV\\WINDOWS10PRO20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A40LIV\\WINDOWS10PRO20H2\\WINRE.wim'

    elif HWCode[:8] == 'A52D105B':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] == 'A52D105D':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:7] == 'A52F91A':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:7] == 'A60D91C':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A60MUV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A60MUV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A60MUV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A60MUV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] in ['A62D107B', 'A62D107D']:


        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A62GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                # image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'

                image['recovery'] = 'z:\\windows_images\\A62GTXLIV\\Windows10HSL20H2\\winre.wim'
                # image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A62GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                # image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'

                image['recovery'] = 'z:\\windows_images\\A62GTXLIV\\Windows10Pro20H2\\WINRE.wim'
                # image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

    elif HWCode[:8] == 'A62D107E':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A62GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                # image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'

                image['recovery'] = 'z:\\windows_images\\A62GTXLIV\\Windows10HSL20H2\\winre.wim'
                # image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A62GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                # image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'

                image['recovery'] = 'z:\\windows_images\\A62GTXLIV\\Windows10Pro20H2\\WINRE.wim'
                # image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'


    elif HWCode[:7] == 'A62F91B':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A52GTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] in ['A65D107E', 'A65D107F']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\A65RTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A65RTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\A65RTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\A65RTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] in ['C62D105B', 'C62D107B', 'C62D107D']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\C62GTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C62GTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'z:\\windows_images\\C62GTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C62GTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] == 'C62D107E':

        if image['wincode'] == 'win10hsl':
                image['system'] = 'z:\\windows_images\\C62RTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C62RTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':

                image['system'] = 'z:\\windows_images\\C62RTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C62RTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:8] in ['C65D107F', 'C65D107G', 'C65D109F', 'C65D109G']:

        if image['wincode'] == 'win10hsl':

                image['system'] = 'z:\\windows_images\\C65RTXLIV\\Windows10HSL20H2\\WINDOWS10HOMESL20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C65RTXLIV\\Windows10HSL20H2\\winre.wim'

        if image['wincode'] == 'win10pro':

                image['system'] = 'z:\\windows_images\\C65RTXLIV\\Windows10Pro20H2\\WINDOWS10PRO20H2.wim'
                image['recovery'] = 'z:\\windows_images\\C65RTXLIV\\Windows10Pro20H2\\WINRE.wim'

    elif HWCode[:5] in ['ST1A4']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

    elif HWCode[:8] in ['A70D107H', 'A70D107I']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

    elif HWCode[:8] in ['A72D107H', 'A72D107I']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
                
                
    elif HWCode[:8] in ['C62D107H']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
                
    elif HWCode[:8] in ['C65D107H', 'C65D107I']:

        if image['wincode'] == 'win10hsl':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
                
                
    
    
    elif HWCode[:8] in ['BOND117X', 'BOND115X', 'A52D115K', 'A65D117H', 'A65D117I', 'A70D117K', 'A70D117H', 'C62D115K', 'C62D117K', 'C62D117H', 'C65D117I', 'C65D117J','C65D119J']:
        
        if image['wincode'] == 'win10pro':
                image['system'] = 'Z:\\windows_images\\DWOS\\DWOWinPRO.wim'
                image['recovery'] = 'Z:\\windows_images\\DWOS\\winre.wim'  
       




        # ??? 2021-11-03  ---- Teste Pendrive Imagem
        #if image['wincode'] == 'win10hsl':
                #image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
                #image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        #if image['wincode'] == 'win10pro':
                #image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
                #image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
    
    #        write2Desktop(
    #            image['wincode'],
    #            image['winname']
    #        )



    else:
        print('DEBUG: Falha geral na selecao de imagem')
        sys.exit(99)


    return(image)


    #  DENTAL
    #  image['system'] = 'z:\\windows_images\\DENTALWINGS\\C62RTXLIV\\DWIOL-05-BRXXXX.win'
    #  image['recovery'] = 'z:\\windows_images\\DENTALWINGS\\C62RTXLIV\\winre.wim'
    #  image['system'] = 'z:\\windows_images\\DENTALWINGS\\C65MUVGTX\\DWIOL-04-BR.wim'
    #  image['recovery'] = 'z:\\windows_images\\DENTALWINGS\\C65MUVGTX\\winre.wim'


#def write2Desktop(filename='', content=''):
#    f = open('w:\users\administrador\desktop\' + filename + '.txt','w+')
#    f.write(content)
#    f.close()
