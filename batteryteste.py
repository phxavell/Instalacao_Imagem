#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import notebook_hwinfo

def main():
    status = battery_status()
    print("Status: %s" % status )
    print("DEBUG: AQUI")