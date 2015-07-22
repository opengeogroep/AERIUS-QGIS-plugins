# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImaerReader
                                 A QGIS plugin
 Import gml conform to the imaer schema output by the AERIUS calculator
                             -------------------
        begin                : 2015-06-24
        copyright            : (C) 2015 by OpenGeoGroep
        email                : info@opengeogroep.nl
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
    """Load ImaerReader class from file ImaerReader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .imaer_reader import ImaerReader
    return ImaerReader(iface)
