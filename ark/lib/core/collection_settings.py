# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK QGIS
                        A QGIS utilities library.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L-P : Heritage LLP
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

from ..project import Project


class CollectionSettings:

    collection = ''
    collectionPath = ''

    parentGroupName = ''
    collectionGroupName = ''
    bufferGroupName = ''
    log = False

    pointsLayerLabel = ''
    pointsLayerName = ''
    pointsLayerPath = ''
    pointsStylePath = ''
    pointsBufferName = ''
    pointsBufferPath = ''
    pointsLogName = ''
    pointsLogPath = ''

    linesLayerLabel = ''
    linesLayerName = ''
    linesLayerPath = ''
    linesStylePath = ''
    linesBufferName = ''
    linesBufferPath = ''
    linesLogName = ''
    linesLogPath = ''

    polygonsLayerLabel = ''
    polygonsLayerName = ''
    polygonsLayerPath = ''
    polygonsStylePath = ''
    polygonsBufferName = ''
    polygonsBufferPath = ''
    polygonsLogName = ''
    polygonsLogPath = ''

    @staticmethod
    def fromProject(scope, collection):
        path = 'collections/' + collection + '/'
        lcs = CollectionSettings()
        lcs.collection = Project.readEntry(scope, path + 'collection')
        lcs.collectionPath = Project.readEntry(scope, path + 'collectionPath')
        lcs.collectionGroupName = Project.readEntry(scope, path + 'collectionGroupName')
        lcs.parentGroupName = Project.readEntry(scope, path + 'parentGroupName')
        lcs.bufferGroupName = Project.readEntry(scope, path + 'bufferGroupName')
        lcs.log = Project.readBoolEntry(scope, path + 'log')
        lcs.pointsLayerLabel = Project.readEntry(scope, path + 'pointsLayerLabel')
        lcs.pointsLayerName = Project.readEntry(scope, path + 'pointsLayerName')
        lcs.pointsLayerPath = Project.readEntry(scope, path + 'pointsLayerPath')
        lcs.pointsBufferName = Project.readEntry(scope, path + 'pointsBufferName')
        lcs.pointsBufferPath = Project.readEntry(scope, path + 'pointsBufferPath')
        lcs.pointsLogName = Project.readEntry(scope, path + 'pointsLogName')
        lcs.pointsLogPath = Project.readEntry(scope, path + 'pointsLogPath')
        lcs.linesLayerLabel = Project.readEntry(scope, path + 'linesLayerLabel')
        lcs.linesLayerName = Project.readEntry(scope, path + 'linesLayerName')
        lcs.linesLayerPath = Project.readEntry(scope, path + 'linesLayerPath')
        lcs.linesBufferName = Project.readEntry(scope, path + 'linesBufferName')
        lcs.linesBufferPath = Project.readEntry(scope, path + 'linesBufferPath')
        lcs.linesLogName = Project.readEntry(scope, path + 'linesLogName')
        lcs.linesLogPath = Project.readEntry(scope, path + 'linesLogPath')
        lcs.polygonsLayerLabel = Project.readEntry(scope, path + 'polygonsLayerLabel')
        lcs.polygonsLayerName = Project.readEntry(scope, path + 'polygonsLayerName')
        lcs.polygonsLayerPath = Project.readEntry(scope, path + 'polygonsLayerPath')
        lcs.polygonsBufferName = Project.readEntry(scope, path + 'polygonsBufferName')
        lcs.polygonsBufferPath = Project.readEntry(scope, path + 'polygonsBufferPath')
        lcs.polygonsLogName = Project.readEntry(scope, path + 'polygonsLogName')
        lcs.polygonsLogPath = Project.readEntry(scope, path + 'polygonsLogPath')
        return lcs

    def toProject(self, scope):
        path = 'collections/' + self.collection + '/'
        Project.writeEntry(scope, path + 'collection', self.collection)
        Project.writeEntry(scope, path + 'collectionPath', self.collectionPath)
        Project.writeEntry(scope, path + 'collectionGroupName', self.collectionGroupName)
        Project.writeEntry(scope, path + 'parentGroupName', self.parentGroupName)
        Project.writeEntry(scope, path + 'bufferGroupName', self.bufferGroupName)
        Project.writeEntry(scope, path + 'log', self.log)
        Project.writeEntry(scope, path + 'pointsLayerLabel', self.pointsLayerLabel)
        Project.writeEntry(scope, path + 'pointsLayerName', self.pointsLayerName)
        Project.writeEntry(scope, path + 'pointsLayerPath', self.pointsLayerPath)
        Project.writeEntry(scope, path + 'pointsBufferName', self.pointsBufferName)
        Project.writeEntry(scope, path + 'pointsBufferPath', self.pointsBufferPath)
        Project.writeEntry(scope, path + 'pointsLogName', self.pointsLogName)
        Project.writeEntry(scope, path + 'pointsLogPath', self.pointsLogPath)
        Project.writeEntry(scope, path + 'linesLayerLabel', self.linesLayerLabel)
        Project.writeEntry(scope, path + 'linesLayerName', self.linesLayerName)
        Project.writeEntry(scope, path + 'linesLayerPath', self.linesLayerPath)
        Project.writeEntry(scope, path + 'linesBufferName', self.linesBufferName)
        Project.writeEntry(scope, path + 'linesBufferPath', self.linesBufferPath)
        Project.writeEntry(scope, path + 'linesLogName', self.linesLogName)
        Project.writeEntry(scope, path + 'linesLogPath', self.linesLogPath)
        Project.writeEntry(scope, path + 'polygonsLayerLabel', self.polygonsLayerLabel)
        Project.writeEntry(scope, path + 'polygonsLayerName', self.polygonsLayerName)
        Project.writeEntry(scope, path + 'polygonsLayerPath', self.polygonsLayerPath)
        Project.writeEntry(scope, path + 'polygonsBufferName', self.polygonsBufferName)
        Project.writeEntry(scope, path + 'polygonsBufferPath', self.polygonsBufferPath)
        Project.writeEntry(scope, path + 'polygonsLogName', self.polygonsLogName)
        Project.writeEntry(scope, path + 'polygonsLogPath', self.polygonsLogPath)
