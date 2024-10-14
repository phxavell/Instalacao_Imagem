#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

#import odoo_hwinfo



def process(in_serial):

    #hwz = odoo_hwinfo.process('AVNB2112215')
    #print(hwz)


    #output = {'name_tm':  'Notebook Avell A40 LIV', 'code':     'A40A35MHV5', 'screen':   '14',    'os':       'Windows 10 Pro'   }
    output = {'name_tm':  'Notebook Avell A40 LIV', 'code':     'A40A35MHV5', 'screen':   '14',    'os':       'Windows 10 HSL'   }
    #output = {'name_tm':  'Notebook Avell A40 LIV', 'code':     'A40A35MHV5', 'screen':   '14',    'os':       'Sem SO'   }

    #output = {'name_tm':  'Notebook Avell A62 LIV', 'code':     'A62D107D',   'screen':   '14',    'os':       'Windows 10 Pro'   }
    #output = {'name_tm':  'Notebook Avell A62 LIV', 'code':     'A62D107D',   'screen':   '14',    'os':       'Windows 10 HSL'   }
    #output = {'name_tm':  'Notebook Avell A62 LIV', 'code':     'A62D107D',   'screen':   '14',    'os':       'Sem SO'   }





    return output

if __name__ == "__main__":
    print(process('qualquer_coisa'))
