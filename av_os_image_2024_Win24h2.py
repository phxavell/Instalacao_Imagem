
import sys
import os

def origem():
    for k in range(ord('a'), ord('z')+1):
        if os.path.exists(f'{chr(k)}:\\windows_images\\WIN24H2\\win11pro24h2.wim'): 
            return chr(k)
        elif os.path.exists(f'{chr(k)}:\\windows_images\\WIN24H2\\win11hsl.wim'): 
            return chr(k)
        

def check(HWCode=None, OS=None):
    print(f"Sistema Operacional: {OS}")

    image = {}

    if OS in [
        'Windows 10 Home',
        'Windows 10 HSL',
        
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
        'Sem Sistema operacional',
        'Sem sistema operacional',
        'SEM SO'
    ]:
        image['winname'] = 'Windows 11 PRO (Sem SO)'
        image['wincode'] = 'win11pro24h2SEMSO'
        
    elif OS in [
        'Virtuo',
        'virtuo'
    ]:
        image['winname'] = 'Windows 10 Professional'
        image['wincode'] = 'virtuo'






    if image['wincode'] == 'win10hsl':
            
        image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
        image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'

    elif image['wincode'] == 'win10pro':
        image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10PRO20h2.wim'
        image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'
    
    elif image['wincode'] == 'win11hsl':
        image['system'] = f'{origem()}:\\windows_images\\WIN24H2\\win11hsl.wim'
        image['recovery'] = ''
    
    elif image['wincode'] == 'win11pro24h2SEMSO':
        image['system'] = f'{origem()}:\\windows_images\\WIN24H2\\win11pro24h2SEMSO.wim'
        image['recovery'] = ''

    elif image['wincode'] == 'win11pro':
        image['system'] = f'{origem()}:\\windows_images\\WIN24H2\\win11pro24h2.wim'
        image['recovery'] = ''
            
    elif image['wincode'] == 'virtuo':
        image['system'] = 'Z:\\windows_images\\DWOS\\IMG_A52ION_A70ION\\A52Ion_1_0_0.wim'
        image['recovery'] = ''
    
    else:
        image['system'] = 'Z:\\windows_images\\GERAL20210526\\Windows10HSL20h2.wim'
        image['recovery'] = 'Z:\\windows_images\\GERAL20210526\\winre.wim'


    return(image)
    