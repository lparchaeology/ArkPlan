# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ark
                                 A QGIS plugin
 Plugin to assist in digitising of Archaeological plans.
                              -------------------
        begin                : 2015-12-13
        git sha              : $Format:%H$
        copyright            : (C) 2014 by John Layt
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

from PyQt4.QtCore import QVariant

from qgis.core import QgsField

from libarkqgis.map_tools import FeatureType

class Config():

    projectGroupName = 'Ark'

    # Field deafults to use if *not* using ARK DB, so as not to confuse normal users
    fieldDefaults = {
        'site'      : QgsField('site',       QVariant.String, '',  10, 0, 'Site Code'),
        'class'     : QgsField('class',      QVariant.String, '',  10, 0, 'Class'),
        'id'        : QgsField('id',         QVariant.Int,    '',   5, 0, 'ID'),
        'name'      : QgsField('name',       QVariant.String, '',  10, 0, 'Name'),
        'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
        'elevation' : QgsField('elevation',  QVariant.Double, '',  10, 3, 'Elevation'),
        'source_cd' : QgsField('source_cd',  QVariant.String, '',  10, 0, 'Source Code'),
        'source_cl' : QgsField('source_cl',  QVariant.String, '',  10, 0, 'Source Class'),
        'source_id' : QgsField('source_id',  QVariant.Int,    '',   5, 0, 'Source ID'),
        'file'      : QgsField('file',       QVariant.String, '', 100, 0, 'Source File'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'map_x'     : QgsField('map_x',      QVariant.Double, '',  10, 3, 'Map X'),
        'map_y'     : QgsField('map_y',      QVariant.Double, '',  10, 3, 'Map Y'),
        'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
        'created_on': QgsField('created_on', QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'created_by': QgsField('created_by', QVariant.String, '',  20, 0, 'Created By')
    }

    # Field defaults to use if using ARK DB, matches field names in ARK
    arkFieldDefaults = {
        'site'      : QgsField('ste_cd',     QVariant.String, '',  10, 0, 'Site Code'),
        'class'     : QgsField('module',     QVariant.String, '',  10, 0, 'ARK Module'),
        'id'        : QgsField('item_no',    QVariant.Int,    '',   5, 0, 'ARK Item Number'),
        'name'      : QgsField('name',       QVariant.String, '',  10, 0, 'Name'),
        'category'  : QgsField('category',   QVariant.String, '',  10, 0, 'Category'),
        'elevation' : QgsField('elevation',  QVariant.Double, '',  10, 3, 'Elevation'),
        'source_cd' : QgsField('source_cd',  QVariant.String, '',  10, 0, 'Source Code'),
        'source_cl' : QgsField('source_mod', QVariant.String, '',  10, 0, 'Source Module'),
        'source_id' : QgsField('source_no',  QVariant.Int,    '',   5, 0, 'Source Item Number'),
        'file'      : QgsField('file',       QVariant.String, '', 100, 0, 'File'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'map_x'     : QgsField('map_x',      QVariant.Double, '',  10, 3, 'Map X'),
        'map_y'     : QgsField('map_y',      QVariant.Double, '',  10, 3, 'Map Y'),
        'comment'   : QgsField('comment',    QVariant.String, '', 100, 0, 'Comment'),
        'created_on': QgsField('cre_on',     QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'created_by': QgsField('cre_by',     QVariant.String, '',  20, 0, 'Created By')
    }

    groupDefaults = {
        'plan' : {
            'path'             : '',
            'pathSuffix'       : 'vector/plan',
            'layersGroupName'  : 'Plan Data',
            'buffersGroupName' : 'Edit Data',
            'bufferSuffix'     : '_mem',
            'pointsLabel'      : 'Plan Points',
            'linesLabel'       : 'Plan Lines',
            'polygonsLabel'    : 'Plan Polygons',
            'pointsBaseName'   : 'plan_pt',
            'linesBaseName'    : 'plan_pl',
            'polygonsBaseName' : 'plan_pg',
            'pointsFields'     : ['site', 'class', 'id', 'name', 'category', 'elevation', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created_on', 'created_by'],
        },
        'grid' : {
            'path'             : '',
            'pathSuffix'       : 'vector/grid',
            'layersGroupName'  : 'Grid',
            'buffersGroupName' : '',
            'bufferSuffix'     : '',
            'pointsLabel'      : 'Grid Points',
            'linesLabel'       : 'Grid Lines',
            'polygonsLabel'    : 'Grid Polygons',
            'pointsBaseName'   : 'grid_pt',
            'linesBaseName'    : 'grid_pl',
            'polygonsBaseName' : 'grid_pg',
            'pointsFields'     : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
        },
        'base' : {
            'path'             : '',
            'pathSuffix'       : 'vector/base',
            'layersGroupName'  : 'Base Data',
            'buffersGroupName' : 'Edit Data',
            'bufferSuffix'     : '_mem',
            'pointsLabel'      : 'Base Points',
            'linesLabel'       : 'Base Lines',
            'polygonsLabel'    : 'Base Polygons',
            'pointsBaseName'   : 'base_pt',
            'linesBaseName'    : 'base_pl',
            'polygonsBaseName' : 'base_pg',
            'pointsFields'     : ['site', 'name', 'category', 'elevation', 'source_cd', 'file', 'comment', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'name', 'category', 'source_cd', 'file', 'comment', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'name', 'category', 'source_cd', 'file', 'comment', 'created_on', 'created_by'],
        },
        'cxt' : {
            'class'            : 'cxt',
            'label'            : 'Context',
            'path'             : '',
            'pathSuffix'       : 'raster/context',
            'layersGroupName'  : 'Drawings'
        },
        'pln' : {
            'class'            : 'pln',
            'label'            : 'Plan',
            'path'             : '',
            'pathSuffix'       : 'raster/plan',
            'layersGroupName'  : 'Drawings'
        },
        'sec' : {
            'class'            : 'sec',
            'label'            : 'Section',
            'path'             : '',
            'pathSuffix'       : 'raster/section',
            'layersGroupName'  : 'Drawings'
        },
    }

    planSourceCodes = [
        ['Checked Drawing', 'drw'],
        ['Unchecked Drawing', 'unc'],
        ['Survey Data', 'svy'],
        ['Sketch', 'skt'],
        ['Cloned from Source', 'cln'],
        ['Modified from Source', 'mod'],
        ['Inferred from Source', 'inf']
    ]

    planSourceClasses = [
        ['Context', 'cxt'],
        ['Plan',    'pln'],
        ['Section', 'sec'],
        ['Find',    'rgf']
    ]

    drawingTypes = ['cxt', 'pln']

    featureCategories = [
        # collection, classCode, category, toolName, icon, featureType, definitiveFeature
        ['plan', 'cxt', 'ext', 'Extent',                  '', FeatureType.Line,    True],
        ['plan', 'cxt', 'veg', 'Vertical Edge',           '', FeatureType.Line,    True],
        ['plan', 'cxt', 'ueg', 'Uncertain Edge',          '', FeatureType.Line,    True],
        ['plan', 'cxt', 'loe', 'Limit of Excavation',     '', FeatureType.Line,    True],
        ['plan', 'cxt', 'trn', 'Truncation',              '', FeatureType.Line,    True],
        ['plan', 'cxt', 'vtr', 'Vertical Truncation',     '', FeatureType.Line,    True],
        ['plan', 'cxt', 'bos', 'Break of Slope',          '', FeatureType.Line,    False],
        ['plan', 'cxt', 'vbs', 'Vertical Break of Slope', '', FeatureType.Line,    False],
        ['plan', 'cxt', 'hch', 'Hachure',                 '', FeatureType.Segment, False],
        ['plan', 'cxt', 'unc', 'Undercut',                '', FeatureType.Segment, False],
        ['plan', 'cxt', 'ros', 'Return of Slope',         '', FeatureType.Segment, False],
        ['plan', 'cxt', 'cbm', 'CBM',                     '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'brk', 'Brick',                   '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'til', 'Tile',                    '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'pot', 'Pot',                     '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'sto', 'Stone',                   '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'fli', 'Flint',                   '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'cha', 'Charcol',                 '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'tim', 'Timber',                  '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'clk', 'Chalk',                   '', FeatureType.Polygon, False],
        ['plan', 'cxt', 'lvl', 'Level',                   '', FeatureType.Point,   False],
        ['plan', 'cxt', 'llv', 'Lowest Level',            '', FeatureType.Point,   False],
        ['plan', 'cxt', 'sch', 'Schema',                  '', FeatureType.Polygon, False],
        ['plan', 'sec', 'sec', 'Section Pin',             '', FeatureType.Point,   False],
        ['plan', 'sec', 'sln', 'Section Line',            '', FeatureType.Line,    False],
        ['plan', 'rgf', 'spf', 'Special Find',            '', FeatureType.Point,   False],
        ['plan', 'smp', 'spl', 'Sample',                  '', FeatureType.Point,   False],
    ]
