#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def origem():
    for k in range(ord('a'), ord('z')+1):
        if os.path.exists(f'{chr(k)}:\\windows_images\\Win11\\win11pro.wim'): 
            return chr(k)
        elif os.path.exists(f'{chr(k)}:\\windows_images\\Win11\\win11hsl.wim'): 
            return chr(k)
        

def check(HWCode=None, OS=None):

    image = {}

    if OS in [
        'Windows 10 Home',
        'Windows 10 HSL',
        'Sem Sistema operacional',
        'Sem sistema operacional',
        'SEM SO'
    ]:
        image['winname'] = 'Windows 10 Home Single Language'
        image['wincode'] = 'win10hsl'

    elif OS in [
        'Windows 10 Pro',
        'Windows 10 PRO',
        'Windows 10 Professional'
    ]:
        image['winname'] = 'Windows 10 Professional'
        image['wincode'] = 'win10pro'
        
        
    elif OS in [
        'Windows 11 Home',
        'Windows 11 HSL'
    ]:
        image['winname'] = 'Windows 11 Home Single Language'
        image['wincode'] = 'win11hsl'

    elif OS in [
        'Windows 11 Pro',
        'Windows 11 PRO',
        'Windows 11 Professional'
    ]:
        image['winname'] = 'Windows 11 Professional'
        image['wincode'] = 'win11pro'

    elif OS in [
        'Virtuo',
        'virtuo'
    ]:
        image['winname'] = 'Windows 10 Professional'
        image['wincode'] = 'virtuo'
    
    if HWCode[:8] in ['BOND117X', 'BOND115X', 'A52D115K', 'A65D117H', 'A65D117I', 'A70D117K', 'A70D117H', 'C62D115K', 'C62D117K', 'C62D117H', 'C65D117I', 'C65D117J','C65D119J', 'B11D117K']:
        if image['wincode'] == 'win10hsl':
                
            image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
            image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

        if image['wincode'] == 'win10pro':
            image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
            image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
        
        if image['wincode'] == 'win11hsl':
                image['system'] = f'{origem()}:\\windows_images\\Win11\\win11hsl.wim'
                image['recovery'] = ''

        if image['wincode'] == 'win11pro':

                image['system'] = f'{origem()}:\\windows_images\\Win11\\win11pro.wim'
                image['recovery'] = ''
                
        if image['wincode'] == 'virtuo':
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
        print('DEBUG: Falha geral na selecao de imagem - Chamar Gabriel')
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
