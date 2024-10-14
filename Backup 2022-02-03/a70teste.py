#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import subprocess
import sys
import time

import av_art
import av_factory
import av_os_image
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
    
    time.sleep(1)
    process = subprocess.Popen('z:\scripts\TFGTools\OemServiceWinApp.exe rwblock0 /load /file "z:\scripts\oem_a70d107.txt" ')

   

if __name__ == "__main__":
    start_time = time.time()
    main()
