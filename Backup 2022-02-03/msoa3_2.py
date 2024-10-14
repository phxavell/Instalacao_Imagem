#!/usr/bin/env python3
'''Windows Activation Tool'''


# ZZZ1 = FQC-08800 (sku da Microsoft)
# ZZZ2 = A52D105BHV2 (modelo do produto)
# ZZZ3 = AVNB2029172 (numero de serie)
# ZZZ4 = 17.3 (tamanho de tela)

def make_cfg(_sku, _model, _serial, _screen, _path):
    '''replace template's variables with parameters'''

    with open("z:\scripts_python\model.cfg", "r") as cfg_template:
        line = str(
            cfg_template.read()).replace(
                "ZZZ1", _sku
                ).replace(
                    "ZZZ2", _model
                    ).replace(
                        "ZZZ3", _serial
                        ).replace(
                            "ZZZ4", _screen)

    with open(_path, 'w', encoding='utf-8') as f_ops:
        f_ops.write(line)


def main():
    '''Default function'''
    make_cfg("QQQ1", "QQQ2", "QQQ3", "QQQ4", "QQQ.txt")


if __name__ == "__main__":
    main()
