import subprocess

###
strExec4 = "L:\\Export\\oa3tool.exe /Validate"
print("DEBUG: linha4 = %s" % strExec4)
aaa = subprocess.call(strExec4, shell=True)

if aaa == 0:
    print("Deu certo!!!")
else:
    print("ERRO DE RETORNO: %s\n" % aaa)
    exit(150)



