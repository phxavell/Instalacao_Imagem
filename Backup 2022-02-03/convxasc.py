

def hex_2ascii(param):
    # Slice string to remove leading `0x`
    # hex_string = "0x616263"[2:]
    hex_string = str(param)

    # Convert to bytes object
    bytes_object = bytes.fromhex(hex_string)

    # Convert to ASCII representation
    ascii_string = bytes_object.decode("ASCII")

    # print it
    print("%s" % ascii_string)



def main():

    hex_demo = '010000000000000001000000000000001d0000004b325848542d4e56504a4d2d48574436582d52375732432d4254444643'


    hex_2ascii(hex_demo)




if __name__ == '__main__':
    main()


