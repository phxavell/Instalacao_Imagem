#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


def art_avell_notebooks():
    """Show Avell ASCII logo"""

    verde = lambda: os.system('color 02') # on Windows System
    verde()

    text = """    _            _ _    _   _       _       _                 _        
   / \\__   _____| | |  | \\ | | ___ | |_ ___| |__   ___   ___ | | _____ 
  / _ \\ \\ / / _ \\ | |  |  \\| |/ _ \\| __/ _ \\ \'_ \\ / _ \\ / _ \\| |/ / __|
 / ___ \\ V /  __/ | |  | |\\  | (_) | ||  __/ |_) | (_) | (_) |   <\\__ \\
/_/   \\_\\_/ \\___|_|_|  |_| \\_|\\___/ \\__\\___|_.__/ \\___/ \\___/|_|\\_\\___/"""

    print(text)

def screen_clear():
    clear = lambda: os.system('cls')  # on Windows System
    clear()


def art_finished():

    verde = lambda: os.system('color 02')  # on Windows System
    verde()

    print(" _____ _             _ _              _       ")
    print("|  ___(_)_ __   __ _| (_)______ _  __| | ___  ")
    print("| |_  | | '_ \ / _` | | |_  / _` |/ _` |/ _ \ ")
    print("|  _| | | | | | (_| | | |/ / (_| | (_| | (_) |")
    print("|_|   |_|_| |_|\__,_|_|_/___\__,_|\__,_|\___/ ")
    print("                                              ")
    print("                                              ")
    print("\nRemover o cabo de rede.\n")
    print("\nRemover as unidades de armazenamento removiveis (pendrives).\n")
    print("\nPressionar ALT+F4 ou fechar esta janela.\n")


def art_serial():

    amarelo = lambda: os.system('color 06')  # on Windows System
    amarelo()

    print(" ____            _       _ ")
    print("/ ___|  ___ _ __(_) __ _| |")
    print("\___ \ / _ \ '__| |/ _` | |")
    print(" ___) |  __/ |  | | (_| | |")
    print("|____/ \___|_|  |_|\__,_|_|")
    
    
def art_os():

    amarelo = lambda: os.system('color 06')  # on Windows System
    amarelo()

    print(" _____   ____   ")
    print("/  _  \ / ___|  ")
    print("| / \ | \___ \  ")
    print("| \_/ |  ___) | ")
    print("\_____/ |____/  ")



def main():
    pass


if __name__ == "__main__":
    main()
