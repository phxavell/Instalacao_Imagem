#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

def cmdexec(command):
    """
    Execute locally the command line as a shell command.
    It will return a result as a dict.
    """

    result = {}

    success = False

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    out, err = process.communicate()

    if process.returncode == 0:
        success = True

    result['success'] = success
    result['input'] = command
    result['output'] = out # .decode('utf-8')
    result['error'] = err.decode('utf-8')
    result['exitstatus'] = process.returncode

    return result



