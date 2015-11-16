# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                    ArkPlan
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                             -------------------
        begin                : 2014-12-07
        copyright            : (C) 2014 by John Layt
        email                : john@layt.net
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Ark class from file Ark.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .src.arkplan import ArkPlan
    return ArkPlan(iface)
