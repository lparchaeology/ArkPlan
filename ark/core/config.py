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

import os

from PyQt4.QtCore import QVariant

from qgis.core import QGis

from ArkSpatial.ark.lib.core import Collection, CollectionSettings, FeatureType, layers


class Config():

    pluginName = u'ARKspatial'
    pluginScope = u'ARK'
    projectGroupName = u'ARK'
    filterSetGroupName = u'Filter Export Data'
    bufferSuffix = u'_buf'
    logSuffix = u'_log'

    # Field Name defaults
    fields = {
        'site': {
            'attribute': 'site',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Site Code',
            'query': 'Please enter the Site Code:',
        },
        'class': {
            'attribute': 'class',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Class Code',
            'query': 'Please enter the Class Code:',
        },
        'id': {
            'attribute': 'id',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'ID',
            'query': 'Please enter the ID:',
        },
        'label': {
            'attribute': 'label',
            'type': QVariant.String,
            'len': 20,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Label',
            'query': 'Please enter the Label:',
        },
        'category': {
            'attribute': 'category',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Category',
            'query': 'Please enter the Category:',
        },
        'elevation': {
            'attribute': 'elevation',
            'type': QVariant.Double,
            'len': 10,
            'decimals': 3,
            'min': -20000,
            'max': 20000,
            'default': 0.0,
            'label': 'Elevation',
            'query': 'Please enter the elevation in meters (m):',
        },
        'source_cd': {
            'attribute': 'source_cd',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Source Code',
            'query': 'Please enter the Source Code:',
        },
        'source_cl': {
            'attribute': 'source_cl',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Source Class',
            'query': 'Please enter the Source Class:',
        },
        'source_id': {
            'attribute': 'source_id',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Source ID',
            'query': 'Please enter the Source ID:',
        },
        'file': {
            'attribute': 'file',
            'type': QVariant.String,
            'len': 10,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Source File',
            'query': 'Please enter the Source File:',
        },
        'local_x': {
            'attribute': 'local_x',
            'type': QVariant.Double,
            'len': 10,
            'decimals': 3,
            'min': -20000,
            'max': 20000,
            'default': 0.0,
            'label': 'Local Grid X',
            'query': '',
        },
        'local_y': {
            'attribute': 'local_y',
            'type': QVariant.Double,
            'len': 10,
            'decimals': 3,
            'min': -20000,
            'max': 20000,
            'default': 0.0,
            'label': 'Local Grid Y',
            'query': '',
        },
        'map_x': {
            'attribute': 'map_x',
            'type': QVariant.Double,
            'len': 10,
            'decimals': 3,
            'min': -20000,
            'max': 20000,
            'default': 0.0,
            'label': 'Map X',
            'query': '',
        },
        'map_y': {
            'attribute': 'map_y',
            'type': QVariant.Double,
            'len': 10,
            'decimals': 3,
            'min': -20000,
            'max': 20000,
            'default': 0.0,
            'label': 'Map Y',
            'query': '',
        },
        'comment': {
            'attribute': 'comment',
            'type': QVariant.String,
            'len': 256,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Comment',
            'query': 'Please enter the Comment:',
        },
        'created': {
            'attribute': 'created',
            'type': QVariant.String,  # '2012-01-01T23:59:59.999Z' in UTC
            'len': 20,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Created On',
            'query': '',
        },
        'creator': {
            'attribute': 'creator',
            'type': QVariant.String,
            'len': 20,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Created By',
            'query': '',
        },
        'modified': {
            'attribute': 'modified',
            'type': QVariant.String,  # '2012-01-01T23:59:59.999Z' in UTC
            'len': 20,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Modified On',
            'query': '',
        },
        'modifier': {
            'attribute': 'modifier',
            'type': QVariant.String,
            'len': 20,
            'decimals': 0,
            'min': None,
            'max': None,
            'default': None,
            'label': 'Modified By',
            'query': '',
        },
    }

    collectionFields = [
        fields['site'],
        fields['class'],
        fields['id'],
        fields['label'],
        fields['category'],
        fields['source_cd'],
        fields['source_cl'],
        fields['source_id'],
        fields['file'],
        fields['comment'],
        fields['created'],
        fields['creator'],
        fields['modified'],
        fields['modifier'],
    ]

    gridFields = [
        fields['site'],
        fields['label'],
        fields['local_x'],
        fields['local_y'],
        fields['map_x'],
        fields['map_y'],
        fields['created'],
        fields['creator'],
    ]

    collections = {
        'plan': {
            'path': 'plan',
            'groupName': 'Plan Data',
            'edit': True,
            'item': True,
            'class': 'context',
            'buffer': True,
            'bufferGroupName': 'Plan Edit',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': [
                {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'plan_pt',
                    'label': 'Plan Points',
                },
                {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'plan_pl',
                    'label': 'Plan Lines',
                },
                {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'plan_pg',
                    'label': 'Plan Polygons',
                },
            ],
        },
        'section': {
            'path': 'section',
            'groupName': 'Section Data',
            'edit': True,
            'item': True,
            'class': 'section',
            'buffer': True,
            'bufferGroupName': 'Section Edit',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': [
                {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'section_pt',
                    'label': 'Section Points',
                },
                {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'section_pl',
                    'label': 'Section Lines',
                },
                {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'section_pg',
                    'label': 'Section Polygons',
                },
            ],
        },
        'site': {
            'path': 'site',
            'groupName': 'Site Data',
            'edit': True,
            'item': True,
            'class': 'site',
            'buffer': True,
            'bufferGroupName': 'Site Edit',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': [
                {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'site_pt',
                    'label': 'Site Points',
                },
                {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'site_pl',
                    'label': 'Site Lines',
                },
                {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'site_pg',
                    'label': 'Site Polygons',
                },
            ],
        },
        'grid': {
            'path': 'grid',
            'groupName': 'Grid Data',
            'edit': False,
            'item': False,
            'class': '',
            'buffer': False,
            'bufferGroupName': '',
            'log': False,
            'multi': False,
            'fields': gridFields,
            'layers': [
                {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'grid_pt',
                    'label': 'Grid Points',
                },
                {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'grid_pl',
                    'label': 'Grid Lines',
                },
                {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'grid_pg',
                    'label': 'Grid Polygons',
                },
            ],
        },
    }

    drawings = {
        'context': {
            'class': 'context',
            'code': 'cxt',
            'name': 'Context',
            'groupName': 'Contexts',
            'path': 'drawings/contexts',
            'layersGroupName': 'Drawings',
        },
        'plan': {
            'class': 'plan',
            'code': 'pln',
            'name': 'Plan',
            'groupName': 'Plans',
            'path': 'drawings/plans',
            'layersGroupName': 'Drawings',
        },
        'section': {
            'class': 'section',
            'code': 'sec',
            'name': 'Section',
            'groupName': 'Sections',
            'path': 'drawings/sections',
            'layersGroupName': 'Drawings',
        },
    }

    sourceCodes = {
        'drawing': {
            'code': 'drawing',
            'label': 'Checked Drawing',
            'sourceItem': True,
        },
        'unchecked': {
            'code': 'unchecked',
            'label': 'Unchecked Drawing',
            'sourceItem': True,
        },
        'survey': {
            'code': 'survey',
            'label': 'Survey Data',
            'sourceItem': False,
        },
        'sketch': {
            'code': 'sketch',
            'label': 'Sketch',
            'sourceItem': True,
        },
        'geophoto': {
            'code': 'geophoto',
            'label': 'Georeferenced Photo',
            'sourceItem': True,
        },
        'photo': {
            'code': 'photo',
            'label': 'Photo',
            'sourceItem': True,
        },
        'cloned': {
            'code': 'cloned',
            'label': 'Cloned from Source',
            'sourceItem': True,
        },
        'modified': {
            'code': 'modified',
            'label': 'Modified from Source',
            'sourceItem': True,
        },
        'inferred': {
            'code': 'inferred',
            'label': 'Inferred from Source',
            'sourceItem': True,
        },
        'creator': {
            'code': 'creator',
            'label': 'Surmised by Creator',
            'sourceItem': False,
        },
        'client': {
            'code': 'client',
            'label': 'Obtained from Client',
            'sourceItem': False,
        },
        'other': {
            'code': 'other',
            'label': 'Other (see comment)',
            'sourceItem': False,
        },
    }
    sourceCodesOrder = [
        'drawing',
        'unchecked',
        'survey',
        'sketch',
        'geophoto',
        'photo',
        'cloned',
        'modified',
        'inferred',
        'creator',
        'client',
        'other'
    ]

    # 'module'  = Module Code
    # 'class'  = Class Code
    # 'label' = Name label
    # 'collection' = If can be drawn as vector data
    # 'drawing' = If is a drawing in own right
    # 'source' = If can be used as a source in the plan data
    # 'group' = If is a group of other classes
    # 'parent' = The parent group (optional)
    # 'child' = The child group (optional)
    # 'ark1' = The ARK v1 code (optional)
    classCodes = {
        'context': {
            'module': 'context',
            'class': 'context',
            'label': 'Context',
            'collection': True,
            'drawing': True,
            'source': True,
            'group': False,
            'parent': 'group',
            'child': '',
            'ark1': 'cxt',
        },
        'subgroup': {
            'module': 'subgroup',
            'class': 'subgroup',
            'label': 'Sub-group',
            'collection': False,
            'drawing': False,
            'source': False,
            'group': True,
            'parent': 'group',
            'child': 'context',
            'ark1': 'sgr',
        },
        'group': {
            'module': 'group',
            'class': 'group',
            'label': 'Group',
            'collection': False,
            'drawing': False,
            'source': False,
            'group': True,
            'parent': 'subgroup',
            'child': 'group',
            'ark1': 'grp',
        },
        'plan': {
            'module': 'plan',
            'class': 'plan',
            'label': 'Plan',
            'collection': False,
            'drawing': True,
            'source': True,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'pln',
        },
        'find': {
            'module': 'find',
            'class': 'find',
            'label': 'Find',
            'collection': True,
            'drawing': False,
            'source': True,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'rgf',
        },
        'section': {
            'module': 'section',
            'class': 'section',
            'label': 'Section',
            'collection': True,
            'drawing': True,
            'source': True,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'sec',
        },
        'sample': {
            'module': 'sample',
            'class': 'sample',
            'label': 'Sample',
            'collection': True,
            'drawing': False,
            'source': False,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'smp',
        },
        'photo': {
            'module': 'photo',
            'class': 'photo',
            'label': 'Photo',
            'collection': False,
            'drawing': False,
            'source': False,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'sph',
        },
        'timber': {
            'module': 'timber',
            'class': 'timber',
            'label': 'Timber',
            'collection': True,
            'drawing': False,
            'source': False,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'tmb',
        },
        'site': {
            'module': 'area',
            'class': 'site',
            'label': 'Site',
            'collection': True,
            'drawing': False,
            'source': False,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'ste',
        },
        'trench': {
            'module': 'area',
            'class': 'trench',
            'label': 'Trench',
            'collection': True,
            'drawing': False,
            'source': False,
            'group': False,
            'parent': '',
            'child': '',
            'ark1': 'tch',
        },
    }

    featureCategories = {
        'ara': {'category': 'ara', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Area'},
        'ash': {'category': 'ash', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Ash'},
        'bhl': {'category': 'bhl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Borehole', 'query': 'label'},
        'bln': {'category': 'bln', 'type': FeatureType.Line,    'definitive': False, 'name': 'Baseline'},
        'bne': {'category': 'bne', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Bone'},
        'bos': {'category': 'bos', 'type': FeatureType.Line,    'definitive': False, 'name': 'Break of Slope'},
        'bpt': {'category': 'bpt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Base Point', 'query': 'label'},
        'brk': {'category': 'brk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Brick'},
        'cbm': {'category': 'cbm', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'CBM'},
        'cha': {'category': 'cha', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Charcoal'},
        'clk': {'category': 'clk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Chalk'},
        'coi': {'category': 'coi', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Coin'},
        'cut': {'category': 'cut', 'type': FeatureType.Line,    'definitive': True,  'name': 'Cut', 'query': 'id'},
        'dep': {'category': 'dep', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Deposit', 'query': 'id'},
        'ext': {'category': 'ext', 'type': FeatureType.Line,    'definitive': True,  'name': 'Extent'},
        'fil': {'category': 'fil', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Fill', 'query': 'id'},
        'fli': {'category': 'fli', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Flint'},
        'gls': {'category': 'gls', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Glass'},
        'hch': {'category': 'hch', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Hachure'},
        'int': {'category': 'int', 'type': FeatureType.Line,    'definitive': True,  'name': 'Interface'},
        'irn': {'category': 'irn', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Iron'},
        'lbl': {'category': 'lbl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Label', 'query': 'label'},
        'loc': {'category': 'loc', 'type': FeatureType.Point,   'definitive': False, 'name': 'Site Location'},
        'loe': {'category': 'loe', 'type': FeatureType.Line,    'definitive': True,  'name': 'Limit of Excavation'},
        'lvl': {'category': 'lvl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Level', 'query': 'elevation'},
        'lvu': {'category': 'lvu', 'type': FeatureType.Point,   'definitive': False, 'name': 'Underside Level', 'query': 'elevation'},
        'mtr': {'category': 'mtr', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Mortar'},
        'pnl': {'category': 'pnl', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Panel'},
        'pot': {'category': 'pot', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Pot'},
        'ren': {'category': 'ren', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Render'},
        'rgf': {'category': 'rgf', 'type': FeatureType.Point,   'definitive': False, 'name': 'Registered Find', 'query': 'id'},
        'ros': {'category': 'ros', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Return of Slope'},
        'sch': {'category': 'sch', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Schematic'},
        'smp': {'category': 'smp', 'type': FeatureType.Point,   'definitive': False, 'name': 'Sample', 'query': 'id'},
        'sln': {'category': 'sln', 'type': FeatureType.Line,    'definitive': False, 'name': 'Section Line', 'query': 'id'},
        'slv': {'category': 'slv', 'type': FeatureType.Point,   'definitive': False, 'name': 'Section Level', 'query': 'elevation'},
        'ste': {'category': 'ste', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Site Boundary'},
        'stn': {'category': 'stn', 'type': FeatureType.Point,   'definitive': False, 'name': 'Base Station', 'query': 'elevation'},
        'sto': {'category': 'sto', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Stone'},
        'tbm': {'category': 'tbm', 'type': FeatureType.Point,   'definitive': False, 'name': 'TBM', 'query': 'elevation'},
        'tch': {'category': 'tch', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Trench (Excavated)', 'query': 'id'},
        'tcp': {'category': 'tcp', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Trench (Proposed)', 'query': 'id'},
        'tgt': {'category': 'tgt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Target', 'query': 'elevation'},
        'til': {'category': 'til', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Tile'},
        'tim': {'category': 'tim', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Timber'},
        'tpt': {'category': 'tpt', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Test Pit'},
        'tip': {'category': 'tip', 'type': FeatureType.Line,    'definitive': False, 'name': 'Tipline'},
        'trn': {'category': 'trn', 'type': FeatureType.Line,    'definitive': True,  'name': 'Truncation'},
        'txt': {'category': 'txt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Comment', 'query': 'comment'},
        'unc': {'category': 'unc', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Undercut'},
        'ueg': {'category': 'ueg', 'type': FeatureType.Line,    'definitive': True,  'name': 'Uncertain Edge'},
        'vbs': {'category': 'vbs', 'type': FeatureType.Line,    'definitive': False, 'name': 'Vertical Break of Slope'},
        'veg': {'category': 'veg', 'type': FeatureType.Line,    'definitive': True,  'name': 'Vertical Edge'},
        'vtr': {'category': 'vtr', 'type': FeatureType.Line,    'definitive': True,  'name': 'Vertical Truncation'},
        'wst': {'category': 'wst', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Wood Stain'},
    }

    featureCollections = {
        'plan': [
            {'collection': 'plan', 'class': 'context', 'category': 'lvl'},
            {'collection': 'plan', 'class': 'context', 'category': 'lvu'},
            {'collection': 'plan', 'class': 'find',    'category': 'rgf'},
            {'collection': 'plan', 'class': 'sample',  'category': 'smp'},

            {'collection': 'plan', 'class': 'context', 'category': 'ext'},
            {'collection': 'plan', 'class': 'context', 'category': 'veg'},
            {'collection': 'plan', 'class': 'context', 'category': 'ueg'},
            {'collection': 'plan', 'class': 'context', 'category': 'loe'},
            {'collection': 'plan', 'class': 'context', 'category': 'trn'},
            {'collection': 'plan', 'class': 'context', 'category': 'vtr'},
            {'collection': 'plan', 'class': 'context', 'category': 'bos'},
            {'collection': 'plan', 'class': 'context', 'category': 'vbs'},
            {'collection': 'plan', 'class': 'context', 'category': 'hch'},
            {'collection': 'plan', 'class': 'context', 'category': 'unc'},
            {'collection': 'plan', 'class': 'context', 'category': 'ros'},

            {'collection': 'plan', 'class': 'context', 'category': 'ash'},
            {'collection': 'plan', 'class': 'context', 'category': 'bne'},
            {'collection': 'plan', 'class': 'context', 'category': 'brk'},
            {'collection': 'plan', 'class': 'context', 'category': 'cbm'},
            {'collection': 'plan', 'class': 'context', 'category': 'cha'},
            {'collection': 'plan', 'class': 'context', 'category': 'clk'},
            {'collection': 'plan', 'class': 'context', 'category': 'coi'},
            {'collection': 'plan', 'class': 'context', 'category': 'fli'},
            {'collection': 'plan', 'class': 'context', 'category': 'gls'},
            {'collection': 'plan', 'class': 'context', 'category': 'irn'},
            {'collection': 'plan', 'class': 'context', 'category': 'mtr'},
            {'collection': 'plan', 'class': 'context', 'category': 'pot'},
            {'collection': 'plan', 'class': 'context', 'category': 'ren'},
            {'collection': 'plan', 'class': 'context', 'category': 'sto'},
            {'collection': 'plan', 'class': 'context', 'category': 'til'},
            {'collection': 'plan', 'class': 'context', 'category': 'tim'},
            {'collection': 'plan', 'class': 'context', 'category': 'wst'},
            {'collection': 'plan', 'class': 'context', 'category': 'sch'},
        ],

        'section': [
            {'collection': 'section', 'class': 'section', 'category': 'slv'},
            {'collection': 'section', 'class': 'section', 'category': 'lbl'},
            {'collection': 'section', 'class': 'section', 'category': 'txt'},

            {'collection': 'section', 'class': 'section', 'category': 'sln'},
            {'collection': 'section', 'class': 'section', 'category': 'int'},
            {'collection': 'section', 'class': 'context', 'category': 'cut'},
            {'collection': 'section', 'class': 'section', 'category': 'ueg'},
            {'collection': 'section', 'class': 'section', 'category': 'tip'},
            {'collection': 'section', 'class': 'section', 'category': 'loe'},
            {'collection': 'section', 'class': 'section', 'category': 'trn'},

            {'collection': 'section', 'class': 'context', 'category': 'fil'},
            {'collection': 'section', 'class': 'context', 'category': 'dep'},
        ],

        'site': [
            {'collection': 'site', 'class': 'site',    'category': 'loc'},
            {'collection': 'site', 'class': 'site',    'category': 'bpt'},
            {'collection': 'site', 'class': 'site',    'category': 'stn'},
            {'collection': 'site', 'class': 'site',    'category': 'bhl'},
            {'collection': 'site', 'class': 'site',    'category': 'lvl'},
            {'collection': 'site', 'class': 'site',    'category': 'tbm'},
            {'collection': 'site', 'class': 'site',    'category': 'tgt'},

            {'collection': 'site', 'class': 'site',    'category': 'bln'},
            {'collection': 'site', 'class': 'section', 'category': 'sln'},

            {'collection': 'site', 'class': 'site',    'category': 'ste'},
            {'collection': 'site', 'class': 'site',    'category': 'ara'},
            {'collection': 'site', 'class': 'site',    'category': 'pnl'},
            {'collection': 'site', 'class': 'site',    'category': 'tpt'},
            {'collection': 'site', 'class': 'trench',  'category': 'tcp'},
            {'collection': 'site', 'class': 'trench',  'category': 'tch'},
        ]
    }
