# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
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

from qgis.core import QgsField, QgsMessageLog

from ..libarkqgis.map_tools import FeatureType
from ..libarkqgis.project import Project

class Config():

    @classmethod
    def useArkDB(cls):
        return Project.readBoolEntry(cls.pluginName, 'useArkDB', True)

    @classmethod
    def fields(cls):
        if cls.useArkDB():
            return cls.arkFieldDefaults
        else:
            return cls.fieldDefaults

    @classmethod
    def field(cls, fieldKey):
        if cls.useArkDB():
            return cls.arkFieldDefaults[fieldKey]
        else:
            return cls.fieldDefaults[fieldKey]

    @classmethod
    def fieldName(cls, fieldKey):
        try:
            if cls.useArkDB():
                return cls.arkFieldDefaults[fieldKey].name()
            else:
                return cls.fieldDefaults[fieldKey].name()
        except:
            return ''

    @classmethod
    def isGroupClass(cls, classCode):
        try:
            return Config.classCodes[classCode]['group']
        except IndexError:
            return False

    @classmethod
    def parentClass(cls, classCode):
        try:
            return Config.classCodes[classCode]['parent']
        except IndexError:
            return ''

    @classmethod
    def childClass(cls, classCode):
        try:
            return Config.classCodes[classCode]['child']
        except IndexError:
            return ''

    pluginName = u'ArkPlan'
    projectGroupName = u'Ark Spatial'
    filterSetGroupName = u'Filter Export Data'
    bufferSuffix = u'_buf'
    logSuffix = u'_log'

    # Field Name defaults
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
        'created'   : QgsField('created',    QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'creator'   : QgsField('creator',    QVariant.String, '',  20, 0, 'Created By'),
        'modified'  : QgsField('modified',   QVariant.String, '',  20, 0, 'Modified On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'modifier'  : QgsField('modifier',   QVariant.String, '',  20, 0, 'Modified By'),
    }

    # Old field defaults for ARK1, deprecated
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
        'created'   : QgsField('cre_on',     QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'creator'   : QgsField('cre_by',     QVariant.String, '',  20, 0, 'Created By'),
        'modified'  : QgsField('mod_on',     QVariant.String, '',  20, 0, 'Updated On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'modifier'  : QgsField('mod_by',     QVariant.String, '',  20, 0, 'Updated By'),
    }

    vectorGroups = {
        'plan' : {
            'pathSuffix'       : 'vector/plan',
            'groupName'        : 'Plan Data',
            'class'            : 'cxt',
            'buffer'           : True,
            'bufferGroupName'  : 'Plan Edit',
            'log'              : True,
            'multi'            : True,
            'pointsLabel'      : 'Plan Points',
            'linesLabel'       : 'Plan Lines',
            'polygonsLabel'    : 'Plan Polygons',
            'pointsBaseName'   : 'plan_pt',
            'linesBaseName'    : 'plan_pl',
            'polygonsBaseName' : 'plan_pg',
            'pointsFields'     : ['site', 'class', 'id', 'name', 'category', 'elevation', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'linesFields'      : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'polygonsFields'   : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
        },
        'section' : {
            'pathSuffix'       : 'vector/section',
            'groupName'        : 'Section Data',
            'class'            : 'sec',
            'buffer'           : True,
            'bufferGroupName'  : 'Section Edit',
            'log'              : True,
            'multi'            : True,
            'pointsLabel'      : 'Section Points',
            'linesLabel'       : 'Section Lines',
            'polygonsLabel'    : 'Section Polygons',
            'pointsBaseName'   : 'section_pt',
            'linesBaseName'    : 'section_pl',
            'polygonsBaseName' : 'section_pg',
            'pointsFields'     : ['site', 'class', 'id', 'name', 'category', 'elevation', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'linesFields'      : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'polygonsFields'   : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
        },
        'base' : {
            'pathSuffix'       : 'vector/base',
            'groupName'        : 'Base Data',
            'class'            : 'ste',
            'buffer'           : True,
            'bufferGroupName'  : 'Base Edit',
            'log'              : False,
            'multi'            : False,
            'pointsLabel'      : 'Base Points',
            'linesLabel'       : 'Base Lines',
            'polygonsLabel'    : 'Base Polygons',
            'pointsBaseName'   : 'base_pt',
            'linesBaseName'    : 'base_pl',
            'polygonsBaseName' : 'base_pg',
            'pointsFields'     : ['site', 'class', 'id', 'name', 'category', 'elevation', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'linesFields'      : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
            'polygonsFields'   : ['site', 'class', 'id', 'name', 'category', 'source_cd', 'source_cl', 'source_id', 'file', 'comment', 'created', 'creator', 'modified', 'modifier'],
        },
        'grid' : {
            'pathSuffix'       : 'vector/grid',
            'groupName'        : 'Grid Data',
            'class'            : '',
            'buffer'           : False,
            'bufferGroupName'  : '',
            'log'              : False,
            'multi'            : False,
            'pointsLabel'      : 'Grid Points',
            'linesLabel'       : 'Grid Lines',
            'polygonsLabel'    : 'Grid Polygons',
            'pointsBaseName'   : 'grid_pt',
            'linesBaseName'    : 'grid_pl',
            'polygonsBaseName' : 'grid_pg',
            'pointsFields'     : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created', 'creator'],
            'linesFields'      : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created', 'creator'],
            'polygonsFields'   : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created', 'creator'],
        },
    }

    rasterGroups = {
        'cxt' : {
            'name'             : 'Context',
            'groupName'        : 'Contexts',
            'pathSuffix'       : 'raster/context',
            'layersGroupName'  : 'Drawings',
        },
        'pln' : {
            'name'             : 'Plan',
            'groupName'        : 'Plans',
            'pathSuffix'       : 'raster/plan',
            'layersGroupName'  : 'Drawings',
        },
        'sec' : {
            'name'             : 'Section',
            'groupName'        : 'Sections',
            'pathSuffix'       : 'raster/section',
            'layersGroupName'  : 'Drawings',
        },
    }

    sourceCodesOrder = ['drw', 'unc', 'svy', 'skt', 'gph', 'cln', 'mod', 'inf', 'cre', 'oth']
    sourceCodes = {
        'drw' : {
            'code'             : 'drw',
            'label'            : 'Checked Drawing',
            'sourceItem'       : True,
        },
        'unc' : {
            'code'             : 'unc',
            'label'            : 'Unchecked Drawing',
            'sourceItem'       : True,
        },
        'svy' : {
            'code'             : 'svy',
            'label'            : 'Survey Data',
            'sourceItem'       : False,
        },
        'skt' : {
            'code'             : 'skt',
            'label'            : 'Sketch',
            'sourceItem'       : True,
        },
        'gph' : {
            'code'             : 'gph',
            'label'            : 'Georeferenced Photo',
            'sourceItem'       : True,
        },
        'cln' : {
            'code'             : 'cln',
            'label'            : 'Cloned from Source',
            'sourceItem'       : True,
        },
        'mod' : {
            'code'             : 'mod',
            'label'            : 'Modified from Source',
            'sourceItem'       : True,
        },
        'inf' : {
            'code'             : 'inf',
            'label'            : 'Inferred from Source',
            'sourceItem'       : True,
        },
        'cre' : {
            'code'             : 'cre',
            'label'            : 'Creator',
            'sourceItem'       : False,
        },
        'oth' : {
            'code'             : 'oth',
            'label'            : 'Other',
            'sourceItem'       : False,
        },
    }

    # 'code'  = Class Code
    # 'label' = Name label
    # 'plan' = If can be drawn in the plan data
    # 'source' = If can be used as a source in the plan data
    # 'drawing' = If is a drawing in own right
    # 'group' = If is a group of other classes
    # 'parent' = The parent group (optional)
    # 'child' = The child group (optional)
    classCodes = {
        'cxt' : {
            'code'             : 'cxt',
            'label'            : 'Context',
            'plan'             : True,
            'source'           : True,
            'drawing'          : True,
            'group'            : False,
            'parent'           : 'grp',
        },
        'sgr' : {
            'code'             : 'sgr',
            'label'            : 'Sub-group',
            'plan'             : False,
            'source'           : False,
            'drawing'          : False,
            'group'            : True,
            'parent'           : 'grp',
            'child'            : 'cxt',
        },
        'grp' : {
            'code'             : 'grp',
            'label'            : 'Group',
            'plan'             : False,
            'source'           : False,
            'drawing'          : False,
            'group'            : True,
            'parent'           : 'sgr',
            'child'            : 'grp',
        },
        'pln' : {
            'code'             : 'pln',
            'label'            : 'Plan',
            'plan'             : False,
            'source'           : True,
            'drawing'          : True,
            'group'            : False,
        },
        'rgf' : {
            'code'             : 'rgf',
            'label'            : 'Find',
            'plan'             : True,
            'source'           : True,
            'drawing'          : False,
            'group'            : False,
        },
        'sec' : {
            'code'             : 'sec',
            'label'            : 'Section',
            'plan'             : True,
            'source'           : True,
            'drawing'          : True,
            'group'            : False,
        },
        'smp' : {
            'code'             : 'smp',
            'label'            : 'Sample',
            'plan'             : True,
            'source'           : False,
            'drawing'          : False,
            'group'            : False,
        },
        'sph' : {
            'code'             : 'sph',
            'label'            : 'Photo',
            'plan'             : False,
            'source'           : False,
            'drawing'          : False,
            'group'            : False,
        },
        'tmb' : {
            'code'             : 'tmb',
            'label'            : 'Timber',
            'plan'             : True,
            'source'           : False,
            'drawing'          : False,
            'group'            : False,
        },
    }

    attributeQuery = {
        'name' : {
            'attribute' : 'name',
            'type'      : QVariant.String,
            'default'   : '',
            'min'       : None,
            'max'       : None,
            'decimals'  : None,
            'title'     : 'Feature Name',
            'label'     : 'Please enter the name of the feature:',
        },
        'comment' : {
            'attribute' : 'comment',
            'type'      : QVariant.String,
            'default'   : '',
            'min'       : None,
            'max'       : None,
            'decimals'  : None,
            'title'     : 'Feature Name',
            'label'     : 'Please enter the name of the feature:',
        },
        'elevation' : {
            'attribute' : 'elevation',
            'type'      : QVariant.Double,
            'default'   : 0.0,
            'min'       : -20000,
            'max'       : 20000,
            'decimals'  : 2,
            'title'     : 'Add Elevation',
            'label'     : 'Please enter the elevation in meters (m):',
        },
        'context' : {
            'attribute' : 'id',
            'type'      : QVariant.Int,
            'default'   : 0,
            'min'       : 0,
            'max'       : 99999,
            'decimals'  : 0,
            'title'     : 'Context Number',
            'label'     : 'Please enter the Context Number:',
        },
        'section' : {
            'attribute' : 'id',
            'type'      : QVariant.Int,
            'default'   : 0,
            'min'       : 0,
            'max'       : 99999,
            'decimals'  : 0,
            'title'     : 'Section Number',
            'label'     : 'Please enter the Section Number:',
        },
        'find' : {
            'attribute' : 'id',
            'type'      : QVariant.Int,
            'default'   : 0,
            'min'       : 0,
            'max'       : 99999,
            'decimals'  : 0,
            'title'     : 'Find Number',
            'label'     : 'Please enter the Find Number:',
        },
        'trench' : {
            'attribute' : 'id',
            'type'      : QVariant.Int,
            'default'   : 0,
            'min'       : 0,
            'max'       : 99999,
            'decimals'  : 0,
            'title'     : 'Trench Number',
            'label'     : 'Please enter the Trench Number:',
        },
        'sample' : {
            'attribute' : 'id',
            'type'      : QVariant.Int,
            'default'   : 0,
            'min'       : 0,
            'max'       : 99999,
            'decimals'  : 0,
            'title'     : 'Sample Number',
            'label'     : 'Please enter the Sample Number:',
        },
    }

    featureCategories = {
        'plan' : [
            {'class': 'cxt', 'category': 'lvl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Level',           'query': 'elevation'},
            {'class': 'cxt', 'category': 'lvu', 'type': FeatureType.Point,   'definitive': False, 'name': 'Underside Level', 'query': 'elevation'},
            {'class': 'rgf', 'category': 'rgf', 'type': FeatureType.Point,   'definitive': False, 'name': 'Registered Find', 'query': 'find'},
            {'class': 'smp', 'category': 'spl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Sample',          'query': 'sample'},

            {'class': 'cxt', 'category': 'ext', 'type': FeatureType.Line,    'definitive': True,  'name': 'Extent'},
            {'class': 'cxt', 'category': 'veg', 'type': FeatureType.Line,    'definitive': True,  'name': 'Vertical Edge'},
            {'class': 'cxt', 'category': 'ueg', 'type': FeatureType.Line,    'definitive': True,  'name': 'Uncertain Edge'},
            {'class': 'cxt', 'category': 'loe', 'type': FeatureType.Line,    'definitive': True,  'name': 'Limit of Excavation'},
            {'class': 'cxt', 'category': 'trn', 'type': FeatureType.Line,    'definitive': True,  'name': 'Truncation'},
            {'class': 'cxt', 'category': 'vtr', 'type': FeatureType.Line,    'definitive': True,  'name': 'Vertical Truncation'},
            {'class': 'cxt', 'category': 'bos', 'type': FeatureType.Line,    'definitive': False, 'name': 'Break of Slope'},
            {'class': 'cxt', 'category': 'vbs', 'type': FeatureType.Line,    'definitive': False, 'name': 'Vertical Break of Slope'},
            {'class': 'cxt', 'category': 'hch', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Hachure'},
            {'class': 'cxt', 'category': 'unc', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Undercut'},
            {'class': 'cxt', 'category': 'ros', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Return of Slope'},

            {'class': 'cxt', 'category': 'ash', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Ash',  },
            {'class': 'cxt', 'category': 'bne', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Bone', },
            {'class': 'cxt', 'category': 'brk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Brick',},
            {'class': 'cxt', 'category': 'cbm', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'CBM',  },
            {'class': 'cxt', 'category': 'cha', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Charcol'},
            {'class': 'cxt', 'category': 'clk', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Chalk'},
            {'class': 'cxt', 'category': 'coi', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Coin'},
            {'class': 'cxt', 'category': 'fli', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Flint'},
            {'class': 'cxt', 'category': 'gls', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Glass'},
            {'class': 'cxt', 'category': 'irn', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Iron'},
            {'class': 'cxt', 'category': 'mtr', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Mortar'},
            {'class': 'cxt', 'category': 'pot', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Pot'},
            {'class': 'cxt', 'category': 'ren', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Render'},
            {'class': 'cxt', 'category': 'sto', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Stone'},
            {'class': 'cxt', 'category': 'til', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Tile'},
            {'class': 'cxt', 'category': 'tim', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Timber'},
            {'class': 'cxt', 'category': 'wst', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Wood Stain'},
            {'class': 'cxt', 'category': 'sch', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Schematic'},
        ],

        'section' : [
            {'class': 'sec', 'category': 'slv', 'type': FeatureType.Point,   'definitive': False, 'name': 'Section Level', 'query': 'elevation'},
            {'class': 'sec', 'category': 'lbl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Label',         'query': 'name'},
            {'class': 'sec', 'category': 'txt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Label',         'query': 'comment'},

            {'class': 'sec', 'category': 'sln', 'type': FeatureType.Segment, 'definitive': False, 'name': 'Section Line'},
            {'class': 'sec', 'category': 'int', 'type': FeatureType.Line,    'definitive': True,  'name': 'Interface'},
            {'class': 'cxt', 'category': 'cut', 'type': FeatureType.Line,    'definitive': True,  'name': 'Cut',           'query': 'context'},
            {'class': 'sec', 'category': 'ueg', 'type': FeatureType.Line,    'definitive': True,  'name': 'Uncertain Edge'},
            {'class': 'sec', 'category': 'tip', 'type': FeatureType.Line,    'definitive': False, 'name': 'Tipline'},
            {'class': 'sec', 'category': 'loe', 'type': FeatureType.Line,    'definitive': True,  'name': 'Limit of Excavation'},
            {'class': 'sec', 'category': 'trn', 'type': FeatureType.Line,    'definitive': True,  'name': 'Truncation'},

            {'class': 'cxt', 'category': 'fil', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Fill',          'query': 'context'},
            {'class': 'cxt', 'category': 'dep', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Deposit',       'query': 'context'},
        ],

        'base' : [
            {'class': 'ste', 'category': 'ste', 'type': FeatureType.Point,   'definitive': False, 'name': 'Site Location'},
            {'class': 'ste', 'category': 'bpt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Base Point',         'query': 'name'},
            {'class': 'ste', 'category': 'stn', 'type': FeatureType.Point,   'definitive': False, 'name': 'Base Station',       'query': 'elevation'},
            {'class': 'ste', 'category': 'bhl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Borehole',           'query': 'name'},
            {'class': 'ste', 'category': 'lvl', 'type': FeatureType.Point,   'definitive': False, 'name': 'Level',              'query': 'elevation'},
            {'class': 'ste', 'category': 'tbm', 'type': FeatureType.Point,   'definitive': False, 'name': 'TBM',                'query': 'elevation'},
            {'class': 'ste', 'category': 'tgt', 'type': FeatureType.Point,   'definitive': False, 'name': 'Target',             'query': 'elevation'},

            {'class': 'ste', 'category': 'bln', 'type': FeatureType.Line,    'definitive': False, 'name': 'Baseline'},
            {'class': 'sec', 'category': 'sln', 'type': FeatureType.Line,    'definitive': False, 'name': 'Section Line',       'query': 'section'},

            {'class': 'ste', 'category': 'red', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Site Red Line'},
            {'class': 'tch', 'category': 'tcp', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Trench (Proposed)',  'query': 'trench'},
            {'class': 'tch', 'category': 'tch', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Trench (Excavated)', 'query': 'trench'},
            {'class': 'ste', 'category': 'ara', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Area'},
            {'class': 'ste', 'category': 'pnl', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Panel'},
            {'class': 'ste', 'category': 'tpt', 'type': FeatureType.Polygon, 'definitive': False, 'name': 'Test Pit'},
        ]
    }
