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

import base64
from enum import Enum
import json
import urllib.error
import urllib.parse
import urllib.request

from ArkSpatial.ark.lib import utils

from .ark_response import ArkResponse


class ViewType(Enum):

    TableView = 0
    TextView = 1
    ThumbView = 2
    MapView = 3
    ChatView = 4


class DataClass(Enum):

    AllClasses = -1
    ActionClass = 0
    AttributeClass = 1
    DateClass = 2
    SpanClass = 3
    TextClass = 4
    NumberClass = 5
    FileClass = 6


class Ark:

    def __init__(self, url, handle=None, passwd=None):
        self.url = ''
        self.handle = ''
        self.passwd = ''
        self.setUrl(url)
        self.setCredentials(handle, passwd)

    def setUrl(self, url):
        self.url = str(url)

    def setCredentials(self, handle, passwd):
        self.handle = str(handle)
        self.passwd = str(passwd)

    def describeARK(self):
        return self._getJson('describeARK', {})

    def describeItems(self):
        return self._getJson('describeItems', {})

    def describeFrags(self, dataclass='all', classtype=None, aliased=None):
        # FIXME Broken
        return self._getJson('describeFrags', {'dataclass': dataclass, 'classtype': classtype, 'aliased': aliased})

    def describeFilters(self):
        return self._getJson('describeFilters', {})

    def describeSubforms(self, item_key='all'):
        return self._getJson('describeSubforms', {'itemkey': item_key})

    def describeFields(self, itemkey='all'):
        # FIXME Broken for 'all', works for exact module
        return self._getJson('describeFields', {'itemkey': itemkey})

    def getItems(self, itemkey='all'):
        return self._getJson('getItems', {'itemkey': itemkey})

    def getFrags(self, itemkey, item_value, dataclass='all', classtype=None, aliased=None):
        return self._getJson('getFrags', {'itemkey': itemkey, itemkey: item_value, 'dataclass': dataclass, 'classtype': classtype, 'aliased': aliased})

    def getFilter(self, ftype, src):
        return self._getJson('getFilter', {'ftype': ftype, 'src': src})

    def getFilterSet(self, retftrset):
        return self._getJson('getFilter', {'retftrset': retftrset})

    def getFields(self, itemkey, item_value, fields, aliased=None):
        return self._getJson('getFields', {'itemkey': itemkey, itemkey: item_value, 'fields': fields, 'aliased': aliased})

    def transcludeFilter(self, ftype, src, retftrset=None, disp_mode=None):
        return self._getHtml('transcludeFilter', {'ftype': ftype, 'src': src, 'retftrset': retftrset, 'disp_mode': disp_mode})

    def transcludeFilterUrl(self, ftype, src, retftrset=None, disp_mode=None):
        return self._buildUrl('transcludeFilter', {'ftype': ftype, 'src': src, 'retftrset': retftrset, 'disp_mode': disp_mode})

    def transcludeSubform(self, itemkey, item_value, sf_conf):
        return self._getHtml('transcludeSubform', {'itemkey': itemkey, itemkey: item_value, 'sf_conf': sf_conf})

    def transcludeSubformUrl(self, itemkey, item_value, sf_conf):
        return self._buildUrl('transcludeSubform', {'itemkey': itemkey, itemkey: item_value, 'sf_conf': sf_conf})

    def putField(self):
        pass

    def readFieldValue(self, fieldName, data):
        value = None
        if fieldName in data and data[fieldName] is not False:
            for item in data[fieldName]:
                if 'current' in item:
                    value = item['current']
        return value

    def getProjectList(self):
        response = self.getItems('job_cd')
        projects = {}
        if response.error:
            utils.debug(response.url)
            utils.debug(response.message)
            utils.debug(response.raw)
        else:
            for item in response.data['job']:
                projects[item["job_cd"]] = item["job_no"]
        return projects

    def getProjectDetails(self, project):
        data = {}
        response = self.getFields(
            'job_cd',
            str(project),
            ['conf_field_job_name', 'conf_field_sitecode', 'conf_field_easting', 'conf_field_northing']
        )
        if response.error:
            utils.debug(response.url)
            utils.debug(response.message)
            utils.debug(response.raw)
        else:
            data['projectName'] = self.readFieldValue('conf_field_job_name', response.data)
            data['siteCode'] = self.readFieldValue('conf_field_sitecode', response.data)
            data['locationEasting'] = self.readFieldValue('conf_field_easting', response.data)
            data['locationNorthing'] = self.readFieldValue('conf_field_northing', response.data)
        return data

    def _viewTypeToToken(self, viewType):
        if viewType == ViewType.TableView:
            return 'table'
        elif viewType == ViewType.TextView:
            return 'text'
        elif viewType == ViewType.ThumbView:
            return 'thumb'
        elif viewType == ViewType.MapView:
            return 'map'
        elif viewType == ViewType.ChatView:
            return 'chat'
        return 'table'

    def _dataClassToToken(self, dataClass):
        if dataClass == DataClass.ActionClass:
            return 'action'
        elif dataClass == DataClass.AttributeClass:
            return 'attribute'
        elif dataClass == DataClass.DateClass:
            return 'date'
        elif dataClass == DataClass.SpanClass:
            return 'span'
        elif dataClass == DataClass.TextClass:
            return 'txt'
        elif dataClass == DataClass.NumberClass:
            return 'number'
        elif dataClass == DataClass.FileClass:
            return 'file'
        return 'all'

    def _tokenToDataClass(self, token):
        if token == 'action':
            return DataClass.ActionClass
        elif token == 'attribute':
            return DataClass.AttributeClass
        elif token == 'date':
            return DataClass.DateClass
        elif token == 'span':
            return DataClass.SpanClass
        elif token == 'txt':
            return DataClass.TextClass
        elif token == 'number':
            return DataClass.NumberClass
        elif token == 'file':
            return DataClass.FileClass
        return Ark.AllClasses

    def _getJson(self, req, args):
        ret = ArkResponse()
        ret.url = self._buildUrl(req, args)
        ret.data = json.loads('{}')
        request = urllib.request.Request(ret.url)
        base64string = base64.encodestring('%s:%s' % (self.handle, self.passwd))[:-1]
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            ret.response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            ret.message = 'ARK server could not complete the request: ' + str(e.code)
            ret.code = e.code
            ret.reason = e.reason
        except urllib.error.URLError as e:
            ret.message = 'Could not reach the ARK server: ' + str(e.reason)
            ret.reason = e.reason
        else:
            ret.code = ret.response.getcode()
            ret.raw = ret.response.read()
            try:
                ret.data = json.loads(ret.raw)
                ret.error = False
            except Exception:
                ret.message = 'Invalid JSON'
                ret.reason = 'Invalid JSON'
        return ret

    def _getHtml(self, req, args):
        ret = ArkResponse()
        ret.url = self._buildUrl(req, args)
        try:
            ret.response = urllib.request.urlopen(ret.url)
        except urllib.error.HTTPError as e:
            ret.message = 'ARK server could not complete the request: ' + str(e.code)
            ret.code = e.code
            ret.reason = e.reason
        except urllib.error.URLError as e:
            ret.message = 'Could not reach the ARK server: ' + str(e.reason)
            ret.reason = e.reason
        else:
            ret.code = ret.response.getcode()
            ret.data = ret.response.read()
            ret.raw = ret.data
            ret.error = False
        return ret

    def _buildUrl(self, req, args):
        url = self.url + '/api.php?req=' + str(req)
        for key in list(args.keys()):
            url += self._arg(key, args[key])
        if self.handle and self.passwd:
            url += self._arg('handle', self.handle)
            url += self._arg('passwd', self.passwd)
        return url

    def _arg(self, key, value):
        ret = ''
        if (key is not None and value is not None):
            if isinstance(value, list):
                for val in value:
                    ret = ret + '&' + str(key) + '[]=' + str(val)
            else:
                ret = '&' + str(key) + '=' + str(value)
        return ret
