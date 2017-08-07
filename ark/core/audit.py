# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
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

from ArkSpatial.ark.lib import utils


class Audit():
    _creator = ''
    _created = ''
    _modifier = ''
    _modified = ''

    def __init__(self, creator=None, created=None, modifier=None, modified=None):
        self.setAudit(creator, created, modifier, modified)

    def __hash__(self):
        return hash((self._creator, self._created, self._modifier, self._modified))

    def __str__(self):
        return ('Audit('
                + str(self._creator) + ', '
                + str(self._created) + ', '
                + str(self._modifier) + ', '
                + str(self._modified) + ')')

    def debug(self):
        return ('Audit('
                + utils.printable(self._creator) + ', '
                + utils.printable(self._created) + ', '
                + utils.printable(self._modifier) + ', '
                + utils.printable(self._modified) + ')')

    def setAudit(self, creator, created, modifier=None, modified=None):
        self.setCreator(creator)
        self.setCreated(created)
        self.setModifier(modifier)
        self.setModified(modified)

    def creator(self):
        return self._creator

    def setCreator(self, creator):
        self._creator = utils.string(creator)

    def created(self):
        return self._created

    def setCreated(self, created):
        self._created = utils.string(created)

    def modifier(self):
        return self._modifier

    def setModifier(self, modifier):
        self._modifier = utils.string(modifier)

    def modified(self):
        return self._modified

    def setModified(self, modified):
        self._modified = utils.string(modified)

    def attributes(self):
        attrs = {}
        attrs['creator'] = utils.strip(self.creator())
        attrs['created'] = utils.strip(self.created())
        attrs['modifier'] = utils.strip(self.modifier())
        attrs['modified'] = utils.strip(self.modified())
        return attrs

    def setAttributes(self, attributes):
        if 'creator' in attributes:
            self.setSiteCode(attributes['creator'])
        if 'created' in attributes:
            self.setSiteCode(attributes['created'])
        if 'modifier' in attributes:
            self.setSiteCode(attributes['modifier'])
        if 'modified' in attributes:
            self.setSiteCode(attributes['modified'])
