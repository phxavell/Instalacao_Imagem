"""
Avell Powercord status
"""

import json
import subprocess
import wmi


def get_serialnumber():
    serial = {}
    command = "wmic bios get serialnumber"
    process = subprocess.run(command, stdout=subprocess.PIPE)

    try:
        chave, valor = process.stdout.decode("utf-8").split()

    except ValueError:
        # Adaptacao tecnica emergencial para A60MUV.
        #print ('\n\nDEBUG: Controle de excecao:\n\n')
        chave = 'SerialNumber' # process.stdout # .decode("utf-8").split()
        valor = 'Standard'
    else:
        # Se chegou aqui, Go Horse!
        pass

    # Adaptacao tecnica para simulacao de serial,
    # em ambiente de teste. Se serial A, entao
    # simula serial B.

    if valor == 'AVNB_SERIALTESTE_A':
        serial[chave] = 'AVNB_SERIALTESTE_B'
    else:
        serial[chave] = valor

    return serial

def get_os():
    os = {}
    command = "wmic baseboard get serialnumber"
    process = subprocess.run(command, stdout=subprocess.PIPE)

    try:
        chave, valor = process.stdout.decode("utf-8").split()

    except ValueError:
        # Adaptacao tecnica emergencial para A60MUV.
        #print ('\n\nDEBUG: Controle de excecao:\n\n')
        chave = 'SerialNumber' # process.stdout # .decode("utf-8").split()
        valor = 'Standard'
    else:
        # Se chegou aqui, Go Horse!
        pass

    # Adaptacao tecnica para simulacao de serial,
    # em ambiente de teste. Se serial A, entao
    # simula serial B.
    if valor == 'AVNB_SERIALTESTE_A':
        os[chave] = 'AVNB_SERIALTESTE_B'
    else:
        os[chave] = valor
    return os



def get_uuid():

    uuid = {}
    command = "wmic csproduct get uuid"
    process = subprocess.run(command, stdout=subprocess.PIPE)
    chave, valor = process.stdout.decode("utf-8").split()
    uuid[str(chave).lower()] = valor

    return uuid




def get_biosversion():

    bios = {}
    command = "wmic bios get BIOSVersion"
    process = subprocess.run(command, stdout=subprocess.PIPE)

    for paramx in process.stdout.decode("utf-8").split():
        # Para os modelos Tong Fang.
        if paramx[:3] == '"N.':
            bios['bios'] = "%s" % paramx.replace('"', '').replace(',', '')

        # Adaptacao tecnica para atender demanda urgente por falha
        # de requisitos no A60MUV (purely Intel).
        if "QCCFL357" in paramx:
            bios['bios'] = "%s" % paramx.replace('"', '').replace(',', '')
            
            
        # Adaptacao tecnica para atender demanda urgente por falha
        # de requisitos no BON (purely Intel).
        if "BCTGL357" in paramx:
            bios['bios'] = "%s" % paramx.replace('"', '').replace(',', '')
            
        if "TBN" in paramx:
            bios['bios'] = "%s" % paramx.replace('"', '').replace(',', '')

    return bios


def get_ecversion():
    ec = {}
    major = {}
    command = "wmic BIOS get EmbeddedControllerMajorVersion"
    process = subprocess.run(command, stdout=subprocess.PIPE)
    chaveA, valorA = process.stdout.decode("utf-8").split()
    major[chaveA] = valorA

    minor = {}
    command = "wmic BIOS get EmbeddedControllerMinorVersion"
    process = subprocess.run(command, stdout=subprocess.PIPE)
    chaveB, valorB = process.stdout.decode("utf-8").split()
    minor[chaveB] = valorB

    ec['ec'] = '%s.%s.00' % (major[chaveA], minor[chaveB])

    return ec


def battery_status():
    """Return if powercord is connected/powered"""
    status = False
    for instance in wmi.WMI().query("Select BatteryStatus From Win32_Battery"):
        for attribute in instance._properties:
            if attribute == "BatteryStatus":
                if getattr(instance, attribute) == 2:
                    status = True
                else:
                    status = False

    return status


def get_vmstatus():
    state = False
    vm = {}
    command = "wmic CSProduct get Vendor"
    process = subprocess.run(command, stdout=subprocess.PIPE)
    chave, valor = process.stdout.decode("utf-8").split()
    vm[chave] = valor
    if valor == "QEMU":
        state = True

    # Se for maquina virtual
    vm['vm'] = True

    return vm


def main():
    #pass
    #print("%s" % battery_status())
    #print(get_serialnumber())
    print(get_biosversion())

if __name__ == "__main__":
    main()
