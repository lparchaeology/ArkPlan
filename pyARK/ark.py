# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                    pyARK
                    A Python library for using ARK Database
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

import json
import urllib2

class ArkResponse():
    url = ''
    response = None
    data = ''
    raw = ''
    message = ''
    error = True
    code = -1
    reason = ''

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
        #FIXME Broken
        return self._getJson('describeFrags', {'dataclass': dataclass, 'classtype': classtype, 'aliased': aliased})

    def describeFilters(self):
        return self._getJson('describeFilters', {})

    def describeSubforms(self, item_key='all'):
        return self._getJson('describeSubforms', {'item_key': item_key})

    def describeFields(self, itemkey='all'):
        #FIXME Broken for 'all', works for exact module
        return self._getJson('describeFields', {'itemkey': itemkey})

    def getItems(self, itemkey='all'):
        return self._getJson('getItems', {'itemkey': itemkey})

    def getFrags(self, itemkey, item_value, dataclass='all', classtype=None, aliased=None):
        return self._getJson('getFrags', {'itemkey': itemkey, itemkey: item_value, 'dataclass': dataclass, 'classtype': classtype, 'aliased': aliased})

    def getFilter(self, ftype, src, retftrset=None):
        return self._getJson('getFilter', {'ftype': ftype, 'src': src, 'retftrset': retftrset})

    def getFields(self, itemkey, item_value, fields, aliased=None):
        #TODO multiple fields!!!
        return self._getJson('getFields', {'itemkey': itemkey, itemkey: item_value, 'fields': fields, 'aliased': aliased})

    def transcludeFilter(self, ftype, src, retftrset=None, disp_mode=None):
        return self._getHtml('transcludeFilter', {'ftype': ftype, 'src': src, 'retftrset': retftrset, 'disp_mode': disp_mode})

    def transcludeSubform(self, itemkey, item_value, sf_conf):
        return self._getHtml('transcludeSubform', {'itemkey': itemkey, itemkey: item_value, 'sf_conf': sf_conf})

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
        if (key is not None and value is not None):
            return u'&' + unicode(key) + u'=' + unicode(value)
        return ''


class ArkContainer(object):

    _data = {}

    def __init__(self, data):
        self._data = data

    def data(self):
        return self._data


class ArkObject(ArkContainer):

    _ark = None
    _aliases = {}

    def __init__(self, ark, data):
        super(ArkObject, self).__init__(data)
        self._ark = ark
        #FIXME If no aliases get false instead of empty list!
        if self._data['aliases']:
            for alias in self._data['aliases']:
                self._aliases[alias['language']] = alias['alias']

    def id(self):
        return self._data['id']

    def alias(self, language=None):
        if language:
            return self._aliases[language]
        else:
            return self._aliases[self._ark.language()]


class ArkInstance(ArkContainer):

    _api = None  # Ark()
    _fragmentTypes = {}  # Set of ArkFragmentType() instances
    _modules = {}  # Set of ArkModule() instances

    def __init__(self, url, handle=None, passwd=None):
        self._api = Ark(url, handle, passwd)
        if self._api:
            data = self._api.describeARK()
            super(ArkInstance, self).__init__(data)
            self._loadFragmentTypes()
            self._loadModules()

    def name(self):
        return self._data['ark_name']

    def displayName(self):
        return self._data['ark_name_readable']

    def version(self):
        return self._data['version']

    def language(self):
        #TODO Find out from ARK, or allow to be set?
        return u'en'

    def fragmentTypes(self, dataClass=None):
        if dataClass ==  None:
            return self._fragmentTypes.values()
        ret = []
        token = self._api._dataClassToToken(dataClass)
        for fragment in self._fragmentTypes.values():
            if fragment._data['dataclass'] == token:
                ret.append(fragment)
        return ret

    def fragmentType(self, dataClass, classType):
        return self._fragmentTypes[self._api._dataClassToToken(dataClass), classType]

    def modules(self):
        return self._modules.values()

    def module(self, name):
        return self._modules[name]

    def moduleForKey(self, key):
        for module in self._modules.values():
            if module.itemKey() == key:
                return module

    def filters(self):
        return self._api.describeFilters()

    def filterResults(self, filterId):
        results = self._api.getFilter(None, None, filterId)
        ret = []
        for result in results.values():
            ret.append(ArkResult(result))
        return ret

    def filterView(self, id, viewType=None):
        return self._api.transcludeFilter(None, None, id, self._api._viewTypeToToken(viewType))

    def searchResults(self, text):
        results = self._api.getFilter('ftx', text)
        ret = []
        for result in results.values():
            ret.append(ArkResult(result))
        return ret

    def searchView(self, text, viewType=None):
        return self._api.transcludeFilter('ftx', text, None, self._api._viewTypeToToken(viewType))

    def _loadFragmentTypes(self):
        if self._api:
            fragments = self._api.describeFrags()
            for fragment in fragments:
                self._fragmentTypes[fragment['dataclass'], fragment['type']] = ArkFragmentType(self, fragment)

    def _loadModules(self):
        if self._api:
            modules = self._api.describeItems()
            for module in modules:
                self._modules[module['name']] = ArkModule(self, module)


class ArkResult(ArkContainer):

    _snips = []

    def __init__(self, data):
        super(ArkResult, self).__init__(data)
        for snip in self._data['snippets']:
            print snip
            self._snips.append(ArkSnippet(snip))

    def itemKey(self):
        return self._data['itemkey']

    def itemValue(self):
        return self._data['itemval']

    def score(self):
        return self._data['score']

    def snippets(self):
        return self._snips


class ArkSnippet(ArkContainer):

    def __init__(self, data):
        super(ArkSnippet, self).__init__(data)

    def dataClass(self):
        return self._data['class']

    def classType(self):
        return self._data['type']

    def snippet(self):
        return self._data['snip']


class ArkFragmentType(ArkObject):

    def __init__(self, ark, data):
        super(ArkFragmentType, self).__init__(ark, data)

    def dataClass(self):
        return self._ark._api._tokenToDataClass(self._data['dataclass'])

    def classType(self):
        key = self._data['dataclass'] + u'type'
        return self._data[key]


class ArkModule(ArkObject):

    _fieldAttr = []

    def __init__(self, ark, data):
        super(ArkModule, self).__init__(ark, data)

    def shortForm(self):
        return self._data['shortform']

    def name(self):
        return self._data['name']

    def description(self):
        return self._data['description']

    def itemKey(self):
        return self._data['itemkey']

    def createdOn(self):
        #TODO convert to date/time object
        return self._data['cre_on']

    def createdBy(self):
        #TODO convert to ArkUser object?
        return self._data['cre_by']

    #TODO Fields, Items, Frags, Subfoms

