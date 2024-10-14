#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Avell Label printing - a tool which gets data from
    packing service.
"""

import ssl
import xmlrpc.client
import odoo_config as config


def _connect():
    """Connect XMLRCP client to Odoo Server"""

    # REF https://gist.github.com
    # /ilyasProgrammer/cf6647356c9a3722f597f72b7685a4c3

    # REF https://www.odoo.com/documentation/13.0
    # /webservices/odoo.html

    _client = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/common'.format(config.URL),
        verbose=False,
        use_datetime=True,
        # REF: https://www.python.org/dev/peps/pep-0476/
        # pylint: disable=protected-access
        context=ssl._create_unverified_context()
    )
    return _client


def run(var_model, var_method, var_param, var_args):

    common = _connect()

    odoo_user_id = common.authenticate(
        config.DATABASE,
        config.USERNAME,
        config.PASSWORD,
        {}
    )

    models = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/object'.format(config.URL),
        verbose=False,
        use_datetime=True,
        # REF https://www.python.org/dev/peps/pep-0476/
        # pylint: disable=protected-access
        context=ssl._create_unverified_context()
    )

    model_generic = models.execute_kw(
        config.DATABASE,
        odoo_user_id,
        config.PASSWORD,
        var_model,  # Model
        var_method,  # Method
        var_param,  # Parameters
        var_args   # Arguments
        )

    return model_generic


def status():
    """status"""
    return bool(_connect().version)


def version():
    """Show version"""
    return str(_connect().version()['server_version'])


def main():
    """Default"""
    pass
    # print("Status=%s" % status())
    # print("Version=%s" % version())


if __name__ == "__main__":
    main()