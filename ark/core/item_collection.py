# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import Collection

from item_collection_layer import ItemCollectionLayer


class ItemCollection(Collection):

    def __init__(self, iface, projectPath, settings):
        super(ItemCollection, self).__init__(iface, projectPath, settings)

    def _newLayer(self, settings):
        return ItemCollectionLayer(self._iface, self.projectPath, settings)

    def moveItemToBuffers(self, item, logMessage='Move Item to Buffers', timestamp=None):
        return self.moveFeatureRequestToBuffers(item.featureRequest(), logMessage, timestamp or utils.timestamp())

    def copyItemToBuffers(self, item, logMessage='Copy Item to Buffers', timestamp=None):
        return self.copyFeatureRequestToBuffers(item.featureRequest(), logMessage, timestamp or utils.timestamp())

    def deleteItem(self, item, logMessage='Delete Item', timestamp=None):
        return self.deleteFeatureRequest(item.featureRequest(), logMessage, timestamp or utils.timestamp())
