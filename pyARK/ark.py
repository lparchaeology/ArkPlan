# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
            A Python library for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-06-05
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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

class Ark():

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

    def _getJson(self, req, args):
        url = self._buildUrl(req, args)
        print 'Making ARK call: ' + url
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print 'ARK server could not complete the request: ', e.code
            return json.loads('{}')
        except urllib2.URLError as e:
            print 'Could not reach the ARK server: ', e.reason
            return json.loads('{}')
        else:
            try:
                return json.load(response)
            except:
                return json.loads('{}')

    def _getHtml(self, req, args):
        url = self._buildUrl(req, args)
        print 'Making ARK call: ' + url
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print 'ARK server could not complete the request: ', e.code
            return ''
        except urllib2.URLError as e:
            print 'Could not reach the ARK server: ', e.reason
            return ''
        else:
            return response.read()

    def _buildUrl(self, req, args):
        url = u'http://' + self.url + u'/api.php?req=' + unicode(req)
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
