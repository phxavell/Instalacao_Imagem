#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# LOG 2020-09-14 Arquivo criado.
# LOG 2021-08-09 Considerar exclusao. Nao ah evidencia de uso.


import os
import sys
import pywintypes
import subprocess
import time
import win32com.client
import av_art
import notebook_hwinfo
import odoo_hwinfo


def Trim(linha: str):
    return (linha.lstrip()).rstrip()


def Left(linha: str, index: int):
    return linha[0:index]


def Right(linha: str, index: int):
    return linha[-index:]


def netmap(driverletter, fullpath, username, password):
    """Map unit drive"""

    strcmdmap = "net use %s: %s /user:%s %s" % (
        driverletter, fullpath, username, password
    )

    # print("DEBUG_COMMAND\n%s" % strcmdmap)

    subprocess.call(strcmdmap, shell=True)

    time.sleep(2)

def netmapunauth(driverletter, fullpath):
    """Map unit drive"""

    strcmdmap = "net use %s: %s" % (
        driverletter, fullpath
    )

    # print("DEBUG_COMMAND\n%s" % strcmdmap)

    subprocess.call(strcmdmap, shell=True)


def main():

    # Forcar mensagem ao montador para conectar
    # fonte de energia externa.
    while not notebook_hwinfo.battery_status():
        print("Ligar a fonte de alimentacao!!!\n\n")
        time.sleep(0.75)

    if len(sys.argv) == 2:
        if sys.argv[1][:4] == "AVNB":
            strSerialNumber = sys.argv[1]
        else:
            print("Falha ne serial = erro 101")
            sys.exit(5)
    else:
        # Obter numero de serie
        strSerialNumber = str(notebook_hwinfo.get_serialnumber()['SerialNumber'])


    hw = odoo_hwinfo.process(strSerialNumber)

    hw_os = hw.get('os')
    hw_screen = hw.get('screen')
    hw_name = hw.get('name_tm')
    hw_code = hw.get('code')

    hw = odoo_hwinfo.process(strSerialNumber)

    strScreenSize = hw.get('screen')

    print(
        "Instalar %s no produto [%s] %s com tela de %s polegadas (SN=%s)." % (
            hw_os, hw_code, hw_name, hw_screen, strSerialNumber
        )
    )

    if str(hw_os) in ['Sem sistema operacional', 'Sem SO']:
        print("Sem sistema operacional. Fim.")
        exit(0)

    # Local dos scripts de execucao
    netmap(
        "L",
        "\\\\tucuma1\\Window$",
        "avellbasic",
        "macaX3ra19"
    )

    if str(hw_os) in ['Windows 10 Home', 'Windows 10 HSL']:
        netmap(
            "J",
            "\\\\tucuma2\\Window$\\Export\\Home",
            "avellbasic",
            "macaX3ra19"
        )

        netmap(
            "I",
            "\\\\tucuma2\\Window$\\Import",
            "avellbasic",
            "macaX3ra19"
        )

    if hw_os == "Windows 10 Pro":
        netmap(
            "J",
            "\\\\tucuma3\\Window$\\Export\\Pro",
            "avellbasic",
            "macaX3ra19"
        )
        netmap(
            "I",
            "\\\\tucuma3\\Window$\\Import",
            "avellbasic",
            "macaX3ra19"
        )

    strSNFile = "X:/output_SP.txt"

    strPasta = "J:\\"

    count = 0
    blResult = True

    time.sleep(2)

    # as variáveis abaixo são necessárias para montar o .cfg no final do script
    strSNFileDISK = Left(strSNFile, 2) + "\\"
    strPastaDISK = Left(strPasta, 2) + "\\"

    # Set strArquivos = fso.getfolder(strPasta) --> manipular diretório
    os.chdir(strPasta)
    strInputFile = ""
    for strArq in os.listdir(strPasta):
        if strArq.endswith(".xml"):
            if not(os.path.isfile(Left(strArq, len(strArq) - 4) + ".cfg")):
                if count == 0:
                    strInputFile = strArq
                    strCFGFile = Left(strArq, len(strArq) - 4) + ".cfg"
                    strBINFile = Left(
                        strInputFile, len(strInputFile) - 4
                    ) + ".bin"
                    strOutputFile = Left(
                        strInputFile, len(strInputFile) - 4
                    ) + "_out.xml"
                    count = 1
                # End if
            else:
                strCFGFileExiste = Left(strArq, (len(strArq) - 4)) + ".cfg"
                # print(strCFGFileExiste)
                with open(strCFGFileExiste, "r") as f:
                    linha = str(f.readline())
                    strCFGFileSN = ""
                    while linha:
                        linha = Trim(linha)
                        if linha == "<Name>ZPC_MODEL_SKU</Name>":
                            # Aqui ele lerah a proxima linha.
                            # Obrigatoriamente esta linha nao deve ser vazia.
                            linha = str(f.readline())
                            tamanho = len(Trim(linha)) - 7
                            strCFGFileSN = Right(Trim(linha), tamanho)
                            tamanho = tamanho - 8
                            strCFGFileSN = Left(strCFGFileSN, tamanho)
                            # O tamanho de strCFGFileSN deveria ser 11,
                            # mas nesse caso é 13. Deve estar errado.
                        # End if
                        linha = str(f.readline())
                    # Loop
                    if strCFGFileSN == strSerialNumber:
                        # print(strCFGFileSN, strSerialNumber)
                        print("Arquivo inspecionado:", strCFGFileExiste, "(Considerar .bin)")
                        blResult = False
                        print(
                            "Chave Windows ja associada para o NS=%s"
                            % strSerialNumber)
                        exit(5)

    time.sleep(2)

    if os.path.isfile(strInputFile):
        with open(strInputFile, "r") as f:
            linha = str(f.readline())
            while linha:
                strID = ''
                Id = Left(Trim(linha), 14)
                if Id == "<ProductKeyID>":
                    Id = Right(linha, 29)
                    Id = Left(Id, 13)
                    strID = str(Id)
                    # print("Debug info A1 (ultima chave lida):", strID)
                # End if

                sku = Left(Trim(linha), 22)
                strSKU = ''
                if sku == "<ProductKeyPartNumber>":
                    # print("DEBUG: sku=%s\n" % sku)
                    sku = Right(linha, 33)
                    # print("DEBUG: sku=%s\n" % sku)
                    sku = Left(sku, 9)
                    # print("DEBUG: sku=%s\n" % sku)
                    if sku == "KU9-00002" or sku == "KU9-00001" or sku == "FQC-08797" or sku == "FQC-08800":
                        strSKU = str(sku)
                        print("Microsoft SKU:", strSKU)
                    else:
                        blResult = False
                    # End if
                # End if
                linha = str(f.readline())
            # Loop

        time.sleep(2)  # end with open...

        if blResult:
            # print(strCFGFile)
            time.sleep(1)
            if not(os.path.isfile(strCFGFile)):
                with open(strCFGFile, "a") as f:
                    f.write("<OA3>\n")
                    f.write(" <FileBased>\n")
                    f.write("       <InputKeyXMLFile>" + strPastaDISK + strInputFile + "</InputKeyXMLFile>\n")
                    f.write("    <Parameters>\n")
                    f.write("      <Parameter name=\"" + "LicensablePartNumber" + "\"" + " value=\"" + strSKU + "\"" + " />\n")
                    f.write("      <Parameter name=\"" + "OEMPartNumber" + "\"" + " value=\"" + strID + "\"" + " />\n")
                    f.write("         <OEMOptionalInfo> \n")
                    f.write("              <Field> \n")
                    f.write("                <Name>ZPC_MODEL_SKU</Name> \n")
                    f.write("                <Value>" + strSerialNumber + "</Value> \n")
                    f.write("              </Field> \n")
                    f.write("              <Field> \n")
                    f.write("                <Name>ZFRM_FACTOR_CL1</Name> \n")
                    f.write("                <Value>Notebook</Value> \n")
                    f.write("              </Field> \n")
                    f.write("              <Field> \n")
                    f.write("                <Name>ZFRM_FACTOR_CL2</Name> \n")
                    f.write("                <Value>Standard</Value> \n")
                    f.write("              </Field> \n")
                    f.write("              <Field> \n")
                    f.write("                <Name>ZSCREEN_SIZE</Name> \n")
                    f.write("                <Value>" + str(strScreenSize) + "</Value> \n")
                    f.write("              </Field> \n")
                    f.write("              <Field> \n")
                    f.write("                <Name>ZTOUCH_SCREEN</Name> \n")
                    f.write("                <Value>Non-Touch</Value> \n")
                    f.write("              </Field> \n")
                    f.write("         </OEMOptionalInfo>\n")
                    f.write("<BusinessID>2671</BusinessID>\n")
                    f.write("    </Parameters>\n")
                    f.write("  </FileBased>\n")
                    f.write("  <OutputData>\n")
                    f.write("    <AssembledBinaryFile>" + strPastaDISK + strBINFile + "</AssembledBinaryFile>\n")
                    f.write("    <ReportedXMLFile>" + strPastaDISK + strOutputFile + "</ReportedXMLFile>\n")
                    f.write("  </OutputData>\n")
                    f.write("</OA3>\n")

                time.sleep(3)

                ###
                strExec1 = "L:\Export\oa3tool.exe /assemble /configfile=%s" % (
                    strCFGFile
                )
                # print("DEBUG linha1 = %s" % strExec1)
                subprocess.call(strExec1, shell=True)
                time.sleep(3)

                ###
                strExec2 = "L:\Export\\afuwinx64.exe /a%s" % (strBINFile)
                # print("DEBUG linha2 = %s" % strExec2)
                subprocess.call(strExec2, shell=True)
                time.sleep(3)

                ###
                strExec3 = "L:\Export\oa3tool.exe /report /configfile=%s" % (
                    strCFGFile
                )
                # print("DEBUG linha3 = %s" % strExec3)
                subprocess.call(strExec3, shell=True)
                time.sleep(3)

                ###
                strExec4 = "L:\\Export\\oa3tool.exe /Validate"
                # print("DEBUG linha4 = %s" % strExec4)
                check_active = subprocess.call(strExec4, shell=True)
                if check_active == 0:
                    pass
                    # O licenca do Windows estah instalada
                    # na tabela MSDM do UEFI \o/
                else:
                    print("ERRO DE RETORNO: %s\n" % check_active)



                    # ./Export/HOME/3273088409417.bin
                    # ./Export/HOME/3273088409417.cfg
                    # ./Export/HOME/3273088409417.xml
                    # ./Export/HOME/3273088409417_out.cfg
                    # ./Export/HOME/3273088409417_out.xml


                    # Aqui move(re)mos todos para a Quarentena!!!
                    exit(150)

                time.sleep(3)


                ###
                strExec5 = "move %s I:\\" % (strOutputFile)
                print("DEBUG linha5 = %s" % strExec5)
                subprocess.call(strExec4, shell=True)
                time.sleep(1)

                # Se chegou ateh aqui, tudo deu certo :)
                av_art.art_finished()

            # End if
        else:
            print("Nenhuma chave de Windows disponível (1.1)")
        # End if
    else:
        print("Nenhuma chave de Windows disponível (1.2)")
    # End if


if __name__ == "__main__":
    main()
