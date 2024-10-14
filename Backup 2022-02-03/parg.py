import sys

def aaa():

    print("O tamanho dos argumentos eh %s." % len(sys.argv))
    if len(sys.argv) == 2:
        if sys.argv[1][:4] == "AVNB":
            print("Prefixo Ok\n")
            strSerialNumber = sys.argv[1]
        else:
            print("Falha ne serial = erro 101")
            sys.exit(101)


    print("O serial eh %s!" % strSerialNumber)

aaa()


