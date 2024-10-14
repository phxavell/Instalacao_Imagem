#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Avell Label printing - a tool which gets data from
    packing service.
"""
import odoo_connect


def packages():
    """Default function"""

    return odoo_connect.run(
        'mrp.workorder',
        'search_read', [
            [
                ['state', 'in', ('ready', 'progress')],
                ['workcenter_id', '=', 2],
                ['final_lot_id', '!=', False],
            ]
        ], {
            'fields': [
                'production_id',
                'final_lot_id',
                'product_id',
                'qty_produced',
                'qty_production'
            ],
            'limit': 500
        })


def manufacturing(mo_id):
    """Default function"""

    return odoo_connect.run(
        'mrp.production',
        'search_read', [
            [
                ['name', '=', mo_id],
            ]
        ], {
            'fields': [
                'origin',
                'product_id',
            ],
            'limit': 100
        })


def product(product_id):
    """Default function"""

    return odoo_connect.run(
        'product.product',
        'search_read', [
            [
                ['id', '=', product_id],
            ]
        ], {
            'fields': [
                'default_code',
                'name',
                'attribute_value_ids',
                # 'product_variant_id',
            ],
            'limit': 100
        })


def consulta_serial(in_numeroserial):
    """Default function"""

    return odoo_connect.run(
        'stock.production.lot',
        'search_read', [
            [
                ['name', '=', in_numeroserial],
            ]
        ], {
            'fields': [
                # 'name',
                # 'ref',
                # 'produtc_id',
            ],
            'limit': 100
        })







#######################################################################################

def notebook_serial_duplicado():

    msg = ''
    output = ''

    ignore_list = [
        'AVNB1947003',
        'AVNB2012107',
        'AVNB2012108',
        'AVNB2012195',
        'AVNB2013130',
        'AVNB2034016',
        'AVNB2044255',
        'AVNB2046122',
        'AVNB2048176',
        'AVNB2048356'
    ] # Situacoes a serem resolvidas ou sem solucao (enviadas em duplicidade de numero serial ao cliente)

    serial_ids = odoo_connect.run(
        'stock.production.lot',
        'search_read', [
            [
                ['product_id.name', 'ilike', 'Notebook Avell'],
                ['name', '!=', 'AVNB1947003'],
                ['name', '!=', 'AVNB2012107'],
                ['name', '!=', 'AVNB2012108'],
                ['name', '!=', 'AVNB2012195'],
                ['name', '!=', 'AVNB2013130'],
                ['name', '!=', 'AVNB2034016'],
                ['name', '!=', 'AVNB2044255'],
                ['name', '!=', 'AVNB2046122'],
                ['name', '!=', 'AVNB2048176'],
                ['name', '!=', 'AVNB2048356'],

            ]
        ], {
            'fields': [
                'name',
                # 'ref',
                # 'produtc_id',
            ],
            # 'limit': 10000000000
        })

    # print('DEBUG: \n\n%s\n\n' % serial_ids)

    list_geral = []
    list_duplicado = []

    for x in serial_ids:
      if x['name'] in list_geral:
        if x['name'] not in ignore_list:
            list_duplicado.append(x['name'])
      else:
          list_geral.append(x['name'])

    list_duplicado.sort()

    for n in list_duplicado:
      msg += "%s\n" % n

    if len(list_duplicado) > 0:
      output += "Numeros seriais duplicados\n\n%s" % msg
    else:
      output += "False"

    return output

###################################################################################


def attributes_preload():
    """Default function"""

    return odoo_connect.run(
        'product.attribute.value',
        'search_read', [
            [
            ]
        ], {
            'fields': [
                'display_name',
            ],
            'limit': 100
        })


def attributes(dict_to_find, attrib_id):
    """??? Default"""

    dict_temp = {}

    for aaa in dict_to_find:
        dict_temp[aaa.get('id')] = aaa.get('display_name')

    if attrib_id in dict_temp.keys():
        output = dict_temp[attrib_id]
    else:
        output = False

    return output


def componentes(dict_to_find, attrib_id):
    """??? Default"""

    dict_temp = {}

    for aaa in dict_to_find:
        dict_temp[aaa.get('id')] = aaa.get('x_studio_descrio')

    if attrib_id in dict_temp.keys():
        output = dict_temp[attrib_id]
    else:
        output = False

    return output


def main():
    "Default"
    pass


if __name__ == "__main__":
    main()
