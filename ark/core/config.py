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

from PyQt4.QtCore import QVariant

from qgis.core import QGis

from ArkSpatial.ark.lib.core import CollectionFieldSettings, CollectionLayerSettings, CollectionSettings, FeatureType


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
        'site',
        'class',
        'id',
        'label',
        'category',
        'source_cd',
        'source_cl',
        'source_id',
        'file',
        'comment',
        'created',
        'creator',
        'modified',
        'modifier',
    ]

    gridFieldsDefaults = [
        'site',
        'label',
        'local_x',
        'local_y',
        'map_x',
        'map_y',
        'created',
        'creator',
    ]

    collections = {
        'plan': {
            'path': 'data/plan',
            'groupName': 'Plan Data',
            'edit': True,
            'class': 'context',
            'buffer': True,
            'bufferGroupName': 'Plan Edit',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': {
                'points': {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'plan_pt',
                    'label': 'Plan Points',
                },
                'lines': {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'plan_pl',
                    'label': 'Plan Lines',
                },
                'polygons': {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'plan_pg',
                    'label': 'Plan Polygons',
                },
            },
        },
        'section': {
            'path': 'data/section',
            'groupName': 'Section Data',
            'edit': True,
            'class': 'section',
            'buffer': False,
            'bufferGroupName': '',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': {
                'points': {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'section_pt',
                    'label': 'Section Points',
                },
                'lines': {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'section_pl',
                    'label': 'Section Lines',
                },
                'polygons': {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'section_pg',
                    'label': 'Section Polygons',
                },
            },
        },
        'site': {
            'path': 'data/site',
            'groupName': 'Site Data',
            'edit': True,
            'class': 'site',
            'buffer': False,
            'bufferGroupName': '',
            'log': True,
            'multi': True,
            'fields': collectionFields,
            'layers': {
                'points': {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'site_pt',
                    'label': 'Site Points',
                },
                'lines': {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'site_pl',
                    'label': 'Site Lines',
                },
                'polygons': {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'site_pg',
                    'label': 'Site Polygons',
                },
            },
        },
        'grid': {
            'path': 'data/grid',
            'groupName': 'Grid Data',
            'edit': False,
            'class': '',
            'buffer': False,
            'bufferGroupName': '',
            'log': False,
            'multi': False,
            'fields': gridFieldsDefaults,
            'layers': {
                'points': {
                    'layer': 'points',
                    'geometry': QGis.Point,
                    'name': 'grid_pt',
                    'label': 'Grid Points',
                },
                'lines': {
                    'layer': 'lines',
                    'geometry': QGis.Line,
                    'name': 'grid_pl',
                    'label': 'Grid Lines',
                },
                'polygons': {
                    'layer': 'polygons',
                    'geometry': QGis.Polygon,
                    'name': 'grid_pg',
                    'label': 'Grid Polygons',
                },
            },
        },
    }

    drawings = {
        'context': {
            'name': 'Context',
            'groupName': 'Contexts',
            'path': 'drawings/contexts',
            'layersGroupName': 'Drawings',
        },
        'plan': {
            'name': 'Plan',
            'groupName': 'Plans',
            'path': 'drawings/plans',
            'layersGroupName': 'Drawings',
        },
        'section': {
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
            'label': 'Creator',
            'sourceItem': False,
        },
        'client': {
            'code': 'client',
            'label': 'Client',
            'sourceItem': False,
        },
        'other': {
            'code': 'other',
            'label': 'Other',
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

    # 'code'  = Class Code
    # 'label' = Name label
    # 'collection' = If can be drawn as vector data
    # 'drawing' = If is a drawing in own right
    # 'source' = If can be used as a source in the plan data
    # 'group' = If is a group of other classes
    # 'parent' = The parent group (optional)
    # 'child' = The child group (optional)
    classCodes = {
        'context': {
            'code': 'context',
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
            'code': 'subgroup',
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
            'code': 'group',
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
            'code': 'plan',
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
            'code': 'find',
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
            'code': 'section',
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
            'code': 'sample',
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
            'code': 'photo',
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
            'code': 'timber',
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
            'code': 'site',
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
            'code': 'trench',
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
        'plan': [
            {'class': 'context', 'category': 'lvl', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Level', 'query': 'elevation'},
            {'class': 'context', 'category': 'lvu', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Underside Level', 'query': 'elevation'},
            {'class': 'find',    'category': 'rgf', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Registered Find', 'query': 'id'},
            {'class': 'sample',  'category': 'smp', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Sample', 'query': 'id'},
            {'class': 'context', 'category': 'ext', 'type': FeatureType.Line, 'definitive': True, 'name': 'Extent'},
            {'class': 'context', 'category': 'veg', 'type': FeatureType.Line,
                'definitive': True, 'name': 'Vertical Edge'},
            {'class': 'context', 'category': 'ueg', 'type': FeatureType.Line,
                'definitive': True, 'name': 'Uncertain Edge'},
            {'class': 'context', 'category': 'loe', 'type': FeatureType.Line,
                'definitive': True, 'name': 'Limit of Excavation'},
            {'class': 'context', 'category': 'trn', 'type': FeatureType.Line,
                'definitive': True, 'name': 'Truncation'},
            {'class': 'context', 'category': 'vtr', 'type': FeatureType.Line,
                'definitive': True, 'name': 'Vertical Truncation'},
            {'class': 'context', 'category': 'bos', 'type': FeatureType.Line,
                'definitive': False, 'name': 'Break of Slope'},
            {'class': 'context', 'category': 'vbs', 'type': FeatureType.Line,
                'definitive': False, 'name': 'Vertical Break of Slope'},
            {'class': 'context', 'category': 'hch', 'type': FeatureType.Segment,
                'definitive': False, 'name': 'Hachure'},
            {'class': 'context', 'category': 'unc', 'type': FeatureType.Segment,
                'definitive': False, 'name': 'Undercut'},
            {'class': 'context', 'category': 'ros', 'type': FeatureType.Segment,
                'definitive': False, 'name': 'Return of Slope'},

            {'class': 'context', 'category': 'ash', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Ash'},
            {'class': 'context', 'category': 'bne', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Bone'},
            {'class': 'context', 'category': 'brk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Brick'},
            {'class': 'context', 'category': 'cbm', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'CBM'},
            {'class': 'context', 'category': 'cha', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Charcoal'},
            {'class': 'context', 'category': 'clk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Chalk'},
            {'class': 'context', 'category': 'coi', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Coin'},
            {'class': 'context', 'category': 'fli', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Flint'},
            {'class': 'context', 'category': 'gls', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Glass'},
            {'class': 'context', 'category': 'irn', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Iron'},
            {'class': 'context', 'category': 'mtr', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Mortar'},
            {'class': 'context', 'category': 'pot', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Pot'},
            {'class': 'context', 'category': 'ren', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Render'},
            {'class': 'context', 'category': 'sto', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Stone'},
            {'class': 'context', 'category': 'til', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Tile'},
            {'class': 'context', 'category': 'tim', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Timber'},
            {'class': 'context', 'category': 'wst', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Wood Stain'},
            {'class': 'context', 'category': 'sch', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Schematic'},
        ],

        'section': [
            {'class': 'section', 'category': 'slv', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Section Level', 'query': 'elevation'},
            {'class': 'section', 'category': 'lbl', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Label', 'query': 'label'},
            {'class': 'section', 'category': 'txt', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Comment', 'query': 'comment'},

            {'class': 'section', 'category': 'sln', 'type': FeatureType.Segment,
                'definitive': False, 'name': 'Section Line'},
            {'class': 'section', 'category': 'int', 'type': FeatureType.Line,
                'definitive': True,  'name': 'Interface'},
            {'class': 'context', 'category': 'cut', 'type': FeatureType.Line,
                'definitive': True,  'name': 'Cut', 'query': 'id'},
            {'class': 'section', 'category': 'ueg', 'type': FeatureType.Line,
                'definitive': True,  'name': 'Uncertain Edge'},
            {'class': 'section', 'category': 'tip', 'type': FeatureType.Line,
                'definitive': False, 'name': 'Tipline'},
            {'class': 'section', 'category': 'loe', 'type': FeatureType.Line,
                'definitive': True,  'name': 'Limit of Excavation'},
            {'class': 'section', 'category': 'trn', 'type': FeatureType.Line,
                'definitive': True,  'name': 'Truncation'},

            {'class': 'context', 'category': 'fil', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Fill', 'query': 'id'},
            {'class': 'context', 'category': 'dep', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Deposit', 'query': 'id'},
        ],

        'site': [
            {'class': 'site',    'category': 'ste', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Site Location'},
            {'class': 'site',    'category': 'bpt', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Base Point', 'query': 'label'},
            {'class': 'site',    'category': 'stn', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Base Station', 'query': 'elevation'},
            {'class': 'site',    'category': 'bhl', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Borehole', 'query': 'label'},
            {'class': 'site',    'category': 'lvl', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Level', 'query': 'elevation'},
            {'class': 'site',    'category': 'tbm', 'type': FeatureType.Point,
                'definitive': False, 'name': 'TBM', 'query': 'elevation'},
            {'class': 'site',    'category': 'tgt', 'type': FeatureType.Point,
                'definitive': False, 'name': 'Target', 'query': 'elevation'},

            {'class': 'site',    'category': 'bln', 'type': FeatureType.Line,
                'definitive': False, 'name': 'Baseline'},
            {'class': 'section', 'category': 'sln', 'type': FeatureType.Line,
                'definitive': False, 'name': 'Section Line', 'query': 'id'},

            {'class': 'site', 'category': 'red', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Site Red Line'},
            {'class': 'trench', 'category': 'tcp', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Trench (Proposed)', 'query': 'id'},
            {'class': 'trench', 'category': 'tch', 'type': FeatureType.Polygon,
                'definitive': False, 'name': 'Trench (Excavated)', 'query': 'id'},
            {'class': 'site', 'category': 'ara', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Area'},
            {'class': 'site', 'category': 'pnl', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Panel'},
            {'class': 'site', 'category': 'tpt', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Test Pit'},
        ]
    }

    def toCollectionSettings(self, collection):
        config = Config.collections[collection]
        path = config['path']
        bufferPath = path + '/buffer'
        logPath = path + '/log'

        settings = CollectionSettings()
        settings.collection = collection
        settings.collectionPath = path
        settings.parentGroupName = Config.projectGroupName
        settings.collectionGroupName = config['groupName']
        settings.bufferGroupName = config['bufferGroupName']
        settings.log = config['log']
        settings.multi = config['multi']

        for field in config['fields']:
            fieldConfig = config['fields'][field]
            fs = CollectionFieldSettings()
            fs.attribute = fieldConfig['attribute']
            fs.type = fieldConfig['type']
            fs.len = fieldConfig['len']
            fs.decimals = fieldConfig['decimals']
            fs.min = fieldConfig['min']
            fs.max = fieldConfig['max']
            fs.default = fieldConfig['default']
            fs.label = fieldConfig['label']
            fs.query = fieldConfig['query']
            settings.fields[field] = fs

        for layer in config['layers']:
            layerConfig = config['layers'][layer]
            ls = CollectionLayerSettings()
            ls.label = layerConfig['label']
            ls.name = layerConfig['name']
            ls.path = self._shapeFile(path, ls.name)
            ls.stylePath = self._styleFile(path, ls.name, config['pointsBaseName'])
            if config['buffer']:
                ls.bufferLayer = True
                ls.bufferName = ls.name + Config.bufferSuffix
                ls.bufferPath = self._shapeFile(bufferPath, ls.bufferName)
            if config['log']:
                ls.logLayer = True
                ls.logName = ls.name + Config.logSuffix
                ls.logPath = self._shapeFile(logPath, ls.logName)
            if layer == 'points':
                settings.points = ls
            if layer == 'lines':
                settings.lines = ls
            if layer == 'polygons':
                settings.polygons = ls

        return settings
