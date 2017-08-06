# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                    pyARK
                    A Python library for using ARK Database
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

import json
import urllib2

import .ArkResponse


class Ark():

    # ViewType
    TableView = 0
    TextView = 1
    ThumbView = 2
    MapView = 3
    ChatView = 4

    # DataClass
    AllClasses = -1
    ActionClass = 0
    AttributeClass = 1
    DateClass = 2
    SpanClass = 3
    TextClass = 4
    NumberClass = 5
    FileClass = 6

    url = u''
    handle = u''
    passwd = u''

    def __init__(self, url, handle=None, passwd=None):
        self.setUrl(url)
        self.setCredentials(handle, passwd)

    def setUrl(self, url):
        self.url = unicode(url)

    def setCredentials(self, handle, passwd):
        self.handle = unicode(handle)
        self.passwd = unicode(passwd)

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
        # TODO multiple fields!!!
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

    def _viewTypeToToken(self, viewType):
        if viewType == Ark.TableView:
            return 'table'
        elif viewType == Ark.TextView:
            return 'text'
        elif viewType == Ark.ThumbView:
            return 'thumb'
        elif viewType == Ark.MapView:
            return 'map'
        elif viewType == Ark.ChatView:
            return 'chat'
        return 'table'

    def _dataClassToToken(self, dataClass):
        if dataClass == Ark.ActionClass:
            return 'action'
        elif dataClass == Ark.AttributeClass:
            return 'attribute'
        elif dataClass == Ark.DateClass:
            return 'date'
        elif dataClass == Ark.SpanClass:
            return 'span'
        elif dataClass == Ark.TextClass:
            return 'txt'
        elif dataClass == Ark.NumberClass:
            return 'number'
        elif dataClass == Ark.FileClass:
            return 'file'
        return 'all'

    def _tokenToDataClass(self, token):
        if token == 'action':
            return Ark.ActionClass
        elif token == 'attribute':
            return Ark.AttributeClass
        elif token == 'date':
            return Ark.DateClass
        elif token == 'span':
            return Ark.SpanClass
        elif token == 'txt':
            return Ark.TextClass
        elif token == 'number':
            return Ark.NumberClass
        elif token == 'file':
            return Ark.FileClass
        return Ark.AllClasses

    def _getJson(self, req, args):
        ret = ArkResponse()
        ret.url = self._buildUrl(req, args)
        ret.data = json.loads('{}')
        try:
            ret.response = urllib2.urlopen(ret.url)
        except urllib2.HTTPError as e:
            ret.message = 'ARK server could not complete the request: ' + str(e.code)
            ret.code = e.code
            ret.reason = e.reason
        except urllib2.URLError as e:
            ret.message = 'Could not reach the ARK server: ' + str(e.reason)
            ret.reason = e.reason
        else:
            ret.code = ret.response.getcode()
            ret.raw = ret.response.read()
            try:
                ret.data = json.loads(ret.raw)
                ret.error = False
            except:
                ret.message = 'Invalid JSON'
                ret.reason = 'Invalid JSON'
        return ret

    def _getHtml(self, req, args):
        ret = ArkResponse()
        ret.url = self._buildUrl(req, args)
        try:
            ret.response = urllib2.urlopen(ret.url)
        except urllib2.HTTPError as e:
            ret.message = 'ARK server could not complete the request: ' + str(e.code)
            ret.code = e.code
            ret.reason = e.reason
        except urllib2.URLError as e:
            ret.message = 'Could not reach the ARK server: ' + str(e.reason)
            ret.reason = e.reason
        else:
            ret.code = ret.response.getcode()
            ret.data = ret.response.read()
            ret.raw = ret.data
            ret.error = False
        return ret

    def _buildUrl(self, req, args):
        url = self.url + u'/api.php?req=' + unicode(req)
        for key in args.keys():
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
                    ret = ret + u'&' + unicode(key) + u'[]=' + unicode(val)
            else:
                ret = u'&' + unicode(key) + u'=' + unicode(value)
        return ret
