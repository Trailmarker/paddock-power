# -*- coding: utf-8 -*-
# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .paddock_power import PaddockPower
    return PaddockPower(iface)
