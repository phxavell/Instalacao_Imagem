#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avell Catalogo"""

import json
import sys
import odoo_queries


class LabelData:
    """Label container"""
    sequence = 0
    serial = ''  # Unique Serial Number
    mo_number = ''  # Manufacturing Order
    so_number = ''  # Sale Order
    product_id = ''  # Product (variant) id (numeric id)
    product_code = ''  # Product (default) code
    product_name = ''  # Product (template) name (short name)
    product_name_var = ''  # Product full name (with variants)
    attributes = ''  # Product (variant) attributes
    display_name = ''
    catalogo_name = ''
    components = []

    def __init__(self, sequence):
        pass

    def pass001(self):
        """To be done pass def"""
        pass

    def pass002(self):
        """To be done pass def"""
        pass


def process(in_sn):
    """Doc String"""

    atr_dict = {}

    lct = 0  # line count
    ldx = []  # line index
    attrib_general = {}
    attrib_general = odoo_queries.attributes_preload()

    for serial_pesquisado in odoo_queries.consulta_serial(in_sn):

        # Populate object LabelData
        ldx.append(LabelData("%s" % lct))
        ldx[lct].serial = serial_pesquisado['name']
        ldx[lct].so_number = "%s" % serial_pesquisado[
            'sale_order_ids'
        ]

        ldx[lct].product_id = serial_pesquisado['product_id'][0]

        ldx[lct].display_name = "%s" % (
            serial_pesquisado['product_id'][1]
        )

        for produto in odoo_queries.product(ldx[lct].product_id):
            ldx[lct].product_code = "%s" % produto['default_code']
            ldx[lct].product_name = "%s" % produto['name']

            msg_attrib = ''

            for atributo in produto['attribute_value_ids']:
                msg_attr = "%s" % (
                    odoo_queries.attributes(
                        attrib_general,
                        atributo,
                    ),
                )

                sep = ': '

                # Commercial Product Name
                atr_dict['name_tm'] = ldx[lct].product_name

                # Commercial Code
                atr_dict['code'] = ldx[lct].product_code

                if "Sistema Operacional: " in msg_attr:
                    atr_dict['os'] = msg_attr[msg_attr.index(sep) + len(sep):]


                if "SO: " in msg_attr:
                    atr_dict['os'] = msg_attr[msg_attr.index(sep) + len(sep):]


                if "tela" in msg_attr:
                    atr_dict['screen'] = msg_attr[
                        msg_attr.index(sep) + len(sep):
                    ]

                ldx[lct].attributes = "%s" % msg_attrib
    return atr_dict


def comp_os(in_os):
    """Compare Operating System"""
    type(in_os)


def main():
    """Chamada padrao"""

    if len(sys.argv) < 2:
        print("Tem parametro de menos")
        exit(1)

    if len(sys.argv) > 2:
        print("Tem parametro demais")
        exit(1)

    if len(sys.argv) == 2:
        print(json.dumps(process(sys.argv)))


if __name__ == "__main__":
    main()